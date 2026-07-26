"""
scoring — Score = V × U × R の計算と束ね（ベンダー単位バンドル）評価。

判断根拠は direction/scoring_methodology.md に対応する。
数式を変えるときはドキュメントとここを両方更新すること。
"""
from __future__ import annotations
import math
from collections import defaultdict


# ---- 有効確度 p_i の解決 -------------------------------------------------

def effective_p(item: dict, scenario: dict) -> dict:
    """
    実行確度 p_i を解決する。
    - contestability_prob と execution_prob が両方あれば積を使う。
      なければ exec_probability 単独にフォールバック（後方互換）。
    返り値に内訳を残す（説明可能性）。

    繰り返し延長は p を割り引かない（重要）。
    延長を確度の低下として扱うと、締切が近く実行意欲だけが低い案件が
    スコア上「捨てる候補」へ沈む。しかしそれは方法論 §3.5 の意図と逆である
    ── 現場任せでは切り替わらない案件こそ、VMOが実行主導すべき対象として
    名指しされねばならない。したがって延長は独立したフラグとして扱い、
    判定ラベル側で浮上させる（escalate_of を参照）。
    """
    contest = item.get("contestability_prob")
    exec_p = item.get("execution_prob")
    ext = int(item.get("extension_count") or 0)

    if contest is not None and exec_p is not None:
        p = contest * exec_p
        split_used = True
    else:
        p = item["exec_probability"]
        contest = None
        exec_p = None
        split_used = False

    return {
        "p": max(0.0, min(1.0, p)),
        "p_contest": contest,
        "p_exec_effective": exec_p,
        "ext_count": ext,
        "ext_escalated": ext >= int(scenario.get("ext_threshold", 2)),
        "p_split_used": split_used,
    }


# ---- 単一候補の因子計算 --------------------------------------------------

def factors(item: dict, scenario: dict) -> dict:
    """1候補について net, V_raw, d_i, U, R と有効確度内訳を計算して返す。"""
    lam = scenario["lambda_risk"]
    h = scenario["lead_time_h_months"]

    pinfo = effective_p(item, scenario)
    p = pinfo["p"]

    net = item["est_return_m"] - item["switch_cost_m"]
    V_raw = p * net * (1 - lam * (1 - p))

    d_i = item["expiry_months"] - item["switch_lead_months"]

    if d_i < 0:
        U = 0.0
    else:
        U = 1.0 / (1.0 + d_i / h)

    g = min(max(d_i, 0.0) / h, 1.0)
    R = 1.0 - item["return_sigma"] * g

    return {"net": net, "V_raw": V_raw, "d_i": d_i, "U": U, "R": R,
            "p_effective": p, **pinfo}


# ---- 束ね（ベンダー単位）------------------------------------------------

def build_bundles(contracts: list[dict], scenario: dict) -> list[dict]:
    """同一ベンダーで2件以上ある契約を束ね候補として合成する。"""
    beta = scenario["beta_bundle"]
    by_vendor: dict[str, list[dict]] = defaultdict(list)
    for c in contracts:
        by_vendor[c["vendor"]].append(c)

    bundles: list[dict] = []
    for vendor, members in by_vendor.items():
        if len(members) < 2:
            continue
        n = len(members)
        ret = beta * sum(m["est_return_m"] for m in members)
        cost = sum(m["switch_cost_m"] for m in members)
        # 束ねの確度: 各メンバーの有効確度の緩めた積（オールオアナッシング性）
        prod_p = 1.0
        for m in members:
            prod_p *= effective_p(m, scenario)["p"]
        p = prod_p ** (1.0 / math.sqrt(n))
        sigma = max(m["return_sigma"] for m in members)
        expiry = min(m["expiry_months"] for m in members)
        lead = max(m["switch_lead_months"] for m in members)

        bundles.append({
            "contract_id": f"B-{vendor}",
            "contract_name": f"{vendor} 一括（{n}件）",
            "contract_type": "Bundle",
            "vendor": vendor,
            "expiry_months": expiry,
            "annual_spend_m": sum(m["annual_spend_m"] for m in members),
            "switch_lead_months": lead,
            "switch_cost_m": cost,
            "switch_cost_sigma": 0.0,
            "est_return_m": ret,
            "return_sigma": sigma,
            "exec_probability": p,          # 束ねは合成済み確度をそのまま p として持つ
            # 延長回数は構成契約の最大を引き継ぐ。1件でも延長常習なら
            # 束ねても現場任せでは動かないため、シグナルを消してはならない。
            "extension_count": max(int(m.get("extension_count") or 0) for m in members),
            "is_bundle": True,
            "members": [m["contract_id"] for m in members],
        })
    return bundles


# ---- 判定ラベル ----------------------------------------------------------

def verdict_of(d_i: float, score: float, Vn: float, U: float, R: float,
               escalated: bool = False) -> str:
    if d_i < 0:
        return "失効"
    if score >= 0.25:
        return "即着手"
    # 繰り返し延長は、確度を割り引くのではなくここで浮上させる。
    # 「現場任せでは切り替わらない」という事実は、沈めるのではなく名指しする。
    if escalated:
        return "VMO主導候補"
    if U >= 0.5 and R < 0.7:
        return "人間判断"
    if Vn > 0.3 and U < 0.4:
        return "温存"
    if Vn < 0.1:
        return "捨てる候補"
    return "検討"



# ---- メイン: 候補集合を構築してスコアリング ------------------------------

def score_all(contracts: list[dict], scenario: dict) -> dict:
    use_bundle = scenario["use_bundle"]

    # is_active=0 の契約は対象外（Single-source確定などで交渉トラックへ移したもの）
    active = [c for c in contracts if int(c.get("is_active", 1)) == 1]
    excluded = [c["contract_name"] for c in contracts if int(c.get("is_active", 1)) != 1]

    # ベースは個別契約（コピー）
    candidates = [dict(c) for c in active]
    for c in candidates:
        c.setdefault("is_bundle", False)

    bundle_decisions: list[dict] = []

    if use_bundle:
        bundles = build_bundles(active, scenario)
        bundled_ids: set = set()
        for b in bundles:
            members = [c for c in active if c["contract_id"] in b["members"]]
            fB = factors(b, scenario)
            sum_indiv_V = sum(max(factors(m, scenario)["V_raw"], 0.0) for m in members)
            adopt = max(fB["V_raw"], 0.0) >= sum_indiv_V
            bundle_decisions.append({
                "vendor": b["vendor"], "n": len(members),
                "bundle_V": round(max(fB["V_raw"], 0.0), 2),
                "indiv_V": round(sum_indiv_V, 2),
                "adopted": adopt,
            })
            if adopt:
                candidates.append(dict(b))
                bundled_ids.update(b["members"])
        candidates = [c for c in candidates
                      if not (c.get("contract_id") in bundled_ids and not c.get("is_bundle"))]

    # 因子計算
    for c in candidates:
        c.update(factors(c, scenario))

    # V の相対正規化（金額の桁で押し切らせない）
    # 下限を定数で切らない。切ると案件群の絶対金額がスコアに漏れ込み、
    # 小規模な案件群だけ一律に低スコアへ沈む（＝相対化の意図に反する）。
    # ゼロ除算だけを避ける。assets/js/scoring.js と同じ基準。
    max_V = max([max(c["V_raw"], 0.0) for c in candidates] + [1e-9])
    for c in candidates:
        c["Vn"] = max(c["V_raw"], 0.0) / max_V
        c["score"] = c["Vn"] * c["U"] * c["R"]
        c["verdict"] = verdict_of(c["d_i"], c["score"], c["Vn"], c["U"], c["R"],
                                  escalated=bool(c.get("ext_escalated")))

    candidates.sort(key=lambda x: x["score"], reverse=True)

    return {
        "as_of": scenario["as_of_date"],
        "scenario": scenario,
        "bundle_decisions": bundle_decisions,
        "excluded_inactive": excluded,
        "candidates": candidates,
    }
