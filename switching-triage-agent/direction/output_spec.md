# 出力仕様とデータ契約

エージェントが各段階で生成するファイルの形式を定義する。

---

## input/ — 処理対象

### `input/contracts.csv`
契約と切替仮説を一元化した1行1仮説のテーブル。列：

| 列名 | 型 | 説明 |
|---|---|---|
| contract_id | int | 契約ID |
| contract_name | str | 契約名 |
| contract_type | str | Maintenance / License |
| vendor | str | 現行ベンダー名 |
| expiry_months | float | 基準日から満了までの月数 |
| annual_spend_m | float | 年間契約額（百万円） |
| switch_lead_months | float | 切替期間 tau（月） |
| switch_cost_m | float | 切替コスト（百万円） |
| switch_cost_sigma | float | 切替コストの不確実性 0..1 |
| est_return_m | float | 想定リターン（百万円） |
| return_sigma | float | リターンの不確実性 0..1（**空欄不可**） |
| exec_probability | float | 実行確度 p 0..1（後方互換用のフォールバック値。下記2列が両方あればそちらを優先） |

以下4列は**任意列**（`loader.py` の `OPTIONAL_COLUMNS`）。無くても読み込めるが、
入れると `effective_p` の計算精度が上がる。詳細は
`direction/scoring_methodology.md` §2.1.1・§3.5 参照。

| 列名 | 型 | 説明 |
|---|---|---|
| contestability_prob | float\|空欄 | 切替の土俵が成立する確率 0..1。`execution_prob` と両方揃えるか両方空欄にする（片方だけは入力エラー） |
| execution_prob | float\|空欄 | 土俵成立後、現場が切替を実行しきる確率 0..1 |
| extension_count | int | 一時延長した回数。既定0。`ext_threshold` 以上で `execution_prob` に自動ペナルティ |
| is_active | int(0/1) | 0なら評価対象外（Single-source確定などで交渉トラックへ移管）。既定1 |

### `input/scenario.json`
```json
{
  "scenario_name": "Base",
  "lambda_risk": 0.5,
  "beta_bundle": 1.15,
  "lead_time_h_months": 3.0,
  "budget_m": 20,
  "safety_margin": 0.2,
  "use_bundle": true,
  "ext_threshold": 2,
  "ext_penalty": 0.15,
  "ext_penalty_cap": 0.6,
  "as_of_date": "2026-04-01"
}
```

`ext_threshold` / `ext_penalty` / `ext_penalty_cap` は延長ペナルティのパラメータ
（`direction/scoring_methodology.md` §3.5）。`loader.py` の必須キーではなく
`scoring.py` 側で既定値（それぞれ 2 / 0.15 / 0.6）にフォールバックするが、
明示指定を推奨する。

---

## mid/ — 中間ファイル

### `mid/scored.json`
スコア計算済みの全候補（束ね判定適用後）。1候補1オブジェクト。
```json
{
  "as_of": "2026-04-01",
  "scenario": { ... },
  "bundle_decisions": [
    {"vendor":"Veeva","n":3,"bundle_V":27.61,"indiv_V":33.84,"adopted":false}
  ],
  "excluded_inactive": ["Adobe Acrobat/Sign"],
  "candidates": [
    {
      "contract_id":1,"contract_name":"Veeva Vault QA 保守","contract_type":"Maintenance",
      "vendor":"Veeva","is_bundle":false,
      "net":26.0,"V_raw":18.75,"d_i":2.0,"U":0.60,"R":0.87,
      "p_effective":0.801,"p":0.801,
      "p_contest":0.90,"p_exec_effective":0.89,
      "ext_count":0,"ext_penalized":false,"ext_penalty":0.0,"p_split_used":true,
      "Vn":1.0,"score":0.520,"verdict":"即着手",
      "switch_cost_m":12.0
    }
  ]
}
```
`excluded_inactive` は `is_active=0` で評価対象外にした契約名の一覧。
`p_contest` / `p_exec_effective` / `ext_count` / `ext_penalized` / `ext_penalty` /
`p_split_used` は実行確度 p の内訳（`contestability_prob`・`execution_prob` が
無い契約では `p_contest`/`p_exec_effective` は `null`、`p_split_used` は `false` になる）。

---

## output/ — 最終成果物

### `output/allocation.json`
予算配分の結果。
```json
{
  "budget_m":20, "available_m":16.0, "safety_margin":0.2,
  "committed_m":12.0, "reserved_m":0.0, "blocked_m":22.0,
  "committed_expected_net_m":20.8,
  "lines":[
    {"tag":"本コミット","name":"...","cost_m":12.0,"score":0.52,"p":0.801}
  ],
  "blocked_top":"Veeva Vault RA 保守"
}
```

### `output/report.md`
人間が読む説明レポート。以下を必ず含む：
1. シナリオ設定の要約（λ, β, h, B, 安全余裕, 基準日）
2. 優先度ランキング表（対象・ネット・p・V/U/R・残月・スコア・判定）
3. 束ね判定の結果（採用したか／個別が有利だったか、その根拠）
4. 予算配分（本コミット・予約枠・予算不足）
5. **追加資金の引き出し根拠**：予算不足で着手できなかった上位案件の合計額と筆頭案件
6. 最上位案件がなぜ最優先かの一文説明

レポートは断定を避け、各判定が3因子のどれに起因するかを明示する。
「いつでも説明できる」ことが最優先要件。
