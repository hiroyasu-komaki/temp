# 01 研究開発・臨床の定義と範囲

## 要旨

研究開発・臨床のシステムは、**研究室での実験の記録と試料の管理**（ELN・LIMS）と、**臨床試験の運営とデータの収集**（CTMS・EDC・eTMF など）の2つに分かれる。臨床試験のシステムは GCP（臨床試験の実施の基準）に従い、記録の信頼性を示せることが求められる。

## 用語

| 区分 | 用語 | 意味 |
|---|---|---|
| 研究 | ELN（電子実験ノート） | 実験の計画・手順・結果を電子で記録する |
| | LIMS（ラボ情報管理システム） | 試料の受け入れ、試験の割り当て、結果、装置を管理する。研究のほか、品質管理（QC）の試験室でも使う |
| | SDMS（科学データ管理システム） | 分析装置が出す生データを集めて保管する |
| 臨床 | CTMS（臨床試験管理システム） | 試験・施設・被験者の登録・モニタリング訪問の進み具合を管理する |
| | EDC（電子データ収集） | 症例報告書（CRF）のデータを電子で集め、点検する |
| | eTMF（電子治験関連文書ファイル） | 治験の必須文書を電子で管理する |
| | RTSM／IRT | 被験者の無作為割付と、治験薬の供給を管理する |
| | eCOA／ePRO | 患者が報告する症状などを電子で集める |
| | eConsent | 説明と同意を電子で行う |

## 規制：ICH E6(R3)

GCP の国際的な基準である ICH E6 は、2025年1月6日に E6(R3) として改訂され、ICH のステップ4に達した。改訂版には、データの管理（データガバナンス）の節が設けられ、リスクに応じた品質管理が全体の考え方になった。各国の当局が順に取り入れている。

## 扱うもの・扱わないもの

| 扱う | 扱わない（→ 移り先） |
|---|---|
| 研究と臨床のシステムの区分と構造 | 承認申請と市販後の安全性（→ quality-regulatory） |
| 主要製品 | Veeva の臨床製品の詳細（→ veeva-platform 付録E） |
| 論点と隣接領域との境界 | 医薬品開発の工程と CMC（→ veeva-platform 付録A） |

---

**出典**（確認日：2026-11-14）

- ICH E6(R3)：PMDA（ガイドライン本文）— https://www.pmda.go.jp/files/000277728.pdf 、RAPS（2025-01-14）— https://www.raps.org/resource/ich-adopts-e6r3-guideline-on-good-clinical-pract.html 、ICR — https://icr-global.org/2025/02/11/ich-e6r3-key-updates-and-their-impact-on-clinical-trials/
- LIMS の機能：Thermo Fisher SampleManager の説明（MarketsandMarkets）— https://www.marketsandmarkets.com/ResearchInsight/lab-informatic-market.asp
- 臨床の用語：[veeva-platform 付録E](../../veeva-platform/appendix/E_rd-products.md)
- 用語の説明は本資料の整理
