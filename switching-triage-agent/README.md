# VMO ベンダー切替投資エージェント

保守・ライセンス契約の切替投資について、リボルビング型予算の配分優先度を計算し、
「いつでも説明できる」形でレポート化するエージェント。ダッシュボードの前段
（データ生成・スコア計算・予算配分・レポート）までを担う。

## 考え方

各契約は満了時期という締切を持つ「オプション」。切替コスト・想定リターン・実行確度は
不確実で随時更新される。手元資金をどこに張るかを、次の3因子の積で優先度化する。

```
Score = V（リスク調整期待価値） × U（緊急度） × R（情報熟度）
```

積にするのは、どれか一つでも決定的に欠けたら張るべきでないから。詳細は
`direction/scoring_methodology.md` を参照。

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

（標準ライブラリのみで動作する。requirements.txt は将来の拡張用。）

## 使い方

1. `input/contracts.csv` に契約と切替仮説を記入する（列は `direction/output_spec.md` 参照）。
   - `return_sigma`（想定リターンの確からしさ）は**空欄不可**。
2. `input/scenario.json` でパラメータを設定する（λ, β, 予算, 安全余裕など）。
3. 実行する。

```bash
python src/Main.py
```

## 出力

- `mid/scored.json` — スコア計算済みの全候補（束ね判定適用後）
- `output/allocation.json` — 予算配分（本コミット・予約枠・予算不足）
- `output/report.md` — 人間が読む説明レポート

レポートには、優先度ランキング、束ね採否の根拠、そして
**予算不足で着手できなかった上位案件（＝追加資金の引き出し根拠）**が含まれる。

## ダッシュボード（index.html）

`index.html` をブラウザで開くと、優先度ランキングをその場で試せる。
表示データ（`assets/js/data.js`）は `python src/Main.py` を実行するたびに
`input/contracts.csv` / `input/scenario.json` の内容へ自動で同期される
（`src/modules/dashboard_sync.py`）。手動での再生成コマンドは不要。

UIで調整できるのは「評価基準日」「手元資金」「安全余裕」「束ね評価のON/OFF（と束ねプレミアム）」
「先延ばしへの厳しさ（延長ペナルティのプリセット）」の5項目のみ。
`lambda_risk` や `lead_time_h_months` は効果の説明が難しいため固定表示にとどめている
（値は `input/scenario.json` を参照）。

予算配分は本体パイプラインのような自動アルゴリズムではなく、ランキング表の「対象」
チェックボックスでユーザーが手動選択する方式。選んだ案件の合計が本コミット額・期待
ネット・ROI（総回収ベース、損益分岐点100%）・手元資金との差額としてKPIに反映される。
束ね案件（同一ベンダーの一括契約案）は、個別契約より有利かどうかに関わらず常にランキ
ングに表示され、背景色で区別される（どちらを選ぶかはユーザーの判断）。詳細は
`CLAUDE.md` の「ダッシュボード」節を参照。

## パラメータ（input/scenario.json）

| キー | 意味 |
|---|---|
| lambda_risk | リスク回避度。上げるほど低確度案件を割り引く |
| beta_bundle | 束ねプレミアム。同一ベンダー一括交渉の交渉力（≧1） |
| lead_time_h_months | 緊急度Uの基準リードタイム（月） |
| budget_m | 手元資金（百万円） |
| safety_margin | 本コミットに使わず残す割合 |
| use_bundle | ベンダー単位の束ねを評価に含めるか |
| as_of_date | 評価基準日 |

## 構成

```
vmo-agent/
├── .claude/commands/   スキル定義（/analyze, /compare）
├── src/Main.py         エントリポイント
├── src/modules/        loader / scoring / allocation / reporter
├── direction/          判断基準・出力仕様
├── input/              契約CSV・シナリオJSON
├── mid/                中間ファイル
├── output/             成果物
├── requirements.txt
├── CLAUDE.md
└── README.md
```
