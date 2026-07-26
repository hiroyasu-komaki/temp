# 予算要求プロセス設計

予算要求を3区分（通常投資／POC／BAU）に分け、区分ごとに必須項目を定義することで説明性と管理強度を上げる提案。POCが投資区分から脱落し「突然登場する」問題への対処を中核課題とする。

## 構成

| ファイル | 内容 |
|---|---|
| `proposal/budget-process-design.md` | **提案書本体**。課題認識 → 3区分の設計原理 → データモデル → POCのゲート管理 → 運用 |
| `appendix/theory-real-options.md` | 付録A：理論的根拠。POCをROI/NPVで測ってはならない理由（リアルオプション等） |
| `appendix/data-item-definition.md` | 付録B：データ項目定義。3区分の列レベル完全定義 |
| `sample/budget-request-unified.csv` | 統合シートのサンプルデータ（35件・全3区分） |
| `budget-dashboard.html` | 集計ダッシュボード。上記CSVを読み込んで表示 |

ダッシュボードはブラウザで `budget-dashboard.html` を開く。ローカルファイルとして直接開くとfetchが使えないため、同内容の埋め込みデータで表示される。CSVを差し替えて反映させる場合は簡易サーバ経由で開く（例：`python3 -m http.server` してから `http://localhost:8000/budget-dashboard.html`）。

## 読む順序

1. `proposal/budget-process-design.md` の要旨 → 第1章（課題）→ 第2章（設計原理）
2. データ項目の詳細が必要なら付録B
3. 「なぜPOCをROIで測らないのか」への反論に備えるなら付録A
