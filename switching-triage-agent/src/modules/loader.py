"""
loader — input/ の契約CSVとシナリオJSONを読み、検証する。

入力規律を強制する:
- return_sigma の空欄を許さない（R の生命線のため）
- 確率系の値は 0..1 に収まっているか検査
- 必須列の欠落を検査
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
from dataclasses import dataclass, asdict


REQUIRED_COLUMNS = [
    "contract_id", "contract_name", "contract_type", "vendor",
    "expiry_months", "annual_spend_m", "switch_lead_months",
    "switch_cost_m", "switch_cost_sigma", "est_return_m",
    "return_sigma", "exec_probability",
]

# 任意列（あれば使う。なければ既定にフォールバック）
OPTIONAL_COLUMNS = ["contestability_prob", "execution_prob", "extension_count", "is_active"]

PROB_FIELDS = ["switch_cost_sigma", "return_sigma", "exec_probability"]


@dataclass
class Contract:
    contract_id: int
    contract_name: str
    contract_type: str
    vendor: str
    expiry_months: float
    annual_spend_m: float
    switch_lead_months: float
    switch_cost_m: float
    switch_cost_sigma: float
    est_return_m: float
    return_sigma: float
    exec_probability: float
    # 任意（確度の2分割・延長回数・有効フラグ）
    contestability_prob: float | None = None
    execution_prob: float | None = None
    extension_count: int = 0
    is_active: int = 1


class InputError(Exception):
    """入力データの規律違反。処理を止めるべきエラー。"""


def load_scenario(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        s = json.load(f)
    required = ["lambda_risk", "beta_bundle", "lead_time_h_months",
                "budget_m", "safety_margin", "use_bundle", "as_of_date"]
    missing = [k for k in required if k not in s]
    if missing:
        raise InputError(f"scenario.json に必須キーがありません: {missing}")
    if not (0 <= s["safety_margin"] < 1):
        raise InputError("safety_margin は 0 以上 1 未満で指定してください。")
    if s["beta_bundle"] < 1:
        raise InputError("beta_bundle は 1 以上（束ねプレミアム）で指定してください。")
    return s


def load_contracts(path: Path) -> list[Contract]:
    if not path.exists():
        raise InputError(f"入力ファイルが見つかりません: {path}")

    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        missing_cols = [c for c in REQUIRED_COLUMNS if c not in header]
        if missing_cols:
            raise InputError(f"CSVに必須列がありません: {missing_cols}")

        contracts: list[Contract] = []
        for lineno, row in enumerate(reader, start=2):
            _validate_row(row, lineno, header)
            contracts.append(Contract(
                contract_id=int(row["contract_id"]),
                contract_name=row["contract_name"].strip(),
                contract_type=row["contract_type"].strip(),
                vendor=row["vendor"].strip(),
                expiry_months=float(row["expiry_months"]),
                annual_spend_m=float(row["annual_spend_m"]),
                switch_lead_months=float(row["switch_lead_months"]),
                switch_cost_m=float(row["switch_cost_m"]),
                switch_cost_sigma=float(row["switch_cost_sigma"]),
                est_return_m=float(row["est_return_m"]),
                return_sigma=float(row["return_sigma"]),
                exec_probability=float(row["exec_probability"]),
                contestability_prob=_parse_opt_float(row.get("contestability_prob")),
                execution_prob=_parse_opt_float(row.get("execution_prob")),
                extension_count=int(_parse_opt_float(row.get("extension_count")) or 0),
                is_active=int(_parse_opt_float(row.get("is_active")) if
                              str(row.get("is_active", "")).strip() else 1),
            ))

    if not contracts:
        raise InputError("契約が1件も読み込めませんでした。")
    return contracts


def _parse_opt_float(val) -> float | None:
    s = str(val).strip() if val is not None else ""
    if not s:
        return None
    return float(s)


def _validate_row(row: dict, lineno: int, header: list[str]) -> None:
    name = row.get("contract_name", f"(line {lineno})")

    # 入力規律: return_sigma は空欄不可
    if not str(row.get("return_sigma", "")).strip():
        raise InputError(
            f"[line {lineno}] '{name}': return_sigma が空欄です。"
            f"想定リターンを入れたら確からしさ(sigma)も必ずセットで入れてください。"
        )

    # 確率系は 0..1
    for field in PROB_FIELDS:
        val = str(row.get(field, "")).strip()
        if not val:
            raise InputError(f"[line {lineno}] '{name}': {field} が空欄です。")
        try:
            v = float(val)
        except ValueError:
            raise InputError(f"[line {lineno}] '{name}': {field} が数値ではありません: {val!r}")
        if not (0.0 <= v <= 1.0):
            raise InputError(f"[line {lineno}] '{name}': {field}={v} は 0..1 の範囲外です。")

    # 任意の確度2列があれば 0..1 を検査（部分入力＝片方だけは不整合として弾く）
    has_contest = ("contestability_prob" in header
                   and bool(str(row.get("contestability_prob", "")).strip()))
    has_exec = ("execution_prob" in header
                and bool(str(row.get("execution_prob", "")).strip()))
    if has_contest != has_exec:
        raise InputError(
            f"[line {lineno}] '{name}': contestability_prob と execution_prob は"
            f"両方揃えるか両方空欄にしてください（片方だけは不可）。"
        )
    for field in ["contestability_prob", "execution_prob"]:
        val = str(row.get(field, "")).strip()
        if val:
            try:
                v = float(val)
            except ValueError:
                raise InputError(f"[line {lineno}] '{name}': {field} が数値ではありません: {val!r}")
            if not (0.0 <= v <= 1.0):
                raise InputError(f"[line {lineno}] '{name}': {field}={v} は 0..1 の範囲外です。")

    # 金額・月数は数値であること
    for field in ["expiry_months", "annual_spend_m", "switch_lead_months",
                  "switch_cost_m", "est_return_m"]:
        val = str(row.get(field, "")).strip()
        try:
            float(val)
        except ValueError:
            raise InputError(f"[line {lineno}] '{name}': {field} が数値ではありません: {val!r}")


def contracts_to_dicts(contracts: list[Contract]) -> list[dict]:
    return [asdict(c) for c in contracts]
