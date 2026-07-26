"""
reporter — mid/scored.json から report.md を生成する。

出力仕様は direction/data_spec.md の output/report.md に対応。
断定を避け、各判定が3因子のどれに起因するかを明示する。

予算配分は扱わない。手元資金を「配分する／使い切る」発想はこのエージェントには
なく、出すのは優先順位とその根拠のみ（原則8）。予算枠に収まるかどうかで
案件を採否すると、スコアの意味が「説明可能な優先順位」から
「予算最適化の解」にすり替わる。
"""
from __future__ import annotations


class _Counter:
    """節番号の連番付与。条件付きの節があるため、出力した節だけを数える。"""

    def __init__(self) -> None:
        self._i = 0

    def next(self) -> int:
        self._i += 1
        return self._i


def _fmt(x: float, nd: int = 2) -> str:
    """末尾のゼロを落として読みやすい数値文字列にする。"""
    s = f"{x:.{nd}f}".rstrip("0").rstrip(".")
    return s or "0"


def _verdict_reason(c: dict, s: dict) -> str:
    """
    判定ラベルの根拠を、実際の値を添えて説明する。
    分岐の順序は scoring.verdict_of と対応させること（片方だけ変えない）。
    """
    v = c["verdict"]
    Vn, U, R = c["Vn"], c["U"], c["R"]
    score = c["score"]
    if v == "失効":
        return (f"猶予期間 $d_i$ が {_fmt(c['d_i'], 1)} と負のため、"
                "着手しても契約満了に間に合わないと整理した（緊急度に起因）。")
    if v == "即着手":
        return (f"最終スコア（$V \\times U \\times R$ = {_fmt(score, 3)}）が "
                "0.25 以上の基準を満たしたため「即着手」と判定。")
    if v == "VMO主導候補":
        return (f"延長回数 {c.get('ext_count', 0)} 回が閾値 "
                f"{int(s.get('ext_threshold', 2))} 回に達したため浮上させた。"
                f"スコア（{_fmt(score, 3)}）は割り引いていない ── 期待価値が"
                "小さいのではなく、現場任せでは動いていない可能性を示す。")
    if v == "人間判断":
        return (f"緊急度 $U$ = {_fmt(U)}（≧0.5）と切迫している一方、"
                f"情報熟度 $R$ = {_fmt(R)}（<0.7）が低い。"
                "情報熟度に起因して機械判定を保留する。")
    if v == "温存":
        return (f"期待価値 $V_n$ = {_fmt(Vn)}（>0.3）は高いが、"
                f"緊急度 $U$ = {_fmt(U)}（<0.4）が低い。時間的余裕に起因する保留。")
    if v == "捨てる候補":
        return (f"正規化後の期待価値 $V_n$ = {_fmt(Vn)} が 0.1 を下回る。"
                "期待価値に起因する低位。")
    return (f"スコア {_fmt(score, 3)}（$V_n$={_fmt(Vn)} / $U$={_fmt(U)} / "
            f"$R$={_fmt(R)}）はいずれの明示基準にも該当せず「検討」に留めた。")


def _build_logic_appendix(top: dict, s: dict, sec_no: int) -> list[str]:
    """計算ロジックの詳細解説（要件は direction/data_spec.md が正）。"""
    lam = s["lambda_risk"]
    h = s["lead_time_h_months"]
    p = top.get("p_effective", top.get("exec_probability"))
    net = top["net"]
    d_i = top["d_i"]
    U, R = top["U"], top["R"]
    sigma = top["return_sigma"]
    g = min(max(d_i, 0.0) / h, 1.0)

    L: list[str] = []
    L.append(f"## {sec_no}. 参考情報：計算ロジックの詳細解説")
    L.append(f"提示されたJSONデータに基づき、最上位案件 {top['contract_name']} "
             "の算出根拠を解説する。")
    L.append("")

    # 1. 実行確度 p
    L.append("1.  **実行確度 ($p$) の算出**")
    if top.get("p_split_used"):
        pc, pe = top["p_contest"], top["p_exec_effective"]
        L.append(f"    *   `p: {_fmt(p, 3)}` は、切替の土俵が成立する確率"
                 f"（$p_{{contest}}: {_fmt(pc)}$）と現場が完遂する確率"
                 f"（$p_{{exec}}: {_fmt(pe)}$）の積。")
        L.append(f"    *   **計算**: ${_fmt(pc)} \\times {_fmt(pe)} = {_fmt(p, 3)}$")
    elif top.get("is_bundle"):
        L.append(f"    *   `p: {_fmt(p, 3)}` は束ね候補のため、構成契約それぞれの確度の積を"
                 "件数で緩めた合成値（$\\prod p_i^{1/\\sqrt{n}}$）。"
                 "束ねはオールオアナッシング性を持つため個別より低く出る。")
    else:
        L.append(f"    *   `p: {_fmt(p, 3)}` は `exec_probability` 単独の値。"
                 "`contestability_prob` / `execution_prob` が未入力のため"
                 "内訳（土俵成立×完遂）には分解できない。")
    L.append(f"    *   延長回数 {top.get('ext_count', 0)} 回は $p$ に反映していない"
             "（確度ではなく判定ラベル側で扱う）。")

    # 2. 期待リターンと価値
    L.append("2.  **期待リターンと価値 ($net$, $V_{raw}$)**")
    L.append(f"    *   **$net$ ({_fmt(net, 1)})**: 想定リターン({_fmt(top['est_return_m'], 1)}) "
             f"－ 切替コスト({_fmt(top['switch_cost_m'], 1)})。")
    L.append(f"    *   **$V_{{raw}}$ ({_fmt(top['V_raw'], 2)})**: $net$ を確度 $p$ と"
             f"リスク回避度 $\\lambda$ で調整した値。")
    L.append(f"    *   **計算**: $p \\times net \\times (1-\\lambda(1-p)) = "
             f"{_fmt(p, 3)} \\times {_fmt(net, 1)} \\times "
             f"(1-{_fmt(lam)}(1-{_fmt(p, 3)})) = {_fmt(top['V_raw'], 2)}$")
    L.append(f"    *   **$V_n$ ({_fmt(top['Vn'], 3)})**: 候補中の最大 $V_{{raw}}$ で"
             "割った相対値。金額の絶対額でスコアを押し切らせないための正規化。")

    # 3. 緊急度と猶予期間
    L.append("3.  **緊急度 ($U$) と 猶予期間 ($d_i$)**")
    L.append(f"    *   **$d_i$ ({_fmt(d_i, 1)})**: 契約満了({_fmt(top['expiry_months'], 1)}) "
             f"－ リードタイム({_fmt(top['switch_lead_months'], 1)})。")
    if d_i < 0:
        L.append(f"    *   **$U$ ({_fmt(U)})**: $d_i$ が負のため 0。着手可能な窓が既にない。")
    else:
        L.append(f"    *   **$U$ ({_fmt(U)})**: $1/(1+d_i/h)$、$h={_fmt(h, 1)}$ ヶ月。"
                 "$d_i$ が小さいほど 1.0 に近づき、緊急性が高まる。")

    # 4. 情報熟度
    L.append("4.  **情報熟度 ($R$)**")
    L.append(f"    *   **$R$ ({_fmt(R, 3)})**: 不確実性（sigma: {_fmt(sigma)}）を"
             f"期限の切迫度で補正した値。$1 - \\sigma \\times \\min(d_i/h, 1) = "
             f"1 - {_fmt(sigma)} \\times {_fmt(g, 3)} = {_fmt(R, 3)}$。")
    L.append("    *   期限が迫るほど補正が効き、情報が固まっていなくても判断を先送りしない。")

    # 5. フラグと判定
    L.append("5.  **フラグと判定 ($verdict$)**")
    L.append(f"    *   {_verdict_reason(top, s)}")
    if top.get("is_bundle"):
        L.append("    *   束ね候補のため、構成契約はランキングから置き換えられている"
                 "（総リターンは増えるが確度は下がる、諸刃の判定）。")
    L.append("")
    return L


def build_report(scored: dict) -> str:
    s = scored["scenario"]
    lines: list[str] = []

    lines.append("# ベンダー切替投資ポートフォリオ 判断レポート")
    lines.append("")
    lines.append(f"基準日: {scored['as_of']}")
    lines.append("")

    # 節番号は「その回に出力した節」で連番にする（条件付きの節があるため）。
    n = _Counter()

    # シナリオ設定
    lines.append(f"## {n.next()}. シナリオ設定")
    lines.append("")
    lines.append(f"- リスク回避度 λ: {s['lambda_risk']}")
    lines.append(f"- 束ねプレミアム β: {s['beta_bundle']}")
    lines.append(f"- リードタイム基準 h: {s['lead_time_h_months']} ヶ月")
    lines.append(f"- 束ね評価: {'有効' if s['use_bundle'] else '無効'}")
    lines.append("")

    # 優先度ランキング
    lines.append(f"## {n.next()}. 優先度ランキング")
    lines.append("")
    lines.append("| 順位 | 対象 | ネット(M) | p有効 | V | U | R | 残月 | スコア | 判定 |")
    lines.append("|---:|---|---:|---:|---:|---:|---:|---:|---:|---|")
    for i, c in enumerate(scored["candidates"], 1):
        mark = ""
        if c.get("is_bundle"):
            mark += " 🔗"
        if c.get("ext_escalated"):
            mark += f" ⚠×{c.get('ext_count', 0)}"
        p_eff = c.get("p_effective", c.get("exec_probability"))
        lines.append(
            f"| {i} | {c['contract_name']}{mark} | {c['net']:.0f} | {p_eff:.2f} "
            f"| {c['Vn']:.2f} | {c['U']:.2f} | {c['R']:.2f} | {c['d_i']:.1f} "
            f"| {c['score']:.3f} | {c['verdict']} |"
        )
    lines.append("")
    if any(c.get("ext_escalated") for c in scored["candidates"]):
        lines.append("⚠×n = 延長 n 回。現場任せでは切り替わらない兆候として判定を"
                     "「VMO主導候補」へ浮上させている（確度・スコアは割り引いていない）。"
                     "スコアが低いまま浮上している案件は、期待価値が小さいのではなく"
                     "**誰も動かしていない**可能性を示す。")
        lines.append("")
    if scored.get("excluded_inactive"):
        lines.append("**対象外（is_active=0）**: " + "、".join(scored["excluded_inactive"])
                     + "（Single-source確定等で交渉トラックへ移管）。")
        lines.append("")

    # 束ね判定
    if scored["bundle_decisions"]:
        lines.append(f"## {n.next()}. 束ね（ベンダー単位）判定")
        lines.append("")
        for d in scored["bundle_decisions"]:
            if d["adopted"]:
                verdict = f"**束ねを採用**（束ね価値 {d['bundle_V']} ≧ 個別合計 {d['indiv_V']}）"
            else:
                verdict = f"個別が有利（束ね価値 {d['bundle_V']} ＜ 個別合計 {d['indiv_V']}）"
            lines.append(f"- {d['vendor']}（{d['n']}件）: {verdict}")
        lines.append("")

    # 最上位の説明
    top = next((c for c in scored["candidates"] if c["d_i"] >= 0 and c["score"] > 0), None)
    if top:
        lines.append(f"## {n.next()}. 最上位案件の位置づけ")
        lines.append("")
        p = top.get("p_effective", top.get("exec_probability"))
        lines.append(
            f"**{top['contract_name']}** が最上位。期待ネット {top['net']:.0f}百万円・"
            f"確度 {p*100:.0f}%、着手期限まで残り {top['d_i']:.1f}ヶ月（緊急度 {top['U']*100:.0f}%）、"
            f"情報熟度 {top['R']*100:.0f}%。期待価値・緊急度・情報熟度の3つが揃うため最優先と判断する。"
        )
        lines.append("")

    # 計算ロジックの詳細解説（data_spec.md「計算ロジック解説節の要件」）
    detail_top = top or (scored["candidates"][0] if scored["candidates"] else None)
    if detail_top:
        lines.extend(_build_logic_appendix(detail_top, s, n.next()))

    return "\n".join(lines)
