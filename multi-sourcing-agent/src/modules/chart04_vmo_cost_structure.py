# -*- coding: utf-8 -*-
"""
04_vmo_cost_structure.png を再生成する。
VMO関連コストの3層構造(準備費用/立ち上げ投資/VMO運営費/RFP実行コスト)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt

import common

OUTPUT_FILENAME = "04_vmo_cost_structure.png"

LAYER_COLORS = {
    "prep": "#e08a1e",       # 第0層: 準備費用
    "vmo_initial": "#8a7a2b",  # 第1層: 立ち上げ投資
    "vmo_opex": "#b5342a",     # 第2層: VMO運営費
    "rfp": "#e0a08a",         # 第3層: RFP実行コスト
}


def render(mid_dir=common.DEFAULT_MID_DIR, output_dir=common.DEFAULT_OUTPUT_DIR):
    common.setup_japanese_font()
    inputs = common.load_inputs_from_mid(mid_dir)

    prep = inputs.prep_cost
    vmo_initial = inputs.vmo_initial_cost
    vmo_opex = inputs.vmo_opex
    rfp = inputs.rfp_cost  # [Y1, Y2, Y3]

    fig, ax = plt.subplots(figsize=(16.8, 8.4))
    fig.suptitle("VMO関連コストの3層構造", fontsize=18, fontweight="bold", y=0.97)

    categories = ["準備\n(今回承認)", "Y0\n立ち上げ", "Y1", "Y2", "Y3"]
    x = range(len(categories))

    # 準備 バー(第0層のみ)
    ax.bar(0, prep, color=LAYER_COLORS["prep"], width=0.6)
    ax.text(0, prep * 1.02, f"{prep:,.0f}", ha="center", fontsize=13)

    # Y0 バー(第1層のみ)
    ax.bar(1, vmo_initial, color=LAYER_COLORS["vmo_initial"], width=0.6)
    ax.text(1, vmo_initial * 1.02, f"{vmo_initial:,.0f}", ha="center", fontsize=13)

    # Y1-Y3 バー(第2層+第3層)
    for i, t in enumerate(range(3)):
        xi = 2 + i
        ax.bar(xi, vmo_opex, color=LAYER_COLORS["vmo_opex"], width=0.6)
        ax.bar(xi, rfp[t], bottom=vmo_opex, color=LAYER_COLORS["rfp"], width=0.6)
        total = vmo_opex + rfp[t]
        ax.text(xi, total * 1.015, f"{total:,.0f}", ha="center", fontsize=13)

    ax.set_xticks(list(x))
    ax.set_xticklabels(categories, fontsize=12)
    ax.set_ylabel("金額(百万円)", fontsize=11)
    ymax = max(prep, vmo_initial, vmo_opex + max(rfp)) * 1.35
    ax.set_ylim(0, ymax)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.text(
        0.01,
        0.97,
        "準備費用と立ち上げ投資は一度きり。恒常的に残るのは第2層(固定)+第3層(変動・逓減)のみ",
        transform=ax.transAxes,
        fontsize=10.5,
        va="top",
        bbox=dict(boxstyle="round", facecolor="#f0f0f0", edgecolor="#cccccc"),
    )

    legend_labels = [
        f"第0層: 準備費用(一度きり・今回の承認対象{prep:,.0f}百万)",
        f"第1層: 立ち上げ投資(一度きり{vmo_initial:,.0f}百万: 体制/プロセス/マスタ/ツール)",
        f"第2層: VMO運営費(恒常固定費{vmo_opex:,.0f}百万/年: 専任人件費・間接費)",
        f"第3層: RFP実行コスト(案件変動費・標準化で逓減{rfp[0]:.0f}→{rfp[1]:.0f}→{rfp[2]:.0f})",
    ]
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=LAYER_COLORS["prep"]),
        plt.Rectangle((0, 0), 1, 1, color=LAYER_COLORS["vmo_initial"]),
        plt.Rectangle((0, 0), 1, 1, color=LAYER_COLORS["vmo_opex"]),
        plt.Rectangle((0, 0), 1, 1, color=LAYER_COLORS["rfp"]),
    ]
    ax.legend(handles, legend_labels, loc="upper right", fontsize=10, framealpha=0.95)

    fig.tight_layout(rect=(0, 0, 1, 0.93))

    output_dir = common.ensure_output_dir(output_dir)
    out_path = os.path.join(output_dir, OUTPUT_FILENAME)
    fig.savefig(out_path)
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    path = render()
    print(f"saved: {path}")
