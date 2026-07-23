---
description: input/ の予算要求CSV（投資・BAU）を集計し、審査フラグ付きダッシュボードデータを生成する
inputs:
  - "input/*.csv"
outputs:
  - "mid/canonical_invest.csv"
  - "mid/canonical_bau.csv"
  - "output/normalized.json"
  - "output/summary.json"
  - "assets/js/data.js"
depends_on:
  - "src/main.py"
  - "direction/data-definition.md"
  - "direction/dashboard-spec.md"
---

`input/` に置かれた予算要求シート（投資：通常投資・POC ／ BAU：継続コスト）を
生CSV（スキーマは可変）を現行の正規スキーマへ変換したうえで、正規化・審査・集計まで
Python で確定させ、ブラウザ用ダッシュボードのデータを生成する Skill。
判断根拠は `direction/data-definition.md`。

## Step 0: ファイル確認

1. `input/` の `*.csv` を列挙する。無ければその旨を伝えて終了。
2. ファイル名に依存せず、ヘッダで種別を自動判別する。列名は現行と違ってもよい
   （`settings.INPUT_MAPPING` の `detect`/`rename` で正規スキーマへ吸収）。
   投資・BAU は同時に複数ファイルでも可。片方だけでも動く。
   `[変換エラー]（種別判定不可 …）` が出たら、`settings.INPUT_MAPPING` の
   `detect`（区分列の名前）と `rename`（列名の読み替え）を実データに合わせて更新する。

## Step 1: パイプライン実行

3. 決定的な処理（読込・検証・正規化・審査・集計・月別按分）は `src/main.py` に委譲する。
   Python は必ず仮想環境の Python を直接指定する：

   ```bash
   .venv/bin/python src/main.py run
   ```

   これで input（生CSV）→ mid（正規形CSV `canonical_*.csv`）→ output
   （`normalized.json` / `summary.json`）→ `assets/js/data.js` の同期までを一気通貫で行う。
   `output/*.json` と `data.js` は同じ processor 出力から並列に書き出す
   （`data.js` は `output/` や `mid/` から作るのではない）。特定ファイルだけ処理する場合は
   `--input input/<ファイル名>` を付ける。

4. 実行に失敗した場合（`[入力エラー] …`）は、不足列や区分判別の失敗をユーザーに伝える。

## Step 2: 審査結果の解釈

5. `output/summary.json` の `audit` を読み、**差し戻し候補（error）／要確認（warn）** を
   ユーザー向けに要約する。特に以下は必ず言及する：
   - POC で軸1（縮減する不確実性）や軸4（Go/No-Go）が空 → 規律欠如で差し戻し候補
   - POC で Gate2 想定時期が空 → 「突然登場」リスク（接続情報欠落）
   - BAU で増減理由が空、または増減率が大きい項目
   - 区分違い（POCにROI記入／通常投資に4軸記入）
6. 判断・解釈が要る部分は Claude が `mid/` の中間結果を読んで補足する
   （Python は集計まで、含意の説明は Claude が担う）。

## Step 3: 出力の提示

7. 生成物を提示する：
   - `assets/js/data.js` … HTML が参照する集計済み JSON（上記実行で自動同期済み・手編集禁止）
   - `output/normalized.json` / `output/summary.json` … 集計結果（審査結果の確認用）
   - `mid/canonical_*.csv` … 正規形に変換した中間データ（変換の確認用）
   - `index.html` … ブラウザで開くと集計ダッシュボードを表示
8. 差し戻し候補の件数と主な指摘、POCパイプライン（Gate2時期別）の要点を短く添える。
