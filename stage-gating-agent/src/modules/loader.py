"""
loader — input/ の CSV を読み込み、投資シート/BAUシートを自動判別して検証する。

入力規律をここで強制する。ヘッダ列で種別を判定し（ファイル名に依存しない）、
必須列の欠落を検査して違反したら InputError で止める。検証済みの生レコードだけを
processor へ渡す。
"""
from __future__ import annotations
import csv
from pathlib import Path

from config import settings

# 各シートの必須ヘッダ（存在チェック用。値の妥当性は processor / 審査で見る）
INVEST_REQUIRED = ["案件ID", "提出部門", "案件区分", "案件名", "要求金額_当年度"]
BAU_REQUIRED = ["項目ID", "提出部門", "項目名", "コスト種別", "当年度要求額"]


class InputError(Exception):
    """入力データの規律違反。処理を止めるべきエラー。"""


def _read_csv(path: Path) -> list[dict]:
    """BOM を除去し、ヘッダ行をキーに dict のリストで返す。空行は捨てる。"""
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise InputError(f"ヘッダが読めません: {path.name}")
        rows = []
        for raw in reader:
            # 全項目が空の行はスキップ
            if not any((v or "").strip() for v in raw.values()):
                continue
            rows.append({(k or "").strip(): (v or "").strip() for k, v in raw.items()})
        return rows, [h.strip() for h in reader.fieldnames]


def _classify(header: list[str]) -> str:
    if settings.INVEST_MARKER_COL in header:
        return "invest"
    if settings.BAU_MARKER_COL in header:
        return "bau"
    raise InputError(
        "投資シート/BAUシートのいずれとも判別できません"
        f"（識別列 '{settings.INVEST_MARKER_COL}' も '{settings.BAU_MARKER_COL}' も無い）"
    )


def _check_required(kind: str, header: list[str], name: str) -> None:
    required = INVEST_REQUIRED if kind == "invest" else BAU_REQUIRED
    missing = [c for c in required if c not in header]
    if missing:
        raise InputError(f"{name}: 必須列が不足しています → {', '.join(missing)}")


def load(path: Path) -> dict:
    """
    input パス（ファイル or ディレクトリ）から投資/BAU を読み込み、検証して返す。

    返り値:
        {"invest": [rawdict...], "bau": [rawdict...], "sources": [ファイル名...]}

    - path がディレクトリなら配下の *.csv を全て読み、種別ごとに束ねる。
    - path がファイルならそれ1本を読む。
    """
    if not path.exists():
        raise InputError(f"入力パスが見つかりません: {path}")

    if path.is_dir():
        files = sorted(path.glob("*.csv"))
        if not files:
            raise InputError(f"CSV が見つかりません: {path}/*.csv")
    else:
        files = [path]

    invest: list[dict] = []
    bau: list[dict] = []
    sources: list[str] = []

    for fp in files:
        rows, header = _read_csv(fp)
        kind = _classify(header)
        _check_required(kind, header, fp.name)
        if kind == "invest":
            invest.extend(rows)
        else:
            bau.extend(rows)
        sources.append(fp.name)

    if not invest and not bau:
        raise InputError("有効なレコードが1件もありません")

    return {"invest": invest, "bau": bau, "sources": sources}
