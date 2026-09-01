# 9. AWS vs Azure　製品・サービス比較表(出典付き)

> **この章の位置づけ**：製品レイヤーでの技術的な効率化を扱うリファレンス章。第10章の契約レイヤー比較と対をなす。
> **対象読者**：AWS・Azure運用管理者／ベンダーマネジメント担当

## 要旨

仮想マシン・サーバーレス・コンテナ・リレーショナルDB・オブジェクトストレージ・生成AI基盤の6分野について、AWSとAzureの課金体系の違い、コスト上昇ドライバーと一般的な対処法を出典付きで整理する。製品レイヤーでの技術的な効率化(本章)と、契約レイヤーでの交渉(第10章)は別トラックとして管理し、製品レイヤーの最適化を先に進めてコスト実績を下げ、そのデータを契約レイヤーの交渉に持ち込むという順序が、「基準点を最適化後の水準にする」という原則と直結する。

## 分野別比較

### 仮想マシン(IaaS)：EC2 / Virtual Machines

**課金体系の違い**：両者とも秒/分単位の従量課金が基本。コミット割引はAWSがReserved Instances(特定インスタンスタイプ・リージョン固定、最大約72%引)またはSavings Plans($/時間コミット、ファミリー横断で柔軟、最大約66%引)の二層。Azureも同様にReserved VM Instances(最大約72%引)とAzure Savings Plan for Compute(最大約65%引)の二層構造。固定型予約が優先適用される点も共通。Azure固有の要素として、既存のWindows Server/SQL ServerライセンスをAzure Hybrid Benefitで持ち込める。

**コスト上昇ドライバーと一般的な対処法**：「動かしっぱなし」の開発・検証環境、実負荷に対するオーバープロビジョニング、新世代の低コストインスタンスへの移行が進まないこと、コミット購入後のアーキテクチャ変更でRI/Reservationが空振りになることが主因。対処法は使用率モニタリングに基づく継続的ライトサイジング、開発環境の自動停止スケジューリング、世代交代の定例棚卸し、コミット購入前の利用実績精査。(出典[1][2])

### サーバーレス実行：Lambda / Azure Functions

**課金体系の違い**：両者ともリクエスト数×実行時間×メモリ割当(GB秒)の従量課金。常時稼働の予測可能な負荷にはAWSがProvisioned Concurrency(時間課金)、AzureがPremiumプラン(vCPU/メモリの時間課金)を用意。

**コスト上昇ドライバーと一般的な対処法**：実処理に対して過大なメモリ割当を設定したままにする、コールドスタート対策として不必要に予約容量を常時稼働させる、関数間の不要な連鎖呼び出しでリクエスト数が水増しされることが主因。対処法はメモリ/CPU設定のプロファイリングに基づく最適化、負荷パターンに応じたプランの使い分け、関数設計の定期レビュー。(出典[3])

### コンテナ：ECS/EKS + Fargate / AKS + Container Apps/Container Instances

**課金体系の違い**：Fargate/Container Appsは秒単位のvCPU・メモリ課金でほぼ同型。マネージドKubernetesの管理費はEKSがクラスタごとの時間課金(約$0.10/時間)、AKSは無料枠(Free tier)では管理費なし、SLA保証付きStandard/Premium tierのみ課金という違いがある。

**コスト上昇ドライバーと一般的な対処法**：部門ごとの小規模クラスタ乱立による管理オーバーヘッドの重複、ノードのオーバープロビジョニング、開発環境まで本番同等のSLA階層で運用してしまうことが主因。対処法はクラスタ統合・マルチテナント化、オートスケーリングの徹底、環境別のSLA階層使い分け。(出典[4])

### リレーショナルDB(SQL Server)：RDS for SQL Server(License Included/2026年6月開始のBYOM) / Azure SQL Database・Azure SQL Managed Instance

**課金体系の違い**：Enterprise Edition利用時、Azure Hybrid BenefitはvCore:物理コアが4:1換算になるのに対し、AWS側(RDS BYOM/EC2上のSQL Server)は1:1換算。同じライセンス資産でも高集約構成ではAzureの方がライセンス効率が良い。Azure SQL Databaseにはサーバーレス階層(自動一時停止・スケール)があるが、RDS for SQL Serverには同等の選択肢がない。

**コスト上昇ドライバーと一般的な対処法**：ライセンス込み課金のまま放置しBYOL/BYOM/Hybrid Benefitへの移行が進まないこと、実際には不要な機能のためにEnterprise Editionを使い続けること、ストレージ/IOPSのオーバープロビジョニングが主因。対処法はライセンス持ち込み適用状況の定期監査、Standard Edition適用可否の見直し、ストレージ階層の最適化。(出典[5][6])

### オブジェクトストレージ：S3 / Blob Storage

**課金体系の違い**：GB月あたりの保管料+リクエスト課金+アクセス階層(Hot/Cool/Archive相当)という同型構造。ライフサイクルポリシーによる自動階層移行も両方に存在。

**コスト上昇ドライバーと一般的な対処法**：古いデータがHot階層に残り続けること(ライフサイクル未設定)、重複データ・不要スナップショットの放置、小さいオブジェクトへの頻繁アクセスによるリクエスト課金の増大が主因。対処法はライフサイクルポリシーの自動化、定期的なストレージ棚卸し、アクセスパターンに応じた階層再設計。(出典[7])

### 生成AI基盤：Bedrock / Azure OpenAI Service

**課金体系の違い**：両者ともトークン単位(入力/出力別課金)の従量課金が基本。予約容量課金はAWSがBedrock Provisioned Throughput(時間課金、最短1か月コミット)、AzureがPTU(時間課金、1年/3年予約で追加割引)。いずれも稼働率が下がっても契約時間分は全額課金され、減額保護はない。Azure OpenAIは表面のトークン単価がOpenAI直販とほぼ同額でも、サポート按分・ネットワーク/egress・コンテンツフィルタリング・ファインチューニングホスティング等が積み上がり実効コストが15〜40%程度上振れするケースが指摘されている。

**コスト上昇ドライバーと一般的な対処法**：全用途に高性能・高単価モデルを一律適用すること、PoC用途がコスト管理対象外のまま本番へ横滑りすること、プロンプト設計の非効率による入力トークンの肥大化、予約容量の稼働率不足が主因。対処法はタスク複雑度に応じたモデルルーティング、部門・プロジェクト別の利用量可視化とチャージバック、プロンプト最適化、予約容量導入前のPoCフェーズでの需要検証。(出典[8])

## 出典

[1] Amazon Web Services, "Reserved Instances for Amazon EC2 overview", AWS Documentation. https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html

[2] Usage.ai, "Azure Savings Plan vs Reserved Instances | Which Discount Gets You More in 2026". https://www.usage.ai/blogs/azure/compare/reservations-vs-savings-plans/

[3] ReliaSoftware, "AWS Lambda vs Azure Functions: Pricing, Performance & Use Cases". https://reliasoftware.com/blog/aws-lambda-vs-azure-functions-comparison

[4] Microsoft Learn, "Azure Kubernetes Service (AKS) Free, Standard, and Premium Pricing Tiers". https://learn.microsoft.com/en-us/azure/aks/free-standard-pricing-tiers

[5] Medium (Matias Coca), "What BYOM for RDS SQL Server Really Changes (And Doesn't)", 2026年6月. https://medium.com/@cocamatias/what-byom-for-rds-sql-server-really-changes-and-doesnt-f25267206dfd

[6] Amazon Web Services, "Amazon RDS for SQL Server supports Bring Your Own Media", 2026年6月2日. https://aws.amazon.com/about-aws/whats-new/2026/06/rds-sqlserver-supports-bring-your-own-media/

[7] Shoviv, "AWS S3 vs Azure Blob Storage: Cost & Performance [2026]". https://www.shoviv.com/blog/aws-s3-vs-azure-blob-storage/

[8] Usage.ai, "Are You Overpaying for AWS Bedrock, Vertex AI, or Azure AI?". https://www.usage.ai/blogs/finops/ai-ml-cost/aws-bedrock-vs-vertex-ai-vs-azure-openai/

## この章の結論

- 仮想マシン・サーバーレス・コンテナ・オブジェクトストレージは、AWSとAzureで課金体系がほぼ同型であり、対処法(ライトサイジング、ライフサイクル管理、オートスケーリング等)も共通する。
- SQL Serverのライセンス換算比率(Azure 4:1 vs AWS 1:1)のように、分野によっては構造的にどちらかのクラウドが有利になるケースがある。
- 生成AI基盤(Bedrock/Azure OpenAI)は実効コストが表面単価より15〜40％上振れし得るため、モデルルーティングや利用量の可視化など、他分野以上に運用面での管理が重要になる。
- 製品レイヤーの最適化(本章)を先に進め、そのコスト実績を契約レイヤーの交渉(第10章)に持ち込む順序が、基準点を最適化後の水準にするという原則と直結する。

---

**参照**：第10章(契約レイヤーの比較)、第3.2章(AWSコミット契約とアーキテクチャ凍結)
