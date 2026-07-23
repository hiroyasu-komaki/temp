"""
processor — 中核処理。loader が検証した生レコードを

  1) 正規化（同一スキーマの1配列へ。金額は数値化）
  2) 審査フラグ付与（appendix のシート設計の記入規律をコード化）
  3) 集計（KPI・部門別・月別按分・POCパイプライン・BAU増減・ベンダー別）

まで行い、ダッシュボードが描くだけで済む集計済みデータを返す。

判断根拠となる規律・数式は direction/data-definition.md に対応させる。コードだけを
変えて根拠と乖離させないこと。
"""
from __future__ import annotations
import re
from datetime import datetime, timezone, timedelta

from config import settings

# 会計年度の12か月 [(year, month), ...] と表示ラベル
def _fy_months() -> list[tuple[int, int]]:
    out = []
    y, m = settings.FY_START_YEAR, settings.FY_START_MONTH
    for _ in range(12):
        out.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


FY_MONTHS = _fy_months()
FY_LABELS = [str(m) for (_, m) in FY_MONTHS]


# ---- 小さなパーサ ---------------------------------------------------------
def _num(x) -> float:
    """文字列から数値を抽出。空・不能は 0.0。"""
    if x is None:
        return 0.0
    s = re.sub(r"[^0-9.\-]", "", str(x))
    if s in ("", "-", ".", "-."):
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0


def _int_or_none(x) -> int | None:
    s = (str(x) if x is not None else "").strip()
    if s == "":
        return None
    return int(round(_num(s)))


def _score(x) -> int | None:
    """1-3 のスコア。空は None。"""
    s = (str(x) if x is not None else "").strip()
    if s == "":
        return None
    v = _int_or_none(s)
    return v


def _str_or_none(x) -> str | None:
    s = (str(x) if x is not None else "").strip()
    return s or None


def _has(x) -> bool:
    return bool((str(x) if x is not None else "").strip())


# ---- 正規化 ---------------------------------------------------------------
def _normalize_invest(r: dict) -> dict:
    cat = (r.get("案件区分") or "").strip()
    is_poc = cat == settings.CATEGORY_POC
    rec = {
        "id": r.get("案件ID", ""),
        "dept": r.get("提出部門", ""),
        "applicant": r.get("起案者", ""),
        "submitDate": r.get("提出日", ""),
        "category": cat,
        "name": r.get("案件名", ""),
        "summary": r.get("概要", ""),
        "amount": _int_or_none(r.get("要求金額_当年度")) or 0,
        "period": _str_or_none(r.get("実施期間")),
        "roiText": _str_or_none(r.get("ROI_pct")),
        "npv": _int_or_none(r.get("NPV")),
        "payback": (_num(r.get("回収期間_年")) or None) if _has(r.get("回収期間_年")) else None,
        "gate2Time": _str_or_none(r.get("Gate2想定時期")),
        "gate2Scale": _str_or_none(r.get("Gate2想定投資規模")),
        "goNoGo": _str_or_none(r.get("軸4_検証項目_GoNoGo条件")),
        "axis1": _score(r.get("軸1_不確実性縮減スコア")),
        "axis2": _score(r.get("軸2_アップサイドスコア")),
        "axis3": _score(r.get("軸3_検証コスト可逆性スコア")),
        # BAU 専用列は None
        "vendor": None, "costType": None, "prevBudget": None,
        "delta": None, "deltaPct": None, "deltaReason": None,
        "continueNeed": None, "reductionRoom": None, "vmo": None, "contractEnd": None,
    }
    # 表表示用の補足
    if is_poc:
        rec["note"] = "Gate2予定 " + (rec["gate2Time"] or "未設定")
    else:
        rec["note"] = ("ROI " + rec["roiText"]) if rec["roiText"] else ""
    rec["flags"] = _audit_invest(r, rec)
    return rec


def _normalize_bau(r: dict) -> dict:
    amount = _int_or_none(r.get("当年度要求額")) or 0
    prev = _int_or_none(r.get("前年度予算額"))
    delta = _int_or_none(r.get("増減額"))
    if delta is None and prev is not None:
        delta = amount - prev
    deltaPct = None
    if _has(r.get("増減率_pct")):
        deltaPct = _num(r.get("増減率_pct"))
    elif prev:
        deltaPct = round((amount - prev) / prev * 100, 1)
    rec = {
        "id": r.get("項目ID", ""),
        "dept": r.get("提出部門", ""),
        "applicant": r.get("起案者", ""),
        "submitDate": r.get("提出日", ""),
        "category": settings.CATEGORY_BAU,
        "name": r.get("項目名", ""),
        "summary": r.get("対象範囲", ""),
        "amount": amount,
        "period": None, "roiText": None, "npv": None, "payback": None,
        "gate2Time": None, "gate2Scale": None, "goNoGo": None,
        "axis1": None, "axis2": None, "axis3": None,
        "vendor": _str_or_none(r.get("ベンダー")),
        "costType": _str_or_none(r.get("コスト種別")),
        "prevBudget": prev,
        "delta": delta,
        "deltaPct": deltaPct,
        "deltaReason": _str_or_none(r.get("増減理由")),
        "continueNeed": _str_or_none(r.get("継続要否")),
        "reductionRoom": _str_or_none(r.get("削減余地")),
        "vmo": _str_or_none(r.get("VMO連携要否")),
        "contractEnd": _str_or_none(r.get("契約満了_更新時期")),
    }
    rec["note"] = rec["deltaReason"] or ""
    rec["flags"] = _audit_bau(r, rec)
    return rec


# ---- 審査フラグ（direction/data-definition.md §4） ------------------------
def _audit_invest(r: dict, rec: dict) -> list[dict]:
    flags: list[dict] = []
    cat = rec["category"]
    if cat not in settings.INVEST_CATEGORIES:
        flags.append({"level": "error", "code": "CATEGORY_INVALID",
                      "message": f"案件区分が不正: '{cat}'（通常投資/POC のいずれかであるべき）"})
        return flags  # 区分不明ならこれ以上は判定しない

    axis_filled = any(_has(r.get(c)) for c in
                      ["軸1_不確実性縮減スコア", "軸2_アップサイドスコア",
                       "軸3_検証コスト可逆性スコア", "軸4_検証項目_GoNoGo条件"])
    roi_filled = any(_has(r.get(c)) for c in
                     ["投資総額", "想定リターン年額", "ROI_pct", "NPV", "回収期間_年"])

    if cat == settings.CATEGORY_POC:
        if roi_filled:
            flags.append({"level": "error", "code": "POC_HAS_ROI",
                          "message": "POC なのに ROI/NPV 等が記入されている（区分違いの疑い）"})
        if not _has(r.get("軸1_縮減する不確実性の内容")):
            flags.append({"level": "error", "code": "POC_MISSING_UNCERTAINTY",
                          "message": "軸1（縮減する不確実性の内容）が空。規律あるオプションでないため差し戻し候補"})
        if not _has(r.get("軸4_検証項目_GoNoGo条件")):
            flags.append({"level": "error", "code": "POC_MISSING_GONOGO",
                          "message": "軸4（Go/No-Go 条件）が空。判断基準が未定義のため差し戻し候補"})
        if not _has(r.get("Gate2想定時期")):
            flags.append({"level": "warn", "code": "POC_MISSING_GATE2",
                          "message": "Gate2 想定時期が空。本格投資への接続情報が欠落（『突然登場』リスク）"})
    else:  # 通常投資
        if axis_filled:
            flags.append({"level": "error", "code": "NORMAL_HAS_AXIS",
                          "message": "通常投資なのに POC の4軸が記入されている（区分違いの疑い）"})
        if not _has(r.get("ROI_pct")):
            flags.append({"level": "warn", "code": "NORMAL_MISSING_ROI",
                          "message": "ROI が未記入"})
    return flags


def _audit_bau(r: dict, rec: dict) -> list[dict]:
    flags: list[dict] = []
    if not _has(r.get("増減理由")):
        flags.append({"level": "error", "code": "BAU_MISSING_REASON",
                      "message": "増減理由が空（据置でも明記が必要・空欄禁止）"})
    thr = settings.FIXED_PARAMS.get("bau_large_delta_pct", 10.0)
    if rec["deltaPct"] is not None and abs(rec["deltaPct"]) >= thr:
        flags.append({"level": "warn", "code": "BAU_LARGE_DELTA",
                      "message": f"増減率 {rec['deltaPct']:.1f}%（±{thr:.0f}% 以上）。説明責任を要確認"})
    if (rec["reductionRoom"] == "あり") and (rec["vmo"] == "不要"):
        flags.append({"level": "warn", "code": "BAU_REDUCTION_NO_VMO",
                      "message": "削減余地あり かつ VMO連携=不要。交渉機会の取りこぼし懸念"})
    return flags


# ---- 集計 -----------------------------------------------------------------
def _month_index(y: int, m: int) -> int:
    for i, (yy, mm) in enumerate(FY_MONTHS):
        if yy == y and mm == m:
            return i
    return -1


def _allocate_monthly(records: list[dict]) -> dict:
    normal = [0.0] * 12
    poc = [0.0] * 12
    bau = [0.0] * 12
    pat = re.compile(r"(\d{4})-(\d{2}).*?(\d{4})-(\d{2})")
    for rec in records:
        cat = rec["category"]
        amt = float(rec["amount"])
        if cat == settings.CATEGORY_BAU:
            for i in range(12):
                bau[i] += amt / 12.0
            continue
        m = pat.search(rec.get("period") or "")
        if not m:
            continue
        si = _month_index(int(m[1]), int(m[2]))
        ei = _month_index(int(m[3]), int(m[4]))
        if si < 0:
            si = 0
        if ei < 0:
            ei = 11
        if ei < si:
            ei = si
        span = ei - si + 1
        per_m = amt / span
        tgt = poc if cat == settings.CATEGORY_POC else normal
        for i in range(si, ei + 1):
            tgt[i] += per_m
    rnd = lambda a: [int(round(v)) for v in a]
    return {"labels": FY_LABELS, "normal": rnd(normal), "poc": rnd(poc), "bau": rnd(bau)}


def _summarize(records: list[dict], sources: list[str]) -> dict:
    inv = [r for r in records if r["category"] in settings.INVEST_CATEGORIES]
    bau = [r for r in records if r["category"] == settings.CATEGORY_BAU]

    normal = sum(r["amount"] for r in inv if r["category"] == settings.CATEGORY_NORMAL)
    poc = sum(r["amount"] for r in inv if r["category"] == settings.CATEGORY_POC)
    bau_total = sum(r["amount"] for r in bau)
    total = normal + poc + bau_total
    bau_prev = sum((r["prevBudget"] or 0) for r in bau)
    bau_delta = bau_total - bau_prev

    pct = lambda v: round(v / total * 100, 1) if total else 0.0

    kpi = {
        "total": total, "normal": normal, "poc": poc, "bau": bau_total,
        "investTotal": normal + poc,
        "bauPrev": bau_prev, "bauDelta": bau_delta,
        "bauDeltaPct": round(bau_delta / bau_prev * 100, 1) if bau_prev else 0.0,
        "normalCount": sum(1 for r in inv if r["category"] == settings.CATEGORY_NORMAL),
        "pocCount": sum(1 for r in inv if r["category"] == settings.CATEGORY_POC),
        "bauCount": len(bau),
        "normalPct": pct(normal), "pocPct": pct(poc), "bauPct": pct(bau_total),
    }

    by_type = [
        {"name": settings.CATEGORY_NORMAL, "value": normal},
        {"name": settings.CATEGORY_POC, "value": poc},
        {"name": settings.CATEGORY_BAU, "value": bau_total},
    ]

    # 部門別（区分別に積み上げ）
    depts: dict[str, dict] = {}
    for r in records:
        d = depts.setdefault(r["dept"], {"dept": r["dept"],
                                          settings.CATEGORY_NORMAL: 0,
                                          settings.CATEGORY_POC: 0,
                                          settings.CATEGORY_BAU: 0, "total": 0})
        # 区分不正（審査で error 付与済み）は種別内訳に加算せず合計だけ計上する
        if r["category"] in d:
            d[r["category"]] += r["amount"]
        d["total"] += r["amount"]
    by_dept = sorted(depts.values(), key=lambda x: x["total"], reverse=True)

    # POC パイプライン（Gate2 時期別）
    g2: dict[str, dict] = {}
    for r in inv:
        if r["category"] != settings.CATEGORY_POC:
            continue
        k = r["gate2Time"] or "未設定"
        g = g2.setdefault(k, {"gate2": k, "count": 0, "amount": 0})
        g["count"] += 1
        g["amount"] += r["amount"]
    poc_pipeline = sorted(g2.values(), key=lambda x: x["gate2"])

    # BAU コスト種別別
    ct: dict[str, dict] = {}
    for r in bau:
        k = r["costType"] or "その他"
        c = ct.setdefault(k, {"costType": k, "amount": 0, "prev": 0})
        c["amount"] += r["amount"]
        c["prev"] += (r["prevBudget"] or 0)
    for c in ct.values():
        c["delta"] = c["amount"] - c["prev"]
    bau_by_type = sorted(ct.values(), key=lambda x: x["amount"], reverse=True)

    # BAU ベンダー別（VMO 入口）
    vd: dict[str, dict] = {}
    for r in bau:
        k = r["vendor"] or "—"
        v = vd.setdefault(k, {"vendor": k, "amount": 0, "count": 0})
        v["amount"] += r["amount"]
        v["count"] += 1
    bau_by_vendor = sorted(vd.values(), key=lambda x: x["amount"], reverse=True)

    # 審査サマリー
    audit_items = []
    for r in records:
        for fl in r["flags"]:
            audit_items.append({"id": r["id"], "dept": r["dept"], "name": r["name"],
                                "level": fl["level"], "code": fl["code"], "message": fl["message"]})
    errors = sum(1 for a in audit_items if a["level"] == "error")
    warns = sum(1 for a in audit_items if a["level"] == "warn")

    jst = timezone(timedelta(hours=9))
    meta = {
        "fy": settings.FIXED_PARAMS.get("fy_label", f"FY{settings.FY_START_YEAR}"),
        "generatedAt": datetime.now(jst).strftime("%Y-%m-%d %H:%M"),
        "investCount": len(inv), "bauCount": len(bau), "totalCount": len(records),
        "sources": sources,
    }

    return {
        "meta": meta,
        "kpi": kpi,
        "byType": by_type,
        "byDept": by_dept,
        "monthly": _allocate_monthly(records),
        "pocPipeline": poc_pipeline,
        "bauByType": bau_by_type,
        "bauByVendor": bau_by_vendor,
        "audit": {"errors": errors, "warnings": warns, "items": audit_items},
    }


def process(data: dict, params: dict | None = None) -> dict:
    """
    loader の検証済みデータを受け取り、正規化・審査・集計した結果を返す。

    返り値: {"records": [...正規化レコード...], "summary": {...集計...}}
    """
    params = params or settings.DEFAULT_PARAMS
    records: list[dict] = []
    for r in data.get("invest", []):
        records.append(_normalize_invest(r))
    for r in data.get("bau", []):
        records.append(_normalize_bau(r))

    summary = _summarize(records, data.get("sources", []))
    return {"records": records, "summary": summary}
