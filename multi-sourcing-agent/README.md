# ITベンダー競争見積もり推進施策 - 効果試算・企画資料プロジェクト

随意契約80%の構造是正によるITコスト最適化を提案する企画書と、その根拠となる効果試算モデル（Excel）・グラフ生成パイプラインをまとめたプロジェクトです。
Excelの前提シート（数値）を更新するだけで、企画書に添付する4枚のグラフを自動で再生成できます。


## 前提条件

- Python 3.10+
- Claude Code（グラフ再生成のスキルを使う場合。任意）

## セットアップ

```bash
# 1. プロジェクトフォルダに移動
cd ~/Documents/03_agents/multi-sourcing-agent

# 2. Python 仮想環境の構築
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## プロジェクト構成

```
multi-sourcing-agent/
├── .claude/commands/
│   └── generate-charts.md      ← Skill: vmo_impact_model.xlsx からグラフ4枚を再生成
├── input/
│   └── vmo_impact_model.xlsx    ← 効果試算モデル（前提シートの数値を編集する）
├── mid/                          ← xlsxから書き出す中間JSON（検証・手動編集用）
│   ├── inputs.json               前提シートの生数値
│   ├── calc.json                 「計算」シート相当（カテゴリ別削減額など）
│   └── investment_eval.json      「投資評価」シート相当（NPV/IRR/PIなど）
├── output/                       ← 生成された4枚のPNG
├── src/
│   ├── main.py                    エントリポイント。Skillはこれを呼び出す
│   └── modules/
│       ├── common.py                 xlsx読み込み・数式再現・中間JSON入出力の共通処理
│       ├── build_mid.py               xlsx → mid/*.json のみを実行するスクリプト
│       ├── generate_all.py            mid/*.json 作成 + 4枚のグラフ生成をまとめて実行
│       ├── chart01_facts_sole_source_contracts.py  グラフ①: 随意契約80%の内訳（事実）
│       ├── chart02_hypothesis_impact.py            グラフ②: 合意パラメータ適用後の期待効果
│       ├── chart03_npv_irr_3years.py               グラフ③: NPV/IRR展開（3年・保守評価）
│       └── chart04_vmo_cost_structure.py           グラフ④: VMO関連コストの3層構造
├── requirements.txt
├── .venv/
└── README.md
```

## 使い方

### 1. Excelの前提を更新する

`input/vmo_impact_model.xlsx` の「前提」シート（青字・黄色セル）の数値を編集して保存します。

### 2. グラフを再生成する

Claude Code から次のスキルを実行します。

```
/generate-charts
```

実行すると次の2択が提示されます。

1. Excelから最新化してグラフを作成する（`input/vmo_impact_model.xlsx` → `mid/*.json` を作り直してからグラフ生成）
2. 今の `mid/*.json`（手動編集を含む）をそのまま使ってグラフだけ作成する（Excelは読み直さない）

Claude Code を使わず直接実行する場合は次のコマンドでも同じ結果になります。

```bash
# xlsxから最新化する場合
cd src && ../.venv/bin/python main.py

# mid/*.json をそのまま使う場合（xlsxは読み直さない）
cd src && ../.venv/bin/python main.py --from-mid

# 中間JSONだけを作り直したい場合
cd src && ../.venv/bin/python modules/build_mid.py
```

生成された4枚のPNGは `output/` に書き出されます。

## アーキテクチャ

```
input/vmo_impact_model.xlsx（前提シートの数値）
    → src/modules/common.py が「計算」「投資評価」シートの数式をPythonで再現
        → mid/*.json（中間ファイル。目視・diffで検証可能）
            → src/modules/chart0X_*.py が mid/*.json だけを参照してPNGを生成
                → output/*.png
```

- **中間ファイル（`mid/`）を挟む理由**: グラフ生成スクリプトはxlsxを直接読まず、`mid/*.json` のみを参照します。xlsxからの転記結果を、グラフ化する前にJSONとして確認・手動修正できるようにするためです。
- **`src/main.py`**: エントリポイント。処理自体は `src/modules/generate_all.py` に委譲する。他のPythonスクリプトは全て `src/modules/` にまとまっている。
- **Skills（`.claude/commands/`）**: Claude Code への指示書。グラフ再生成の手順（Excel再読み込みか、中間JSONの流用か）をユーザーに選ばせた上で `main.py` を実行する。

## 注意事項

- グラフ中の数値は、実データ確定前の一般的な代表値によるプレースホルダを含みます。契約マスタ整備・現場合意・調達ベンチマークの結果をもって確定値に差し替える想定です。
- `mid/*.json` を手動編集した場合、`input/vmo_impact_model.xlsx` を読み直す（選択肢1 / `build_mid.py` の実行）と上書きされます。
