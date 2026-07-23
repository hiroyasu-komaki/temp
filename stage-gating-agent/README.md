# stage-gating-agent — POC投資ゲーティング 予算集計エージェント

各部門から提出された予算要求CSV（投資：通常投資・POC ／ BAU：継続コスト）を、
Python で正規化・審査・集計まで確定させ、ブラウザ用ダッシュボードのデータを
生成するエージェント。POC投資ゲーティング提案
（`../../02_concepts/governance/stage-gating`）の予算シート設計に対応する。

## 前提条件

- Claude Pro / Max / Teams / Enterprise アカウント
- Claude Code（ネイティブインストーラー推奨）
- Python 3.10+（外部パッケージ不要。標準ライブラリのみで動作）

## セットアップ

```bash
# 1. Claude Code のインストール
curl -fsSL https://claude.ai/install.sh | bash

# 2. プロジェクトフォルダに移動
cd ~/Documents/03_agents/stage-gating-agent

# 3. Python 仮想環境の構築（外部依存が無いため pip は不要）
python3 -m venv .venv --without-pip

# 4. Claude Code を起動（初回認証）
claude
```

## プロジェクト構成

```
stage-gating-agent/
├── .claude/commands/   ← Skills（build-dashboard）
├── src/
│   ├── main.py         ← エントリポイント（input→mid→output→data.js）
│   ├── config/         ← settings.py（パス・会計年度・区分マスタ・審査閾値・正規スキーマ・入力列マッピング）
│   └── modules/        ← adapter / loader / processor / dashboard_sync
├── direction/          ← data-definition.md（データ定義・審査規律）/ dashboard-spec.md（表示仕様）
├── input/              ← 生CSVを置く（スキーマ可変。ヘッダで投資/BAUを自動判別）
├── mid/                ← canonical_invest.csv / canonical_bau.csv（正規形に変換した中間データ）
├── output/             ← normalized.json / summary.json（集計結果）
├── index.html          ← ブラウザ用ダッシュボード
├── assets/
│   ├── css/style.css
│   └── js/             ← data.js（自動生成）/ logic.js / ui.js / main.js
├── .venv/
├── requirements.txt    ← 空（外部依存なし）
├── CLAUDE.md
└── README.md
```

## 使い方

`input/` に生CSVを置いてから、Claude Code でスキルを実行する。ファイル名は任意
（ヘッダに `案件区分`＝投資シート、`コスト種別`＝BAUシートと自動判別）。**列名が現行と
違ってもよい**——`src/config/settings.py` の `INPUT_MAPPING` で正規スキーマへ吸収する。

### /build-dashboard

```
/build-dashboard
```

生CSVを正規形へ変換し、正規化・審査・集計してダッシュボードのデータを生成する。

- 変換: `input/` 生CSV → `mid/canonical_*.csv`（正規形）
- 出力: `output/normalized.json` / `output/summary.json`（集計結果）／ `assets/js/data.js`（HTML用）
- 閲覧: `index.html` をブラウザで開くとダッシュボードを表示。
- 内容: 区分別・部門別の要求額、POCパイプライン（Gate2想定時期別）、BAU前年対比、
  月別按分、そして審査フラグ（差し戻し候補／要確認）の一覧。

Python パイプラインを直接動かす場合：

```bash
.venv/bin/python src/main.py run
```

input → mid（正規形CSV）→ output（集計結果）に加え、ダッシュボード用の
`assets/js/data.js` まで自動同期する。処理後は `index.html` をブラウザで開いて確認できる。

## 入力スキーマが変わったとき

入力CSVの列名が変わっても、変更は `src/config/settings.py` の `INPUT_MAPPING` だけ。

- `detect`: その種別と判定するための生列名（区分列などの名前が変わったら追加）。
- `rename`: `"新しい生の列名": "正規の列名"` を1行足す（例: `"当年度要求額": "要求金額_当年度"`）。

`rename` に無い生列は、正規列名と一致すればそのまま採用し、一致しなければ捨てる。
正規スキーマ自体（`CANONICAL_*_COLUMNS`）と後段のコードは触らずに済む。

## アーキテクチャ

```
Skills が手順を定義
    → Claude Code が Python を実行
        → adapter が生CSVを正規スキーマへ変換（mid/）
            → loader→processor が正規化・審査・集計（output/）
                → dashboard_sync が集計済みJSONを assets/js/data.js へ同期
                    → ブラウザは描画専念（集計しない）／ Claude が審査結果を解釈・要約
```

- **Skills**（`.claude/commands/`）— 処理手順の指示書。
- **Python**（`src/`）— 決定的処理を集計まで担う。
  - `src/config/settings.py` — パス・会計年度・区分マスタ・審査閾値・正規スキーマ・入力列マッピング。調整はここ。
  - `src/modules/` — `adapter`（生CSV→正規形CSV / mid）→ `loader`（読込・種別判別・検証）→
    `processor`（正規化・審査・集計）→ `dashboard_sync`（`data.js` 同期）。
    `processor` の結果は `output/*.json` にも保存する。
- **direction/** — データ定義と審査規律・表示仕様の正。コードを変えたら両方更新して乖離させない。
- **ダッシュボード**（`index.html` + `assets/`）— `data.js` は自動生成物（手編集禁止）。
  JS は集計済み値を描くだけで、合算・按分・比率計算はしない。

## 役割分担の要点

Python が集計まで完了し、HTML/JS は最低限の表示処理（フィルタ・ソート・整形）に徹する。
中間データ（`mid/`）と供給データ（`data.js`）はいずれも JSON で、CSV は入力段階のみ。

## 審査ロジック

`direction/data-definition.md` に定義。主な差し戻し候補（error）／要確認（warn）：

- POC で軸1（縮減する不確実性）・軸4（Go/No-Go 条件）が空 → 差し戻し候補
- POC で Gate2 想定時期が空 → 「突然登場」リスク（接続情報欠落・要確認）
- 区分違い（POCにROI記入／通常投資に4軸記入）→ 差し戻し候補
- BAU で増減理由が空 → 差し戻し候補、増減率が大きい → 要確認

## 注意事項

- Claude Code の利用には Pro 以上の有料プランが必要（追加の API 課金は不要）。
- 本エージェントの出力は査定確定前の要求値に基づく集計・審査補助であり、最終的な予算判断は
  投資委員会・予算管理担当の責任で行うこと。
