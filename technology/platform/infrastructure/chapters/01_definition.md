# 01 クラウド・インフラの定義と範囲

## 要旨

クラウド・インフラは、業務アプリケーションとデータが動くための**計算資源（サーバー）・保存領域（ストレージ）・ネットワーク・データベース**を、自社のデータセンター（オンプレミス）またはクラウドで提供する層である。クラウドでは、資源を必要なときに自分で用意し、使った分だけ払う。その代わり、**どこまでをクラウド事業者が守り、どこからを自社が守るか**の線を理解しておく必要がある。

## 定義

NIST SP 800-145（2011年）は、クラウドコンピューティングを、設定可能な計算資源（ネットワーク、サーバー、ストレージ、アプリケーション、サービス）の共有プールに、どこからでも必要なときにネットワーク経由でアクセスでき、最小限の管理の手間で素早く用意・解放できるモデルと定義している。このモデルは、5つの本質的な特徴、3つのサービスモデル、4つの配置モデルで構成される。

| 区分 | 内容 |
|---|---|
| 5つの特徴 | オンデマンド・セルフサービス、幅広いネットワークアクセス、資源の共用（リソースプーリング）、素早い伸縮性、利用量の計測 |
| 3つのサービスモデル | IaaS（基盤を借りる。OS とその上は利用者が管理）、PaaS（アプリの実行環境を借りる）、SaaS（アプリそのものを使う） |
| 4つの配置モデル | パブリック、プライベート、コミュニティ、ハイブリッド |

本トピックが主に扱うのは IaaS と PaaS である。SaaS は、それぞれの業務アプリケーションのトピック（erp、veeva-platform など）とワークプレイスで扱う（本資料の整理）。

## 成り立ち

| 年 | 出来事 | 意味 |
|---|---|---|
| 2006 | AWS が Amazon S3（3月）と Amazon EC2（8月、ベータ）を公開 | ハードウェアを持たずに、保存領域と仮想サーバーを API で借りられるようになる |
| 2011 | NIST SP 800-145 を公開 | クラウドの定義と分類の共通の言葉ができる |
| 2022〜2023 | デジタル庁がガバメントクラウドの対象に AWS・Google Cloud・Microsoft Azure・Oracle Cloud Infrastructure を選定（2022年10月）。2023年11月にさくらのクラウドを条件付きで選定 | 国内の公共システムでもクラウドが標準の選択肢になる |
| 2023 | Broadcom が VMware の買収を完了（11月）。永続ライセンスの販売を終了し、サブスクリプションに移行 | オンプレミスの仮想化基盤の費用と契約の前提が変わる |
| 2026 | さくらのクラウドが技術要件を満たし、ガバメントクラウドの5つ目の対象サービスとして条件が外れる（3月） | — |

2026年第2四半期のクラウドインフラ市場（IaaS・PaaS・ホステッドプライベートクラウド）は約1,434億ドルで、シェアは AWS 28%、Microsoft 20%、Google 15% だった（Synergy Research Group）。生成 AI が成長の主な要因とされている。

## 範囲（何であり、何でないか）

| クラウド・インフラが扱うもの | 扱わないもの（隣接領域） |
|---|---|
| IaaS・PaaS、オンプレミスのサーバー・仮想化・ストレージ | SaaS の業務アプリケーションそのもの（各業務アプリのトピック） |
| ネットワーク（拠点間、クラウドとの接続、DNS） | システム間のデータ連携（integration） |
| データベースの基盤（製品・提供形態・可用性） | データの分析基盤（analytics） |
| クラウドの環境の設計（アカウント構成、ランディングゾーン）、費用の管理（FinOps） | システムの監視・障害対応・バックアップの運用（it-operations） |
| | アプリの防御とセキュリティの監視（web-security、security-operations） |

---

**出典**（確認日：2026-11-14）

- クラウドの定義：NIST SP 800-145（2011-09）— https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf
- S3・EC2 の公開：AWS News Blog「Twenty years of Amazon S3」— https://aws.amazon.com/blogs/aws/twenty-years-of-amazon-s3-and-building-whats-next 、TechCrunch（EC2 の最初のベータ、2006-08）— https://techcrunch.com/2021/08/28/how-amazon-ec2-grew-from-a-notion-into-a-foundational-element-of-cloud-computing/
- ガバメントクラウド：さくらインターネットの条件付き認定（Impress Watch、2023-11）— https://www.watch.impress.co.jp/docs/news/1550234.html 、対象5サービスと選定時期の整理 — https://www.issoh.co.jp/column/details/16643/ 、デジタル庁資料（2025-01-24）— https://www.oracle.com/jp/a/ocom/docs/oracle-sapporo-govcloud-jp.pdf
- Broadcom による VMware 買収と永続ライセンスの販売終了：Longview Systems（完了日 2023-11-22）— https://www.longviewsystems.com/blog/broadcom-acquisition-and-the-impact-to-your-vmware-licensing/ 、Computing — https://computing.co.uk/news/4156147/broadcom-shifts-vmware-subscription-model-perpetual-license-sales
- 市場規模とシェア：Synergy Research Group（2026-07-30）— https://www.srgresearch.com/articles/q2-cloud-market-passes-143-billion-highest-growth-rate-in-eight-years
- 範囲の分け方は本資料の整理
