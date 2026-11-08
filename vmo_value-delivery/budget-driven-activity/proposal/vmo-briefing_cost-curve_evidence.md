# 区分ごとのコスト曲線（典型モデル）の裏付け

対象：`vmo-briefing_v2.pptx` 16〜21枚目（区分ごとのスライド）の典型的なシナリオのグラフ。グラフはすべて模式図（数値なし）。

強さの目安：**強い**＝学術・定番モデル／公式の事実、**中**＝業界の調査・実例、**弱**＝実務家の観察のみ。

| モデル | 裏付け | 強さ | 補足 |
|---|---|---|---|
| 運用保守（運用コスト）：稼働直後 → 安定期 → 終盤。シグナル：1 作業量が稼働直後から下がりきる → 2 ベンダーから複数年契約の提案が来る → 3 月次報告が定型化し、稼働率が一定 | 稼働直後の支援（ITILのEarly Life Support）は、移行と運用が重なる期間で、終了は時間・サービスオーナーの確認・合意などの出口基準で決める（Advisera）。試験対策資料では、インシデントの頻度と重大度が基準値まで下がり、SLAを安定して満たし、運用が開発者の助けなしに回ることを基準に挙げている（OpenExamPrep。ITIL公式文書ではない）。ソフトウェア業は多重下請構造のサプライチェーンで、買いたたきや仕様変更への無償対応の要求が懸念されている（公正取引委員会、2022年6月）。仕事は、完了までに使える時間を満たすまで膨張する（パーキンソンの法則。The Economist、1955年） | 中 | 「保守運用の契約は、下請けとの関係から自動更新つきの単年契約が実態」「ベンダーからの複数年契約の提案はシグナル」「稼働が余っても報告に出さず、品質改善の名目で文書化・リファクタリング・ベンダー社内の勉強会に充てることがある（ベンダーの要員入れ替えの準備）」「安定期の見直しが、終盤の廃止・移行のコスト管理の準備になる」は当社の実情にもとづく観察 |
| 運用保守のバスタブ曲線（作業量） | 信頼性工学のバスタブ曲線（初期故障期・偶発故障期・摩耗故障期）。ソフトウェアは摩耗しないが、変更のたびに故障率が上がり劣化する（Pressmanの理想曲線と実際の曲線）。Lehmanのソフトウェア進化の法則（継続的変更・複雑さの増大） | 強い | 「契約は体制のまま固定」は当社の実情にもとづく観察 |
| 運用保守の判断できる力が閾値を割る（ブラックボックス化） | Williamsonの「根本的な転換」：契約前は多数の売り手から選べるが、特定の売り手に固有の投資をした後は乗り換えにコストがかかり、少数の交渉に変わる。組織の忘却：生産を通じて得た知識は急速に価値を失う（Argote, Beckman & Epple, 1990）。Feeny & Willcocksの9つのコアIS能力（賢い発注・契約の監視など）。英国HSEのIntelligent Customer Capability：委託する製品・サービスを明確に理解する能力と、組織の記憶を残す必要 | 強い（考え方） | 閾値の位置を数値で示した研究はない。概念上の線として扱う。閾値を割るのはバスタブ曲線の底（安定期）と重なる、というのは当社向けの解釈 |
| 開発・改修（既存システムの追加改修）：開発体制 → 運用体制への移行期 → 運用体制。指標は要件と重要課題（二次開発以降の要件と、問題管理で積まれている重要課題）。シグナル：1 チケットの対応者が変わり、対応が定型化する → 2 要件と重要課題が天井を打つ → 3 エスカレーションが増え、応答時間が変わる | ソフトウェア業は多重下請構造のサプライチェーンで、買いたたきや仕様変更への無償対応の要求が懸念されている（公正取引委員会、2022年6月） | 弱〜中 | 「ベンダーは運用フェーズ以降の体制縮小を急ぐ（社内の組織が分かれている、開発メンバーはSESでも高単価）」「保守専用の下請けに移して単価差の利鞘を稼ぐビジネスモデルで、最初の打ち手が固定定額契約。その中で保守ベンダーのSEへ知識・技術を移す」「体制の切り替えを透明にすることはコスト構造を明かすことと同じで、通常は難しい。そのため切り替えの前に出るシグナルで見極める」「運用体制への移行期は早い時期に始まる。要件の天井で判断されるのは開発メンバーの離脱の時期」「開発メンバーは運用の教育を受けておらずチケット対応が独自色を帯び、運用体制では定型文に変わる」「開発メンバーの離脱で、内部で解決していた事案がエスカレーションとして表に出る」は当社の実情にもとづく観察 |
| 開発・改修（新規システム開発）：提案（RFP）→ 要件定義 → 設計・開発、本番稼働 → 二次開発（要件定義・設計開発をひとまわり小さく繰り返す）。要件は要件定義の初期に提案時より膨らみ、中盤以降の期待値調整で当初の予算範囲に収まる。調整で外れた要件のうちRFPの目的に強く関わるものが二次開発の候補になる。シグナル：1 要件定義の初期に、要件が提案時より膨れ上がる → 2 見積の解像度が低い → 3 開発の中盤以降に二次開発の打診が来る → 4 二次開発の前に、開発体制の固定契約を打診される（保守契約とは別に、または保守契約の改訂として）。先行指標は要件の充足度を管理できているか | 見積の幅は、構想の段階では実際の0.25〜4倍までぶれ、変動要因を取り除く決定をした分だけ狭まる。要件が後から変われば再び広がる（Cone of Uncertainty。Construx／McConnell）。効果の責任者（benefits owner）は効果の管理を見渡す役割だが、それだけでは効果の管理は回らない（PMI） | 中 | 「ベンダーは自社のやり方に最適化しており、提案書の内容が要件定義でゼロベースになることがある」「ベンダーは重要案件が続くことを示して、体制の固定契約を打診してくる。打診は受け入れられないのが普通で、ベンダーも織り込み済み。その後の追加改修を固定契約で結ぶための布石であることがほとんど」「二次開発の打診は本番稼働前（開発の中盤以降）に来て、その中身は本来一次のスコープ」「追加予算には一次開発の効果を示す必要があるが、ビジネスオーナーが効果を管理していないことが多い」は当社の実情にもとづく観察 |
| 開発の案件ごとの山 | Putnam-Norden-Rayleigh曲線：プロジェクトの要員・工数は立ち上がって山を作り、収束する | 強い | 「山が年々高くなる（単価の上昇）」は国内の公的データ未確認。JUAS・IPAの調査で要追加調査 |
| 保守の中の改修が、次の開発を高くする | ISO/IEC 14764は保守を是正・適応・完全化（機能追加や性能改善）・予防の4つに分け、機能追加は欠陥の是正と区別される。Parnasの「Software Aging」（1994）：元の設計を理解していない人による変更は、ほぼ必ずプログラムの構造を劣化させ、やがて誰も製品を理解できなくなる。技術的負債（Cunningham, 1992）：内部品質の劣化は、将来の変更に余分な工数（利子）を生む | 強い（考え方） | 「保守で改修できるのは手が空いている兆候」「元の開発ベンダーが現状分析・影響分析を高く積む」は当社の実情にもとづく観察 |
| ライセンス（全社で使うもの）の横軸：評価 → パイロット → 長期契約1回目（3年。単価を固定し、最低数量をコミット）→ 2回目 → 3回目 | MicrosoftのFastTrackは導入をEnvision・Onboard・Drive Valueの3段階で示し、Microsoft Learnはパイロットの結果で全体展開の可否を判断するとしている。Enterprise Agreementは、500ユーザー／デバイス以上の組織が最低3年をコミットする契約で、3年先までコストを見通せる。追加分は年1回のTrue-upで、事前に合意した条件と価格で精算する。3年ごとに更新する。サブスクリプション型の契約では、数量の増減は年1回に限られる | 強い（公式文書） | 長期契約の期間中は、コミットした数量と単価が支払いの下限になる。そのため期間中に数量を最適化しても支払いは下がらない、という描き方は当てはめ |
| ライセンス（全社で使うもの）のシグナル（いずれも利用者数の側）：1 利用者数が天井を打つ（1回目の期間中のどこでも起こり得る）→ 利用状況を確かめて数量を最適化する → 2 1回目の3年目ごろ、更新の前に値上げが発表される → 3 2回目の契約で、法人契約のメリットを受けられなくなる → 4 2回目の期中に、製品の体系が一新される | 展開後の成否は利用と満足度で決まる（FastTrack、Drive Value）。使われていないライセンスへの支出は1社あたり年平均2,100万ドル、前年比14.2%増（Zylo、2025）。SaaS支出の33%が無駄になっている（Flexera、2022）。値上げは施行の前に発表される：Microsoftは2025年12月4日に、2026年7月1日からのMicrosoft 365／Office 365の値上げを発表した。法人契約のメリットの縮小：Microsoftは2025年11月から、EAのオンライン サービスの数量割引（約6〜12%）をやめ、レベルAの価格にそろえた（Directions on Microsoft）。製品体系の一新：Microsoftは2024年4月1日、TeamsなしのMicrosoft 365／Office 365を全世界で提供すると発表し、Teamsを含まない12のSKUを新設した。Teamsが必要な新規顧客は、別にTeams Enterpriseを買う（Directions on Microsoft）。切り替えコストのある市場では、売り手は顧客を囲い込んだ後に価格を上げて回収する（bargains-then-ripoffs。Farrell & Klemperer） | 中〜強 | 「製品体系が一新されると、利用状況の調べ直しと次の契約の最低条件探しに追われ、交渉の準備が進まない」は、上の実例を当てはめたもの |
| ライセンス（全社で使うもの：Microsoft 365）の階段状の値上げ | 2022年：E3を$32→$36、E5は導入を促すため$57に据え置き。2026年7月：E3 $36→$39、E5 $57→$60、F3 $8→$10（AI機能の追加などが理由） | 強い | 「利用者数が収束する」は it-cost-reduction 第3.1章で置いた仮定 |
| ライセンス（特定の業務で使うもの）：個人で使う → チームで使う → 部門をまたいで使う。シグナル：1 業務に組み込まれる → 2 管理が煩雑で、IT部門・ヘルプデスクの支援が不十分 → 3 監査対応など付随業務が重い。コストはチームで使う途中まで利用に一致し、2でベンダーと保守契約を結ぶと大きく上がり、3で部門をまたぐとプロフェッショナルサービスやオンサイトサポートが加わってさらに上がる。コストが利用を下回ることはない | 製品主導で広がるソフトウェアは、個人の無料・試用から始まり、組織の中で利用者がまとまると全社契約に進む。企業は管理機能やセキュリティの統制を求め、ベンダーはその機能に課金の関門を置く（Bessemer Venture Partners）。SSOなどを上位プランに置くことで、価格が3〜10倍以上になる例がある（例：Airtableは1ユーザー月10ドルが、SSO付きで60ドル。sso.tax）。従業員の41%がIT部門の外で技術を扱う「ビジネス テクノロジスト」である（Gartner、2022）。GxPに関わるコンピュータ化システムは、バリデーション、監査証跡、アクセス制御、委託先との正式な取決めが求められ、その程度はリスクに応じて決める（EU GMP Annex 11） | 中〜強 | 「IT部門の支援やヘルプデスクを使いにくく、ベンダーのプロフェッショナルサービス・オンサイトサービスを足してしまう」「導入当初と便利さは変わらないのに、手間とコストが重くなる」は当社の実情にもとづく観察 |
| （参考）専用品の横ばいと急な跳ね上がり | SaaSの価格上昇は2023年に8.7%で米国CPI（3.2%）の2倍超。約4分の3のベンダーが値上げし、バンドル等の実質値上げも進んだ（Vertice）。Broadcomによる買収後のVMwareは、サブスクリプション化とバンドル化で更新時に100〜800%の値上げもあり得る（IDC。VMwareは当社の区分ではミドルウェアに含める） | 中 | 「同じ金額で更新が続く」は当社の実情にもとづく観察 |
| ミドルウェアの定義と2つの区分：ミドルウェアはOSとアプリケーションの間に位置し、アプリケーションが共通に使う機能を提供するソフトウェア。サーバーに紐づくミドルウェア（DB・アプリケーションサーバー・運用管理。課金は台数・コア数に紐づく）と、連携のミドルウェア（システム間のデータ連携。コストは連携の本数に紐づく）に分ける。シグナル（左）：1 統合・移行で配備数が減る → 2 配備数が減っても保守料が変わらない → 3 ベンダーが課金体系の変更を発表する。シグナル（右）：1 SaaSの導入のたびに連携を個別に作る → 2 連携の本数がシステム数より速く増える → 3 GxPに関わり、連携ごとにDI検証が乗る | ミドルウェアは「アプリケーションとOSの間を橋渡しするソフトウェア」で、ソフトウェアの階層の中でOSとその上で動くアプリケーションの間に位置することからこう呼ばれる。種類にデータベース、アプリケーションサーバー、メッセージ指向、アプリケーション連携（EAI）がある（TechTarget）。保守料・課金体系の変更・連携の本数・DIの検証の根拠は以下の行 | 中〜強 | 「ネットワーク関連」ではなく「連携」と呼ぶのは、データ連携製品がネットワーク機器のソフトウェアと混同されないようにするため |
| ミドルウェア（サーバーに紐づくもの）の保守料が残る | Oracleの保守料はライセンス価格の約22%／年で、年3〜5%上がることが多い。同じ製品の中で一部のライセンスだけ保守を外すことは認められない。2023年1月、Oracle Javaが従業員数ベースの課金（Java SE Universal Subscription）に変更 | 中〜強 | 保守料の出典はライセンス助言会社で、Oracleの公式文書ではない |
| ミドルウェア連携系：SaaSを入れるたびに積み上がる | 1対1（フルメッシュ）の連携は、システム数に対して2乗で接続が増える。ブローカー（ハブ）型なら、各アプリケーションに必要な接続は1本で済む（Enterprise application integration）。GxPの検証は、リスクに応じて重さを変える方向に進んでいる：GAMP 5 第2版（ISPE、2022年）、FDAのComputer Software Assurance最終ガイダンス（2025年9月23日、対象は医療機器の製造・品質システム用ソフトウェア） | 中〜強 | 「SaaS導入のたびに連携とブリッジが必要で、GxPのDIで金額を落とせない」は当社の仮説。CSAは医薬品GMPにそのまま当てはまるものではない |
| オンプレ維持のシグナル（いずれも故障率の側）。買い替え：1 保証期限が近づく → 2 故障率が上がり始める（3年目以降）→ 3 買い替えの時期が決まる → 4 買い替えで台数が減る。延命：1 主な業務システムの更改が決まる → 2 メーカーがサポート終了（EOL）を発表する → 3 延命の間も故障率が上がり続ける | 保証期間・保守期限・故障率・ESU・第三者保守の根拠は、以下のオンプレの各行による | 中〜強 | 「買い替えか延命かは、保証切れとサポート終了の前にしか選べない」「機器台帳と保守契約・保守期限を突き合わせて判断する」は当社の考え方 |
| オンプレのEOL後の跳ね上がり | サーバーの運用コストは3年目以降に大きく上がり、4〜6年目の累計は購入額の10倍に達し得る（IDCの調査をDellが引用） | 中 | 販売側の引用で、元の調査名は不明 |
| オンプレ：OSの延長サポートは期限付きの階段 | Windows 10の法人向けESUは1台61ドルから毎年倍になり、最長3年。Windows Server 2012のESUも3年が上限。期限後は延命の手段がなく、移行しか残らない | 強い（公式の価格・期間） | ファームウェア・BIOSの更新は多くがハードウェア保守に含まれ、保守切れはコストではなくリスク（更新停止）として現れる |
| オンプレ：機器の第三者保守 | 第三者保守はメーカー保守より50〜70%安くなり得る（Gartnerの数字を第三者保守会社のスポンサー記事が引用）。EOL発表から2〜3年たつと切り替えの経済性が高まる | 中 | 販売側の引用。サブスクリプションやOEM限定のソフト更新に依存する機器はメーカー保守に残すべきとされる |
| オンプレ：延命（役割が細っても費用は元のまま） | 調査したサーバーの約30%が6か月以上処理をしていない「昏睡状態」だった（Koomey & Anthesis Group, 2015）。GartnerのTIMEモデルはアプリケーションをTolerate・Invest・Migrate・Eliminateに分けて扱う | 中 | 費用と役割のずれを曲線で示した研究はなく、模式図として扱う。ラック・電力・回線が台数減に追随しないのは当社の観察 |
| （参考）開発：ウォーターフォールのフェーズ契約と、本番稼働後の改修の継続 | 未調査（フェーズごとに契約を分ける進め方と、稼働後に改修案件が続くことは当社の実情にもとづく想定） | 弱 | 変更要求の件数を先行指標とするのも当社の想定 |
| （参考）開発：アジャイルは体制×期間でコストがほぼ一定 | 未調査（固定メンバーが学習しながら短い周期で成果を出す、というアジャイルの前提にもとづく） | 弱 | メンバーの入れ替え・作業の定型化をシグナルとするのは当社の考え |
| オンプレ：買い替えと延命の対比 | 上のESU・第三者保守・延命の行を組み合わせたもの | 中 | 保守期限を境に一気に上がる形は、ESUの価格（初年度から毎年倍）にもとづく |
| オンプレ：故障率（買い替えは低く一定、延命は買い替え時期を境に一段上がり、その後も上がる） | IDC：x86サーバーは稼働3〜3.5年で可用性・信頼性が大きく下がり、約3.2年での更新が適当。推奨時期に更新しないサーバーの故障率は85%上がる（TechRadarがIDCのホワイトペーパーを引用）。Backblazeの2013年データ：ディスクの年間故障率は0〜18か月で5.1%、18か月〜3年で1.4%、3〜4年で11.8%。2021年データでは初期故障がほぼなく、ホッケースティック型。Schroeder & Gibson（FAST 2007）：交換率は年数とともに一貫して増え、摩耗は想定より早く始まる。Pinheiroら（Google、FAST 2007）：年間故障率は1年目1.7%から3年目で8.6%超（機種構成の影響あり） | 中〜強 | 「高止まり」を裏付けるデータは見つからない（6年を超えるデータは少ない）。グラフは上がり続ける形にした。IDCの数字は二次引用 |
| オンプレ：保証期間（3年前後）は保守費が低く、保証切れで有償保守に移ると一段上がる。買い替えは業務アプリケーションのライフサイクルに合わせ5年以上 | 一般的な製品保証の慣行。買い替え周期5年以上は当社の実情（業務アプリケーションのライフサイクル）にもとづく。IDCは約3.2年での更新を推奨しているが、当社ではそれより長く使う前提。第三者保守はメーカー保守より50〜70%安くなり得る（上の第三者保守の行） | 中 | 保証年数は機種・契約による。段差の大きさは模式 |
| （参考）地域限定のクラウド（国内・EUなど）：確保した分と上乗せで払い、グローバル契約と別建てになる | AWS European Sovereign Cloudは2026年1月に一般提供開始。他リージョンと物理的・論理的に分離し、EU居住者が運用、請求も別（Amazon）。料金はフランクフルト比で約15%高いという試算（tecRacer分析、Qovery引用）。Bleu・S3NSは個別見積で最低利用額を求められることが多い（Qovery）。さくらのクラウドは2026年3月にガバメントクラウドに正式採択（国産初） | 中 | 「確保した分で払い、減らさない」は当社の想定 |
| クラウド①：更新前のコミット額の提案（AWSのPPA、AzureのMACC） | コミット未達分は現金で支払う。上位の割引段階を狙ったコミットで10〜25%が未使用に残った例がある。ベンダーは将来の伸びを取り込もうとする | 弱〜中 | EDPの条件は非公開。「更新のたびに前回を上回る」を直接裏付ける資料は未確認 |

## 扱いの方針（案）

- 「強い」ものは典型モデルとして言い切る。「中」「弱」は「当社ではこう見えている」「業界でこういう例がある」と、観察・実例として話す。
- 開発の単価上昇とAWSの更新時の上積みは、主張を弱めた（開発の単価上昇は18枚目「開発・改修」で扱わない。AWSの更新時の上積みは21枚目「クラウド」で言い切らず、①のシグナル「更新前に、コミット額の提案が来る」にとどめた）。根拠が見つかれば戻す。
- 「参考」の行は、v2で使わなくなったシナリオの根拠である。シナリオを戻すときのために残す。
- 出典はスライドに載せず、本ファイルを手元の根拠一覧として使う。

## 出典

- TechTarget, What is middleware? — https://www.techtarget.com/it-infrastructure/definition/middleware

- Construx, The Cone of Uncertainty — https://www.construx.com/wp-content/uploads/2019/02/CxWhitePaper_ConeOfUncertainty.pdf
- PMI, Establishing Benefits Ownership and Accountability — https://www.pmi.org/learning/thought-leadership/series/benefits-realization/establishing-benefits-realization-ownership-accountability

- Advisera, Early Life Support – Live environment introduction made easy — https://advisera.com/20000academy/?p=4450
- OpenExamPrep, ITIL 4 CDS: Transition, Validation & Testing（Early Life Supportの出口基準） — https://open-exam-prep.com/study-guides/itil-4-cds/value-stream-new-services/transition-validation-testing
- 公正取引委員会, ソフトウェア業の下請取引等に関する実態調査報告書（2022年6月29日） — https://www.jftc.go.jp/houdou/pressrelease/2022/jun/220629_software.html
- C. N. Parkinson, Parkinson's Law（The Economist, 1955年11月） — https://doc.cat-v.org/economics/parkinsons-law

- Bessemer Venture Partners, Introducing enterprise sales to a product-led growth organization — https://www.bvp.com/atlas/introducing-enterprise-sales-to-a-product-led-growth-organization/
- sso.tax（SSOを上位プランに置くベンダーの価格の一覧） — https://sso.tax/
- APMdigest, Gartner: funding for tech purchases moving outside IT（2022年） — https://www.apmdigest.com/gartner-funding-for-tech-purchases-moving-outside-it
- European Commission, EU GMP Annex 11: Computerised Systems — https://health.ec.europa.eu/system/files/2016-11/annex11_01-2011_en_0.pdf

- Directions on Microsoft, What to Know Before You Go Teams-Less（2024年4月2日） — https://www.directionsonmicrosoft.com/blog/what-to-know-before-you-go-teams-less/

- Zylo, 2025 SaaS Management Index — https://zylo.com/news/2025-saas-management-index
- Flexera, State of ITAM Report（2022） — https://www.flexera.com/about-us/press-center/flexera-state-of-itam-report-shows-wasted-spend-remains-high-across-it-estate
- Directions on Microsoft, EA online services volume discounts end（2025年8月14日） — https://www.directionsonmicrosoft.com/?p=161355

- Farrell & Klemperer, Coordination and Lock-In: Competition with Switching Costs and Network Effects（Handbook of Industrial Organization, Vol. 3 所収） — https://escholarship.org/content/qt9n26k7v1/qt9n26k7v1.pdf
- Microsoft, FastTrack journey（Envision／Onboard／Drive Value） — https://www.microsoft.com/en-us/fasttrack/journey
- Microsoft Learn, Implement pilot deployment — https://learn.microsoft.com/en-us/training/modules/windows-deploy/implement-pilot-deployment
- Microsoft Learn, Implement broad deployment（デプロイメントリング） — https://learn.microsoft.com/en-us/training/modules/windows-deploy/implement-broad-deployment
- Microsoft, Enterprise Agreement（3年契約、年次True-up、更新） — https://microsoft.com/licensing/guidance/Enterprise-Agreement

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

## クラウド（21枚目：契約の単位 × ワークロードの性質の2×2）

| 項目 | 根拠 | 出典 |
|---|---|---|
| 単価の最適化（コミット・予約・Savings Plans）と使用量の最適化を分けて扱う | "Rate optimization is the practice of obtaining reduced rates on cloud services, often by committing to a certain level of usage or spend over a specific period." | Microsoft Learn, FinOps rate optimization（https://learn.microsoft.com/en-us/cloud-computing/finops/framework/optimize/rates） |
| ① 安定した部分だけをコミットに載せる／② 変動分は従量に戻す | コミットは安定して予測できる利用に対して行うのが原則 | FinOps Foundation, Rate Optimization（https://www.finops.org/framework/capabilities/rate-optimization） |
| ③ 部門ごとのアカウントを全社の契約に寄せる、④ タグで費用の持ち主を決める | 費用の配賦（Allocation）とタグ付けは FinOps の基本機能 | FinOps Foundation Framework |
| ② 消化のための利用、③ 同じ用途のアカウントが部門ごとにある | 社内の観察（外部出典なし） | — |
| 下段メッセージ（FinOpsの原則） | 原則「FinOps should be enabled centrally」（中央のチームが単価・コミットの最適化を担う）と「Everyone takes ownership for their technology usage」（利用はそれぞれのチームが持つ） | FinOps Foundation, FinOps Principles（https://www.finops.org/framework/principles/） |
