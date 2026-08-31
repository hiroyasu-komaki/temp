# README：ベンダーマネジメントガイド

## 概要

このフォルダには、企業IT組織におけるベンダーマネジメント（Vendor Management）に関する実践ガイド、関連データモデルの定義書、および社内提案資料が含まれています。VMO（Vendor Management Office／ベンダーマネジメント担当者）が日々の業務で直面する課題に対応するための実践的な手引きとして構成されています。

## フォルダ構成

```
vmo/
├── README.md                                  ← 本ファイル（全体の案内）
├── vmo-guide.md                                ← 実践ガイド フル版（第1〜7章＋付録A〜Dを1本にまとめたもの）
│
├── chapters/                                   ← 実践ガイドを章ごとに分割した版
│   ├── 1_vmo-guide.md                             第1章：役割と位置づけ
│   ├── 2_vmo-guide-procurement.md                 第2章：調達プロセス
│   ├── 3_vmo-guide-lifecycle-management.md        第3章：ベンダーライフサイクル管理
│   ├── 4_vmo-guide-responsibility.md              第4章：クラウド/SaaS・運用保守委託でのVMOの特別な注意点
│   ├── 5_vmo-guide-raci.md                        第5章：VMOの組織内での役割と連携（RACI）
│   ├── 6_vmo-guide-kpi.md                         第6章：成果を測る指標（KPI）
│   ├── 7_vmo-guide-checklist.md                   第7章：VMOの実践チェックリスト
│   └── vmo-guide-appendix.md                      付録A〜D（テンプレート集／Q&A／ITIL準拠L1-L3問題解決フロー／Follow-the-sunモデル）
│
├── data/                                        ← ベンダー管理データモデルのテーブル定義書
│   ├── table_vendors.md                           vendors：ベンダー基本情報
│   ├── table_contracts.md                         contracts：個別契約情報（FK: vendor_id）
│   ├── table_services.md                          services：提供サービス詳細（FK: contract_id, vendor_id）
│   └── table_orders.md                            orders：発注実績トランザクション（FK: contract_id, vendor_id）
│
└── proposal/                                    ← 社内提案資料
    ├── cost-optimization/                         ICTコスト最適化提案（.md/.pptx/.pdf）
    ├── data-governance/                            データガバナンス提案（.pptx/.pdf）
    │   └── spend_data/                                支出データ分析資料（日本語・英語、.docx/.pdf）
    └── prepaid-contract/                           前払い契約見直し提案（.md/.pptx/.pdf）
```

## 各文書の概要

### 実践ガイド（VMO向け）

#### vmo-guide.md（フル版）
- **目的**：実践ガイドの全体を1つのファイルで通読する
- **内容**：目次付きで第1章〜第7章、付録A〜Dまでを収録した完全版。章ごとの版（`chapters/`）と内容は同一

#### chapters/1_vmo-guide.md（第1章：役割と位置づけ）
- VMOの責任（ベンダー台帳管理、分類・リスク評価、パフォーマンスレビュー、契約交渉、関係性構築）
- VMOが関わる組織との関係図
- COBIT 2019フレームワークとの対応（APO10が中核）

#### chapters/2_vmo-guide-procurement.md（第2章：調達プロセス）
- 調達プロセス全体の流れ（シーケンス図）
- 調達の8ステップとVMOのアクション
- VMOが作成・管理すべき主要文書

#### chapters/3_vmo-guide-lifecycle-management.md（第3章：ベンダーライフサイクル管理）
- ベンダー台帳の作成と管理（ER図、分類基準）
- オンボーディング（30日計画）
- パフォーマンス/リスクモニタリング（月次・四半期レビュー）
- 関係性・コスト最適化、リスク管理とエスカレーション
- オフボーディング（90日計画）

#### chapters/4_vmo-guide-responsibility.md（第4章：クラウド/SaaS・運用保守委託でのVMOの特別な注意点）
- クラウド/SaaS調達でのVMOの追加業務（データ所在地、ロックイン回避）
- 運用保守委託でのVMOの管理ポイント（L1-L4サポート体制）
- VMOが交渉すべきSLA設計、セキュリティ・データ保護（Shared Responsibility Model）
- 継続監視ダッシュボード

#### chapters/5_vmo-guide-raci.md（第5章：VMOの組織内での役割と連携）
- VMOの組織上の位置づけ（組織図）
- 調達プロセス／運用フェーズでのRACIマトリクス
- エスカレーションルート、VMOが活用すべきツール、スキル向上ロードマップ

#### chapters/6_vmo-guide-kpi.md（第6章：成果を測る指標（KPI））
- VMOの個人KPI（効率性、コスト、品質、リスク）
- VMO組織全体のKPI
- 成熟度向上（COBIT準拠、Level 1-5）

#### chapters/7_vmo-guide-checklist.md（第7章：VMOの実践チェックリスト）
- 日常（週次・月次）／四半期／年次／緊急時の各チェックリスト

#### chapters/vmo-guide-appendix.md（付録）
- **付録A**：テンプレート集（ベンダー台帳、RFP評価マトリクス、月次レビューアジェンダ、ベンダー評価シート、オフボーディングチェックリスト）
- **付録B**：Q&A（VMO設置タイミング、SLA未達対応、価格削減交渉、ロックイン回避、評価が低い場合の判断）
- **付録C**：ITIL準拠 L1-L3問題解決フロー
- **付録D**：Follow-the-sunモデル

### データモデル（data/）

ベンダー管理システムのテーブル定義書一式。`vendors`（ベンダー基本情報）を起点に、`contracts`（個別契約）、`services`（提供サービス）、`orders`（発注実績）が外部キーで連携する構成。各定義書にはカラム定義（データ型・必須・制約）を記載（最終更新日：2026-01-24）。

### 提案資料（proposal/）

- **cost-optimization/**：ICTコストの最適化提案。Spend Dataの可視化とContract Masterの一元管理を、コスト削減交渉の"レバー"として位置づけている
- **data-governance/**：データガバナンス提案。支出データ分析資料（`spend_data/`、日本語・英語版）を裏付け資料として添付
- **prepaid-contract/**：業務システム委託における前払い契約の見直し提案。月額払いへの移行によるリスク低減・ガバナンス強化・交渉力回復を論じる

## 読み進め方の推奨

### 初めて読む方（VMO初心者）

1. **chapters/1_vmo-guide.md**（第1章）でVMOの役割と位置づけを理解
2. **chapters/2_vmo-guide-procurement.md**（第2章）で調達プロセスの基本を把握
3. **chapters/3_vmo-guide-lifecycle-management.md**（第3章）でライフサイクル管理の全体像を理解
4. **chapters/vmo-guide-appendix.md**（付録）のテンプレートを確認し、実務に活用

### 実務で活用する方（VMO経験者）

1. **chapters/6_vmo-guide-kpi.md・7_vmo-guide-checklist.md**（第6-7章）のチェックリストを日常業務に組み込む
2. **chapters/4_vmo-guide-responsibility.md**（第4章）で特殊ケースへの対応を確認
3. **chapters/5_vmo-guide-raci.md**（第5章）で組織内連携を最適化
4. **chapters/vmo-guide-appendix.md**（付録）のテンプレートをカスタマイズして使用

### 全体を通読したい方

**vmo-guide.md**（フル版）を上から読む

## 関連リソース

- COBIT 2019 Framework
- ITIL 4 Foundation

---

**注意事項**：本ガイドは一般的なベンダーマネジメントのベストプラクティスを提供していますが、各組織の状況に応じてカスタマイズが必要です。法務・財務・セキュリティ部門との連携を必ず実施してください。
