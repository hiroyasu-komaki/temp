# データ仕様

`input/` → `mid/` → `output/` の各段階で読み書きするファイルの形式と、
そこに何を必ず記載するかを定義する。列の追加・削除やレポートの節構成を
変えるときは、コードと本ドキュメントを両方更新する（原則3）。

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
  "as_of_date": "2026-04-01"
}
```

`ext_threshold` は、繰り返し延長を「VMO主導候補」として浮上させる延長回数の閾値
（`direction/scoring_methodology.md` §3.5）。`loader.py` の必須キーではなく
`scoring.py` 側で既定値 2 にフォールバックするが、明示指定を推奨する。
**延長は確度を割り引かないため、割引率・上限のパラメータは持たない。**

`lambda_risk` は 0..1 の範囲でのみ受理する（loader が検証して停止）。

`budget_m` / `safety_margin` は**本体パイプラインでは使わない**（予算配分を
行わないため。`direction/scoring_methodology.md` §4）。ダッシュボード
（`index.html`）が手元資金との突き合わせ表示に使う初期値であり、
loader の必須キーではない。

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
      "ext_count":0,"ext_escalated":false,"p_split_used":true,
      "Vn":1.0,"score":0.520,"verdict":"即着手",
      "switch_cost_m":12.0
    }
  ]
}
```
`excluded_inactive` は `is_active=0` で評価対象外にした契約名の一覧。
`p_contest` / `p_exec_effective` / `p_split_used` は実行確度 p の内訳
（`contestability_prob`・`execution_prob` が無い契約では `p_contest`/`p_exec_effective`
は `null`、`p_split_used` は `false` になる）。
`ext_count` は延長回数、`ext_escalated` は閾値到達により判定を「VMO主導候補」へ
浮上させたかどうか。**いずれも p・score には影響しない。**

---

## output/ — 最終成果物

### output/report.md の構成

`reporter.build_report` が生成する。断定を避け、各判定が3因子（期待価値・緊急度・
情報熟度）のどれに起因するかを常に明示する。

| 節 | 内容 | 出力条件 |
|---|---|---|
| シナリオ設定 | λ・β・h・束ね評価のON/OFF | 常に |
| 優先度ランキング | スコア降順の全候補（判定ラベル付き） | 常に |
| 束ね（ベンダー単位）判定 | 束ね価値と個別合計の比較・採否 | `bundle_decisions` があるとき |
| 最上位案件の位置づけ | 3因子が揃う理由の要約 | 有効な最上位候補があるとき |
| 参考情報：計算ロジックの詳細解説 | 最上位案件の算出過程 | 同上 |

**予算配分に関する節は持たない**（`scoring_methodology.md` §4）。
本コミット額・予約枠・予算不足・追加資金の引き出し根拠といった、資金枠に
収まるかを論じる出力は一切書かない。手元資金・安全余裕もシナリオ設定節に
出さない（本体パイプラインが使わない値のため）。

節番号は**出力した節だけで連番**にする（条件付きの節があるため、
`reporter._Counter` が採番する）。番号を固定文字列で書かないこと。

#### 計算ロジック解説節の要件

最上位案件1件について、`mid/scored.json` の値から算出過程を再構成する
（レポート側で再計算しない／固定値を書かない）。必須の5項目：

1. **実行確度 $p$** — 内訳を示す。`p_split_used=true` なら
   $p_{contest} \times p_{exec}$ の積として、`false` なら `exec_probability` 単独として、
   束ね候補なら合成確度 $\prod p_i^{1/\sqrt{n}}$ として説明を切り替える。
   延長回数は $p$ に反映していない旨を併記する（原則6）。
2. **$net$ と $V_{raw}$** — 想定リターン－切替コスト、および
   $p \times net \times (1-\lambda(1-p))$ に実値を代入した計算式。
   正規化後の $V_n$ が候補中最大 $V_{raw}$ との相対値であることも示す。
3. **$d_i$ と $U$** — 契約満了－リードタイム、$U = 1/(1+d_i/h)$。
   $d_i<0$ のときは $U=0$ の理由（着手可能な窓が既にない）を書く。
4. **$R$** — $1 - \sigma \times \min(d_i/h, 1)$ に実値を代入した計算式。
5. **$verdict$** — `scoring.verdict_of` の**実際に成立した分岐**の根拠を、
   閾値と実値を添えて説明する。全案件に「スコア0.25以上のため即着手」と
   書いてはならない（失効／VMO主導候補／人間判断／温存／捨てる候補／検討の
   各分岐に対応する説明を持つこと）。

具体的な文面と数値は `src/modules/reporter.py`（`_build_logic_appendix` /
`_verdict_reason`）が持つ。ここでは**何を必ず説明するか**のみを定める。
`_verdict_reason` は `scoring.verdict_of` と分岐順を対応させること
── 判定ロジックを変えるときは、コードと本節を両方更新する（原則3）。
