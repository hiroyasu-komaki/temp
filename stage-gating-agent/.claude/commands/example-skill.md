---
description: このSkillが何をするかを1文で書く
inputs: []
outputs: output/example_{date}.md
depends_on: []
---

このファイルは Skill（カスタムコマンド）のテンプレートです。
`.claude/commands/` 配下に Markdown ファイルを1つ置くと、
ファイル名（拡張子なし）が `/コマンド名` として呼び出せるようになります。

コピーして実際のSkillを作成したら、このファイルは削除してください。

## Step 0: ファイル選択

1. `input/` フォルダ内の対象ファイルを列挙する。
2. 見つからない場合はその旨を伝えて終了する。
3. 複数ある場合はユーザーに番号で選択させる。

## Step 1: 処理

4. 決定的な処理（読み込み・検証・抽出・変換・計算）は `src/main.py` に委譲する。
   Python は必ず仮想環境の Python を直接指定して呼び出す：

   ```bash
   .venv/bin/python src/main.py run --input input/<選択したファイル>
   ```

   このコマンドが input → mid → output → `assets/js/data.js` の同期までを
   一気通貫で行う（パイプラインの実体は `src/modules/`、設定は `src/config/`）。
5. Python が担うのはファイル処理・データ変換など。判断・生成が必要な部分は
   Claude が `mid/` の中間結果を読んで行う。

## Step 2: 出力

6. 最終成果物を `output/example_YYYYMMDD_HHmmss.md` の形式で保存する。
7. ブラウザで結果を確認する場合は `index.html` を開く
   （表示データ `assets/js/data.js` は上記実行で自動同期済み）。
8. 保存完了後、出力ファイルパスと処理内容のサマリーを表示する。
