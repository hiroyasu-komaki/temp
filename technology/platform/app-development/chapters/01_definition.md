# 01 アプリ開発・DevOps・ローコードの定義と範囲

## 要旨

アプリ開発は、業務に必要なソフトウェアを**作り、変え、届け続ける**活動である。企業の IT では、ゼロから作るより、**パッケージ・SaaS の拡張**や**ローコードでの開発**の比重が大きい。DevOps は、開発と運用を分けずに、**小さな変更を自動化された工程で頻繁に、安全に届ける**考え方である。近年は、**AI がコードを書く**ことが当たり前になり、速さと安定の両立が改めて問われている。

## 定義

アプリ開発と DevOps に、1つに定まった標準の定義はない。本資料では、DevOps を「開発と運用が協力し、自動化と計測で、変更を速く安全に届ける考え方と実践」として扱う（本資料の整理）。ローコードについては、Gartner が企業向けのローコードの基盤を、モデル駆動の開発の道具・生成 AI・既製の部品を使って、アプリの開発と保守を速める基盤と定義している。

## 成り立ち

| 時期 | できごと |
|---|---|
| 2010年代前半 | DevOps の考え方が広がり、DORA などが開発の成果を測る調査を始める。DORA は2018年に Google に加わる |
| 2017〜2018年 | Gartner が、のちのローコードの評価を「High-Productivity aPaaS」の名前で出す |
| 2020年代前半 | ローコードと市民開発が企業に広がる。米国では安全な開発の枠組み（NIST SSDF 1.1、2022年）が整う |
| 2024年〜 | AI のコード支援の評価が始まる（Gartner の AI Code Assistants の評価は2025年が2回目）。DORA は2025年に報告書の名前を AI による開発の支援を主題にしたものに改める |

## 用語集

| 用語 | 意味 |
|---|---|
| SDLC（ソフトウェア開発ライフサイクル） | 計画・設計・開発・試験・リリース・運用・廃棄の一連の流れ |
| DevOps | 開発（Dev）と運用（Ops）が協力し、自動化と計測で、変更を速く安全に届ける考え方と実践 |
| CI（継続的インテグレーション） | 変更をこまめにまとめ、そのたびに自動でビルドと試験を行うこと |
| CD（継続的デリバリー／デプロイ） | 試験を通った変更を、いつでも（または自動で）本番に出せる状態にすること |
| DevSecOps | セキュリティの確認を、開発の工程の中に組み込むこと |
| プラットフォームエンジニアリング | 開発者が共通に使う道具と環境を、社内の基盤として整えて提供すること |
| ローコード | 画面の部品の組み合わせや、モデルの定義で、コードを少なく書いてアプリを作る方式 |
| 市民開発 | IT 部門ではない業務部門の担当者が、ローコードなどでアプリや自動化を作ること |
| フュージョンチーム | 業務部門と IT の担当者が組んで開発するチーム |

## 開発の形

| 形 | 内容 | 例 |
|---|---|---|
| 自社開発 | 自社または委託先が、要件に合わせてゼロから作る | 独自の業務アプリ、社外向けの Web サービス |
| パッケージ・SaaS の拡張 | 製品の標準の機能に、拡張の仕組みで機能を足す | ERP の拡張（→ erp 02章）、Salesforce の基盤の上の開発 |
| ローコードでの開発 | ローコードの基盤で、IT または業務部門が作る | Power Apps のアプリ、Power Automate の自動化 |
| 表計算・マクロ | 利用者が表計算のファイルやマクロで処理を作る | Excel の計算表、VBA |

## 指標と枠組み

| 名称 | 発行元 | 内容 |
|---|---|---|
| DORA の指標 | Google の DORA（DevOps Research and Assessment） | 開発の成果を測る指標。2025年版では、**速さ**（変更のリードタイム、デプロイの頻度、失敗したデプロイからの回復の時間）と**不安定さ**（変更の失敗率、デプロイのやり直しの率）の5つに整理した。2025年からは報告書の名前を「State of AI-assisted Software Development」に変えた |
| NIST SP 800-218（SSDF） | 米国 NIST | 安全なソフトウェア開発の実践の枠組み。どの開発の手法にも組み込めるよう、高い水準の実践をまとめる。確定版は2022年2月3日の 1.1。1.2 の案が2025年12月17日に出た |
| NIST SP 800-218A | 米国 NIST（2024年7月26日） | 生成 AI と基盤モデルの開発に向けた SSDF の追加の指針 |
| ISPE GAMP 5 第2版 | ISPE | GxP のシステムの開発・変更での検証の考え方。アジャイルな開発も扱う（→ gxp-compliance） |

## 範囲（何であり、何でないか）

| 含むもの | 含まないもの（隣接領域） |
|---|---|
| 開発の工程・環境・道具・指標 | Web アプリの脅威と設計原則、認証・認可（→ web-security） |
| ローコードの基盤と、その技術的な統制の仕組み | 本番の監視・障害対応・ITSM（→ it-operations） |
| AI による開発の支援 | AI の仕組みそのもの（→ ai） |
| | GxP のシステムのバリデーションの要件（→ gxp-compliance） |
| | 市民開発の社内ルール・承認の手順（→ governance 側、未作成） |

---

**出典**（確認日：2026-11-14）

- DORA の5つの指標：Engineering Enablement（DX）— https://newsletter.getdx.com/p/doras-2025-research-on-the-impact 、報告書の改称：RedMonk（2025-12）— https://redmonk.com/rstephens/2025/12/18/dora2025/
- SSDF：NIST CSRC — https://csrc.nist.gov/news/2025/draft-ssdf-version-1-2 、刊行の一覧 — https://csrc.nist.gov/Projects/ssdf/publications
- SP 800-218A：NIST CSRC — https://csrc.nist.gov/Projects/ssdf/news
- ローコードの基盤の定義（Gartner）：Process Excellence Network — https://www.processexcellencenetwork.com/low-code-automation/news/gartner-releases-magic-quadrant-for-low-code-application-platforms
- DORA が Google に加わったこと：RedMonk — https://redmonk.com/rstephens/?p=943
- High-Productivity aPaaS の名前：OutSystems — https://www.outsystems.com/p/low-code-application-platforms-gartner-2023/
- AI Code Assistants の評価が2025年で2回目であること：kurtsh — https://kurtsh.com/2025/11/18/news-github-copilot-a-leader-in-the-gartner-magic-quadrant-for-ai-code-assistants-sept-2025/
- 用語の説明、開発の形の表、DevOps の定義、成り立ちの「2010年代前半」「2020年代前半」の時期の目安は本資料の整理
