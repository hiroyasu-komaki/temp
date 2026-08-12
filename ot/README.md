# ot — 生産系ITアーキテクチャとガバナンス

本社IT部門の立場から、生産本部が主管する工場設備・生産系情報システム(ERP/MES/SCADA/PLC)の全体像を理解し、中長期IT戦略の策定に向けた土台を整理したコンセプト。ISA-95モデルによる技術的な階層構造の理解から出発し、当社の実際のシステム構成(国内mcframe、海外D365)への適用、IT部門と生産IT間の責任分解、マスタデータガバナンス、IT投資案件の承認ルーティングまでを扱う。段階的な移行計画(ロードマップ)は本コンセプトでは未着手。

## ディレクトリツリー

```
ot/
├── README.md                     このファイル
├── chapters/
│   ├── 00_framework.md           理論:組織用語の定義, ISA-95, MOM 4領域(MES/LIMS/CMMS/WMS), MESA-11, IT/OT区分基準, 生産管理システムの位置づけ, QCD
│   ├── 01_current-state.md       診断:当社の現状構成、責任分解の実態、マスタ多重管理の実例
│   ├── 02_recommendations.md     提言:責任分解の原則、データガバナンス体制、投資承認ルーティングの枠組み
│   ├── 03_decision-criteria.md   判断基準:MESA-11×運用主管マッピング、投資案件追加項目、承認フロー
│   └── 04_operation.md           運用:プロンプトを用いた2段階運用フロー、推測強度の設計
├── appendix/
│   └── form1_investment-approval-prompts.md   IT投資案件リスト(Excel)への項目追加・承認ルート判定プロンプト
└── images/                       各章で参照する図版(SVG)
```

## 正本・読む順序

- 章は `chapters/00` から `04` の順に読む。`05_roadmap.md`(段階的な移行計画)は未作成。
- プロンプトの正本は `appendix/form1_investment-approval-prompts.md`。
- `proposal/`(経営会議・IT委員会向けの提案書)は、データガバナンス体制や投資承認ルールを正式に提案する段階になったら作成する。現時点では未作成。
