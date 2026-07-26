# VMO ベンダー切替投資エージェント

保守・ライセンス契約の切替投資について、「どれから手を付けるべきか」を
「いつでも説明できる」形でレポート化するエージェント。ダッシュボードの前段
（データ生成・スコア計算・レポート）までを担う。

**予算配分は行わない。** 手元資金を枠として配分したり使い切ったりする発想は
このエージェントにはなく、出すのは優先順位とその根拠だけである
（`direction/scoring_methodology.md` §4）。

## 考え方

各契約は満了時期という締切を持つ「オプション」。切替コスト・想定リターン・実行確度は
不確実で随時更新される。どこに張るべきかを、次の3因子の積で優先度化する。

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

1. `input/contracts.csv` に契約と切替仮説を記入する（列は `direction/data_spec.md` 参照）。
   - `return_sigma`（想定リターンの確からしさ）は**空欄不可**。R の生命線のため
     空欄があると loader が停止する。
2. `input/scenario.json` でパラメータを設定する（λ, β, h, ext_threshold, 束ね評価）。
3. 実行する。

```bash
python src/Main.py

# パラメータを振って比較したいときは、シナリオJSONを複製して値を変え、複数回実行する
# （output/report.md は上書きされるので、実行ごとに退避する）
python src/Main.py --scenario mid/scenario_lambda02.json
```

Claude Code / Cowork から使う場合は `/analyze` でパイプライン実行とレポート要約まで
まとめて行える（`.claude/commands/analyze.md`）。

## 出力

- `mid/scored.json` — スコア計算済みの全候補（束ね判定適用後）
- `output/report.md` — 人間が読む説明レポート

レポートの構成は、シナリオ設定／優先度ランキング／束ね採否の根拠／最上位案件の
位置づけ／最上位案件の計算過程の詳細解説。**予算枠に収まるかを論じる節は持たない。**

## 判定ラベル

| ラベル | 意味 |
|---|---|
| 即着手 | 3因子が揃う（score ≧ 0.25）。最優先 |
| VMO主導候補 | 繰り返し延長。現場任せでは切り替わらない兆候（スコアは割り引かない） |
| 人間判断 | 締切は近いが情報が不完全。人が最終判断 |
| 温存 | 有望だが時間がある。情報を待つ |
| 捨てる候補 | 期待価値が低い |
| 失効 | 満了までに切替が間に合わない |
| 検討 | 上記以外 |

条件は `direction/scoring_methodology.md` §5 が正。

## ダッシュボード（index.html）

`index.html` をブラウザで開くと、優先度ランキングをその場で試せる。
表示データ（`assets/js/data.js`）は `python src/Main.py` を実行するたびに
`input/contracts.csv` / `input/scenario.json` の内容へ自動で同期される
（`src/modules/dashboard_sync.py`）。手動での再生成コマンドは不要。

UIで調整できるのは「評価基準日」「手元資金」「安全余裕」「束ね評価のON/OFF（と束ねプレミアム）」
「先延ばしへの厳しさ（延長ペナルティのプリセット）」の5項目のみ。
`lambda_risk` や `lead_time_h_months` は効果の説明が難しいため固定表示にとどめている
（値は `input/scenario.json` を参照）。

ダッシュボードでは、ランキング表の「対象」チェックボックスでユーザーが案件を手動選択
する。選んだ案件の合計が本コミット額・期待ネット・ROI（総回収ベース、損益分岐点100%）・
手元資金との差額としてKPIに反映される。これは自動配分ではなく、ユーザー自身の選択を
手元資金と突き合わせて見るための表示である（本体パイプラインには対応する処理がない）。
束ね案件（同一ベンダーの一括契約案）は、個別契約より有利かどうかに関わらず常にランキ
ングに表示され、背景色で区別される（どちらを選ぶかはユーザーの判断）。詳細は
`CLAUDE.md` の「ダッシュボード」節を参照。

## パラメータ（input/scenario.json）

| キー | 意味 |
|---|---|
| lambda_risk | リスク回避度。上げるほど低確度案件を割り引く |
| beta_bundle | 束ねプレミアム。同一ベンダー一括交渉の交渉力（≧1） |
| lead_time_h_months | 緊急度Uの基準リードタイム（月） |
| ext_threshold | 「VMO主導候補」へ浮上させる延長回数の閾値（既定2） |
| use_bundle | ベンダー単位の束ねを評価に含めるか |
| as_of_date | 評価基準日 |
| budget_m | 手元資金（百万円）。**ダッシュボード表示専用**（本体は未使用） |
| safety_margin | 安全余裕。**ダッシュボード表示専用**（本体は未使用） |

`budget_m` / `safety_margin` は本体パイプラインが読まない。予算配分を行わないため、
これらはダッシュボードでユーザーの選択と手元資金を突き合わせる表示にのみ使う
（`scenario.json` から削除してもパイプラインは動作する）。

## 構成

```
vmo-agent/
├── .claude/commands/   スキル定義（/analyze）
├── src/Main.py         エントリポイント
├── src/modules/        loader / scoring / reporter / dashboard_sync
├── direction/          判断根拠（scoring_methodology.md / data_spec.md）
├── input/              契約CSV・シナリオJSON
├── mid/                中間ファイル
├── output/             成果物
├── requirements.txt
├── CLAUDE.md
└── README.md
```
