# CLAUDE.md

このファイルは Claude Code がリポジトリで作業する際のガイドです。

POC投資ゲーティング（stage-gating）提案に対応する予算集計エージェント。
`input/` の予算要求CSV（投資：通常投資・POC ／ BAU：継続コスト）を、Python で
**正規スキーマへ変換 → 正規化・審査・集計** まで確定させ、ブラウザ用ダッシュボードの
データを生成する。入力CSVのスキーマ（列名）は変化しうる前提で、変換層（adapter）が
現行の正規スキーマへ吸収する。根拠・設計は `../../02_concepts/governance/stage-gating`。

## ディレクトリの役割

| ディレクトリ | 用途 |
|-------------|------|
| `input/` | **生CSVの置き場所（スキーマは可変）。** 投資要求シート／ BAU予算要求シート。ファイル名は任意。列名が現行と違ってもよい（`settings.INPUT_MAPPING` で吸収）。 |
| `mid/` | 中間ファイル。adapter が変換した**正規形CSV**（`canonical_invest.csv` / `canonical_bau.csv`）。processor の入力。 |
| `output/` | processor の集計結果 JSON。`normalized.json`（正規化レコード）と `summary.json`（集計＋審査フラグ）。 |
| `src/` | Python ソースコード。`main.py` がエントリポイント。Skills から呼び出される処理の実体。 |
| `src/config/` | Python 用の設定（`settings.py`：パス定数・会計年度・区分マスタ・審査閾値・**正規スキーマと入力列マッピング**）。数値・列名の調整はここで行う。 |
| `src/modules/` | パイプラインを構成する処理単位（adapter / loader / processor / dashboard_sync）。 |
| `direction/` | スキル仕様・参照ドキュメント。`data-definition.md`（データ定義・審査規律）と `dashboard-spec.md`（表示仕様）。 |
| `.claude/commands/` | Skills（カスタムコマンド）の定義。`build-dashboard.md`。 |
| `index.html` / `assets/` | ブラウザ用ダッシュボード。`assets/js/data.js` は `dashboard_sync` が自動生成する（手編集禁止）。JS は描画専念で集計しない。 |

## データフローと成果物（重要）

```
input/ 生CSV（可変スキーマ）
  └─ adapter … 列マッピングで正規スキーマへ変換 → mid/canonical_*.csv
  └─ loader → processor … 正規形を集計（メモリ上の1オブジェクト）
        ├─→ output/normalized.json, output/summary.json  （集計結果JSON）
        └─→ assets/js/data.js                            （HTMLが参照・閲覧成果物）
```

`output/*.json` と `data.js` は同じ processor 出力から**並列に**書き出す
（`data.js` を `output/` や `mid/` から作るのではない）。HTML が参照するのは `data.js` のみ。

## 入力スキーマが変わったとき（重要）

入力CSVの列名が変わっても、コードは触らず `src/config/settings.py` の
`INPUT_MAPPING` だけを直す。種別判定の列名は `detect`、列名の読み替えは
`rename`（`"新しい生の列名": "正規の列名"`）に1行足す。正規スキーマそのもの
（`CANONICAL_*_COLUMNS`）は原則固定。

## 役割分担（重要）

- **Python（`src/`）が集計まで完了する。** 正規化・検証・審査・集計・月別按分・構成比まで
  Python で確定し、`assets/js/data.js` に集計済み JSON として渡す。
- **HTML/JS は描画に専念する。** 受け取った値を描くだけ。JS 側で金額の合算・按分・比率計算は
  しない（表のフィルタ／ソート等の表示操作のみ）。
- データ受け渡しは CSV ではなく **JSON**（`data.js` に `const` 埋め込み）。`file://` で
  `index.html` を直接開いても動く。

## Python 実行ルール

Python は必ず仮想環境内で実行すること。コマンドは `.venv/bin/python` を直接指定する。

```bash
# ✅ 正しい（仮想環境のPythonを直接指定）
.venv/bin/python src/main.py {サブコマンド}

# ❌ 避ける（activate 忘れのリスクがある）
python src/main.py {サブコマンド}
```

パッケージの追加も仮想環境内で行う：

```bash
.venv/bin/pip install <パッケージ名>
.venv/bin/pip freeze > requirements.txt
```

> 注: このエージェントは標準ライブラリのみで動作し、外部パッケージは不要。
> venv は `python3 -m venv .venv --without-pip` で作成してよい（`requirements.txt` は空）。

## Python コマンド（src/main.py）

```bash
.venv/bin/python src/main.py run                      # input/ 配下のCSVを全処理
.venv/bin/python src/main.py run --input input/<ファイル名>   # 特定ファイルのみ
```

いずれも input→mid（正規形CSV）→output（`normalized.json`/`summary.json`）→
`assets/js/data.js` 同期までを一気通貫で行う。パイプラインの実体は `src/modules/`
（adapter→loader→processor→dashboard_sync）、設定は `src/config/settings.py`。
審査規律・集計定義を変えるときはコードと `direction/data-definition.md` を両方更新し、
乖離させないこと。

## カスタムコマンド（Skills）

`.claude/commands/` に定義済み。`/コマンド名` で呼び出せる。

| コマンド | 主な入力 | 主な出力 | 動作概要 |
|---------|---------|---------|---------|
| `/build-dashboard` | `input/*.csv`（可変スキーマ） | `mid/canonical_*.csv`, `output/*.json`, `assets/js/data.js` | 生CSVを正規形へ変換し、正規化・審査・集計してダッシュボードデータを生成。差し戻し候補／要確認を要約。 |
