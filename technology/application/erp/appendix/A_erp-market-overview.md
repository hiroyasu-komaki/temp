# 付録A　主要ERPの比較

> **参照元**：01_definition.md、03_landscape.md
> **注意**：2026-11-14 に、出典で確認できた事実だけに絞って作り直した。2026年2月作成の旧版にあった市場シェア・導入社数・導入費用・導入期間・強み／弱み・向いている企業は、出典がなく、誤り（mcframe の導入社数、更新頻度など）も含んでいたため削除した。製品の評価は 04章の論点で行う。

## 主要製品の基本情報

| 項目 | SAP S/4HANA | Oracle Fusion Cloud ERP | Microsoft Dynamics 365（Finance / Supply Chain Management） | GLOVIA One | mcframe |
|------|------|------|------|------|------|
| **提供企業** | SAP SE（ドイツ・ヴァルドルフ） | Oracle（米国） | Microsoft（米国） | 富士通（日本） | ビジネスエンジニアリング（B-EN-G、日本） |
| **提供開始** | 2015年2月 | — | — | 2026年4月（GLOVIA SUMMIT・iZ・きららを統合した後継ブランド） | 1996年（mcframe 7 は2017年、mcframe X は2023年から段階的に提供） |
| **提供形態** | オンプレミス、プライベートクラウド（RISE with SAP）、パブリッククラウド（GROW with SAP） | SaaS | SaaS | マルチテナントの SaaS | mcframe 7：パッケージ／mcframe X：SaaS |
| **更新の頻度** | オンプレミス・プライベートクラウドは2年ごとのメジャーリリース（2023年から）と、その間の機能パック。パブリッククラウドは年2回 | 四半期ごと（26A〜26D のように命名。スキップ不可） | サービス更新は年4回（2月・4月・7月・10月）。年2回以上の適用が必須 | 標準機能を頻繁にリリースする方針（頻度は未公表） | — |
| **主な対象** | — | — | — | 年間売上約30億〜1,000億円の日本企業 | 製造業 |
| **主な構成** | — | — | Finance、Supply Chain Management など | 会計、人事給与、販売、生産 | mcframe 7：SCM（生産・販売・在庫）、PCM（原価管理）、CFP（CO2排出量）、LiteMES（製造実行）。会計機能は持たない |
| **拡張の方式** | 標準を改変せず、BTP 上に拡張を置く（Clean Core） | — | 標準コードの上書き（オーバーレイ）は不可で、拡張（Extension）だけが使える。Power Platform とも連携する | API で他社ソリューションと連携し、アドオン開発を最小限に抑える | mcframe 7 はビジネスロジックの組み換えや機能拡張ができる |
| **導入実績** | — | — | — | — | 1,000社以上、海外は17か国2,000サイト以上（公式サイト） |

「—」は、今回の確認で一次資料に当たれなかった項目。

## MRP・MRP II・ERP の変遷

| 段階 | 時期 | 何が加わったか |
|------|------|------|
| MRP（資材所要量計画） | 1960年代〜 | 基準生産計画と部品表（BOM）から、必要な資材の量と時期を計算する |
| クローズドループ MRP | 1970年代 | MRP に能力計画を組み込み、計画と実績を突き合わせる |
| MRP II（製造資源計画） | 1980年代 | 財務、販売・業務計画（S&OP）、能力計画を統合し、設備・人員・資金まで計画する。名称は Oliver Wight による |
| ERP | 1990年〜 | 製造以外（会計・販売・人事など）を含む全社の業務を統合する。用語は1990年に Gartner が使い始めた |

---

**出典**（確認日：2026-11-14）

- SAP S/4HANA の提供開始：Wikipedia「SAP S/4HANA」— https://en.wikipedia.org/wiki/SAP_S/4HANA
- SAP S/4HANA のリリースサイクル：SAP Learning「Navigating Release Upgrades」— https://learning.sap.com/courses/implementing-sap-s-4hana-cloud-private-edition/navigating-release-upgrades_ae2d796c-bafd-4e04-8b41-562ebda9eb49 、SAP PRESS「The roadmap to SAP S/4HANA」— https://blog.sap-press.com/the-roadmap-to-sap-s4hana
- Oracle Fusion の四半期更新：Oracle Fusion Insider「Quarterly updates made easy」— https://blogs.oracle.com/fusioninsider/quarterly-updates-made-easy
- Dynamics 365 のサービス更新：Microsoft Learn「Service update availability」— https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/get-started/public-preview-releases
- Dynamics 365 の拡張方式：Microsoft Learn「Extensibility home page」— https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/extensibility/extensibility-home-page 、Power Platform 連携 — https://learn.microsoft.com/en-us/training/modules/explore-technical-architecture-finance-operations/extend-functionality
- GLOVIA One：富士通 プレスリリース（2026-04-20）— https://global.fujitsu/ja-jp/pr/news/2026/04/20-01 、統合前の3製品：IT Leaders — https://it.impress.co.jp/articles/-/29261
- mcframe 7 の発売（2017年）と初版（1996年）：MONOist（2016-12）— https://monoist.itmedia.co.jp/mn/articles/1612/15/news052.html
- mcframe 7 に会計機能がない点：MONOist（2020-01）— https://monoist.itmedia.co.jp/mn/articles/2001/15/news013.html
- mcframe 7 のモジュール構成：mcframe 公式サイト 製品ページ — https://www.mcframe.com/product/7
- mcframe の導入実績：mcframe 公式サイト About — https://www.mcframe.com/about
- mcframe X：IT Leaders（2023-01）— https://it.impress.co.jp/articles/-/24332
- MRP〜ERP の変遷：NetSuite「ERP の歴史」— https://www.netsuite.com/portal/br/resource/articles/erp/erp-history.shtml 、The CFO Club「The History of ERP」— https://thecfoclub.com/operational-finance/history-of-erp/
