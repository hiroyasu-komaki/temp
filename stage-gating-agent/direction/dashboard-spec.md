# ダッシュボード出力仕様

`index.html` が `assets/js/data.js` の `DATA.summary` / `DATA.records` を描画する。
計算は行わず、Python が確定した値を表示するだけ（データ定義は `data-definition.md`）。

## 画面構成（既存 budget-dashboard.html を踏襲）

1. **KPI 4枚** — 要求総額（全体）／通常投資／POC／BAU。`summary.kpi` を表示。
   BAU は前年対比（`bauDelta` / `bauDeltaPct`）を色分けで併記。
2. **全体構成** — 予算種別の構成（`byType`）と、部門別の積み上げ（`byDept`）。
3. **要点ビュー** — POCパイプライン（`pocPipeline`：Gate2時期別の件数・金額）と、
   BAU前年対比（`bauByType`：コスト種別ごとの当年度額と増減、増額=赤/減額=緑/据置=灰）。
4. **月別推移** — `summary.monthly` を積み上げSVGで2つ（実額・100%構成比）。
5. **要求明細テーブル** — `records` を表示。区分/部門で絞り込み、列クリックでソート。
   POC行は Gate2 バッジ、審査 `flags` があれば警告バッジを付す。

## 配色（既存踏襲）

- 通常投資 `--normal:#2f6f8f` / POC `--poc:#c0782a` / BAU `--bau:#5a6b52`
- 増額 `--up:#b3453b` / 減額 `--down:#2d7d5a` / 据置 `--flat:#8a93a3`

## JS ファイル分割

- `data.js` — 自動生成（`dashboard_sync`）。`DEFAULT_PARAMS` / `FIXED_PARAMS` / `DATA`。手編集禁止。
- `logic.js` — 表示補助のみ（金額フォーマット、表のフィルタ/ソート）。集計はしない。
- `ui.js` — DOM 描画（KPI・バー・SVG・テーブル）。
- `main.js` — 初期化と結線。

## 審査フラグの表示

`records[].flags` に `error` があればテーブル行に赤バッジ、`warn` は橙バッジ。
件数サマリーは `summary.audit`（processor が集約、`data.js` に同梱）で
「差し戻し候補 N件／要確認 M件」をヘッダ付近に表示する。
