# 01 分析基盤の定義と範囲

## 要旨

分析基盤は、業務システムから取引などのデータを集めて**蓄積し、分析できる形に整え、見せる**ための仕組みである。蓄積の置き場所として**データウェアハウス（DWH）**、**データレイク**、両者を合わせた**レイクハウス**があり、見せる道具として **BI** がある。

## 用語

| 用語 | 意味 |
|---|---|
| データウェアハウス（DWH） | 意思決定のために、複数の業務システムのデータを統合して蓄積する場所。Inmon は1992年の著書『Building the Data Warehouse』で、「主題別・統合・不揮発・時系列の、経営の意思決定のためのデータの集まり」と定義した |
| データマート | 特定の部門や用途に絞った、小さな DWH |
| 次元モデル（スタースキーマ） | 数値（ファクト）と、それを切り分ける軸（ディメンション：顧客・製品・期間など）に分けた表の設計。Kimball が1996年の『The Data Warehouse Toolkit』で広めた |
| データレイク | データを元の形のまま大量に置く場所。Pentaho の James Dixon が2010年10月のブログで名づけた。整えて包装した「ボトル入りの水」がデータマートなら、データレイクは自然な状態の大きな水たまり、というたとえ |
| レイクハウス | データレイクと同じ安価な保管場所の上に、DWH と同等のデータ管理（トランザクションなど）を載せる構成。Databricks の研究者らが2021年1月の CIDR で論文として示した |
| オープンテーブルフォーマット | Parquet などのファイルの上に、表としての管理情報（版、変更履歴）を載せる形式。Apache Hudi、Apache Iceberg、Delta Lake が代表 |
| BI（ビジネスインテリジェンス） | データを集計し、ダッシュボード・レポート・対話的な分析で見せる道具 |
| ETL／ELT | 抽出・変換・書き込み。先に変換してから書き込むのが ETL、書き込んでから分析基盤の中で変換するのが ELT |

## 扱うもの・扱わないもの

| 扱う | 扱わない（→ 移り先） |
|---|---|
| DWH・データレイク・レイクハウスの構成 | 業務システムの間のデータ連携（→ integration） |
| データモデル（Inmon・Kimball・Data Vault）とレイヤー（メダリオン） | マスタの正本の決め方（→ master-data） |
| 主要な DWH・レイクハウス製品と BI 製品 | 機械学習・生成AIの活用（→ ai） |
| 論点と隣接領域との境界 | データベースの基盤としての運用（→ infrastructure） |

---

**出典**（確認日：2026-11-14）

- Inmon の著書と定義：DATAVERSITY — https://www.dataversity.net/?p=14127 、Bill Inmon — https://williaminmon.substack.com/p/a-tale-of-two-architectures-kimball
- Kimball の著書と次元モデル：TDAN（書評）— https://tdan.com/?p=5594 、Holistics — https://www.holistics.io/books/setup-analytics/kimball-s-dimensional-data-modeling/
- データレイクの命名：Martin Fowler — https://martinfowler.com/bliki/DataLake.html 、Springer — https://link.springer.com/doi/10.1007/978-3-319-63962-8_7-1
- レイクハウス：Armbrust ほか（CIDR 2021）— https://vldb.org/cidrdb/2021/lakehouse-a-new-generation-of-open-platforms-that-unify-data-warehousing-and-advanced-analytics.html
- オープンテーブルフォーマット：Apache Hudi — https://hudi.apache.org/blog/2026/07/14/what-is-an-open-table-format
