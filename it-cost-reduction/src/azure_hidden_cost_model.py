"""第4章 Azure利用に伴う見えにくいコストのモデル(図4-2)を生成する。

金額は年間支出(億円、仮定)。t は Azure OpenAI を採用してからの年数。
  Azureの消費額        Az(t) = 図4-1(azure_beachhead_model.py)の ①AI基盤＋②データ基盤＋③コンピュート・その他
  Unified Support増分   US(t) = US_RATE × Az(t)
      … Unified Support は Microsoft 全体の支出額に連動し、Azure/Dynamics 系は Office 系より高い料率(付録A.2)
  クロスクラウド連携(AWS上の業務システムとAzureの連携)
      データ転送(両クラウドのegress)  E(t) = EGRESS_RATE × (A_data(t) + A_comp(t))
      中継サーバ                      R(t) = RELAY_UNIT × n(t)、n(t) = floor(RELAY_BASE + RELAY_MAX × 連携の進み具合)
                                       連携の進み具合 = (A_data + A_comp) / (CAP_DATA + CAP_COMP)
      セキュリティ・監視の二重化       S(t) = SEC_FIXED(連携開始後) + SEC_RATE × Az(t)
  数値は構造を示すための仮定値。

使い方：python3 src/azure_hidden_cost_model.py → images/04_azure-hidden-cost-model.png を出力
"""
from pathlib import Path
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
import azure_beachhead_model as bh  # noqa: E402  (フォント・色・図4-1の消費額を共有)

US_RATE = 0.10       # Unified Support の Azure 分料率(付録A.2：Azure/Dynamics 系 8〜12%)
EGRESS_RATE = 0.08   # データ転送(両クラウドのegress)：データ基盤・コンピュート消費額に対する比率
RELAY_UNIT = 0.10    # 中継サーバ1系統あたりの年間費用(億円)
RELAY_BASE = 1       # 連携開始時の中継サーバ系統数
RELAY_MAX = 9        # 連携が進んだときに追加される系統数
SEC_START = 1.0      # クロスクラウド連携が始まる年
SEC_FIXED = 0.2      # セキュリティ・監視の二重化の固定費(億円)
SEC_RATE = 0.04      # 同、Azure消費額に対する比率


def costs(t):
    ai, data, comp, _ = bh.layers(t)
    az = ai + data + comp
    us = US_RATE * az
    egress = EGRESS_RATE * (data + comp)
    progress = (data + comp) / (bh.CAP_DATA + bh.CAP_COMP)
    started = t >= SEC_START
    relay = np.where(started, RELAY_UNIT * np.floor(RELAY_BASE + RELAY_MAX * progress), 0.0)
    sec = np.where(started, SEC_FIXED + SEC_RATE * az, 0.0)
    return az, us, egress, relay, sec


def main():
    t = np.linspace(0, bh.HORIZON, 1601)
    az, us, egress, relay, sec = costs(t)
    hidden = us + egress + relay + sec
    total = az + hidden

    INK, NAVY, ACCENT = bh.INK, bh.NAVY, bh.ACCENT
    fig, ax = plt.subplots(figsize=(12.5, 6.4))
    ax.stackplot(t, az, us, egress, relay, sec,
                 colors=["#9db4cc", ACCENT, "#dd9a5f", "#e9bd92", "#f3dcc4"], alpha=0.95, lw=0)
    ax.plot(t, az, color=NAVY, lw=2)
    ax.plot(t, total, color=INK, lw=1.4)

    # Azureの消費額は図の中に、見えにくいコストは右側に引き出し線で記載
    ax.text(5.6, 2.6, "Azureの消費額\n(Azureの請求として見えるコスト)", ha="center", va="center", fontsize=11, color=NAVY)
    tops = np.cumsum([az[-1], us[-1], egress[-1], relay[-1], sec[-1]])
    lows = [az[-1], tops[1], tops[2], tops[3]]
    highs = [tops[1], tops[2], tops[3], tops[4]]
    labels = ["Unified Support増分(Azure利用に連動)", "データ転送(両クラウドのegress)",
              "中継サーバ(連携の追加ごとに増設)", "セキュリティ・監視の二重化"]
    label_y = [8.6, 10.2, 11.8, 13.4]
    xr = bh.HORIZON
    for lo, hi, lab, ly in zip(lows, highs, labels, label_y):
        ax.annotate(lab, xy=(xr, (lo + hi) / 2), xytext=(xr + 0.35, ly), fontsize=9.5, color=INK, va="center",
                    annotation_clip=False, arrowprops=dict(arrowstyle="-", color=INK, lw=0.7, shrinkA=0, shrinkB=0))
    ax.text(xr + 0.35, 14.6, "どちらのクラウドにも計上されにくいコスト(死角)", fontsize=10, color=ACCENT, va="center")
    ax.text(xr + 0.35, 4.9, "見えるコスト", fontsize=10, color=NAVY, va="center")
    ax.annotate("", xy=(xr + 0.2, 0), xytext=(xr + 0.2, az[-1]), annotation_clip=False,
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=2.5, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(xr + 0.2, az[-1] + 0.1), xytext=(xr + 0.2, total[-1]), annotation_clip=False,
                arrowprops=dict(arrowstyle="-", color=ACCENT, lw=2.5, shrinkA=0, shrinkB=0))

    j = np.searchsorted(t, 4.0)
    ax.annotate("Azureの利用が増えるほど、\nUnified Supportが雪だるま式に増える", xy=(4.0, float(az[j] + us[j] / 2)),
                xytext=(0.3, 9.5), fontsize=10, color=INK, arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))
    k = np.searchsorted(t, 5.0)
    ax.annotate("AWS上の業務システムとの連携が増えるほど、\n転送・中継・セキュリティのコストが積み上がる",
                xy=(5.0, float(az[k] + us[k] + egress[k] + relay[k])), xytext=(0.3, 12.6), fontsize=10, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))

    ax.set_xlim(0, bh.HORIZON); ax.set_ylim(0, 15)
    ax.set_xticks(range(bh.HORIZON + 1))
    ax.set_xlabel("Azure OpenAI 採用からの年数")
    ax.set_ylabel("年間支出(億円、仮定)")
    ax.set_title("図4-2　Azure利用に伴う見えにくいコストの積み上がり", loc="left", color=INK, fontsize=13)
    fig.subplots_adjust(left=0.07, right=0.66, top=0.92, bottom=0.1)
    fig.savefig(bh.OUT / "04_azure-hidden-cost-model.png")
    plt.close(fig)
    return float(az[-1]), float(us[-1]), float(egress[-1]), float(relay[-1]), float(sec[-1]), float(hidden[-1] / az[-1])


if __name__ == "__main__":
    print("図4-2  8年目 Azure=%.2f, US=%.2f, egress=%.2f, 中継=%.2f, セキュリティ=%.2f, 見えにくいコスト比=%.2f" % main())
