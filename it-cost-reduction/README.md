# it-cost-reduction — IT予算 コスト最適化検討(中間整理資料)

来年度IT予算(約120億円)の再検討にあたり、ベンダーマネジメント担当(VMO)としての検討内容を整理した資料。クラウド領域(AWS／Azure／M365)は管掌外のため、ベンダーのロックイン戦略とビーチヘッド戦略を分析する視点の提供にとどめる。管掌範囲であるビジネスアプリケーション領域(約60億円)は、削減目標を作る作業計画と、その中核である運用保守委託の契約形態の移行(SESから managed services／T&Mへ)を示す。**扱わないもの**：ビジネスアプリケーション関連の内訳、施策ごとの金額インパクト、削減目標の値(いずれも第5章の作業計画の中で明らかにする)。

- 作成日：2026年8月17日／改訂日：2026年10月17日
- 対象読者：経営層／IT部門／ベンダーマネジメント担当

## ディレクトリ

```
it-cost-reduction/
├── README.md
├── .gitignore
├── chapters/                               本文
│   ├── 01_positioning.md                   本資料の位置づけ(背景・対象範囲と管掌・章構成)
│   ├── 02_situation-and-policy.md          状況整理と全体方針(増加要因の3分類、一般的な打ち手)
│   ├── 03_vendor-lock-in.md                ベンダーのロックイン戦略(Microsoftの価格転嫁、AWSのコミット額の下方硬直)
│   ├── 04_azure-expansion.md               Azureの伸長とビーチヘッド戦略(見えにくいコストの積み上がり)
│   ├── 05_business-applications.md         ビジネスアプリケーション領域(約60億円)の削減目標の考え方とRunbook
│   └── 06_maintenance-outsourcing.md       運用保守委託費のディープダイブ(契約形態の移行と工数調査)
├── appendix/                               参照資料
│   ├── A_aws-microsoft-contract-reference.md  付録A AWS・Microsoftの契約体系とコスト体系
│   ├── B_m365-price-revision.md               付録B Microsoft 365 価格改定表(2026年7月実施)
│   ├── C_aws-azure-service-comparison.md      付録C AWS vs Azure 製品・サービス比較表(製品レイヤー)
│   ├── D_aws-azure-contract-comparison.md     付録D AWS vs Azure/Microsoft 契約比較表(契約レイヤー)
│   └── E_contract-types.md                    付録E ITの外部委託における契約類型(請負・準委任・派遣、SES・T&M・managed services)
├── data/
│   └── maintenance-effort-survey.xlsx     第6章 運用保守委託の工数調査ワークシート(データシート)
├── images/
│   ├── 03_lock-in-pricing-model.png        図3-1 ロックイン後の価格転嫁モデル(Microsoft)
│   ├── 03_commit-lock-in-model.png         図3-2 コミット契約によるロックインモデル(AWS)
│   ├── 04_azure-beachhead-model.png        図4-1 Azureのビーチヘッド戦略モデル
│   └── 04_azure-hidden-cost-model.png      図4-2 Azure利用に伴う見えにくいコストの積み上がり
└── src/
    ├── lock_in_models.py                   図3-1・3-2を生成する(python3 src/lock_in_models.py)
    ├── azure_beachhead_model.py            図4-1を生成する(python3 src/azure_beachhead_model.py)
    └── azure_hidden_cost_model.py          図4-2を生成する(python3 src/azure_hidden_cost_model.py)
```

## 正本と読み方

- 正本は `chapters/` と `appendix/` のMarkdown、および `data/maintenance-effort-survey.xlsx`(生成スクリプトはなく、このファイルを直接更新する)。他の形式の副本(Word・HTML等)は持たない。
- 全体像は第1章 → 第2章から読む。
- 第3・4章はクラウド領域の分析(管掌外。分析の視点の提供にとどめる)。
- 第5・6章はビジネスアプリケーション領域(管掌範囲)。第5章で削減目標を作る作業計画を示し、第6章で運用保守委託を掘り下げる。工数調査は `data/maintenance-effort-survey.xlsx` を各契約先ベンダーに配布して記入してもらう。
- 付録A〜Eは本文から参照されたときに開く(付録Eは第6章の契約類型の前提)。
- 図を変更するときは `src/` のスクリプトを編集して再生成する。
