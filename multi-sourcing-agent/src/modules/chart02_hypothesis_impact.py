# -*- coding: utf-8 -*-
"""
02_hypothesis_impact.png を再生成する。
【仮説パート:3パラメータ合意済み】競争見積もりによる削減インパクト

パネル①②はxlsxの「前提」「計算」シートの数式をそのまま使用(3年評価と同じロジック)。
パネル③④は元資料に合わせてY1-Y5の5年間で表示するが、xlsxの評価期間は3年
(前提!C8)であるため、Y4・Y5のRFP実行コストは実データが無い。
そこで「Y3/Y2のコスト逓減比率をそのまま延長する」という単純なルールで
延長した参考値として算出する(=このパネルのみ推定を含む旨をグラフ内に明記)。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt

import common
from common import CATEGORY_COLORS, CATEGORY_ORDER

OUTPUT_FILENAME = "02_hypothesis_impact.png"

COLOR_FACT = "#3a3a3a"
COLOR_FACT2 = "#8a6a1e"
COLOR_HYPOTHESIS = "#2e6a9e"
COLOR_HYPOTHESIS2 = "#2e8b57"
COLOR_RFP_LINE = "#c0392b"
COLOR_NET = "#2e8b57"
COLOR_CUM_NET = "#8e44ad"


def render(mid_dir=common.DEFAULT_MID_DIR, output_dir=common.DEFAULT_OUTPUT_DIR):
    common.setup_japanese_font()
    inputs = common.load_inputs_from_mid(mid_dir)
    n_extend = 5
    calc_rows = common.load_calc_from_mid(mid_dir)

    total_it_spend = inputs.it_spend
    total_sole_source = sum(r.sole_source for r in calc_rows)
    total_competitive = sum(r.competitive for r in calc_rows)
    total_mid_reduction = sum(r.reduction_mid for r in calc_rows)

    fig, axes = plt.subplots(2, 2, figsize=(19.5, 15.6))
    ax1, ax2, ax3, ax4 = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

    fig.suptitle(
        "【仮説パート:3パラメータ合意済み】競争見積もりによる削減インパクト",
        fontsize=19,
        fontweight="bold",
        y=0.985,
    )
    fig.text(
        0.5,
        0.955,
        "合意済: 競争可能割合(現場)・削減率レンジ(調達購買)・実行コスト(VMO) ／ 金額は代表値プレースホルダ、実データ差込で確定",
        ha="center",
        fontsize=11,
        color="#444444",
    )

    # ---- ① 事実から合意仮説への接続 ----
    labels = ["年間\nIT支出", "随意契約\n(事実)", "競争対象\n(合意割合)", "期待削減\n(合意率)"]
    values = [total_it_spend, total_sole_source, total_competitive, total_mid_reduction]
    bar_colors = [COLOR_FACT, COLOR_FACT2, COLOR_HYPOTHESIS, COLOR_HYPOTHESIS2]
    bars = ax1.bar(labels, values, color=bar_colors, width=0.6)
    for b, v in zip(bars, values):
        ax1.text(b.get_x() + b.get_width() / 2, v + total_it_spend * 0.015, f"{v:,.0f}\n({v / 100:.1f}億)", ha="center", fontsize=11)
    ax1.axvline(1.5, color="#c0392b", linestyle="--", linewidth=1)
    ax1.text(0.5, total_it_spend * 0.92, "←事実", ha="center", fontsize=10, color="#3a3a3a")
    ax1.text(2.4, total_it_spend * 0.92, "合意仮説→", ha="center", fontsize=10, color="#2e6a9e")
    ax1.set_title("① 事実から合意仮説への接続", fontsize=13.5)
    ax1.set_ylabel("金額(百万円)", fontsize=11)
    ax1.set_ylim(0, total_it_spend * 1.05)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # ---- ② カテゴリ別 期待削減額(合意レンジ付き) ----
    rows_sorted = sorted(calc_rows, key=lambda r: r.reduction_mid, reverse=True)
    names = [r.name for r in rows_sorted]
    mids = [r.reduction_mid for r in rows_sorted]
    los = [r.reduction_conservative for r in rows_sorted]
    his = [r.reduction_optimistic for r in rows_sorted]
    colors2 = [CATEGORY_COLORS[n] for n in names]
    y_pos = range(len(names))[::-1]

    ax2.barh(list(y_pos), mids, color=colors2, height=0.6)
    err_lo = [m - lo for m, lo in zip(mids, los)]
    err_hi = [hi - m for m, hi in zip(mids, his)]
    ax2.errorbar(mids, list(y_pos), xerr=[err_lo, err_hi], fmt="none", ecolor="black", capsize=4, linewidth=1.2)
    for yp, m in zip(y_pos, mids):
        ax2.text(m + max(his) * 0.03, yp, f"{m:,.0f}", va="center", fontsize=11)
    ax2.set_yticks(list(y_pos))
    ax2.set_yticklabels([n.replace("・", "・\n") if len(n) > 8 else n for n in names], fontsize=10.5)
    ax2.set_title("② カテゴリ別 期待削減額(合意レンジ付き)", fontsize=13.5)
    ax2.set_xlabel("年間期待削減額(百万円) ― バーは中位、線は保守〜楽観レンジ", fontsize=10.5)
    ax2.set_xlim(0, max(his) * 1.15)
    total_mid = sum(mids)
    total_lo = sum(los)
    total_hi = sum(his)
    ax2.text(
        0.98,
        0.03,
        f"中位合計 {total_mid:,.0f}百万/年\n(保守 {total_lo:,.0f}〜楽観 {total_hi:,.0f})",
        transform=ax2.transAxes,
        ha="right",
        fontsize=10.5,
        bbox=dict(boxstyle="round", facecolor="#eaf6ee", edgecolor="#2e8b57"),
    )
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    # ---- ③ 更新到来に沿った効果の立ち上がり (Y1〜Y5, 累積グロス削減) ----
    year_labels5 = [f"Y{t}" for t in range(1, n_extend + 1)]
    bottoms = [0.0] * n_extend
    for name in CATEGORY_ORDER:
        row = next(r for r in calc_rows if r.name == name)
        seg = [row.gross_reduction_by_year[t] for t in range(1, n_extend + 1)]
        ax3.bar(year_labels5, seg, bottom=bottoms, color=CATEGORY_COLORS[name], label=name, width=0.6)
        bottoms = [b + s for b, s in zip(bottoms, seg)]
    for x, total in enumerate(bottoms):
        ax3.text(x, total + max(bottoms) * 0.015, f"{total:,.0f}", ha="center", fontsize=11)
    ax3.set_title("③ 更新到来に沿った効果の立ち上がり", fontsize=13.5)
    ax3.set_xlabel("経過年", fontsize=11)
    ax3.set_ylabel("累積グロス削減(百万円/年)", fontsize=11)
    ax3.set_ylim(0, max(bottoms) * 1.2)
    ax3.legend(loc="lower right", fontsize=9, framealpha=0.9)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)

    # ---- ④ 実行コスト控除後のネット効果と累積 (Y1〜Y5) ----
    gross5 = bottoms  # 上で計算済みの累積グロス削減(中位)
    rfp3 = list(inputs.rfp_cost)  # Y1,Y2,Y3(xlsxの実データ)
    # Y4・Y5はxlsxの評価期間(3年)を超えるため、Y3/Y2の逓減比率を延長した参考値
    decay_ratio = rfp3[2] / rfp3[1] if rfp3[1] else 1.0
    rfp5 = rfp3 + [rfp3[-1] * decay_ratio, rfp3[-1] * decay_ratio ** 2]
    net5 = [g - c for g, c in zip(gross5, rfp5)]

    cumulative_net = []
    running = 0.0
    for v in net5:
        running += v
        cumulative_net.append(running)

    x_pos = range(n_extend)
    width = 0.35
    ax4b = ax4.twinx()
    ax4.bar([p - width / 2 for p in x_pos], gross5, width=width, color="#7fb8e0", label="グロス削減")
    ax4.bar([p + width / 2 for p in x_pos], net5, width=width, color="#2e8b57", label="ネット削減")
    ax4.plot(x_pos, rfp5, color=COLOR_RFP_LINE, marker="o", linewidth=1.8, label="実行コスト(合意)")
    ax4b.plot(x_pos, cumulative_net, color=COLOR_CUM_NET, marker="s", linestyle="--", linewidth=1.8, label="累積ネット(右軸)")

    for p, v in zip(x_pos, gross5):
        pass
    for p, v in zip(x_pos, net5):
        ax4.text(p + width / 2, v + max(gross5) * 0.02, f"{v:,.0f}", ha="center", fontsize=9.5, color="#1f6b3d")
    for p, v in zip(x_pos, cumulative_net):
        ax4b.text(p, v + max(cumulative_net) * 0.02, f"{v:,.0f}", ha="center", fontsize=9, color=COLOR_CUM_NET)

    ax4.set_xticks(list(x_pos))
    ax4.set_xticklabels(year_labels5)
    ax4.set_title("④ 実行コスト控除後のネット効果と累積", fontsize=13.5)
    ax4.set_xlabel("経過年", fontsize=11)
    ax4.set_ylabel("単年 金額(百万円)", fontsize=11)
    ax4b.set_ylabel("累積ネット削減(百万円)", fontsize=11, color=COLOR_CUM_NET)
    ax4.set_ylim(0, max(gross5) * 1.25)
    ax4b.set_ylim(0, max(cumulative_net) * 1.25)

    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4b.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=9, framealpha=0.9)
    ax4.text(
        0.98,
        0.06,
        f"{n_extend}年累積ネット\n≈{cumulative_net[-1]:,.0f}百万({cumulative_net[-1] / 100:.1f}億)",
        transform=ax4.transAxes,
        ha="right",
        fontsize=10.5,
        color=COLOR_CUM_NET,
        bbox=dict(boxstyle="round", facecolor="#f3ecf8", edgecolor=COLOR_CUM_NET),
    )
    ax4.spines["top"].set_visible(False)

    fig.text(
        0.5,
        0.005,
        "※④のY4・Y5はxlsxの評価期間(3年)を超えるため実データが無く、Y3/Y2の実行コスト逓減比率を延長した参考値",
        ha="center",
        fontsize=9,
        color="#777777",
    )

    fig.tight_layout(rect=(0, 0.02, 1, 0.93))

    output_dir = common.ensure_output_dir(output_dir)
    out_path = os.path.join(output_dir, OUTPUT_FILENAME)
    fig.savefig(out_path)
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    path = render()
    print(f"saved: {path}")
