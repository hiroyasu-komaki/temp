# README：VMOベンダーマネジメント資料

## 概要

このフォルダには、企業IT組織におけるベンダーマネジメント（Vendor Management）に関する実践ガイド、独立した参照用の付録、および社内外向けの提案・案内HTML資料が含まれています。VMO（Vendor Management Office／ベンダーマネジメント担当者）が日々の業務で直面する課題に対応するための実践的な手引きとして構成されています。

## フォルダ構成

```
vmo_value-delivery/
├── README.md                                  ← 本ファイル（全体の案内）
├── index.html                                  ← html/ 内資料へのランディングページ
│
├── chapters/                                   ← 実践ガイド 第I部〜第III部
│   ├── 1_value-delivery.md                        第I部：VMOの価値提供（第1〜4章）
│   ├── 2_practice-guide-entry.md                  第II部：実務ガイド（相談の入口編）（第5〜6章）
│   └── 3_practice-guide-response.md               第III部：実務ガイド（相談への対応編）（第7〜10章）
│
├── appendix/                                   ← 第IV部：付録（独立したリファレンス文書）
│   ├── A_templates.md                             付録A：相談受付テンプレート集
│   ├── B_templates-forms.md                       付録B：実務様式集（台帳・評価・比較・レビュー・チェックリスト）
│   ├── C_itil-flow.md                             付録C：ITILの基礎知識（インシデント管理・問題管理・サポート階層）
│   ├── D_support-model-comparison.md              付録D：サポート運用体制モデルの比較（Follow-the-sun／24-365／通常営業）
│   ├── E_cobit-mapping.md                         付録E：VMOの業務とCOBIT 2019フレームワークの対応
│   ├── F_sow-sla.md                               付録F：SOWとSLA（運用保守委託の契約文書の構造）
│   └── G_data-protection.md                       付録G：データ保護・セキュリティの契約要件
│
├── html/                                        ← 社内外向けHTML資料
│   ├── consultation-landing.html                   「こんなとき、VMOにご相談ください」（利用者向け・日英切替）
│   └── three-models.html                           「エージェント型VMOの特徴」（社内向け・導入方針）
│
└── proposal/                                    ← 社内提案資料（部内共有・承認用）
    ├── VMO役割定義.pptx                            基盤担当・受付担当（L1）の役割定義（提案資料）
    └── VMO役割定義.pdf                             同上（PDF版）
```

## 各文書の概要

### 実践ガイド（chapters/）

#### chapters/1_value-delivery.md（第I部：VMOの価値提供）
- 第1章：VMOの提供方法 ― エージェント型（伴走型サービス）（3モデルの比較、選定理由、導入後のモニタリング）
- 第2章：VMOの機能と役割（定義、4フェーズと11の相談の入口、担う業務）
- 第3章：ステークホルダーとそれぞれに対する提供価値
- 第4章：VMOとその他IT機能との役割と責任（組織上の位置づけ、RACI、A（最終責任）の置き方の原則）

#### chapters/2_practice-guide-entry.md（第II部：実務ガイド／相談の入口編）
- 第5章：相談を受けるときの共通の型（5ステップ、初回に確認する7項目、引き受ける範囲の合意）
- 第6章：相談に応じるための基盤業務（台帳維持、相場情報の蓄積、契約更新カレンダー等）

#### chapters/3_practice-guide-response.md（第III部：実務ガイド／相談への対応編）
- 第7章：探索フェーズの実務
- 第8章：選定・契約フェーズの実務
- 第9章：運用・改善フェーズの実務
- 第10章：見直し・転換フェーズの実務

### 付録（appendix/）

第IV部として位置づけ、各付録は本編を参照しない、独立したリファレンス文書として構成しています。

- **付録A**：相談受付テンプレート集 ― 相談の切り分けと、相談種別ごとの情報提供依頼テンプレート
- **付録B**：実務様式集 ― ベンダー台帳項目定義、評価基準表、提案比較表、月次レビューアジェンダ、年次評価、オンボーディング／オフボーディングのチェックリスト
- **付録C**：ITILの基礎知識 ― サービスマネジメントの基礎、インシデント管理と問題管理の区別、サポート階層とエスカレーション
- **付録D**：サポート運用体制モデルの比較 ― Follow-the-sun／24-365／通常営業の3モデルの選定基準
- **付録E**：COBIT 2019フレームワークとの対応 ― ガバナンスとマネジメントの基礎知識、APO10を中核としたVMO関連目標の整理
- **付録F**：SOWとSLA ― 運用保守委託における契約文書の構造、SOW・SLAそれぞれの設計と点検チェックリスト
- **付録G**：データ保護・セキュリティの契約要件 ― クラウド/SaaSにおける責任分界、契約に定めるべき事項、点検チェックリスト

### 提案資料（proposal/）

- **proposal/VMO役割定義.pptx／.pdf**：基盤担当・受付担当（L1）の役割を再定義するための、部内共有・承認用の提案資料

### ランディングページ・HTML資料

- **index.html**（ルート直下）：html/ 内の資料一覧に接続するランディングページ
- **html/consultation-landing.html**：「こんなとき、VMOにご相談ください」。探索／選定・契約／運用・改善／見直し・転換の4フェーズ・11の相談の入口を、利用者の言葉に沿って紹介する案内ページ（日本語・英語切替対応）
- **html/three-models.html**：「エージェント型VMOの特徴」。VMOの提供方法として採用する「エージェント型（伴走型サービス）」を、他のモデルと比較しながら説明する社内向け導入方針資料

## 読み進め方の推奨

### 初めて読む方（VMO初心者）

1. **chapters/1_value-delivery.md**（第I部）でVMOの役割・提供価値・提供方法の全体像を理解
2. **chapters/2_practice-guide-entry.md**（第II部）第5章で相談対応の共通の型を把握
3. **chapters/3_practice-guide-response.md**（第III部）で該当する相談の入口（第7〜10章）を確認
4. **appendix/A_templates.md・B_templates-forms.md**（付録A・B）のテンプレート・様式を確認し、実務に活用

### 実務で活用する方（VMO経験者）

1. **chapters/2_practice-guide-entry.md**第6章で、相談に応じるための基盤業務（台帳・相場情報・更新カレンダー）を日常業務に組み込む
2. **appendix/D_support-model-comparison.md・F_sow-sla.md・G_data-protection.md**（付録D・F・G）で、契約・サポート体制の特殊論点を確認
3. **appendix/C_itil-flow.md・E_cobit-mapping.md**（付録C・E）で、標準フレームワークとの対応を確認

### 利用者・関係者に共有する方

ルート直下の **index.html** から、状況説明用の **html/consultation-landing.html**、または導入方針説明用の **html/three-models.html** を案内する

## 関連リソース

- COBIT 2019 Framework
- ITIL 4 Foundation
