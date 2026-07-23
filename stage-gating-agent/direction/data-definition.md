# データ定義 — 正規化レコードと集計サマリー

このドキュメントは、Python パイプラインが生成する正規形（`mid/`）・集計結果（`output/`）・
ダッシュボード供給データ（`assets/js/data.js`）の**正**である。コードを変えるときは
必ずこのドキュメントも更新し、乖離させないこと（`adapter.py` / `processor.py` / `dashboard_sync.py`）。

## 全体方針（役割分担）

- **Python 側（`src/`）が集計まで完了する。** 正規化・検証・審査・集計・月別按分・
  構成比まで Python で確定させ、結果を JSON として渡す。
- **HTML/JS 側は描画に専念する。** 受け取った集計済み値をそのまま描く。JS 側で
  金額の合算・按分・比率計算は行わない（表のソート／フィルタ等、表示操作のみ）。
- データは CSV ではなく **JSON**（`data.js` に `const` 埋め込み）で受け渡す。
  `file://` で `index.html` を直接開いても fetch 不要で動く。

## パイプライン段階と成果物

```
input/*.csv（生・可変スキーマ）
  └─ adapter  … 列マッピングで正規スキーマへ変換     → mid/canonical_invest.csv, mid/canonical_bau.csv
  └─ loader   … 正規形CSVを投資/BAU判別・検証        → 検証済みレコード
  └─ processor… 正規化 → 審査フラグ付与 → 集計        → output/normalized.json, output/summary.json
  └─ dashboard_sync … 描画用に統合                     → assets/js/data.js
```

`output/*.json` と `assets/js/data.js` は同じ processor 出力から並列に書き出す
（`data.js` を `output/` や `mid/` から生成するわけではない）。HTML が参照するのは `data.js` のみ。

## 0. 入力スキーマの吸収（adapter）

`input/` の生CSVは列名が変化しうる。adapter が `settings.INPUT_MAPPING` に従って
現行の正規スキーマ（`CANONICAL_INVEST_COLUMNS` / `CANONICAL_BAU_COLUMNS`）へ変換し、
`mid/` に正規形CSVとして書き出す。以降（loader / processor）は正規形だけを見る。

- `detect`: 生ヘッダにこの列名があればその種別と判定（変わったら別名を追加）。
- `rename`: `"新しい生の列名": "正規の列名"`。無い生列は正規列名と一致すれば採用、しなければ捨てる。
- 対応の取れない正規列は空欄。**スキーマ変更時に直すのは `INPUT_MAPPING` だけ。**

## 1. 種別の自動判別（正規形での判定）

`mid/` の正規形CSVは、ヘッダ列で種別を判定する（ファイル名に依存しない）。

- ヘッダに `案件区分` を含む → **投資要求シート**（通常投資／POC）
- ヘッダに `コスト種別` を含む → **BAU 予算要求シート**
- どちらも無ければ `InputError` で停止。

## 2. 正規化レコード（`output/normalized.json` / `data.js` の `DATA.records`）

投資・BAU を**同一スキーマの1配列**に統合する。区分により使わない項目は `null`。
金額は数値（円）に正規化する。

| キー | 型 | 説明 | 由来 |
|---|---|---|---|
| `id` | str | 案件ID／項目ID | 案件ID / 項目ID |
| `dept` | str | 提出部門 | 提出部門 |
| `applicant` | str | 起案者 | 起案者 |
| `submitDate` | str | 提出日 (YYYY-MM-DD) | 提出日 |
| `category` | str | `通常投資` / `POC` / `BAU` | 案件区分（BAUは固定） |
| `name` | str | 案件名／項目名 | 案件名 / 項目名 |
| `summary` | str | 概要 | 概要（BAUは対象範囲） |
| `amount` | int | 当年度要求額（円） | 要求金額_当年度 / 当年度要求額 |
| `period` | str\|null | 実施期間 | 実施期間 |
| `roiText` | str\|null | ROI表記（通常投資） | ROI_pct |
| `npv` | int\|null | NPV（通常投資） | NPV |
| `payback` | float\|null | 回収期間_年 | 回収期間_年 |
| `gate2Time` | str\|null | Gate2想定時期（POC） | Gate2想定時期 |
| `gate2Scale` | str\|null | Gate2想定投資規模（POC） | Gate2想定投資規模 |
| `goNoGo` | str\|null | Go/No-Go条件（POC・軸4） | 軸4_検証項目_GoNoGo条件 |
| `axis1` | int\|null | 軸1 不確実性縮減スコア | 軸1_不確実性縮減スコア |
| `axis2` | int\|null | 軸2 アップサイドスコア | 軸2_アップサイドスコア |
| `axis3` | int\|null | 軸3 検証コスト可逆性スコア | 軸3_検証コスト可逆性スコア |
| `vendor` | str\|null | ベンダー（BAU） | ベンダー |
| `costType` | str\|null | コスト種別（BAU） | コスト種別 |
| `prevBudget` | int\|null | 前年度予算額（BAU） | 前年度予算額 |
| `delta` | int\|null | 増減額（BAU, 当年度−前年度） | 増減額（無ければ算出） |
| `deltaPct` | float\|null | 増減率%（BAU） | 増減率_pct（無ければ算出） |
| `deltaReason` | str\|null | 増減理由（BAU） | 増減理由 |
| `continueNeed` | str\|null | 継続要否（BAU） | 継続要否 |
| `reductionRoom` | str\|null | 削減余地（BAU） | 削減余地 |
| `vmo` | str\|null | VMO連携要否（BAU） | VMO連携要否 |
| `contractEnd` | str\|null | 契約満了/更新時期（BAU） | 契約満了_更新時期 |
| `note` | str | 表表示用の補足（区分別に生成） | 派生 |
| `flags` | list | 審査フラグ配列（§4） | 派生 |

## 3. 集計サマリー（`output/summary.json` / `data.js` の `DATA.summary`）

JS はこの構造を描くだけ。すべて Python が確定する。

```
summary = {
  meta: { fy, generatedAt, investCount, bauCount, totalCount, sources:[...] },
  kpi: {
    total, normal, poc, bau,          // 円
    investTotal,                      // normal+poc
    bauPrev, bauDelta, bauDeltaPct,   // BAU前年対比
    normalCount, pocCount, bauCount,
    normalPct, pocPct, bauPct         // 対 total（%）
  },
  byType: [ {name:"通常投資", value}, {name:"POC", value}, {name:"BAU", value} ],
  byDept: [ {dept, 通常投資, POC, BAU, total} ],   // total 降順
  monthly: { labels:[...12...], normal:[...], poc:[...], bau:[...] },  // 円/月
  pocPipeline: [ {gate2, count, amount} ],          // Gate2想定時期 昇順
  bauByType:   [ {costType, amount, prev, delta} ], // amount 降順
  bauByVendor: [ {vendor, amount, count} ]          // amount 降順（VMO入口）
}
```

### 月別按分ロジック（`monthly`）

会計年度は `settings.FY_START_YEAR` の4月〜翌3月（12か月）。

- **投資（通常投資・POC）**：`実施期間`（`YYYY-MM〜YYYY-MM`）を FY 内の月に均等割り。
  期間が FY 外なら端に丸める。パースできなければ按分から除外。
- **BAU**：通年コストとみなし、当年度要求額を12等分。

## 4. 審査フラグ（`flags` / `summary.audit` は processor が集約）

`appendix/*-sheet-design.md` の記入規律をコード化する。各フラグは
`{level, code, message}`。`level` は `error`（差し戻し相当）/`warn`（要確認）。

### 投資シート
- `CATEGORY_INVALID`(error): `案件区分` が `通常投資`/`POC` 以外。
- `POC_HAS_ROI`(error): POC なのに ROI/NPV 等（C群）が記入されている（区分違い）。
- `NORMAL_HAS_AXIS`(error): 通常投資なのに 4軸（D群）が記入されている（区分違い）。
- `POC_MISSING_UNCERTAINTY`(error): POC で軸1縮減内容（D2）が空（規律欠如→差し戻し）。
- `POC_MISSING_GONOGO`(error): POC で Go/No-Go条件（D7）が空（同上）。
- `POC_MISSING_GATE2`(warn): POC で Gate2想定時期（E1）が空（接続情報欠落）。
- `NORMAL_MISSING_ROI`(warn): 通常投資で ROI 未記入。

### BAU シート
- `BAU_MISSING_REASON`(error): 増減理由（C6）が空（空欄禁止）。
- `BAU_LARGE_DELTA`(warn): 増減率の絶対値が `settings.BAU_LARGE_DELTA_PCT`（既定10%）以上。
- `BAU_REDUCTION_NO_VMO`(warn): 削減余地=あり かつ VMO連携要否=不要（交渉機会の取りこぼし懸念）。

閾値は `src/config/settings.py` の `FIXED_PARAMS`（審査系）で一元管理する。
