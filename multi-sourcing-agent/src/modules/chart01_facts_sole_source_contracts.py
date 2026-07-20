# -*- coding: utf-8 -*-
"""
01_facts_sole_source_contracts.png を再生成する。
【事実の提示】随意契約80%の内訳 ― カテゴリ別・契約更新時期別
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt

import common
from common import CATEGORY_COLORS, CATEGORY_ORDER, RENEWAL_TIMING_RATIOS

OUTPUT_FILENAME = "01_facts_sole_source_contracts.png"


def render(mid_dir=common.DEFAULT_MID_DIR, output_dir=common.DEFAULT_OUTPUT_DIR):
    common.setup_japanese_font()
    inputs = common.load_inputs_from_mid(mid_dir)
    calc_rows = common.load_calc_from_mid(mid_dir)
    by_name = {r.name: r for r in calc_rows}

    total_sole_source = sum(r.sole_source for r in calc_rows)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(19.5, 8.2))
    fig.suptitle(
        f"【事実の提示】随意契約{inputs.sole_source_ratio * 100:.0f}%の内訳 ― カテゴリ別・契約更新時期別",
        fontsize=18,
        fontweight="bold",
        y=0.985,
    )
    fig.text(
        0.5,
        0.945,
        "※支出比率・更新分布は一般的代表値のプレースホルダ。実データ差込で確定。ここは全て「事実」であり合意対象ではない",
        ha="center",
        fontsize=10.5,
        color="#444444",
    )

    # ---- ① カテゴリ別 随意契約額 ----
    names = CATEGORY_ORDER
    values = [by_name[n].sole_source for n in names]
    colors = [CATEGORY_COLORS[n] for n in names]
    y_pos = range(len(names))[::-1]

    ax1.barh(list(y_pos), values, color=colors)
    ax1.set_yticks(list(y_pos))
    ax1.set_yticklabels(names, fontsize=12)
    ax1.set_xlabel("随意契約の金額(百万円)", fontsize=11)
    ax1.set_title(
        f"① どのカテゴリにいくら ― 随意契約 計{total_sole_source:,.0f}百万円({total_sole_source / 100:.1f}億円)",
        fontsize=13,
    )
    xmax = max(values) * 1.55
    ax1.set_xlim(0, xmax)
    for yp, v in zip(y_pos, values):
        ax1.text(
            v + xmax * 0.012,
            yp,
            f"{v:,.0f}百万\n({v / 100:.2f}億)",
            va="center",
            fontsize=10.5,
        )
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # ---- ② 契約更新時期別分布 ----
    timing_labels = list(RENEWAL_TIMING_RATIOS.keys())
    bottoms = [0.0] * len(timing_labels)
    for name in names:
        amt = by_name[name].sole_source
        seg_values = [amt * RENEWAL_TIMING_RATIOS[t] for t in timing_labels]
        ax2.bar(
            timing_labels,
            seg_values,
            bottom=bottoms,
            color=CATEGORY_COLORS[name],
            label=name,
            width=0.6,
        )
        bottoms = [b + s for b, s in zip(bottoms, seg_values)]

    for x, total in enumerate(bottoms):
        ax2.text(
            x,
            total + max(bottoms) * 0.015,
            f"{total:,.0f}\n({total / 100:.1f}億)",
            ha="center",
            fontsize=11,
            fontweight="bold",
        )

    ax2.set_title("② いつ競争のテーブルに載せられるか ― 更新時期別分布", fontsize=13)
    ax2.set_xlabel("契約更新の到来時期", fontsize=11)
    ax2.set_ylabel("随意契約の金額(百万円)", fontsize=11)
    ax2.set_ylim(0, max(bottoms) * 1.22)
    ax2.legend(loc="upper right", fontsize=9.5, framealpha=0.9)
    ax2.text(
        0.02,
        0.97,
        "更新時期が来た契約しか競争にかけられない。\nこの分布が施策の「実行スケジュール」を規定する",
        transform=ax2.transAxes,
        fontsize=9,
        va="top",
        bbox=dict(boxstyle="round", facecolor="#f0f0f0", edgecolor="#cccccc"),
    )
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.tight_layout(rect=(0, 0, 1, 0.93))

    output_dir = common.ensure_output_dir(output_dir)
    out_path = os.path.join(output_dir, OUTPUT_FILENAME)
    fig.savefig(out_path)
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    path = render()
    print(f"saved: {path}")
