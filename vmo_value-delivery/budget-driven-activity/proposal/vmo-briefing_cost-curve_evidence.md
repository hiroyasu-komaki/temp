# 区分ごとのコスト曲線（典型モデル）の裏付け

対象：`vmo-briefing.pptx` 12〜17枚目の上段グラフ。グラフはすべて模式図（数値なし）。

強さの目安：**強い**＝学術・定番モデル／公式の事実、**中**＝業界の調査・実例、**弱**＝実務家の観察のみ。

| モデル | 裏付け | 強さ | 補足 |
|---|---|---|---|
| 運用保守のバスタブ曲線（作業量） | 信頼性工学のバスタブ曲線（初期故障期・偶発故障期・摩耗故障期）。ソフトウェアは摩耗しないが、変更のたびに故障率が上がり劣化する（Pressmanの理想曲線と実際の曲線）。Lehmanのソフトウェア進化の法則（継続的変更・複雑さの増大） | 強い | 「契約は体制のまま固定」は当社の実情にもとづく観察 |
| 運用保守の判断できる力が閾値を割る（ブラックボックス化） | Williamsonの「根本的な転換」：契約前は多数の売り手から選べるが、特定の売り手に固有の投資をした後は乗り換えにコストがかかり、少数の交渉に変わる。組織の忘却：生産を通じて得た知識は急速に価値を失う（Argote, Beckman & Epple, 1990）。Feeny & Willcocksの9つのコアIS能力（賢い発注・契約の監視など）。英国HSEのIntelligent Customer Capability：委託する製品・サービスを明確に理解する能力と、組織の記憶を残す必要 | 強い（考え方） | 閾値の位置を数値で示した研究はない。概念上の線として扱う。閾値を割るのはバスタブ曲線の底（安定期）と重なる、というのは当社向けの解釈 |
| 開発の案件ごとの山 | Putnam-Norden-Rayleigh曲線：プロジェクトの要員・工数は立ち上がって山を作り、収束する | 強い | 「山が年々高くなる（単価の上昇）」は国内の公的データ未確認。JUAS・IPAの調査で要追加調査 |
| 保守の中の改修が、次の開発を高くする | ISO/IEC 14764は保守を是正・適応・完全化（機能追加や性能改善）・予防の4つに分け、機能追加は欠陥の是正と区別される。Parnasの「Software Aging」（1994）：元の設計を理解していない人による変更は、ほぼ必ずプログラムの構造を劣化させ、やがて誰も製品を理解できなくなる。技術的負債（Cunningham, 1992）：内部品質の劣化は、将来の変更に余分な工数（利子）を生む | 強い（考え方） | 「保守で改修できるのは手が空いている兆候」「元の開発ベンダーが現状分析・影響分析を高く積む」は当社の実情にもとづく観察 |
| コモディティ（Microsoft）の階段状の値上げ | 2022年：E3を$32→$36、E5は導入を促すため$57に据え置き。2026年7月：E3 $36→$39、E5 $57→$60、F3 $8→$10（AI機能の追加などが理由） | 強い | 「利用者数が収束する」は it-cost-reduction 第3.1章で置いた仮定 |
| 専用品の横ばいと急な跳ね上がり | SaaSの価格上昇は2023年に8.7%で米国CPI（3.2%）の2倍超。約4分の3のベンダーが値上げし、バンドル等の実質値上げも進んだ（Vertice）。Broadcomによる買収後のVMwareは、サブスクリプション化とバンドル化で更新時に100〜800%の値上げもあり得る（IDC。VMwareは当社の区分ではミドルウェアに含める） | 中 | 「同じ金額で更新が続く」は当社の実情にもとづく観察 |
| ミドルウェア（サーバーに紐づくもの）の保守料が残る | Oracleの保守料はライセンス価格の約22%／年で、年3〜5%上がることが多い。同じ製品の中で一部のライセンスだけ保守を外すことは認められない。2023年1月、Oracle Javaが従業員数ベースの課金（Java SE Universal Subscription）に変更 | 中〜強 | 保守料の出典はライセンス助言会社で、Oracleの公式文書ではない |
| ミドルウェア連携系：SaaSを入れるたびに積み上がる | 1対1（フルメッシュ）の連携は、システム数に対して2乗で接続が増える。ブローカー（ハブ）型なら、各アプリケーションに必要な接続は1本で済む（Enterprise application integration）。GxPの検証は、リスクに応じて重さを変える方向に進んでいる：GAMP 5 第2版（ISPE、2022年）、FDAのComputer Software Assurance最終ガイダンス（2025年9月23日、対象は医療機器の製造・品質システム用ソフトウェア） | 中〜強 | 「SaaS導入のたびに連携とブリッジが必要で、GxPのDIで金額を落とせない」は当社の仮説。CSAは医薬品GMPにそのまま当てはまるものではない |
| オンプレのEOL後の跳ね上がり | サーバーの運用コストは3年目以降に大きく上がり、4〜6年目の累計は購入額の10倍に達し得る（IDCの調査をDellが引用） | 中 | 販売側の引用で、元の調査名は不明 |
| オンプレ：OSの延長サポートは期限付きの階段 | Windows 10の法人向けESUは1台61ドルから毎年倍になり、最長3年。Windows Server 2012のESUも3年が上限。期限後は延命の手段がなく、移行しか残らない | 強い（公式の価格・期間） | ファームウェア・BIOSの更新は多くがハードウェア保守に含まれ、保守切れはコストではなくリスク（更新停止）として現れる |
| オンプレ：機器の第三者保守 | 第三者保守はメーカー保守より50〜70%安くなり得る（Gartnerの数字を第三者保守会社のスポンサー記事が引用）。EOL発表から2〜3年たつと切り替えの経済性が高まる | 中 | 販売側の引用。サブスクリプションやOEM限定のソフト更新に依存する機器はメーカー保守に残すべきとされる |
| オンプレ：延命（役割が細っても費用は元のまま） | 調査したサーバーの約30%が6か月以上処理をしていない「昏睡状態」だった（Koomey & Anthesis Group, 2015）。GartnerのTIMEモデルはアプリケーションをTolerate・Invest・Migrate・Eliminateに分けて扱う | 中 | 費用と役割のずれを曲線で示した研究はなく、模式図として扱う。ラック・電力・回線が台数減に追随しないのは当社の観察 |
| 開発：ウォーターフォールのフェーズ契約と、本番稼働後の改修の継続 | 未調査（フェーズごとに契約を分ける進め方と、稼働後に改修案件が続くことは当社の実情にもとづく想定） | 弱 | 変更要求の件数を先行指標とするのも当社の想定 |
| 開発：アジャイルは体制×期間でコストがほぼ一定 | 未調査（固定メンバーが学習しながら短い周期で成果を出す、というアジャイルの前提にもとづく） | 弱 | メンバーの入れ替え・作業の定型化をシグナルとするのは当社の考え |
| オンプレ：買い替えと延命の対比 | 上のESU・第三者保守・延命の行を組み合わせたもの | 中 | 保守期限を境に一気に上がる形は、ESUの価格（初年度から毎年倍）にもとづく |
| オンプレ：故障率（買い替えは低く一定、延命は買い替え時期を境に一段上がり、その後も上がる） | IDC：x86サーバーは稼働3〜3.5年で可用性・信頼性が大きく下がり、約3.2年での更新が適当。推奨時期に更新しないサーバーの故障率は85%上がる（TechRadarがIDCのホワイトペーパーを引用）。Backblazeの2013年データ：ディスクの年間故障率は0〜18か月で5.1%、18か月〜3年で1.4%、3〜4年で11.8%。2021年データでは初期故障がほぼなく、ホッケースティック型。Schroeder & Gibson（FAST 2007）：交換率は年数とともに一貫して増え、摩耗は想定より早く始まる。Pinheiroら（Google、FAST 2007）：年間故障率は1年目1.7%から3年目で8.6%超（機種構成の影響あり） | 中〜強 | 「高止まり」を裏付けるデータは見つからない（6年を超えるデータは少ない）。グラフは上がり続ける形にした。IDCの数字は二次引用 |
| オンプレ：保証期間（3年前後）は保守費が低く、保証切れで有償保守に移ると一段上がる。買い替えは業務アプリケーションのライフサイクルに合わせ5年以上 | 一般的な製品保証の慣行。買い替え周期5年以上は当社の実情（業務アプリケーションのライフサイクル）にもとづく。IDCは約3.2年での更新を推奨しているが、当社ではそれより長く使う前提。第三者保守はメーカー保守より50〜70%安くなり得る（上の第三者保守の行） | 中 | 保証年数は機種・契約による。段差の大きさは模式 |
| 地域限定のクラウド（国内・EUなど）：確保した分と上乗せで払い、グローバル契約と別建てになる | AWS European Sovereign Cloudは2026年1月に一般提供開始。他リージョンと物理的・論理的に分離し、EU居住者が運用、請求も別（Amazon）。料金はフランクフルト比で約15%高いという試算（tecRacer分析、Qovery引用）。Bleu・S3NSは個別見積で最低利用額を求められることが多い（Qovery）。さくらのクラウドは2026年3月にガバメントクラウドに正式採択（国産初） | 中 | 「確保した分で払い、減らさない」は当社の想定 |
| 大手クラウドの下がらないコミット額（AWSのPPA、AzureのMACC） | コミット未達分は現金で支払う。上位の割引段階を狙ったコミットで10〜25%が未使用に残った例がある。ベンダーは将来の伸びを取り込もうとする | 弱〜中 | EDPの条件は非公開。「更新のたびに前回を上回る」を直接裏付ける資料は未確認 |

## 扱いの方針（案）

- 「強い」ものは典型モデルとして言い切る。「中」「弱」は「当社ではこう見えている」「業界でこういう例がある」と、観察・実例として話す。
- 開発の単価上昇とAWSの更新時の上積みは、主張を弱めた（14枚目「案件ごとに山ができ、決め方がばらつく」、17枚目「コミット額は下げにくい」）。根拠が見つかれば戻す。
- 出典はスライドに載せず、本ファイルを手元の根拠一覧として使う。

## 出典

- Infraspeak, What is the Bathtub Curve — https://infraspeak.com/en/blog/bathtub-curve
- Tractian, Bathtub Curve — https://tractian.com/en/glossary/bathtub-curve
- GeeksforGeeks, Failure Curve for Software in Software Engineering — https://www.geeksforgeeks.org/?p=969080
- Lehman's Laws of Software Evolution — https://lawsofsoftwareengineering.com/laws/lehmans-laws/
- Harvey Mudd College, Putnam, Norden, Rayleigh Curves — https://cs.hmc.edu/~markk/cs121.f07/supp/pnr.html
- JMU, The Maintenance of Software Products（ISO/IEC 14764の保守区分） — https://users.cs.jmu.edu/bernstdh/web/common/lectures/summary_maintenance.php
- the morning paper, Software Aging（Parnas, 1994の解説） — https://blog.acolyer.org/2014/10/14/software-aging/
- Martin Fowler, Technical Debt — https://martinfowler.com/bliki/TechnicalDebt.html
- Wikipedia, Enterprise application integration — https://en.wikipedia.org/wiki/Enterprise_application_integration
- QbD Group, Second edition of GAMP 5 — https://qbdgroup.com/en/?p=72076
- RQA, FDA issues final guidance on Computer Software Assurance（2025） — https://www.therqa.com/news/fda-issues-final-guidance-computer-software-assura/
- PC Gamer, Windows 10 ESU: $61, then double every year for up to three years — https://www.pcgamer.com/software/windows/to-stay-safe-in-windows-10-from-next-october-youll-have-to-pay-dollar61-then-double-every-consecutive-year-for-a-maximum-of-three-years
- Microsoft Learn, Windows 10 Extended Security Updates — https://learn.microsoft.com/en-gb/windows/whats-new/extended-security-updates
- Microsoft Q&A, Windows Server 2012 ESU pricing — https://learn.microsoft.com/en-us/answers/questions/1315098/about-the-price-of-windows-2012-and-windows-2012-r
- Data Center Knowledge, Exploring alternatives to OEM maintenance（Gartner引用、スポンサー記事） — https://www.datacenterknowledge.com/networking/exploring-alternatives-to-oem-maintenance-for-your-networking-hardware
- Stanford Law School, 30% of servers are sitting comatose（2015） — https://law.stanford.edu/press/30-of-servers-are-sitting-comatose-according-to-research/
- LeanIX, Gartner TIME model — https://www.leanix.net/en/wiki/ea/gartner-time-model
- Directions on Microsoft, Office suite price increases starting July 2026 — https://www.directionsonmicrosoft.com/microsoft-to-increase-office-suite-prices-across-the-board-starting-july-2026/
- CIO Dive, Stubbornly high SaaS prices outpace CPI inflation（Vertice SaaS Inflation Index, 2023） — https://www.ciodive.com/news/stubbornly-high-saas-prices-outpace-cpi-inflation/699807/
- IDC, VMware cost increases: how Broadcom VMware product offerings are evolving（2024） — https://idc.com/resource-center/blog/vmware-cost-increases-how-broadcom-vmware-product-offerings-are-evolving
- Oracle Licensing Experts, How Oracle support contracts relate to your licenses — https://oraclelicensingexperts.com/how-oracle-support-contracts-relate-to-your-licenses
- InfoWorld, Oracle per-employee Java pricing causes concern（2023） — https://www.infoworld.com/article/3686611/oracle-per-employee-java-pricing-causes-concern.html
- Dell, Refreshed servers can refresh profitability（IDC引用） — https://www.dell.com/en-us/blog/refreshed-servers-can-refresh-profitability-while-boosting-speed-innovation-and-agility/
- Redress Compliance, AWS EDP renewal negotiation strategy — https://redresscompliance.com/aws-edp-renewal-negotiation-strategy
- Cloud Commitment Advisory, AWS EDP for high-growth vs flat workloads — https://cloudcommitmentadvisory.pages.dev/aws-edp/aws-edp-for-high-growth-vs-flat-workloads/
- Aalto University, Fundamental transformation — https://mycourses.aalto.fi/mod/glossary/showentry.php?eid=2178
- Argote, Beckman & Epple (1990), The Persistence and Transfer of Learning in Industrial Settings, Management Science 36(2) — https://econpapers.repec.org/RePEc:inm:ormnsc:v:36:y:1990:i:2:p:140-154
- Willcocks, Reynolds & Feeny, Evolving IS Capabilities to Leverage the External IT Services Market, MIS Quarterly Executive 6(3) — https://aisel.aisnet.org/misqe/vol6/iss3/3
- HSE, Intelligent customer capability — https://www.hse.gov.uk/Humanfactors/topics/customers.htm
- TechTarget, Data gravity — https://whatis.techtarget.com/definition/data-gravity
- Computer Weekly, Data gravity: what is it and how to manage it — https://www.computerweekly.com/feature/Data-gravity-What-is-it-and-how-to-manage-it
- TechRadar, Understanding a server replacement cycle（IDC引用） — https://www.techradar.com/news/world-of-tech/roundup/understanding-a-server-replacement-cycle-1128842
- Backblaze, Drive Failure Over Time: The Bathtub Curve Is Leaking — https://www.backblaze.com/blog/drive-failure-over-time-the-bathtub-curve-is-leaking/
- Schroeder & Gibson, Disk failures in the real world（FAST 2007） — https://www.usenix.org/conference/fast-07/disk-failures-real-world-what-does-mttf-1000000-hours-mean-you
- Pinheiro, Weber & Barroso, Failure Trends in a Large Disk Drive Population（FAST 2007） — https://static.usenix.org/events/fast07/tech/full_papers/pinheiro/pinheiro_html/index.html
- Amazon, AWS launches AWS European Sovereign Cloud（2026年1月） — https://press.aboutamazon.com/aws/2026/1/aws-launches-aws-european-sovereign-cloud-and-announces-expansion-across-europe
- Qovery, Sovereign cloud pricing: AWS, Bleu, S3NS, STACKIT vs standard regions — https://www.qovery.com/blog/sovereign-cloud-pricing-aws-bleu-s3ns-stackit-vs-standard-regions
- 電波新聞デジタル, ガバメントクラウドに初の国産事業者、さくらインターネットが採択（2026年3月28日） — https://dempa-digital.com/?p=711792
