"""
settings — プロジェクト全体で参照する設定を集約する。

パス定数・会計年度・区分/種別のマスタ・審査閾値をここに置くことで、各モジュールが
ディレクトリ構成やチューニング値をハードコードせずに済む。数値の調整はコードではなく
ここで行う方針。

DEFAULT_PARAMS / FIXED_PARAMS は dashboard_sync 経由で assets/js/data.js にも
書き出され、ブラウザ側と同じ既定値を共有できる。
"""
from __future__ import annotations
from pathlib import Path

# ---- パス定数 -------------------------------------------------------------
# settings.py = <ROOT>/src/config/settings.py なので parents[2] がプロジェクトルート。
ROOT = Path(__file__).resolve().parents[2]

INPUT_DIR = ROOT / "input"          # 生CSV（スキーマ可変）の置き場所
MID_DIR = ROOT / "mid"              # adapter が変換した「正規形CSV」の置き場所（processor の入力）
OUTPUT_DIR = ROOT / "output"        # processor の集計結果JSON（normalized/summary）
ASSETS_DIR = ROOT / "assets"
DATA_JS_PATH = ASSETS_DIR / "js" / "data.js"

# adapter が書き出す正規形CSV（mid/）。種別ごとに1本。
CANONICAL_INVEST_CSV = MID_DIR / "canonical_invest.csv"
CANONICAL_BAU_CSV = MID_DIR / "canonical_bau.csv"

# processor の集計結果（output/）
NORMALIZED_JSON = OUTPUT_DIR / "normalized.json"
SUMMARY_JSON = OUTPUT_DIR / "summary.json"

# ---- 会計年度 -------------------------------------------------------------
# 4月始まりの12か月。月別按分（processor）とラベル（dashboard）で共有する。
FY_START_YEAR = 2026
FY_START_MONTH = 4  # 4月始まり

# ---- 区分・種別マスタ -----------------------------------------------------
CATEGORY_NORMAL = "通常投資"
CATEGORY_POC = "POC"
CATEGORY_BAU = "BAU"
INVEST_CATEGORIES = (CATEGORY_NORMAL, CATEGORY_POC)
ALL_CATEGORIES = (CATEGORY_NORMAL, CATEGORY_POC, CATEGORY_BAU)

# 投資シート／BAUシートの判別に使う識別列（正規形。loader が使う）
INVEST_MARKER_COL = "案件区分"
BAU_MARKER_COL = "コスト種別"

# ---- 正規スキーマ（現行CSVの列。adapter の出力＝processor の入力の正） -------
# 入力CSVのスキーマが変わっても、adapter がこの列セット・列順の CSV に変換する。
CANONICAL_INVEST_COLUMNS = [
    "案件ID", "提出部門", "起案者", "提出日", "案件区分", "案件名", "概要",
    "ビジネスメリット定性", "要求金額_当年度", "実施期間", "関連部門",
    "投資総額", "想定リターン年額", "ROI_pct", "NPV", "回収期間_年", "リターン根拠",
    "軸1_不確実性縮減スコア", "軸1_縮減する不確実性の内容",
    "軸2_アップサイドスコア", "軸2_アップサイド概要", "軸3_検証コスト可逆性スコア",
    "軸4_判断期限", "軸4_検証項目_GoNoGo条件",
    "Gate2想定時期", "Gate2想定投資規模", "本格投資時の想定所管",
    "ゲート判定", "オプション枠計上", "台帳ID", "審査コメント",
]
CANONICAL_BAU_COLUMNS = [
    "項目ID", "提出部門", "起案者", "提出日", "項目名", "コスト種別", "ベンダー",
    "対象範囲", "契約満了_更新時期",
    "前年度予算額", "前年度実績額", "当年度要求額", "増減額", "増減率_pct", "増減理由",
    "継続要否", "削減余地", "削減余地の内容", "VMO連携要否",
    "査定結果", "査定後金額", "VMO引継", "審査コメント",
]

# ---- 入力→正規 の列マッピング（スキーマ変更時はここだけ直す） --------------
# adapter の動作:
#   1) 生CSVのヘッダに `detect` のいずれかがあれば、その種別と判定する。
#   2) 各生列は `rename`（元列名→正規列名）で対応づける。rename に無い生列は、
#      正規列名と一致すればそのまま採用し、一致しなければ捨てる。
#   3) 上記で対応が取れなかった正規列は空欄にする。
# ＝ 現行CSVと同じ列名のうちはマッピング不要（恒等）。列名が変わったら rename に
#    「新しい生列名: 正規列名」を1行足すだけでよい。
INPUT_MAPPING: dict = {
    "invest": {
        "detect": ["案件区分"],   # 生CSVでの区分列名（変わったら別名を追加）
        "rename": {
            # "新しい生の列名": "正規の列名",
            # 例) "区分": "案件区分",
            # 例) "当年度要求額": "要求金額_当年度",
        },
    },
    "bau": {
        "detect": ["コスト種別"],
        "rename": {
            # 例) "種別": "コスト種別",
        },
    },
}

# ---- 既定パラメータ（UIで露出しうる値） -----------------------------------
DEFAULT_PARAMS: dict = {
    # 現状ダッシュボードで動かすパラメータは無し（集計は Python 側で確定）。
}

# ---- 固定パラメータ（審査閾値など。UIには出さない） -----------------------
FIXED_PARAMS: dict = {
    "fy_label": f"FY{FY_START_YEAR}",
    # BAU 増減率がこの絶対値(%)以上で「大きな増減」警告
    "bau_large_delta_pct": 10.0,
}
