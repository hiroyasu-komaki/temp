"""第4章 Azureのビーチヘッド戦略モデル(図4-1)を生成する。

金額はAzureの年間支出(億円、仮定)。t は Azure OpenAI を採用してからの年数。
  入口のAIから、隣接領域へ遅れて広がる
      ① AI基盤(Azure OpenAI)          A_ai(t)   = CAP_AI   / (1 + exp(-K_AI   (t - MID_AI)))
      ② データ基盤(SQL Server等)        A_data(t) = CAP_DATA / (1 + exp(-K_DATA (t - MID_DATA)))
      ③ コンピュート・その他サービス     A_comp(t) = CAP_COMP / (1 + exp(-K_COMP (t - MID_COMP)))
  数値は構造を示すための仮定値。

使い方：python3 src/azure_beachhead_model.py → images/04_azure-beachhead-model.png を出力
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

HORIZON = 8
NOW = 2
CAP_AI, K_AI, MID_AI = 2.5, 2.0, 1.5
CAP_DATA, K_DATA, MID_DATA = 3.0, 1.5, 4.0
CAP_COMP, K_COMP, MID_COMP = 4.5, 1.2, 5.5
US_RATE = 0.10        # Unified Support の Azure 分料率(付録A：Azure/Dynamics 系 8〜12%)
AWS_NOW = 6.0
AWS_SHIFT = 0.8       # 新規システムが Azure に寄ることによる AWS の減少幅(億円)

OUT = Path(__file__).resolve().parent.parent / "images"
INK, NAVY, GRAY, LIGHT, ACCENT = "#1b2430", "#12305e", "#8a94a3", "#d9dee6", "#c8641e"

_installed = {f.name for f in font_manager.fontManager.ttflist}
JP_FONT = next((f for f in ["Hiragino Sans", "Hiragino Kaku Gothic ProN", "Noto Sans CJK JP", "IPAexGothic"]
                if f in _installed), "sans-serif")
plt.rcParams.update({
    "font.family": JP_FONT, "font.size": 11, "axes.edgecolor": GRAY, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "axes.spines.top": False,
    "axes.spines.right": False, "savefig.dpi": 200,
})


def logistic(t, cap, k, mid):
    return cap / (1 + np.exp(-k * (t - mid)))


def layers(t):
    ai = logistic(t, CAP_AI, K_AI, MID_AI)
    data = logistic(t, CAP_DATA, K_DATA, MID_DATA)
    comp = logistic(t, CAP_COMP, K_COMP, MID_COMP)
    us = US_RATE * (ai + data + comp)
    return ai, data, comp, us


def aws(t):
    ai, data, comp, _ = layers(t)
    total = ai + data + comp
    t0 = sum(layers(np.array([NOW]))[:3])[0]
    cap = CAP_AI + CAP_DATA + CAP_COMP
    return AWS_NOW - AWS_SHIFT * np.clip((total - t0) / (cap - t0), 0, 1)


def main():
    t = np.linspace(0, HORIZON, 801)
    ai, data, comp, _ = layers(t)

    fig, ax = plt.subplots(figsize=(11, 5.8))
    ax.stackplot(t, ai, data, comp, colors=[ACCENT, NAVY, "#9db4cc"], alpha=0.85, lw=0)

    def mid_y(lo, hi, x):
        i = np.searchsorted(t, x)
        return float((lo[i] + hi[i]) / 2)
    s1, s2, s3 = ai, ai + data, ai + data + comp
    ax.text(5.5, 1.25, "① 入口：AI基盤(Azure OpenAI)", ha="center", va="center", fontsize=10.5, color="white")
    ax.text(6.3, mid_y(s1, s2, 6.3), "② 隣接領域：データ基盤(SQL Server等)", ha="center", va="center", fontsize=10.5, color="white")
    ax.text(6.3, mid_y(s2, s3, 6.3) + 0.4, "③ さらに隣接：コンピュート・その他Azureサービス", ha="center", va="center", fontsize=10.5, color=INK)
    ax.annotate("「今すぐ必要」な機能で足場を築く", xy=(1.3, 0.9), xytext=(0.2, 4.2),
                fontsize=10, color=INK, arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))
    ax.annotate("AIとつなぐ手間を避けるため、\n隣接するサービスも同じクラウドに寄る", xy=(4.2, 3.6), xytext=(1.6, 7.6),
                fontsize=10, color=INK, arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))

    ax.set_xlim(0, HORIZON); ax.set_ylim(0, 11)
    ax.set_xticks(range(HORIZON + 1))
    ax.set_xlabel("Azure OpenAI 採用からの年数")
    ax.set_ylabel("Azureの年間支出(億円、仮定)")
    ax.set_title("図4-1　Azureのビーチヘッド戦略モデル", loc="left", color=INK, fontsize=13)
    fig.tight_layout()
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / "04_azure-beachhead-model.png")
    plt.close(fig)
    total = ai + data + comp
    return float(total[-1]), float(ai[-1] / total[-1])


if __name__ == "__main__":
    print("図4-1  8年目Azure=%.2f, AI比率=%.2f" % main())
