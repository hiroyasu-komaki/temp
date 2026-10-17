"""第3章 ベンダーロックインの図示モデル(図3-1・図3-2)を生成する。

共通の時間軸
  t は利用開始からの年数。利用開始時は利用ゼロ・契約なしで、従量課金(個別購入／オンデマンド)から始まる。
  CONTRACT_START 年目にベンダーからのオファーで法人契約(MS：EA／AWS：PPA)を締結し、以後 TERM 年ごとに更新する。

図3-1 Microsoft：ロックイン後の価格転嫁モデル(従量 → land → expand → 回収)
  単価はリストプライスを100とした指数。
  利用ユーザー数(全社展開率)  N(t) = L(t) (1 - N_DROP · D(t))
      L(t) = 1 / (1 + exp(-A_N (t - T_N)))        … 試行(数十人)→導入期(100〜1,000人)→展開期(全社員)
      D(t) = 1 / (1 + exp(-A_D (t - T_D)))        … 代替製品の登場・利用方法の細分化による収束
      N_DROP = 0.4 のとき、収束後の展開率は約60%
  ベンダー単価(契約締結・更新時にのみ改定)
      従量期(t < CONTRACT_START)  リストプライス(個別購入)
      契約後                      VENDOR_PRICES[k](k 番目の契約期間の単価。仮定値)
      … 導入期・拡張期はリストプライスを下回る値引き(MSの持ち出し)。
        2回目の契約期間を「回収期への移行判断期」とし、その次の更新から
        リストプライスを上回る水準に引き上げる(MSの回収)。判断の基準や判断者は不明
  MSの持ち出し = ∫max(リストプライス - 単価, 0)dt、MSの回収 = ∫max(単価 - リストプライス, 0)dt(1ユーザーあたり)

図3-2 AWS：コミット契約によるロックインモデル
  金額はユーザーの予算の天井を100とした指数。描画期間は AWS_HORIZON 年。
  従量制の支払額(コミット契約なし)  U(t) = 100 (3x^2 - 2x^3)、x = min(t / T_CAP, 1)
      … 三次曲線(S字)で増え、T_CAP 年目に予算の天井に達したあとは天井に張り付く
  コミット契約(CONTRACT_START 年目から TERM 年ごとに更新)
      割引後の利用額   V(t) = U(t) (1 - DISCOUNT)
      必要なコミット額 初回は締結時点の V、更新時は Req_k = max(Commit_(k-1) (1 + MIN_UPLIFT), V(更新時点))
      契約するかどうか Req_k < U(更新時点) なら契約する。Req_k ≥ U(更新時点) なら契約せず従量制に戻る
      支払額           契約期間中は Pay(t) = max(コミット額, V(t))、契約しない期間は U(t)
  ユーザーのメリット = ∫(U(t) - Pay(t))dt
  割引の目減り       = コミット額 > V(t) の期間の ∫(コミット額 - V(t))dt
  最適化ケース：OPT_START 年目から最適化を始めた場合の利用額
      Uo(t) = U(t) (1 - R(t))、R(t) = R_MAX (3y^2 - 2y^3)、y = min((t - OPT_START) / T_OPT_FULL, 1)
      … 小さな最適化から始まり、2〜3年目に大きく効いて、T_OPT_FULL 年で最大の削減率に達する
      コミット額・契約判断・支払額は U を Uo に置き換えて同じ規則で計算する

使い方：python3 src/lock_in_models.py  → images/03_*.png を出力
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

# ---- 共通 ----
CONTRACT_START = 2  # 法人契約・コミット契約を締結する年
TERM = 3            # 契約期間(年)
HORIZON = 14        # 描画期間(年)
RENEWALS = list(range(CONTRACT_START, HORIZON, TERM))   # 締結・更新の時点

# ---- パラメータ(図3-1) ----
P_LIST = 100      # リストプライス
EMPLOYEES = 20000     # 全社員数(仮定)
A_N, T_N = 1.63, 3.8  # 展開の速さと中間点(0年目≒0.2%＝数十人、2年目≒5%＝約1,000人)
A_D, T_D = 1.2, 9.0   # 収束の速さと中間点
N_DROP = 0.4          # 収束による減少幅(全社員の40%が離脱し、約60%で継続)
VENDOR_PRICES = [70, 90, 139, 145]   # 契約期間ごとの単価(2年目締結、5・8・11年目更新)

# ---- パラメータ(図3-2) ----
T_CAP = 6           # 従量制の支払額が予算の天井に達する年
DISCOUNT = 0.10     # コミット契約の割引率
MIN_UPLIFT = 0.05   # 更新時に前回コミット額を上回る幅(仮定)
AWS_HORIZON = 20    # 図3-2の描画期間(年)
OPT_START = 6       # 最適化ケース：最適化を始める年
R_MAX = 0.15        # 最適化ケース：最終的な削減率
T_OPT_FULL = 4      # 最適化ケース：最大の削減率に達するまでの年数
ACCENT = "#c8641e"  # 最適化ケースの強調色

OUT = Path(__file__).resolve().parent.parent / "images"
INK, NAVY, GRAY, LIGHT = "#1b2430", "#12305e", "#8a94a3", "#d9dee6"

_installed = {f.name for f in font_manager.fontManager.ttflist}
JP_FONT = next((f for f in ["Hiragino Sans", "Hiragino Kaku Gothic ProN", "Noto Sans CJK JP", "IPAexGothic"]
                if f in _installed), "sans-serif")
plt.rcParams.update({
    "font.family": JP_FONT, "font.size": 11, "axes.edgecolor": GRAY, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "axes.spines.top": False,
    "axes.spines.right": False, "savefig.dpi": 200,
})


def term_index(t):
    """各時点が何番目の契約期間か(従量期は -1)。"""
    k = np.minimum(((t - CONTRACT_START) // TERM).astype(int), len(RENEWALS) - 1)
    return np.where(t < CONTRACT_START, -1, k)


def draw_renewals(ax):
    for r in RENEWALS:
        ax.axvline(r, color=LIGHT, lw=1, zorder=0)


# ======== 図3-1 Microsoft ========
def adoption(t):
    rise = 1 / (1 + np.exp(-A_N * (t - T_N)))
    drop = 1 / (1 + np.exp(-A_D * (t - T_D)))
    return rise * (1 - N_DROP * drop)


def fig_microsoft():
    t = np.linspace(0, HORIZON, 1401)
    prices = VENDOR_PRICES
    k = term_index(t)
    p = np.where(k < 0, P_LIST, np.array(prices, dtype=float)[np.clip(k, 0, None)])
    recover_at = next(r for r, pr in zip(RENEWALS, prices) if pr > P_LIST)

    fig, (ax0, ax) = plt.subplots(2, 1, figsize=(11, 8.8), sharex=True,
                                  gridspec_kw={"height_ratios": [1.4, 3.4], "hspace": 0.08})
    # 上段：利用ユーザー数
    n = adoption(t) * 100
    ax0.fill_between(t, 0, n, color=LIGHT)
    ax0.plot(t, n, color=GRAY, lw=1.8)
    ax0.set_ylim(0, 125); ax0.set_yticks([0, 50, 100]); ax0.set_ylabel("展開率(%)")
    ax0.text(HORIZON - 0.1, 80, f"利用ユーザー数\n(全社展開率、全社員{EMPLOYEES:,}人)", ha="right", fontsize=10, color=INK)
    for x, label in [(0.6, "試行"), (1.9, "導入期"), (4.2, "展開期"), (10.0, "収束期")]:
        ax0.text(x, 112, label, ha="center", fontsize=9.5, color=INK)
    for x, txt, dy in [(0.0, "数十人", 14), (2.0, "約1,000人", 14)]:
        y = float(adoption(x)) * 100
        ax0.annotate(txt, xy=(x, y), xytext=(x + 0.15, y + dy + 20), fontsize=8.5, color=INK,
                     arrowprops=dict(arrowstyle="-", color=INK, lw=0.6))
    y_end = float(adoption(HORIZON)) * 100
    ax0.text(HORIZON - 0.1, y_end - 14, f"約{y_end:.0f}%で継続", ha="right", fontsize=9, color=INK)
    draw_renewals(ax0)
    ax0.set_title("図3-1　ロックイン後の価格転嫁モデル(Microsoft)", loc="left", color=INK, fontsize=13)

    # 下段：単価
    INVEST, RECOVER = "#9db4cc", NAVY   # MSの持ち出し／回収
    ax.fill_between(t, p, P_LIST, where=p < P_LIST, color=INVEST, alpha=0.55, lw=0)
    ax.fill_between(t, P_LIST, p, where=p > P_LIST, color=RECOVER, alpha=0.45, lw=0)
    ax.axhline(P_LIST, color=INK, lw=1, ls="--")
    ax.plot(t, p, color=NAVY, lw=2.6, label="ベンダー単価(契約締結・更新時に改定)")

    dt = t[1] - t[0]
    invest = float(np.clip(P_LIST - p, 0, None).sum() * dt)
    recover = float(np.clip(p - P_LIST, 0, None).sum() * dt)
    ax.text((RENEWALS[0] + RENEWALS[1]) / 2, 85, "MSの持ち出し\n(値引き)",
            ha="center", va="center", fontsize=11, color=INK)
    ax.text((recover_at + HORIZON) / 2, 120, "MSの回収\n(リストプライス引き上げ・SKU再編・\n上位SKU誘導)",
            ha="center", va="center", fontsize=11, color="white")

    ax.text(HORIZON + 0.08, P_LIST, "リストプライス", va="center", fontsize=9, color=INK)
    # 回収期への移行判断期(2回目の契約期間)
    j0, j1 = RENEWALS[1], recover_at
    for a_ in (ax0, ax):
        a_.axvspan(j0, j1, color=ACCENT, alpha=0.10, zorder=0)
    ax.text((j0 + j1) / 2, 155, "MSによる\n回収期への移行判断期", ha="center", va="top", fontsize=10.5, color=ACCENT)
    ax.text((j0 + j1) / 2, 143,
            "業務に組み込まれ、ないと\n業務効率が著しく落ちる\n状態(移行コストが高い状態)\nになったかを見定める期間\n\n定量化は難しく、\n誰がどう判断するかは不明\n(展開率などの経験則か、\n判断していないか)",
            ha="center", va="top", fontsize=8.5, color=INK, linespacing=1.35)
    ax.annotate("法人契約(EA)の\nオファー・締結", xy=(CONTRACT_START, 70), xytext=(CONTRACT_START + 0.3, 50),
                fontsize=9.5, color=INK, arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    draw_renewals(ax)

    ax.set_xlim(0, HORIZON); ax.set_ylim(40, 160)
    ax.set_xticks(range(HORIZON + 1)); ax.set_xlabel("利用開始からの年数(縦の薄線は契約の締結・更新)")
    ax.set_ylabel("ユーザー単価(リストプライス＝100)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=1, fontsize=9, frameon=False)
    fig.subplots_adjust(left=0.08, right=0.88, top=0.95, bottom=0.13)
    fig.savefig(OUT / "03_lock-in-pricing-model.png")
    plt.close(fig)
    return recover_at, prices, round(invest, 1), round(recover, 1)


# ======== 図3-2 AWS ========
def payg(t):
    x = np.clip(np.asarray(t, dtype=float) / T_CAP, 0, 1)
    return 100 * (3 * x ** 2 - 2 * x ** 3)


def payg_opt(t):
    t = np.asarray(t, dtype=float)
    y = np.clip((t - OPT_START) / T_OPT_FULL, 0, 1)
    r = R_MAX * (3 * y ** 2 - 2 * y ** 3)
    return payg(t) * (1 - r)


def commit_plan(u_func=payg):
    """各更新時点の(時点, 必要なコミット額, 契約するか)。契約しなかった時点以降は従量制。"""
    plan, prev = [], None
    for r in range(CONTRACT_START, AWS_HORIZON, TERM):
        v = float(u_func(r)) * (1 - DISCOUNT)
        req = v if prev is None else max(prev * (1 + MIN_UPLIFT), v)
        sign = req < float(u_func(r))
        plan.append((r, req, sign))
        if not sign:
            break
        prev = req
    return plan


def scenario(t, u_func):
    u = u_func(t)
    v = u * (1 - DISCOUNT)
    plan = commit_plan(u_func)
    commit = np.full_like(t, np.nan)
    for r, req, sign in plan:
        if sign:
            commit[(t >= r) & (t < r + TERM)] = req
    contracted = ~np.isnan(commit)
    pay = np.where(contracted, np.maximum(np.nan_to_num(commit), v), u)
    return u, v, plan, commit, contracted, pay


def fig_aws():
    t = np.linspace(0, AWS_HORIZON, 6001)
    u, v, plan, commit, contracted, pay = scenario(t, payg)
    stuck = contracted & (np.nan_to_num(commit) > v)
    uo, vo, plan_o, commit_o, contracted_o, pay_o = scenario(t, payg_opt)

    fig, ax = plt.subplots(figsize=(11, 6.6))
    ax.fill_between(t, pay, u, where=contracted & (u > pay), color=NAVY, alpha=0.15,
                    label="ユーザーのメリット(従量制との差)")
    ax.fill_between(t, v, pay, where=stuck, color=NAVY, alpha=0.55,
                    label="割引の目減り(支払額がコミット額に張り付き)")
    ax.axhline(100, color=INK, lw=1, ls=":")
    ax.plot(t, u, color=GRAY, lw=2.2, label="従量制の支払額(コミット契約なし)")
    ax.plot(t, np.where(contracted, v, np.nan), color=GRAY, lw=1.2, ls=(0, (2, 2)), label="割引後の利用額")
    ax.plot(t, np.where(contracted, pay, np.nan), color=NAVY, lw=2.6, label="コミット契約時の支払額＝max(割引後の利用額, コミット額)")
    ax.plot(t, commit, color=NAVY, lw=1.2, ls=(0, (4, 3)), label="コミット額(更新時は前回を上回る必要がある)")
    mo = t >= OPT_START
    ax.plot(t[mo], uo[mo], color=ACCENT, lw=2.0, ls=(0, (5, 3)),
            label=f"最適化した場合の利用額({OPT_START}年目から最適化、最大{R_MAX:.0%}削減)")
    r_o, req_o, sign_o = plan_o[-1]
    if not sign_o:
        r_end = plan[-1][0] if not plan[-1][2] else AWS_HORIZON
        ax.axvspan(r_o, r_end, color=ACCENT, alpha=0.10, zorder=0)
        ax.text((r_o + r_end) / 2, 14, "最適化により従量制が\nコミット額を下回る余地あり", ha="center", fontsize=10.5, color=ACCENT)
        ax.plot([r_o, r_o], [float(payg_opt(r_o)) - 6, req_o + 4], color=ACCENT, lw=1.4)
        ax.plot([r_o, r_o + TERM], [req_o, req_o], color=ACCENT, lw=1.2, ls=":")
        ax.annotate(f"最適化した場合：{r_o}年目の更新で必要なコミット額(約{req_o:.0f})が\n"
                    f"利用額(約{float(payg_opt(r_o)):.0f})を上回り、契約しない(最適化しない場合より{plan[-1][0] - r_o}年早い)",
                    xy=(r_o, float(payg_opt(r_o)) - 6), xytext=(6.3, 38), fontsize=10, color=ACCENT,
                    arrowprops=dict(arrowstyle="->", color=ACCENT, lw=0.9))
    for r, req, sign in plan:
        ax.axvline(r, color=LIGHT, lw=1, zorder=0)
        if sign:
            ax.text(r + 0.08, req - 4.5, f"{req:.0f}", fontsize=9, color=NAVY)
    r_exit, req_exit, sign_exit = plan[-1]
    if not sign_exit:
        ax.plot([r_exit, AWS_HORIZON], [req_exit, req_exit], color=NAVY, lw=1.2, ls=":", alpha=0.7)
        ax.text(r_exit + 0.08, req_exit + 1.5, f"必要なコミット額 約{req_exit:.0f}", fontsize=9, color=NAVY)
        ax.axvspan(r_exit, AWS_HORIZON, color=LIGHT, alpha=0.5, zorder=0)
        mm = t >= r_exit
        ax.plot(t[mm], u[mm], color=INK, lw=3)
        ax.text((r_exit + AWS_HORIZON) / 2, 20, "従量制と\nコミット契約で\n違いなし", ha="center", fontsize=10.5, color=INK)
        ax.annotate(f"{r_exit}年目の更新：必要なコミット額(約{req_exit:.0f})が\n利用額(約100)を上回るため、契約しない",
                    xy=(r_exit, 99), xytext=(r_exit - 4.6, 64), fontsize=10, color=INK,
                    arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))
    t_stuck = t[stuck][0] if stuck.any() else None
    if t_stuck is not None:
        ax.annotate("コミット額が割引後の利用額を上回り、\n支払額がコミット額に張り付く",
                    xy=(t_stuck + 1.8, 92), xytext=(6.3, 64), fontsize=10, color=INK,
                    arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))
    ax.text(AWS_HORIZON + 0.08, 100, "予算の天井", va="center", fontsize=9, color=INK)
    ax.annotate("コミット契約の締結", xy=(CONTRACT_START, plan[0][1]), xytext=(0.3, 45),
                fontsize=9.5, color=INK, arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))

    dt = t[1] - t[0]
    area = lambda y, mm: float(((np.where(mm, y, 0)[1:] + np.where(mm, y, 0)[:-1]) / 2).sum() * dt)
    terms = [(r, area(u - pay, (t >= r) & (t < r + TERM))) for r, _, sg in plan if sg]
    ax.text(0.2, 117, "契約期間ごとのユーザーのメリット(指数)：" +
            "／".join(f"{r}〜{r + TERM}年 約{b:.0f}" for r, b in terms),
            fontsize=9.5, color=INK, va="top")
    ax.set_xlim(0, AWS_HORIZON); ax.set_ylim(0, 120)
    ax.set_xticks(range(AWS_HORIZON + 1))
    ax.set_xlabel("利用開始からの年数(縦の薄線はコミット契約の締結・更新)")
    ax.set_ylabel("年間支払額(予算の天井＝100)")
    ax.set_title("図3-2　コミット契約によるロックインモデル(AWS)", loc="left", color=INK, fontsize=13)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=9, frameon=False)
    fig.tight_layout(rect=(0, 0, 0.95, 1))
    fig.savefig(OUT / "03_commit-lock-in-model.png")
    plt.close(fig)
    return ([(r, round(q, 1), sg) for r, q, sg in plan], [(r, round(b, 1)) for r, b in terms],
            (round(float(t_stuck), 2) if t_stuck is not None else None), [(r, round(q, 1), sg) for r, q, sg in plan_o])


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    print("図3-1  回収開始=%d年目, 単価=%s, 持ち出し=%s, 回収=%s" % fig_microsoft())
    print("図3-2  plan=%s, 期ごとのメリット=%s, 張り付き開始=%s, 最適化plan=%s" % fig_aws())
