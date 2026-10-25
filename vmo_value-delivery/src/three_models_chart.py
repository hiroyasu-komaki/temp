"""第2章（chapters/02_introduction.md）の3モデルの推移グラフを生成する。

式・パラメータ・描き方は 02_introduction.md の 2.12「補足：3モデルの推移（グラフの仕様）」に対応する。
パラメータを変えたときは、Markdown の数値表もあわせて更新すること（--table で数値表を出力できる）。

使い方:
    python3 src/three_models_chart.py           # images/ に PNG を3枚出力
    python3 src/three_models_chart.py --table   # 0.1刻みの数値表（Markdown）を標準出力に表示

必要なもの: Python 3.9+, numpy, matplotlib
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import font_manager  # noqa: E402

# ---------------------------------------------------------------- パラメータ（2.12「曲線の式とパラメータ」）
V_START, V_A, V_B, V_K = 50.0, 201.1, 151.1, 0.905  # v(t) = 201.1 − 151.1·e^(−0.905t)：50から始まりt=1で140
GOV_D_FLOOR, GOV_D_K = 10.0, 12.0                    # ②の d(t) = 10 + 90·e^(−12t)
GOV_P_K = 11.25                                      # ②の p(t) = 1 − e^(−11.25t)
GOV_LAMBDA = 0.1875                                  # ②の伝達ロス λ
AGENT_D, AGENT_C = 100.0, 6.0                        # ③の d と調整コスト c
BASE = 100.0                                         # 現在の水準

# 個別案件のばらつき σ(t)（2.12「グラフごとの描画要素と読み取り」）
SIGMA_START = 20.0
SIGMA_END_GOV = 7.0
SIGMA_END_AGENT = 11.0
N_CASES = 30
SEED = 7  # 乱数の種。固定して毎回同じ点が打たれるようにする

# 色（2.12「共通の描き方」）
C_V, C_D, C_VMO = "#2a5fa0", "#c05a17", "#00875a"
C_BASE, C_GRID, C_AXIS, C_TEXT = "#b9b3a4", "#e4e0d6", "#c9c4b8", "#4a515f"
C_MUTED, C_BG = "#6f7268", "#ffffff"

T = np.linspace(0.0, 1.0, 41)  # 0.025刻み

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "images"


# ---------------------------------------------------------------- 曲線の式
def vmo(t):
    """VMOの専門性 v(t)。②・③で共通。"""
    return V_A - V_B * np.exp(-V_K * t)


def gov_d(t):
    """② 現場の寄与度 d(t)。"""
    return GOV_D_FLOOR + (BASE - GOV_D_FLOOR) * np.exp(-GOV_D_K * t)


def gov_p(t):
    """② 移管の進み具合 p(t)。"""
    return 1.0 - np.exp(-GOV_P_K * t)


def gov_v_mean(t):
    """② 成果の平均 V(t) = d(t) + p(t)·v(t)·(1−λ)。"""
    return gov_d(t) + gov_p(t) * vmo(t) * (1.0 - GOV_LAMBDA)


def agent_v_mean(t):
    """③ 成果の平均 V(t) = max(d, v(t) − c)。"""
    return np.maximum(AGENT_D, vmo(t) - AGENT_C)


def agent_threshold():
    """③で v(t) − c が基準を超える時刻 t*。"""
    return float(-np.log((V_A - (BASE + AGENT_C)) / V_B) / V_K)


def sigma_current(t):
    return np.full_like(t, SIGMA_START)


def sigma_gov(t):
    return SIGMA_START - (SIGMA_START - SIGMA_END_GOV) * t


def sigma_agent(t):
    ts = agent_threshold()
    shrink = np.clip((t - ts) / (1.0 - ts), 0.0, 1.0)
    return SIGMA_START - (SIGMA_START - SIGMA_END_AGENT) * shrink


# ---------------------------------------------------------------- 描画
def setup_font():
    candidates = ["Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo",
                  "Noto Sans CJK JP", "IPAexGothic", "IPAGothic"]
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in installed:
            plt.rcParams["font.family"] = name
            return name
    raise SystemExit("日本語フォントが見つかりません: " + ", ".join(candidates))


def draw(path, title, v_mean, sigma, d=None, d_offset=0.0, v_line=False, shade=None, shade_label=None, seed=SEED):
    rng = np.random.default_rng(seed)
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=200)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 軸・グリッド・基準線
    ax.set_xlim(0, 1.32)
    ax.set_ylim(0, 150)
    ax.set_yticks([0, 50, 100, 150])
    ax.tick_params(axis="y", length=0, labelsize=8, colors=C_MUTED)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["導入時", "数年後"], fontsize=8.5, color=C_MUTED)
    ax.tick_params(axis="x", length=0)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(C_AXIS)
    ax.spines["bottom"].set_bounds(0, 1)
    for y in (50, 150):
        ax.plot([0, 1], [y, y], color=C_GRID, lw=0.8, zorder=0)
    ax.plot([0, 1], [BASE, BASE], color=C_BASE, lw=0.8, ls=(0, (4, 4)), zorder=1)
    ax.text(0.012, BASE + 4, "現在 = 100", fontsize=8, color=C_MUTED)

    vm = v_mean(T)

    # 網掛け
    if shade == "below":
        ax.fill_between(T, vm, BASE, where=vm < BASE, color=C_V, alpha=0.10, lw=0, interpolate=True, zorder=1)
    elif shade == "above":
        ax.fill_between(T, vm, BASE, where=vm > BASE, color=C_V, alpha=0.10, lw=0, interpolate=True, zorder=1)

    # 個別案件の点：tを30等分した区間ごとに1件、縦位置は V(t)+N(0, σ(t))
    tc = (np.arange(N_CASES) + rng.uniform(0.15, 0.85, N_CASES)) / N_CASES
    yc = v_mean(tc) + rng.normal(0.0, 1.0, N_CASES) * sigma(tc)
    ax.scatter(tc, yc, s=12, color=C_V, alpha=0.45, lw=0, zorder=2)

    # 線
    labels = []
    if d is not None:
        dv = d(T) - d_offset
        ax.plot(T, dv, color=C_D, lw=1.6, zorder=3)
        labels.append((dv[-1], "d 現場の寄与度", C_D))
    if v_line:
        ax.plot(T, vmo(T), color=C_VMO, lw=1.6, ls=(0, (5, 4)), zorder=3)
        labels.append((vmo(T)[-1], "v VMOの専門性", C_VMO))
    ax.plot(T, vm, color=C_V, lw=2.4, solid_capstyle="round", zorder=4)
    ax.scatter([1], [vm[-1]], s=20, color=C_V, zorder=5)
    labels.append((vm[-1], "V 成果の平均", C_V))

    # 右端ラベル（重なる場合は上下にずらす）
    labels.sort(key=lambda x: x[0])
    placed = []
    for y, text, _ in labels:
        y_txt = y
        for p in placed:
            if abs(y_txt - p) < 9:
                y_txt = p + 9
        placed.append(y_txt)
        ax.text(1.025, y_txt, text, fontsize=8.5, color=C_TEXT, va="center")

    ax.set_title(title, fontsize=11, color="#1d2333", loc="left", pad=10)

    # 凡例（グラフ下）
    handles = []
    if d is not None:
        handles.append(plt.Line2D([], [], color=C_D, lw=1.6, label="現場の寄与度（d）"))
    if v_line:
        handles.append(plt.Line2D([], [], color=C_VMO, lw=1.6, ls=(0, (5, 4)), label="VMOの専門性（v）"))
    handles.append(plt.Line2D([], [], color=C_V, lw=2.4, label="成果の平均（V）"))
    handles.append(plt.Line2D([], [], color=C_V, alpha=0.45, marker="o", ls="", ms=4, label="個別案件の成果"))
    if shade_label:
        handles.append(matplotlib.patches.Patch(color=C_V, alpha=0.10, label=shade_label))
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=len(handles),
              fontsize=7, frameon=False, handlelength=1.6, columnspacing=1.0)
    fig.text(0.5, 0.01, "現在の水準を100とした指数／点は個別案件、線はその平均（概念図）",
             ha="center", fontsize=7, color=C_MUTED)

    fig.subplots_adjust(left=0.08, right=0.98, top=0.88, bottom=0.25)
    fig.savefig(path, facecolor=C_BG)
    plt.close(fig)


def build():
    setup_font()
    OUT_DIR.mkdir(exist_ok=True)
    draw(OUT_DIR / "02_model-current.png", "① 現状（分散・自前）",
         lambda t: np.full_like(np.asarray(t, float), BASE), sigma_current)
    draw(OUT_DIR / "02_model-governance.png", "② ガバナンス型（機能集約）",
         gov_v_mean, sigma_gov, d=gov_d, v_line=True,
         shade="below", shade_label="基準を下回っている期間")
    draw(OUT_DIR / "02_model-agent.png", "③ エージェント型（伴走）",
         agent_v_mean, sigma_agent, d=lambda t: np.full_like(np.asarray(t, float), AGENT_D),
         d_offset=2.1, v_line=True, shade="above", shade_label="基準への上乗せ分")
    for p in sorted(OUT_DIR.glob("02_model-*.png")):
        print("wrote", p.relative_to(ROOT))


def table():
    print("| t | v（②③共通） | d（②） | V（②） | V（③） |")
    print("|---|---|---|---|---|")
    for t in np.round(np.arange(0, 1.01, 0.1), 1):
        print(f"| {t:.1f} | {vmo(t):.0f} | {gov_d(t):.0f} | {gov_v_mean(t):.0f} | {agent_v_mean(t):.0f} |")
    tt = np.linspace(0.05, 1.0, 1901)
    tg = tt[np.argmax(gov_v_mean(tt) >= BASE)]
    print(f"\n②が基準に戻る t ≒ {tg:.3f}／③が基準を超える t* ≒ {agent_threshold():.3f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--table", action="store_true", help="数値表を出力する")
    args = ap.parse_args()
    table() if args.table else build()
