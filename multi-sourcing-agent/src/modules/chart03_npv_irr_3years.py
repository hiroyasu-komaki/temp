# -*- coding: utf-8 -*-
"""
03_npv_irr_3years.png を再生成する。
【投資評価:3年】競争見積もり施策のNPV / IRR 展開
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt

import common

OUTPUT_FILENAME = "03_npv_irr_3years.png"

COLOR_NET_LINE = "#1f7a4c"
COLOR_GROSS = "#4a90c4"
COLOR_RFP = "#e8a08a"
COLOR_VMO_OPEX = "#b5342a"
COLOR_PRE_DISCOUNT = "#a9cbe8"
COLOR_POST_DISCOUNT = "#2e5f8a"
COLOR_CUM_UNDISCOUNTED = "#999999"
COLOR_CUM_NPV = "#7b3fa0"


def render(mid_dir=common.DEFAULT_MID_DIR, output_dir=common.DEFAULT_OUTPUT_DIR):
    common.setup_japanese_font()
    inputs = common.load_inputs_from_mid(mid_dir)
    ev = common.load_investment_eval_from_mid(mid_dir)

    initial_investment = inputs.prep_cost + inputs.vmo_initial_cost

    fig, axes = plt.subplots(2, 2, figsize=(19.5, 15.6))
    ax1, ax2, ax3, ax4 = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

    fig.suptitle(
        "【投資評価:3年】競争見積もり施策のNPV / IRR 展開", fontsize=19, fontweight="bold", y=0.985
    )
    fig.text(
        0.5,
        0.955,
        f"初期投資{initial_investment:,.0f}百万(準備費用{inputs.prep_cost:,.0f}+立ち上げ{inputs.vmo_initial_cost:,.0f}) "
        f"+ RFP実行コスト・VMO運営費を控除した「真のネット」で評価 ／ WACC {inputs.wacc * 100:.0f}%・評価期間{inputs.eval_years:.0f}年",
        ha="center",
        fontsize=11,
        color="#444444",
    )

    years = [1, 2, 3]
    year_labels = [f"Y{t}" for t in years]

    # ---- ① 年次キャッシュフローの構成 ----
    gross = [ev.gross_reduction[t] for t in years]
    rfp = [-ev.rfp_cost[t] for t in years]
    vmo = [-ev.vmo_opex[t] for t in years]
    net = [ev.net_cf[t] for t in years]

    ax1.bar(year_labels, gross, color=COLOR_GROSS, label="グロス削減(+)", width=0.55)
    ax1.bar(year_labels, rfp, color=COLOR_RFP, label="RFP実行コスト(−)", width=0.55)
    ax1.bar(year_labels, vmo, bottom=rfp, color=COLOR_VMO_OPEX, label="VMO運営費(−)", width=0.55)
    ax1.plot(year_labels, net, color=COLOR_NET_LINE, marker="o", markersize=9, linewidth=2.2, label="真のネット(=CF)")
    for x, v in zip(year_labels, net):
        ax1.text(x, v + max(gross) * 0.03, f"{v:,.0f}", ha="center", fontsize=11, color=COLOR_NET_LINE, fontweight="bold")
    ax1.axhline(0, color="black", linewidth=0.8)
    ax1.set_title("① 年次キャッシュフローの構成", fontsize=13.5)
    ax1.set_ylabel("金額(百万円)", fontsize=11)
    ax1.legend(loc="upper left", fontsize=9.5, framealpha=0.9)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # ---- ② 割引前 vs 割引後キャッシュフロー ----
    all_labels = ["Y0"] + year_labels
    pre = [ev.net_cf[0]] + [ev.net_cf[t] for t in years]
    post = [ev.discounted_cf[0]] + [ev.discounted_cf[t] for t in years]
    x_pos = range(len(all_labels))
    width = 0.35
    ax2.bar([p - width / 2 for p in x_pos], pre, width=width, color=COLOR_PRE_DISCOUNT, label="割引前CF")
    ax2.bar([p + width / 2 for p in x_pos], post, width=width, color=COLOR_POST_DISCOUNT, label=f"割引後CF(WACC{inputs.wacc * 100:.0f}%)")
    for p, v in zip(x_pos, pre):
        ax2.text(p - width / 2, v + (5 if v >= 0 else -18), f"{v:,.0f}", ha="center", fontsize=9.5)
    for p, v in zip(x_pos, post):
        ax2.text(p + width / 2, v + (5 if v >= 0 else -18), f"{v:,.0f}", ha="center", fontsize=9.5)
    ax2.axhline(0, color="black", linewidth=0.8)
    ax2.set_xticks(list(x_pos))
    ax2.set_xticklabels(all_labels)
    ax2.set_title("② 割引前 vs 割引後キャッシュフロー", fontsize=13.5)
    ax2.set_ylabel("金額(百万円)", fontsize=11)
    ax2.legend(loc="upper left", fontsize=9.5, framealpha=0.9)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    # ---- ③ 累積NPVカーブと回収点 ----
    cum_undiscounted = [ev.cumulative_cf_undiscounted[t] for t in (0, 1, 2, 3)]
    cum_npv = [ev.cumulative_npv[t] for t in (0, 1, 2, 3)]
    ax3.plot(all_labels, cum_undiscounted, color=COLOR_CUM_UNDISCOUNTED, linestyle="--", marker="s", label="累積CF(割引前)")
    ax3.plot(all_labels, cum_npv, color=COLOR_CUM_NPV, marker="o", linewidth=2.2, label="累積NPV(割引後)")
    for x, v in zip(all_labels, cum_npv):
        ax3.text(x, v + (max(cum_npv) * 0.05 if v >= 0 else -max(cum_npv) * 0.09), f"{v:,.0f}", ha="center", fontsize=10, color=COLOR_CUM_NPV)
    ax3.axhline(0, color="#c0392b", linewidth=1, linestyle=":")
    if ev.payback_years == ev.payback_years:  # not NaN
        ax3.axvline(ev.payback_years, color="#2e8b57", linewidth=1.2, linestyle="--")
        ax3.text(
            ev.payback_years,
            ax3.get_ylim()[1] if False else max(cum_npv) * 0.55,
            f"割引回収\n{ev.payback_years:.2f}年",
            fontsize=10,
            color="#2e8b57",
            ha="left",
        )
    ax3.fill_between(range(len(all_labels)), cum_npv, 0, where=[v >= 0 for v in cum_npv], color=COLOR_CUM_NPV, alpha=0.08)
    ax3.set_title("③ 累積NPVカーブと回収点", fontsize=13.5)
    ax3.set_ylabel("累積(百万円)", fontsize=11)
    ax3.legend(loc="upper left", fontsize=9.5, framealpha=0.9)
    ax3.text(
        0.98,
        0.05,
        f"NPV({inputs.eval_years:.0f}年)={ev.npv:,.0f}百万\n({ev.npv / 100:.1f}億円)",
        transform=ax3.transAxes,
        ha="right",
        fontsize=11,
        bbox=dict(boxstyle="round", facecolor="#f3ecf8", edgecolor=COLOR_CUM_NPV),
    )
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)

    # ---- ④ 投資評価サマリ ----
    ax4.axis("off")
    ax4.set_title("④ 投資評価サマリ", fontsize=13.5, loc="left")

    cum_net_undiscounted_1to3 = sum(ev.net_cf[t] for t in years)
    summary_rows = [
        (f"NPV ({inputs.eval_years:.0f}年, WACC{inputs.wacc * 100:.0f}%)", f"{ev.npv:,.0f} 百万円 / {ev.npv / 100:.1f} 億円", COLOR_CUM_NPV),
        ("IRR", f"{ev.irr * 100:,.0f}%", COLOR_NET_LINE),
        ("割引回収期間", f"{ev.payback_years:.2f} 年", COLOR_POST_DISCOUNT),
        ("収益性指数 PI", f"{ev.pi:.1f}  (投資1に対し価値{ev.pi:.1f})", COLOR_VMO_OPEX),
        (f"{inputs.eval_years:.0f}年累積ネット(割引前・Y1-Y3)", f"{cum_net_undiscounted_1to3:,.0f} 百万円 / {cum_net_undiscounted_1to3 / 100:.1f} 億円", "#555555"),
    ]
    n = len(summary_rows)
    box_h = 0.15
    top = 0.88
    for i, (label, value, color) in enumerate(summary_rows):
        y0 = top - i * (box_h + 0.02)
        ax4.add_patch(
            plt.Rectangle((0.0, y0 - box_h), 1.0, box_h, transform=ax4.transAxes, fill=True, facecolor="#faf9f6", edgecolor=color, linewidth=1.8)
        )
        ax4.text(0.03, y0 - box_h / 2, label, transform=ax4.transAxes, fontsize=12, va="center")
        ax4.text(0.97, y0 - box_h / 2, value, transform=ax4.transAxes, fontsize=13, va="center", ha="right", color=color, fontweight="bold")

    ax4.text(
        0.0,
        top - n * (box_h + 0.02) - 0.02,
        "※準備費用・VMO人件費まで投資に含めた保守評価。\n"
        f"評価期間{inputs.eval_years:.0f}年に短縮・Y4以降の継続効果は含めない(=上振れ余地)。\n"
        "削減率を「保守」レンジに置いてもNPVプラスを維持",
        transform=ax4.transAxes,
        fontsize=9.5,
        va="top",
        color="#555555",
    )

    fig.tight_layout(rect=(0, 0, 1, 0.93))

    output_dir = common.ensure_output_dir(output_dir)
    out_path = os.path.join(output_dir, OUTPUT_FILENAME)
    fig.savefig(out_path)
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    path = render()
    print(f"saved: {path}")
