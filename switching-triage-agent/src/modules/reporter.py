"""
reporter — mid/scored.json と output/allocation.json から report.md を生成する。

出力仕様は direction/output_spec.md の output/report.md に対応。
断定を避け、各判定が3因子のどれに起因するかを明示する。
"""
from __future__ import annotations


def build_report(scored: dict, alloc: dict) -> str:
    s = scored["scenario"]
    lines: list[str] = []

    lines.append("# ベンダー切替投資ポートフォリオ 判断レポート")
    lines.append("")
    lines.append(f"基準日: {scored['as_of']}")
    lines.append("")

    # 1. シナリオ設定
    lines.append("## 1. シナリオ設定")
    lines.append("")
    lines.append(f"- リスク回避度 λ: {s['lambda_risk']}")
    lines.append(f"- 束ねプレミアム β: {s['beta_bundle']}")
    lines.append(f"- リードタイム基準 h: {s['lead_time_h_months']} ヶ月")
    lines.append(f"- 手元資金 B: {s['budget_m']} 百万円")
    lines.append(f"- 安全余裕: {int(s['safety_margin']*100)}%")
    lines.append(f"- 束ね評価: {'有効' if s['use_bundle'] else '無効'}")
    lines.append("")

    # 2. 優先度ランキング
    lines.append("## 2. 優先度ランキング")
    lines.append("")
    lines.append("| 順位 | 対象 | ネット(M) | p有効 | V | U | R | 残月 | スコア | 判定 |")
    lines.append("|---:|---|---:|---:|---:|---:|---:|---:|---:|---|")
    for i, c in enumerate(scored["candidates"], 1):
        mark = ""
        if c.get("is_bundle"):
            mark += " 🔗"
        if c.get("ext_penalized"):
            mark += f" ⚠×{c.get('ext_count', 0)}"
        p_eff = c.get("p_effective", c.get("exec_probability"))
        lines.append(
            f"| {i} | {c['contract_name']}{mark} | {c['net']:.0f} | {p_eff:.2f} "
            f"| {c['Vn']:.2f} | {c['U']:.2f} | {c['R']:.2f} | {c['d_i']:.1f} "
            f"| {c['score']:.3f} | {c['verdict']} |"
        )
    lines.append("")
    if any(c.get("ext_penalized") for c in scored["candidates"]):
        lines.append("⚠×n = 延長 n 回によりexecution_probにペナルティ適用（現場任せでは"
                     "切り替わらない兆候。VMO主導を検討すべき対象）。")
        lines.append("")
    if scored.get("excluded_inactive"):
        lines.append("**対象外（is_active=0）**: " + "、".join(scored["excluded_inactive"])
                     + "（Single-source確定等で交渉トラックへ移管）。")
        lines.append("")

    # 3. 束ね判定
    if scored["bundle_decisions"]:
        lines.append("## 3. 束ね（ベンダー単位）判定")
        lines.append("")
        for d in scored["bundle_decisions"]:
            if d["adopted"]:
                verdict = f"**束ねを採用**（束ね価値 {d['bundle_V']} ≧ 個別合計 {d['indiv_V']}）"
            else:
                verdict = f"個別が有利（束ね価値 {d['bundle_V']} ＜ 個別合計 {d['indiv_V']}）"
            lines.append(f"- {d['vendor']}（{d['n']}件）: {verdict}")
        lines.append("")

    # 4. 予算配分
    lines.append("## 4. 予算配分")
    lines.append("")
    lines.append(
        f"本コミット {alloc['committed_m']}M ／ 使用可能 {alloc['available_m']}M"
        f"（安全余裕 {int(alloc['safety_margin']*100)}%）"
    )
    lines.append("")
    lines.append(f"予約枠込み {alloc['committed_m']+alloc['reserved_m']:.1f}M ／ 手元資金 {alloc['budget_m']:.0f}M")
    lines.append("")
    lines.append("| 区分 | 対象 | コスト(M) | スコア |")
    lines.append("|---|---|---:|---:|")
    for ln in alloc["lines"]:
        lines.append(f"| {ln['tag']} | {ln['name']} | {ln['cost_m']} | {ln['score']} |")
    lines.append("")

    # 5. 追加資金の引き出し根拠
    if alloc["blocked_top"]:
        lines.append("## 5. 追加資金の引き出し根拠")
        lines.append("")
        lines.append(
            f"**予算不足で着手不能**：「{alloc['blocked_top']}」ほか、"
            f"優先度は上位だが資金が届かない案件が計 **{alloc['blocked_m']}M** 分ある。"
            f"手元資金 {alloc['budget_m']:.0f}M では最優先群を取り切れない。"
            f"実績（本コミット分の期待ネット {alloc['committed_expected_net_m']}M）を示した上で、"
            f"次の資金引き出しを協議する根拠となる。"
        )
        lines.append("")

    # 6. 最上位の説明
    top = next((c for c in scored["candidates"] if c["d_i"] >= 0 and c["score"] > 0), None)
    if top:
        lines.append("## 6. 最上位案件の位置づけ")
        lines.append("")
        p = top.get("p_effective", top.get("exec_probability"))
        lines.append(
            f"**{top['contract_name']}** が最上位。期待ネット {top['net']:.0f}百万円・"
            f"確度 {p*100:.0f}%、着手期限まで残り {top['d_i']:.1f}ヶ月（緊急度 {top['U']*100:.0f}%）、"
            f"情報熟度 {top['R']*100:.0f}%。期待価値・緊急度・情報熟度の3つが揃うため最優先と判断する。"
        )
        lines.append("")

    return "\n".join(lines)
