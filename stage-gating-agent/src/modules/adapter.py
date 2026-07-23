"""
adapter — input/ の生CSV（スキーマは変化しうる）を、現行の正規スキーマ
（settings.CANONICAL_*_COLUMNS）へ決定的に変換し、mid/ に「正規形CSV」として書き出す。

入力の列名が変わっても、変更は settings.INPUT_MAPPING の `rename` / `detect` を直すだけで
吸収する（コードは触らない）。後段（loader → processor）は常に正規形だけを見るため、
入力スキーマの揺れが後段に波及しない。

出力:
    mid/canonical_invest.csv … 投資要求（正規列・正規列順）
    mid/canonical_bau.csv    … BAU予算要求（正規列・正規列順）
"""
from __future__ import annotations
import csv
from pathlib import Path

from config import settings


class AdapterError(Exception):
    """入力を正規形へ変換できないときのエラー。処理を止める。"""


def _read_csv(path: Path) -> tuple[list[dict], list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise AdapterError(f"ヘッダが読めません: {path.name}")
        header = [h.strip() for h in reader.fieldnames]
        rows = []
        for raw in reader:
            if not any((v or "").strip() for v in raw.values()):
                continue
            rows.append({(k or "").strip(): (v or "").strip() for k, v in raw.items()})
        return rows, header


def _classify(header: list[str]) -> str | None:
    """生ヘッダから種別を判定。detect のいずれかが含まれれば該当。"""
    for kind, conf in settings.INPUT_MAPPING.items():
        if any(marker in header for marker in conf.get("detect", [])):
            return kind
    return None


def _canonical_columns(kind: str) -> list[str]:
    return (settings.CANONICAL_INVEST_COLUMNS if kind == "invest"
            else settings.CANONICAL_BAU_COLUMNS)


def _to_canonical_row(raw: dict, kind: str, canon_cols: list[str]) -> dict:
    """
    生行 → 正規行。
      - rename（元列名→正規列名）で対応づけ
      - rename に無い生列は、正規列名と一致すればそのまま採用
      - 対応が取れない正規列は空欄
    """
    rename = settings.INPUT_MAPPING[kind].get("rename", {})
    out = {c: "" for c in canon_cols}
    for src, val in raw.items():
        target = rename.get(src, src if src in out else None)
        if target in out:
            out[target] = val
    return out


def _write_canonical(rows: list[dict], canon_cols: list[str], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # BOM 付きで書き出し（loader は utf-8-sig で読む）
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=canon_cols)
        writer.writeheader()
        writer.writerows(rows)


def convert(input_path: Path) -> dict:
    """
    input（ファイル or ディレクトリ）の生CSV群を正規形CSVへ変換し、mid/ に書き出す。

    返り値:
        {"invest": Path|None, "bau": Path|None, "sources": [ファイル名...],
         "counts": {"invest": n, "bau": m}}
    """
    if not input_path.exists():
        raise AdapterError(f"入力パスが見つかりません: {input_path}")

    files = sorted(input_path.glob("*.csv")) if input_path.is_dir() else [input_path]
    if not files:
        raise AdapterError(f"CSV が見つかりません: {input_path}")

    buckets: dict[str, list[dict]] = {"invest": [], "bau": []}
    sources: list[str] = []
    unclassified: list[str] = []

    for fp in files:
        rows, header = _read_csv(fp)
        kind = _classify(header)
        if kind is None:
            unclassified.append(fp.name)
            continue
        canon_cols = _canonical_columns(kind)
        buckets[kind].extend(_to_canonical_row(r, kind, canon_cols) for r in rows)
        sources.append(fp.name)

    if not buckets["invest"] and not buckets["bau"]:
        hint = ""
        if unclassified:
            hint = ("（種別判定不可: " + ", ".join(unclassified)
                    + "。settings.INPUT_MAPPING の detect を確認）")
        raise AdapterError("正規形に変換できる投資/BAUデータがありません" + hint)

    result: dict = {"invest": None, "bau": None, "sources": sources,
                    "counts": {"invest": len(buckets["invest"]), "bau": len(buckets["bau"])}}
    if buckets["invest"]:
        _write_canonical(buckets["invest"], settings.CANONICAL_INVEST_COLUMNS,
                         settings.CANONICAL_INVEST_CSV)
        result["invest"] = settings.CANONICAL_INVEST_CSV
    elif settings.CANONICAL_INVEST_CSV.exists():
        settings.CANONICAL_INVEST_CSV.unlink()  # 今回入力に無い種別の古い正規形を残さない
    if buckets["bau"]:
        _write_canonical(buckets["bau"], settings.CANONICAL_BAU_COLUMNS,
                         settings.CANONICAL_BAU_CSV)
        result["bau"] = settings.CANONICAL_BAU_CSV
    elif settings.CANONICAL_BAU_CSV.exists():
        settings.CANONICAL_BAU_CSV.unlink()
    result["unclassified"] = unclassified
    return result
