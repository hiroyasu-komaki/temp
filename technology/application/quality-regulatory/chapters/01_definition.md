# 01 品質・薬事・安全性の定義と範囲

## 要旨

この領域は、医薬品が**決められた品質で作られ（品質）、承認を受けて維持され（薬事）、市販後の安全性が監視される（安全性）**ことを支える3つのシステムからなる。品質の QMS、薬事の RIM、安全性の PV（安全性データベース）である。どれも規制当局への説明責任を負う記録を持つ。

## 3つのシステム

| 区分 | システム | 主な機能 |
|---|---|---|
| 品質 | QMS（品質マネジメントシステム） | 文書管理、逸脱、CAPA（是正・予防措置）、変更管理、教育訓練、監査、苦情 |
| 薬事 | RIM（薬事情報管理） | 製品×国ごとの承認状況、承認申請の資料の作成と提出（eCTD）、当局とのやり取り |
| 安全性 | PV（ファーマコビジランス）の安全性データベース | 副作用などの個別症例（ICSR）の受け付け・評価・当局への報告、シグナルの検出、定期報告 |

## 標準と規制

| 項目 | 内容 |
|---|---|
| eCTD v4.0 | 承認申請の電子形式。日本の PMDA は2022年4月から v4.0 の受け付けを始め、2026年3月までを移行期間とし、2026年4月から v4.0 へ完全に移行する予定とした |
| ICH E2B(R3) | 個別症例の安全性報告（ICSR）を電子で交換する国際標準 |
| FDA の CSA ガイダンス | FDA は2025年9月24日に、製造と品質システムで使うソフトウェアの確からしさを、リスクに応じて確かめる考え方（Computer Software Assurance）の最終ガイダンスを出した。医療機器の担当部門（CDRH・CBER）によるもので、2026年2月3日に改訂版が出ている。CSV・データインテグリティの全体は gxp-compliance にまとめた |
| IDMP | 医薬品の製品・物質の識別の国際標準（→ master-data） |

## 扱うもの・扱わないもの

| 扱う | 扱わない（→ 移り先） |
|---|---|
| QMS・RIM・PV の機能と構造 | Veeva の品質・薬事・安全性製品の詳細（→ veeva-platform 付録E） |
| 主要製品 | 臨床試験の運営とデータ（→ rd） |
| 論点と隣接領域との境界 | 製造の実行（→ manufacturing） |

---

**出典**（確認日：2026-11-14）

- QMS の機能：IntuitionLabs — https://intuitionlabs.ai/articles/pharmaceutical-compliance-software-guide
- RIM の機能：[veeva-platform 付録E](../../veeva-platform/appendix/E_rd-products.md)
- eCTD v4.0 の国内の予定：PMDA（2023-06-27）— https://www.pmda.go.jp/files/000263198.pdf
- E2B(R3)：IntuitionLabs — https://intuitionlabs.ai/articles/pharmacovigilance-software-systems-overview
- CSA ガイダンス：FDA — https://www.fda.gov/regulatory-information/search-fda-guidance-documents/computer-software-assurance-production-and-quality-system-software 、NSF（改訂版）— https://www.nsf.org/life-science-regulatory-news/fda-final-guidance-computer-software-assurance-csa
