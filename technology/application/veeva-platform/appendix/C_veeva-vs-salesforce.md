# 付録C　Veeva と Salesforce Life Sciences Cloud の比較

> **参照元**：[04章](../chapters/04_tradeoffs.md) 論点1

CRM 領域の競争環境を整理します。システム選定や移行判断の背景情報です。

> 競争環境は変化が速い領域です。判断に使う場合は最新情報を確認してください。

---

## C-1 背景

Veeva CRMは元来Salesforceプラットフォーム上で構築されていましたが、現在は自社基盤の **Vault CRM** への移行を進めています。旧 Veeva CRM のサポート終了は **2029年12月31日**（当初の2030年9月から前倒し）で、2026年3月時点で Vault CRM の稼働顧客は125社を超えています。一方、Salesforceは2024年に **Life Sciences Cloud**（現在の名称は Agentforce Life Sciences）を投入し、2025年10月には営業・メディカル向けの **Life Sciences Cloud for Customer Engagement** の一般提供を始めて、Veeva CRM の領域に直接参入しています。
## C-2 アーキテクチャ思想の比較

| 観点 | Veeva | Salesforce Life Sciences Cloud |
|------|-------|-------------------------------|
| 設計思想 | 業界特化の閉じたエコシステム | 多業界基盤のライフサイエンス拡張 |
| 強み | Vault-CRM一体統制、GxPネイティブ、即戦力 | AI（Agentforce）先行、Data Cloud、パートナー規模 |
| データ統合 | Vault間のネイティブ連携 | Data Cloud + Informatica（80億ドル買収）による柔軟統合 |
| AI | Vault AI（各アプリ組み込みのエージェント。Vault CRM 向けは2025年12月に提供開始）、Veeva Falcon（業務を代行する標準エージェント。Falcon MLR は提供中、治験・薬事・安全性向けは2026年11月から早期提供、日本は2027年以降） | Agentforce（HCPスケジューリング等） |
| コンテンツ統制 | PromoMats-CLMネイティブ連携 | パートナーエコシステムで構築 |
| 主な採用実績 | Vault CRM 稼働125社超（上位20社のうち2社を含む、2026年3月） | 選定を公表：Novartis・AstraZeneca（2025年12月）、Pfizer（早期導入企業）など |
## C-3 Salesforceの勝ち筋

1. **AI/Agentforceの先行**：HCPスケジューリング・コールプランニング・コンテンツ提案・音声ログをAIエージェントで自動化
2. **データ統合の優位**：Data Cloud・MuleSoft に、2025年11月に買収を完了した Informatica（約80億ドル）を加え、外部データ（処方・請求・EHRなど）を統合する
3. **パートナーエコシステム**：athenahealth（EHR）・H1（HCP/KOLデータ）・Infinitus.ai（給付確認）などと連携。AppExchange のパートナー製品も使える
4. **移行支援とコスト**：旧 Veeva CRM（Salesforce基盤）のサポート終了（2029年末）を活かし、低コスト移行＋AIアップグレードを提案
## C-4 Veevaの防衛力と弱点

| Veevaの強み | Veevaの弱点（リスク） |
|---|---|
| 業界特化のコンプライアンス・サンプリング・MSL機能 | AI競争（Agentforceとの競合。Veevaも Vault AI・Falcon を展開） |
| 閉じたライフサイエンスエコシステムの深さ | 2029年末のサポート終了に伴う移行時の離脱リスク |
| Vault-CRM一体統制（GxPネイティブ） | エコシステムの狭さ（EHR・患者データなど外部データとの連携は Salesforce のほうが広い。IQVIA とは2025年に係争を解消して提携し、IQVIA データを Veeva Network・Nitro で使えるようになった） |
| R&Dからコマーシャルまで同一基盤で揃う製品の幅 | 業界向けに作り込まれている分、汎用プラットフォームに比べてカスタマイズの自由度が低い |

**競争の本質**：「業界特化の深さ」vs「汎用プラットフォームの広さと速さ」。
## C-5 データエンジニアへの示唆

Veevaは「閉じた統合の深さ」、Salesforceは「オープンな統合の広さ」をそれぞれ武器にしています。

- **Veeva環境での設計**：Vault API / VQLを中心とした統一インターフェースで設計できる
- **Salesforce環境での設計**：パートナー製品ごとのAPI仕様を個別に把握する必要がある
- **移行・共存シナリオ**：HCP/HCO識別子マッピングと、コンテンツ配布状態の整合性維持が最大の課題

---

**出典**（確認日：2026-11-14。数値はいずれも記載の時点のもの）

- 旧 Veeva CRM のサポート終了の前倒し、Vault CRM の稼働社数：Veeva「Fiscal 2026 Fourth Quarter Results」（2026-03-04）— https://ir.veeva.com/news/news-details/2026/Veeva-Announces-Fourth-Quarter-and-Fiscal-Year-2026-Results/default.aspx 、Veeva ニュース（2026-03-03）— https://www.veeva.com/eu/wp-json/wp/v2/resources/94884
- IQVIA との提携：Veeva FY2026 Q2 決算の要約 — https://fintool.com/app/research/companies/VEEV/earnings/Q2%202026
- Vault AI（Vault CRM 向けエージェント）：Veeva プレスリリース（2025-12-04）— https://kyodonewsprwire.jp/release/202512040355
- Veeva Falcon：Veeva 製品ページ — https://www.veeva.com/products/falcon/ 、日本語ページ — https://www.veeva.com/jp/products/falcon/
- Life Sciences Cloud for Customer Engagement の一般提供（2025年10月）：Salesforce — https://www.salesforce.com/au/life-sciences/cloud/
- Novartis・AstraZeneca の選定：Salesforce Life Sciences — https://www.salesforce.com/life-sciences/ 、Pfizer：Salesforce ニュース — https://www.salesforce.com/ap/news/stories/life-sciences-cloud-for-customer-engagement-availability/
- パートナー連携（athenahealth・H1・Infinitus.ai）：Salesforce の発表（2025） — https://www.silicon.co.uk/press-release/salesforce-unveils-life-sciences-partner-network-to-accelerate-digital-labor-and-data-programs
- Informatica の買収完了（2025-11）：TechRadar — https://www.techradar.com/pro/salesforce-snaps-up-informatica-in-usd8bn-deal-to-boost-ai-tools
- 「勝ち筋」「防衛力と弱点」「データエンジニアへの示唆」は、上記をもとにした本資料の評価
