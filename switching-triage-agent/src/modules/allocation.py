"""
allocation — スコア順に手元資金 B を配分する（第2層）。

- 本コミット: p>=0.6 かつ 使用可能額(B*(1-margin)) に収まる
- 予約枠: p<0.6、手元資金 B の範囲で仮押さえ（不成立なら次へ回す＝リボルビング）
- 予算不足: 優先度は高い(score>=0.1)が資金が届かない → 明示（追加資金の根拠）
"""
from __future__ import annotations

COMMIT_PROB = 0.6      # 本コミット閾値（確度）
MIN_SCORE = 0.05       # これ未満は配分対象外
BLOCK_SCORE = 0.1      # これ以上なら予算不足として明示


def allocate(scored: dict) -> dict:
    scenario = scored["scenario"]
    B = float(scenario["budget_m"])
    margin = float(scenario["safety_margin"])
    avail = B * (1 - margin)

    committed = 0.0
    reserved = 0.0
    blocked = 0.0
    blocked_top = None
    lines: list[dict] = []

    for c in scored["candidates"]:
        if c["d_i"] < 0 or c["score"] < MIN_SCORE:
            continue
        cost = c["switch_cost_m"]
        if c["p_effective"] >= COMMIT_PROB:
            if committed + cost <= avail:
                committed += cost
                lines.append(_line("本コミット", c))
            else:
                blocked += cost
                blocked_top = blocked_top or c["contract_name"]
                lines.append(_line("予算不足", c))
        else:
            if committed + reserved + cost <= B:
                reserved += cost
                lines.append(_line("予約枠", c))
            elif c["score"] >= BLOCK_SCORE:
                blocked += cost
                blocked_top = blocked_top or c["contract_name"]
                lines.append(_line("予算不足", c))

    # 本コミット分の期待ネット合計
    committed_net = sum(
        c["p_effective"] * c["net"]
        for c in scored["candidates"]
        for ln in lines
        if ln["name"] == c["contract_name"] and ln["tag"] == "本コミット"
    )

    return {
        "budget_m": B,
        "available_m": round(avail, 1),
        "safety_margin": margin,
        "committed_m": round(committed, 1),
        "reserved_m": round(reserved, 1),
        "blocked_m": round(blocked, 1),
        "committed_expected_net_m": round(committed_net, 1),
        "blocked_top": blocked_top,
        "lines": lines,
    }


def _line(tag: str, c: dict) -> dict:
    return {
        "tag": tag,
        "name": c["contract_name"],
        "cost_m": round(c["switch_cost_m"], 1),
        "score": round(c["score"], 3),
        "p": round(c["p_effective"], 3),
    }
