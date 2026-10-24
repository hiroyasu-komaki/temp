# IT Financial Management（GDS予算管理）

GDSの予算・実績・着地見込みを月次で管理するための、Excel台帳一式と設計文書です。チャージバック・ショーバックは現時点では対象外です。

## 1. このフォルダの構成（設計・原本の置き場）

```
it-financial-management/
├─ README.md                         … このファイル
├─ ledger/                           … Excelファイルの原本（SharePointに配置する前のマスター版）
│   ├─ gds_master_data.xlsx          … マスタの正本（コストセンター・勘定科目・プロジェクト・為替・選択肢）
│   ├─ gds_budget_ledger.xlsx        … 共有台帳（予算・実績・予実対比・Dashboard）
│   └─ gds_budget_utility.xlsx       … 入力者用ユーティリティ（契約・資産・要員から予算行を作る）※最新の列構成に未対応
└─ requirements/                     … 設計文書
    ├─ it_budget_requirements.md     … 業務要件定義書
    ├─ it_budget_adr.md              … アーキテクチャ決定記録（ADR）
    └─ it_budget_monthly_runbook.md  … 月次運用手順書
```

## 2. ファイルの役割

| ファイル | 役割 | 更新する人 | 使うExcel |
|---|---|---|---|
| `gds_master_data.xlsx` | マスタの正本。台帳・ユーティリティはここからPower Queryで写しを読み込む | ITファイナンスのみ | Web版・デスクトップ版 |
| `gds_budget_ledger.xlsx` | 1ファイルを全員で共同編集する台帳。`Opex_Budget`（予算・確定後に固定）、`Actuals`（実績）、`Budget_vs_Actual`（予実対比・見込み・理由）、`Dashboard`（全体像） | 入力者・責任者・予算管理者 | 入力はWeb版で可。Power Queryの更新はデスクトップ版 |
| `gds_budget_utility.xlsx` | 各入力者が手元に持つ変換ツール。`Export` を台帳の `Opex_Budget` に値で貼り付ける | 各入力者 | Web版・デスクトップ版 |

## 3. 想定しているSharePoint（SPO）の構成

運用版はSharePointのチームサイトに置きます。以下は想定案で、サイト名・フォルダ名は運用開始時に確定します。

```
SharePointサイト：GDS Finance（チームサイト）
└─ ドキュメントライブラリ：Budget
    ├─ 01_Master/
    │   └─ gds_master_data.xlsx                 … マスタの正本
    ├─ 02_Ledger/
    │   └─ FY2027/
    │       ├─ gds_budget_ledger.xlsx           … 共有台帳（年度ごとに1ファイル）
    │       └─ Archive/                         … 月次の控え（gds_budget_ledger_YYYYMM.xlsx）。任意
    ├─ 03_Actuals/
    │   └─ FY2027/
    │       ├─ JP/                              … 会計システムからダウンロードした実績（原本）
    │       ├─ NA/
    │       └─ EMEA/
    ├─ 04_Utility/
    │   └─ gds_budget_utility.xlsx              … 配布用の雛形。各自がコピーして使う
    └─ 05_Docs/
        ├─ it_budget_requirements.md
        ├─ it_budget_adr.md
        └─ it_budget_monthly_runbook.md
```

### アクセス権の想定

| フォルダ | ITファイナンス | 予算管理者 | 入力者・責任者（北米・EMEA・各サブファンクション含む） |
|---|---|---|---|
| 01_Master | 編集 | 閲覧 | 閲覧 |
| 02_Ledger | 編集 | 編集 | 編集（同じファイル・同じシートを共同編集） |
| 03_Actuals | 閲覧 | 編集 | 権限なし（または閲覧） |
| 04_Utility | 編集 | 閲覧 | 閲覧（コピーして使う） |
| 05_Docs | 編集 | 閲覧 | 閲覧 |

### Power Queryの接続

| 読み込む側 | 読み込む元 | 更新のタイミング |
|---|---|---|
| 台帳・ユーティリティの `Cost_Centers`／`Accounts`／`Projects`／`FX_Rates`／`Lists` | `01_Master/gds_master_data.xlsx` | マスタが変わったとき（「データ＞すべて更新」） |
| 台帳の `Prior_Forecast` | 台帳自身の `Budget_vs_Actual`（Actual + Forecast行） | 毎月、実績を貼り付ける前（「すべて更新」の対象外） |

Power Queryの接続は別環境で構築する予定です。各ファイルには、読み込み先となる仮のテーブルと名前付き範囲を用意してあります。

## 4. 運用の流れ（概要）

1. **予算編成**：入力者が `Opex_Budget` に入力する（直接入力、またはユーティリティの `Export` を貼り付け）。確定したら予算管理者がシートを固定する。
2. **年度の準備**：ITファイナンスが、為替レートと `Budget_vs_Actual` のブロック（コストセンター×勘定科目）を設定する。
3. **毎月**：予算管理者が「前月見込みの控え → 実績の貼り付け → 締め月の更新」を行い、責任者が見込みと理由を更新し、`Dashboard` で確認する。

手順の詳細は `requirements/it_budget_monthly_runbook.md` を参照。

## 5. 残っている課題

2026-10-24時点。詳細は各文書の未確定事項（要件定義書11章、手順書5章）を参照。

### Excel・環境の構築

| # | 課題 | 関連 |
|---|---|---|
| 1 | Power Queryの接続を構築する（マスタの写し、`Prior_Forecast`）。別環境で作成予定 | ADR-012・013 |
| 2 | SharePointのサイト・フォルダ・アクセス権を確定し、ファイルを配置する（3章は案） | ADR-011 |
| 3 | `Actuals` の列を、各リージョンの会計システムのダウンロード形式に合わせる | 要件11-8、手順書5-4 |
| 4 | ユーティリティの `Export` を、`Opex_Budget` の現在の列構成（cost_category・system_name・vendor_name・project_id・asset_id）に合わせる | ADR-012 |
| 5 | ユーティリティから人件費が1人単位で共有台帳に載る点の扱い（全員に見えてよいか、合算して出すか） | ADR-012 |
| 6 | `cost_category` の選択肢を、社内の分類に合わせて確定する（現在は案） | 要件6.4 |
| 7 | マスタの `Cost_Centers` の `function`／`sub_function` の表記を、Dashboardの集計区分（GDS、Applications／Infrastructure／Data／Security／Governance）と揃える | Dashboard |

### 運用ルール

| # | 課題 | 関連 |
|---|---|---|
| 8 | 月次の日程（締めから何営業日目に何をするか）と報告先 | 要件11-16、手順書5-1 |
| 9 | 差異の説明を求める閾値（率・金額） | 要件11-16、手順書5-2 |
| 10 | 修正予算（期中に承認された予算の増減）の持ち方 | 要件8.2、手順書5-3 |
| 11 | 予実の対象範囲（Run＋移管予算に限るか、GDS予算全体か）と、実績の切り分け方 | 要件11-13 |
| 12 | 移管元コストセンターの実績を、コストセンター×勘定科目で切り出せるか | 要件11-14 |
| 13 | マスタ（コストセンター・勘定科目・プロジェクト・為替）の更新責任者と承認の流れ | 要件11-5・9・11・12 |
| 14 | 為替レート（予算レート）の情報源と改定時の承認 | 要件11-7 |

### 経理・関係部門への確認

| # | 課題 | 関連 |
|---|---|---|
| 15 | 各リージョン経理が発生主義で未払計上しているか（計上月のずれの扱い） | 要件11-15 |
| 16 | 勘定科目の3階層（現地勘定科目→GlobalCOA→管理会計区分）の対応表の入手元 | 要件11-9 |
| 17 | 固定資産：少額資産の一括償却基準、除却・売却時の償却停止 | 要件11-1・2 |
| 18 | 人件費：正社員の単価の算定基準（実額か標準単価か）、外部人材の予算計上額の更新運用 | 要件11-3・4 |
| 19 | プロジェクト完了後の費用をRun予算に引き渡すタイミング | 要件11-10 |
| 20 | 初期データ（契約台帳・固定資産台帳・人事データ）の入手と投入方法 | 要件11-6 |
