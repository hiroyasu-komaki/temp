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
    - 繰り返し延長（extension_count >= 閾値）なら execution_prob を割り引く。
    返り値に内訳を残す（説明可能性）。
    """
    contest = item.get("contestability_prob")
    exec_p = item.get("execution_prob")
    ext = int(item.get("extension_count") or 0)

    ext_threshold = int(scenario.get("ext_threshold", 2))
    ext_penalty = float(scenario.get("ext_penalty", 0.15))
    ext_cap = float(scenario.get("ext_penalty_cap", 0.6))

    penalty = 0.0
    penalized = False
    if exec_p is not None and ext >= ext_threshold:
        over = ext - ext_threshold + 1
        penalty = min(ext_penalty * over, ext_cap)
        penalized = True

    if contest is not None and exec_p is not None:
        exec_eff = exec_p * (1 - penalty)
        p = contest * exec_eff
        split_used = True
    else:
        # フォールバック: exec_probability 単独。延長ペナルティは単独値に適用。
        base = item["exec_probability"]
        p = base * (1 - penalty) if ext >= ext_threshold else base
        penalized = ext >= ext_threshold and penalty > 0
        contest = None
        exec_eff = None
        split_used = False

    return {
        "p": max(0.0, min(1.0, p)),
        "p_contest": contest,
        "p_exec_effective": exec_eff,
        "ext_count": ext,
        "ext_penalized": penalized,
        "ext_penalty": round(penalty, 3),
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
            "extension_count": 0,           # 束ねは延長カウントを持たない
            "is_bundle": True,
            "members": [m["contract_id"] for m in members],
        })
    return bundles


# ---- 判定ラベル ----------------------------------------------------------

def verdict_of(d_i: float, score: float, Vn: float, U: float, R: float) -> str:
    if d_i < 0:
        return "失効"
    if score >= 0.25:
        return "即着手"
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
    max_V = max([max(c["V_raw"], 0.0) for c in candidates] + [1.0])
    for c in candidates:
        c["Vn"] = max(c["V_raw"], 0.0) / max_V
        c["score"] = c["Vn"] * c["U"] * c["R"]
        c["verdict"] = verdict_of(c["d_i"], c["score"], c["Vn"], c["U"], c["R"])

    candidates.sort(key=lambda x: x["score"], reverse=True)

    return {
        "as_of": scenario["as_of_date"],
        "scenario": scenario,
        "bundle_decisions": bundle_decisions,
        "excluded_inactive": excluded,
        "candidates": candidates,
    }
