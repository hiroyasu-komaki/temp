---
description: 契約データからベンダー切替の優先度スコアを計算し、説明レポートを生成する
---

# analyze — ベンダー切替投資の分析実行

`input/contracts.csv` と `input/scenario.json` を読み、優先度スコア（V×U×R）と
束ね評価を計算して `output/report.md` を生成する。

**予算配分は行わない。** 手元資金への割り付けや「予算不足で着手不能」といった
資金枠の話は出力にも要約にも含めないこと（`direction/scoring_methodology.md` §4）。

## 手順

1. `input/contracts.csv` が存在するか確認する。なければユーザーに配置を促す。
2. パイプラインを実行する:
   ```
   python src/Main.py
   ```
3. 実行後、以下を確認して結果を要約する:
   - `mid/scored.json` — スコア計算済みの全候補
   - `output/report.md` — 説明レポート
4. `output/report.md` の要点をユーザーに伝える。特に:
   - 即着手と判定された案件と、その判定が3因子のどれに起因するか
   - 束ね（バンドル）の採否とその根拠
   - **VMO主導候補**（繰り返し延長。スコアが低くても現場任せでは動かない兆候）

## 判断基準

スコアの意味・束ねの扱い・判定ラベルは `direction/scoring_methodology.md` に従う。
入力データに `return_sigma` の空欄があると loader が停止する。その場合は
ユーザーに確からしさの入力を促すこと（R の生命線のため）。

## 注意

- 数値ロジックを変更したい場合は、コードではなく `input/scenario.json`
  （λ, β, h, ext_threshold）を編集して再実行する。
- 断定的な投資判断は下さない。各判定が3因子のどれに起因するかを説明する。
