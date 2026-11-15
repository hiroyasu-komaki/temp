# 01 GxP のコンピュータ化システムの定義と範囲

## 要旨

GxP は、医薬品の研究・臨床・製造・流通などで守るべき「適正な実践の基準」の総称である。GxP の記録をコンピュータで扱う場合、**システムが意図どおりに動くことを確かめ（バリデーション）**、**記録が作られてから廃棄されるまで正しく完全なまま保たれる（データインテグリティ）**ことが求められる。これは品質部門のシステムだけでなく、ERP・MES・LIMS・EDC・文書管理・表計算のファイルまで、**GxP の記録を扱うすべてのシステム**にかかる横断の要件である（本資料の整理）。

## 定義

PIC/S と英国 MHRA は、データインテグリティを、データが完全で、一貫し、正確で、信頼でき、頼りにできる度合いであり、その性質がデータのライフサイクルを通じて保たれていること、と定義する。CSV は、コンピュータ化システムが意図した用途に合い、その状態を保っていることを示す活動である（本資料の整理）。

## 成り立ち

| 時期 | できごと |
|---|---|
| 1997年 | 米国 FDA が 21 CFR Part 11 を定める。その後、規則の範囲が実際より広いと業界で受け止められ、すべての電子記録に重い管理をかける運用が広がった |
| 2003年 | FDA が Part 11 の範囲を狭く解釈するガイダンスを出し、リスクに基づく考え方に転じる |
| 2008年 | ISPE が GAMP 5 を出し、リスクに基づく管理とソフトウェアのカテゴリを示す |
| 2010年代 | 査察でデータインテグリティの違反の指摘が増え、FDA（2016年に案、2018年に最終）や PIC/S（2016年に案、2021年に発効）がデータインテグリティのガイダンスを出す |
| 2022年〜 | GAMP 5 第2版（2022年）、FDA の CSA ガイダンス（2022年に案、2025年に最終）、EU GMP Annex 11 の改訂案（2025年）と、クラウド・アジャイル・AI を前提にした見直しが続く |

## 用語集

| 用語 | 意味 |
|---|---|
| GxP | GMP（製造）・GCP（臨床試験）・GLP（非臨床試験）・GDP（流通）・GVP（安全性監視）などの適正基準の総称 |
| コンピュータ化システム | ソフトウェア・ハードウェアと、それを使う人・手順を合わせたもの |
| CSV（Computerized System Validation） | コンピュータ化システムが意図した用途に合い、それを続けていることを、文書で示すこと |
| CSA（Computer Software Assurance） | 品質へのリスクに応じて、確かめる方法と量を変える考え方。FDA が医療機器の領域でガイダンスにした |
| データインテグリティ | データが完全で、一貫し、正確で、信頼でき、それがデータのライフサイクルを通じて保たれている度合い |
| ALCOA+ | データインテグリティの要件を表す頭字語（→ 02章） |
| 電子記録・電子署名（ER/ES） | 紙の記録・手書きの署名と同等に扱える電子の記録と署名 |
| 監査証跡 | 誰が・いつ・何を・なぜ作成・変更・削除したかを、システムが自動で残す記録 |
| 予測規則（predicate rule） | 記録の作成・保存を求める元の規則（GMP など）。Part 11 は、これらの規則が求める記録を電子で扱う場合にかかる |

## 規制とガイダンス

| 地域 | 規制・ガイダンス | 内容 |
|---|---|---|
| 米国 | 21 CFR Part 11 | 電子記録・電子署名の規則。1997年に最終規則として定められた |
| 米国 | Part 11 Scope and Application（2003年8月） | Part 11 の範囲を狭く解釈し、バリデーション・監査証跡・記録の保存・記録の複製の要件の一部について、規制の執行を控える方針を示した。Part 11 自体は有効なまま |
| 米国 | Data Integrity and Compliance With Drug CGMP（2018年12月） | 医薬品の CGMP におけるデータインテグリティの Q&A。ALCOA の5つの属性を示す |
| 米国 | Electronic Systems, Electronic Records, and Electronic Signatures in Clinical Investigations（2024年10月） | 臨床試験での電子システム・電子記録・電子署名の Q&A。2007年の臨床試験のコンピュータシステムのガイダンスを置き換えた |
| 米国 | Computer Software Assurance（2025年9月24日、最終） | 医療機器の製造と品質システムのソフトウェアを、リスクに応じて確かめる考え方。医療機器の担当部門によるもので、医薬品の GMP への直接の適用ではない（→ quality-regulatory 01章） |
| EU | EU GMP Annex 11「Computerised Systems」 | 現行版は2011年6月30日から適用。GMP の活動で使うすべての形態のコンピュータ化システムが対象 |
| EU | Annex 11 の改訂案（2025年7月7日公表） | 文書化の第4章の改訂案、AI の新しい Annex 22 の案と同時に公表され、意見募集は2025年10月7日まで。約4ページから約19ページに増え、アクセス管理・セキュリティ・委託先の管理などを詳しく定める。最終版は2026年の公表が見込まれていたが、2026年10月時点では2011年版のままと報じられている |
| 国際 | PIC/S PI 041-1（2021年7月1日発効） | GMP/GDP 環境のデータ管理とデータインテグリティのガイダンス。ALCOA+ を示す。査察官向けだが業界も参照する |
| 国際 | ISPE GAMP 5 第2版（2022年7月） | コンピュータ化システムのリスクに基づく管理の業界ガイド。規制ではない（→ 02章） |
| 日本 | ER/ES 指針（2005年4月1日、薬食発第0401022号の別添） | 承認・許可などの申請に関わる資料を電磁的記録で提出・保存する場合の留意事項 |
| 日本 | コンピュータ化システム適正管理ガイドライン（2010年10月21日、薬食監麻発1021第11号） | 国内の CSV のガイドライン。2012年4月1日から適用 |
| 日本 | GMP 省令の改正（2021年8月施行） | 約16年ぶりの改正。記録の信頼性の確保（データインテグリティ）を明示的に求め、通知で PIC/S のガイダンスの参照を求めている |

## 範囲（何であり、何でないか）

| 含むもの | 含まないもの（隣接領域） |
|---|---|
| GxP の記録を扱うシステムに共通の要件と、それを満たす技術の仕組み | 社内の SOP・役割・承認の手順（→ governance 側、未作成） |
| バリデーションのライフサイクルと、SaaS での責任分担 | QMS・RIM・PV などの業務システムの機能（→ quality-regulatory） |
| 規制とガイダンスの位置づけ | 製造設備・ユーティリティの適格性評価、工程バリデーション（→ manufacturing） |
| | 臨床試験の運営とデータ（→ rd） |

---

**出典**（確認日：2026-11-14）

- Part 11 の制定（1997年）：JD Supra（2024-10）— https://www.jdsupra.com/legalnews/fda-finalizes-guidance-on-use-of-part-5122297
- Part 11 と 2003年のガイダンス：FDA「Part 11, Electronic Records; Electronic Signatures - Scope and Application」— https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application 、Federal Register（2003-09-05）— https://webarchive.library.unt.edu/eot2008/20080916174457/http://www.fda.gov/OHRMS/DOCKETS/98fr/03-22574.htm
- 2018年のデータインテグリティのガイダンス：FDA — https://fda.gov/media/119570/download 、Federal Register（2018-12-13）— https://www.govinfo.gov/content/pkg/FR-2018-12-13/html/2018-26957.htm
- 2024年の臨床試験のガイダンス：Federal Register（2024-10-02）— https://www.govinfo.gov/content/pkg/FR-2024-10-02/html/2024-22562.htm
- CSA：[quality-regulatory 01章](../../../application/quality-regulatory/chapters/01_definition.md) の出典を参照。2002年のソフトウェアバリデーションのガイダンスの第6節を置き換えたこと：Life Science Daily — https://lifesciencedaily.news/?p=14343
- Annex 11 の現行版：LearnSignal — https://www.learnsignal.com/blog/computer-system-validation-eu-gmp-annex-11-requirements-guide/
- Annex 11 の改訂案：PIC/S（2025-07-07）— https://picscheme.org/en/news/131/joint-stakeholders-consultation-on-the-revision-of-chapter-4 、ECA Academy — https://www.gmp-compliance.org/gmp-news/drafts-of-eu-gmp-guideline-annex-11-annex-22-and-chapter-4-released-for-comment 、ページ数：ISPE Pharmaceutical Engineering（2026年5-6月号）— https://ispe.org/index.php/pharmaceutical-engineering/may-june-2026/innovation-and-regulation-danish-medicines-agency-insights 、2026年10月時点の状況：Life Science Daily — https://lifesciencedaily.news/?p=14343
- PIC/S PI 041-1：PIC/S — https://picscheme.org/docview/4234
- ER/ES 指針：日本薬事法令データ（治験関連文書の事務連絡での引用）— https://nk.jiho.jp/document/93398
- CSV ガイドラインと適用日：大阪府の通知（2012-02-29）— https://ecompliance.co.jp/CSV/pdf/osaka.pdf
- GMP 省令の改正とデータインテグリティ：PwC（2023-05）— https://www.pwc.com/jp/ja/knowledge/prmagazine/pwcs-view/202305/44-07.html
- データインテグリティの定義：PIC/S PI 041-1（MHRA の定義を引用）— https://picscheme.org/docview/4234
- 1997〜2003年に範囲が広く受け止められたこと：Applied Clinical Trials — https://www.appliedclinicaltrialsonline.com/view/navigating-new-21-cfr-11-guidelines
- GAMP の版の経緯：CASRAI — https://casrai.org/compare/gamp-4-vs-gamp-5
- データインテグリティの違反の増加と FDA のガイダンスの経緯：Contract Pharma — https://www.contractpharma.com/fda-data-integrity/ 、PIC/S の案（2016年）と発効：Pharmaceutical Industry Information Portal — https://pharmprom.ru/en/entry-into-force-of-pic-s-guidance-on-good-practices-for-data-management-and-integrity/
- CSA の案（2022年）：Life Science Daily — https://lifesciencedaily.news/?p=14343
- GxP の用語の説明、横断の要件という位置づけ、CSV の定義の言い換えは本資料の整理
