# プロセスオーナー原則の根拠（GxP・J-SOX）

| 項目 | 内容 |
|---|---|
| 文書番号 | BTR-APX-02 |
| 版 | 0.4（案） |
| 位置づけ | 参考。[移管後の役割と業務プロセス](./01-post-transfer-operating-model.md)（BTR-APX-01）§2 のプロセスオーナー原則について、情報ソースと、各ソースに書かれていることを示す |
| 所管 | 予算移管事務局 |
| 承認者 | IT部門長 |
| 最終改訂日 | 2026-10-12 |

---

## 1. この文書の読み方

- 各ソースについて、**情報ソース**（発行者・名称・版・入手先）、**規定されていること**（原文の引用。章・項・頁つき）、**本件での読み方**（予算移管での使い方）を分けて書く。引用は原文どおりとし、読み方は予算移管事務局の解釈である。
- 原文を確かめたかどうかを、各ソースの「確認」の欄に示す。
- 結論を先に示す。

| 側 | 適用する部門 | 結論 |
|---|---|---|
| GxP | GxP 対象の部門 | 現行の EU GMP Annex 11 が、プロセスオーナーとシステムオーナーを別の役割として定義している。PIC/S PI 011-3 は、システムの利用者を所有者（owners）とし、社内の IT を含む供給者と責任を分けるとしている。この2つで、業務アプリケーションの Accountability を業務側に置く根拠になる。Annex 11 の改訂案（2025年）では両者の定義が消えるが、代わりに、業務側が責任を持ち、社内の IT部門は SLA・KPI で監督される運用の担い手、という構図がはっきり書かれる |
| J-SOX | 本社機能（財務・経理、人事・総務、法務・経営企画） | 「業務プロセスオーナー」という語は、確認した国内の一次資料にはない。ただし、IT統制ガイダンスが「業務プロセスの責任者」をシステム側の責任者と分けて扱い、役割と責任を規程で定めることを求めている。システム管理基準は、業務要件と運用の判断を利用部門との合意・判断に置いている。これらで、GxP のプロセスオーナー原則を援用することを補強する |

---

## 2. GxP 側

### 2.1 EU GMP Annex 11: Computerised Systems（現行）

| 項目 | 内容 |
|---|---|
| 発行者 | European Commission（EudraLex Volume 4） |
| 名称・版 | Annex 11: Computerised Systems（2011年6月30日施行。現行） |
| 入手先 | https://health.ec.europa.eu/system/files/2016-11/annex11_01-2011_en_0.pdf |
| 確認 | 原文を確認済み |

**規定されていること**

| 箇所 | 原文 |
|---|---|
| Principle | "This annex applies to all forms of computerised systems used as part of a GMP regulated activities." |
| Principle | "The application should be validated; IT infrastructure should be qualified." |
| 2. Personnel | "There should be close cooperation between all relevant personnel such as Process Owner, System Owner, Qualified Persons and IT." |
| Glossary: Process owner | "The person responsible for the business process." |
| Glossary: System owner | "The person responsible for the availability, and maintenance of a computerised system and for the security of the data residing on that system." |

**本件での読み方**

- Process Owner と System Owner は、規制の上で別の役割として定義されている。前者は業務プロセスに、後者はシステムの可用性・保守とデータのセキュリティに責任を持つ。
- 業務アプリケーションの要否・業務要件・適正な使用は業務プロセスに属するので、その Accountability はプロセスオーナー（ビジネスオーナー）に残る。IT部門は System Owner として、可用性・保守・セキュリティを担う。
- Principle がアプリケーション（validated）と IT インフラ（qualified）を分けていることは、予算移管の対象（業務アプリケーション）と対象外（全社横断のインフラ）の区別とも合う。

### 2.2 EU GMP Annex 11 改訂案（2025年）

| 項目 | 内容 |
|---|---|
| 発行者 | European Commission |
| 名称・版 | Draft guidelines: Revised Annex 11 – Computerised Systems（2025年7月 意見募集。2025年10月7日締切。確定前の案） |
| 入手先 | https://health.ec.europa.eu/document/download/40231f18-e564-4043-94de-c031f813d38b_en?filename=mp_vol4_chap4_annex11_consultation_guideline_en.pdf |
| 確認 | 原文を確認済み（数字は改訂案の行番号） |

**書かれていること**

| 箇所 | 原文 |
|---|---|
| 5.1 Cooperation（87–90行） | "When conducting the activities required in this document, there should be, where applicable, close cooperation between all relevant parties. This includes process owner, system owner, users, subject matter experts (SME), QA, QP, the internal IT department, vendors, and service providers." |
| 6.1 GMP functionality（95–97行） | "A regulated user should establish and approve a set of system requirements (e.g. a User Requirements Specification, URS), which accurately describe the functionality the regulated user has automated and is relying on when performing GMP activities." |
| 7.1 Responsibility（128–132行） | "When a regulated user is relying on a vendor's qualification of a system used in GMP activities, a service provider, or an internal IT department's qualification and/or operation of such system, this does not change the requirements put forth in this document. The regulated user remains fully responsible for these activities …" |
| 7.3 Oversight（139–143行） | "When a regulated user is relying on a service provider's or an internal IT department's operation of a system used in GMP activities, the regulated user should exercise effective oversight of this according to defined service level agreements (SLA) and key performance indicators (KPI) agreed with the service provider or the internal IT department." |
| 7.5 Contracts（149–152行） | "When a regulated user is relying on a service provider's or an internal IT department's qualification and/or operation of a system used in GMP activities, the regulated user should have a contract with a service provider or have approved procedures with an internal IT department …" |
| Glossary: Regulated user（599–600行） | "A company regulated under GMP." |

**現行版との違い**

- 用語集に Process owner・System owner の定義がない（5.1 に関係者として名前が出るだけ）。
- 一方で、社内の IT部門（internal IT department）を、ベンダー・サービス提供者と並ぶ「頼る先」として扱っている。regulated user は、IT部門に運用を任せても全面的に責任を持ち（7.1）、IT部門と合意した SLA・KPI で監督し（7.3）、IT部門との間で承認された手順を持つ（7.5）。

**本件での読み方**

- 用語集の regulated user は「会社」だが、本文は regulated user と社内の IT部門を別のものとして扱っている。GMP の業務を行う側（業務部門）が責任を持ち、IT部門は運用を担って SLA・KPI で監督される、という関係が読み取れる。
- これは BTR-APX-01 の After（IT部門のシステムオーナーが運用を担い、ビジネスオーナーが判断と監督を行う。E-7 運用のモニタリングなど）とよく合う。
- 改訂が確定すると、Annex 11 を「プロセスオーナーとシステムオーナーを定義した規制」としては示せなくなる。その場合は、「業務側が責任を持ち、社内 IT部門は SLA で監督される運用の担い手」という改訂後の構図と、PIC/S PI 011-3（2.3）を根拠にする。

### 2.3 PIC/S PI 011-3 Good Practices for Computerised Systems in Regulated "GxP" Environments

| 項目 | 内容 |
|---|---|
| 発行者 | PIC/S（医薬品査察協定・医薬品査察協同スキーム。日本の厚生労働省・PMDA も加盟） |
| 名称・版 | PI 011-3（2007年9月25日） |
| 入手先 | https://picscheme.org/docview/3444 |
| 確認 | 原文を確認済み |

**規定されていること**

| 箇所 | 原文 |
|---|---|
| 脚注1（p.1） | "Throughout this document the 'users' (owners of the good practice computerised systems being inspected) are collectively referred to as 'regulated users' for clarity." |
| 脚注2（p.2） | "… between the supplier(s) [developer(s) and producer(s) of individual components or complete computerised system] and the regulated user [purchaser and user of the computerised system]." |
| 3.6（p.3） | "There will normally be a need to manage and control the split responsibilities of contracted suppliers (whether in-house or external party) and regulated user businesses (customers), for project management, product specifications, quality assurance standards and performance." |
| 4.11（p.5） | "The regulated users of the system have the ultimate responsibility for ensuring that documented validation evidence is available to GxP inspectors for review." |
| 8.5（p.10） | "Within the regulated user organisation there should be clearly defined responsibilities for the management of all ICT products, computerised systems and projects." |
| 13（p.16） | "The test scripts related to the user requirements specification are the responsibility of the regulated users." |
| 18.6（p.23） | "Any changes to the validated computerised system should not be undertaken without review and authorisation on behalf of all stakeholders responsible for the current user requirements. It may be appropriate for this to be undertaken by the system owner and QA representative." |
| 19.1（p.23） | "'System owner's' responsibilities will include the management of access to their systems …" |
| 22.3（p.30） | "The individual areas of responsibility should be laid down in writing and be clearly understandable to every member of staff." |

**本件での読み方**

- 「users」はシステムの所有者（owners）とされ、システムを購入し使う者（regulated user）として、開発・供給する者（supplier）と区別されている。
- 供給者には社内の者も含まれ（"whether in-house or external party"）、供給者と「regulated user businesses (customers)」の間で責任を分けて管理する、とある。社内の IT部門は供給者の側、業務部門は利用者・所有者の側に当たる。業務アプリケーションの所有と最終責任は業務側にある、という読み方の、最も直接的な裏付けになる。
- 責任を文書で明確に定めることを求めている（8.5、22.3）。予算移管の後の役割を BTR-APX-01 で定めておくことと合う。
- 利用者要求に関わるテストは利用者の責任（13）であり、受け入れを業務側が担うことと合う。

### 2.4 厚生労働省「コンピュータ化システム適正管理ガイドライン」

| 項目 | 内容 |
|---|---|
| 発行者 | 厚生労働省 医薬食品局 監視指導・麻薬対策課 |
| 名称・版 | 医薬品・医薬部外品製造販売業者等におけるコンピュータ化システム適正管理ガイドライン（平成22年10月21日 薬食監麻発1021第11号。平成24年4月1日適用） |
| 入手先 | https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573&dataType=1&pageNo=1（厚生労働省 法令等データベース） |
| 確認 | 原文を確認済み |

**規定されていること**

| 箇所 | 原文 |
|---|---|
| 1.2 コンピュータ化システムの取扱い | 「製造販売業者等において組織の形態や該当するシステムの範囲を考慮して各々の組織・役割に応じた責任と権限を3．に規定する「コンピュータ化システムの開発、検証及び運用管理に関する文書」の中に明確にすることが必要である。」 |
| 3. | 「製造販売業者等はコンピュータ化システムの開発、検証及び運用にあたっては、あらかじめ、その基本方針等に関する文書(以下「コンピュータ化システム管理規定」という。)を定めるものとする。」 |
| 4.2 要求仕様に関する文書の作成 | 「開発責任者はコンピュータ化システムに求められている事項を記載した文書(以下「要求仕様書」という。)を作成するものとする。」 |
| 4.4 機能仕様に関する文書の作成 | 「開発責任者は、供給者に要求仕様書に記載された要件に対応した具体的なコンピュータ化システムの機能と性能を記載した機能仕様に関する文書(以下「機能仕様書」という。)を作成させ、承認するものとする。」 |
| 用語の定義：運用責任者 | 「コンピュータ化システム運用業務を行うための責任者として、製造販売業者等により運用管理基準書において指定された者。」 |

**規定されていないこと**：「使用部門」「情報システム部門」のような部門名による役割分担はない。開発責任者・運用責任者を業務側と IT側のどちらに置くかも定めていない。

**本件での読み方**

- 国内の GxP 規制は、各組織の責任と権限を、会社が規定で前もって明確にすることを求めている。BTR-APX-01 で予算移管の後の役割を定めておくことの根拠になる。
- 要求仕様書を作り、供給者の機能仕様書を承認する者（開発責任者）を、供給者とは別に置いている。業務の要求を定める側と、それを実現する側を分ける考え方である。誰に置くかは会社が決めるので、業務側に Accountability を置くという本件の決定は、この規定と矛盾しない。

### 2.5 ISPE GAMP 5（参考）

| 項目 | 内容 |
|---|---|
| 発行者・名称 | ISPE「GAMP 5: A Risk-Based Approach to Compliant GxP Computerized Systems」（Second Edition, 2022） |
| 確認 | **原文は入手できず、未確認** |

- 業界の指針として名前を挙げるにとどめ、根拠としては引用しない。ISPE の公式記事（Pharmaceutical Engineering 2023年1-2月号「What You Need to Know About GAMP 5 Guide, 2nd Edition」）も確認したが、プロセスオーナー・システムオーナーへの言及はなかった。解説記事は、プロセスオーナーがシステムの導入・バリデーション・適正な使用に最終責任を負うと説明している（[Investigations & Quality](https://investigationsquality.com/2024/06/22/the-gamp5-system-owner-and-process-owner/)）。

---

## 3. J-SOX 側

### 3.1 金融庁「財務報告に係る内部統制の評価及び監査の基準」

| 項目 | 内容 |
|---|---|
| 発行者 | 金融庁 企業会計審議会 |
| 名称・版 | 財務報告に係る内部統制の評価及び監査の基準並びに財務報告に係る内部統制の評価及び監査に関する実施基準の改訂について（意見書）（2023年4月7日） |
| 入手先 | https://www.fsa.go.jp/news/r4/sonota/20230407/1.pdf |
| 確認 | 原文を確認済み |

**規定されていること**

| 箇所 | 原文 |
|---|---|
| 基準 Ⅰ.4(1) 経営者 | 「経営者は、組織の全ての活動について最終的な責任を有しており、その一環として、取締役会が決定した基本方針に基づき内部統制を整備及び運用する役割と責任がある。」 |
| 同 | 「経営者は、その責任を果たすための手段として、社内組織を通じて内部統制の整備及び運用（モニタリングを含む。）を行う。」 |
| 基準 Ⅰ.4(5) 組織内のその他の者 | 「内部統制は、組織内の全ての者によって遂行されるプロセスであることから、上記以外の組織内のその他の者も、自らの業務との関連において、有効な内部統制の整備及び運用に一定の役割を担っている。」 |

**規定されていないこと**：「業務プロセスオーナー」「プロセスオーナー」の語はない。業務部門と IT部門の役割分担も書かれていない。

**本件での読み方**

- 内部統制は社内組織を通じて整備・運用され、各人は「自らの業務との関連において」役割を担う。業務プロセス（とそれを支える業務アプリケーション）の統制は、その業務を担う組織の役割である、という考え方の土台になる。

### 3.2 経済産業省「システム管理基準 追補版（財務報告に係るIT統制ガイダンス）」

| 項目 | 内容 |
|---|---|
| 発行者 | 経済産業省 |
| 名称・版 | システム管理基準 追補版（財務報告に係るIT統制ガイダンス）（令和6年12月25日） |
| 入手先 | https://www.meti.go.jp/policy/netsecurity/docs/secgov/2024_ZaimuHoukokuNiKakaruITTouseiGuidance.pdf |
| 確認 | 原文を確認済み（平成19年版は令和6年版に置き換わっているため、使わない） |

**規定されていること**

| 箇所 | 原文 |
|---|---|
| 第Ⅲ章 図表Ⅲ.5-1「IT統制の評価技法の例」（p.Ⅲ-35） | 「担当者（開発責任者、システム管理者、業務プロセスの責任者）へのヒアリング」 |
| 第Ⅲ章 図表Ⅲ.4-1「IT全般統制の評価における留意点の例」a.（p.Ⅲ-30） | 「開発業務に関しては、ユーザ部門等が参画したテストが実施されているかを評価する。」 |
| 第Ⅳ章 2.(1) 統制目標の例 2-(1)-③（p.Ⅳ-8） | 「ITに関する業務を適正かつ効率的に行うために、要員の責任及び権限を定める。」 |
| 第Ⅳ章 2.(1) 統制の例と統制評価手続の例 2-(1)-③（p.Ⅳ-9） | リスクの例：「ITに関する業務の管理・実施責任が不明確なことにより、不正やミスが見逃され、情報の信頼性が確保されない。」／統制の例：「ITに関する業務の役割分担と責任が明確になっている。」／統制評価手続の例：「IT部門、ユーザ部門、委託先（情報システム子会社を含む）の役割と責任が職務分掌規程等により適切に定められ、その内容が関連する部門及びグループ企業に周知・徹底されていることを確かめる。」 |

**規定されていないこと**：「業務プロセスオーナー」「プロセスオーナー」の語はない。業務アプリケーションの最終責任がどちらにあるかを直接定めた記述もない。

**本件での読み方**

- 「業務プロセスの責任者」を「開発責任者」「システム管理者」と分けて扱っている。これは Annex 11 の Process Owner と System Owner の区別に対応する国内の記述である。
- IT部門・ユーザ部門・委託先の役割と責任を規程で定めて周知することが、統制の例として示されている。予算移管の後の役割を、あらかじめ文書（BTR-APX-01）で定義しておくことの根拠になる。
- 開発時のテストへのユーザ部門の参画が評価の観点になっている。受け入れ（業務要件を満たすか）を業務側が担うことと合う。

### 3.3 経済産業省「システム管理基準」（補完）

J-SOX のための文書ではないが、3.2 の追補版の本体であり、IT部門と利用部門の役割の考え方を補う。

| 項目 | 内容 |
|---|---|
| 発行者 | 経済産業省 |
| 名称・版 | システム管理基準（令和5年4月26日） |
| 入手先 | https://www.meti.go.jp/policy/netsecurity/sys-kansa/sys-kanri-2023.pdf |
| 確認 | 原文を確認済み |

**規定されていること**

| 箇所 | 原文 |
|---|---|
| 前文（4）利用部門等（p.6） | 「組織内において、IT部門以外の部門を「利用部門等」と呼ぶ。」 |
| Ⅰ.1.4 実行責任及び説明責任の明確化 達成目標2（p.19） | 「ITに関連する意思決定の構造及びパフォーマンスの確認体制は、経営者、IT部門及び利用部門が関与しており、権限はそれを行使するのに最適な立場にある者に委譲されている。」 |
| 同 ガバナンス活動の例5（p.19） | 「（ITシステムの利活用に関する責任の明確化）ITサービスの提供と利活用に関する実行責任と説明責任を明確にする。」 |
| Ⅱ.3.2 業務要件定義 達成目標3（p.42） | 「優先順位付けされた要望が業務要件として明確にされ、利用者及び関係者と合意されている。」 |
| 同 管理活動の例4（p.42） | 「（業務要件定義の文書化と承認）業務要件定義の成果を文書化し、承認を得る。」 |
| Ⅱ.5.4 運用における構成管理・変更管理 管理活動の例5（p.54） | 「（利用部門との合意）IT部門と利用部門との間で変更について合意する。」 |
| Ⅱ.5.5 インシデント管理・問題管理 管理活動の例4・5（p.55） | 「（利用部門との合意）利用部門とIT部門の間で、インシデントの影響度及び緊急度を評価し、インシデント対応の優先度について合意する。」「（インシデント対応の完了）利用部門の判断の下でインシデント対応を完了する手続を定める。」 |
| Ⅱ.5.6 サービスレベル管理 達成目標2（p.55） | 「サービスの範囲及びサービスレベルがIT部門及び利用部門の間で合意されている。」 |

**本件での読み方**

- 「ITサービスの提供」と「利活用」の実行責任・説明責任を分けて明確にすることを求めている。IT部門（提供）と業務側（利活用）で責任を分ける考え方に合う。
- 業務要件は利用者と合意して承認を得る。運用の変更、インシデント対応の優先度、サービスレベルは IT部門と利用部門で合意し、インシデント対応の完了は利用部門が判断する。BTR-APX-01 の経費プロセスの After（IT部門のシステムオーナーが実務を担い、判断は業務側に残す）は、この形に対応する。

---

## 4. 本社機能への共通メッセージ（案）

> 業務アプリケーションの Accountability は、その業務プロセスに責任を持つビジネス側に残る。GxP 対象の部門では、EU GMP Annex 11 がプロセスオーナーとシステムオーナーを別の役割として定め、PIC/S のガイダンスもシステムの利用者を所有者とし、社内の IT を含む供給者と責任を分けるとしている。本社機能は GxP の対象ではないが、同じ原則を援用する。国内でも、経済産業省の IT統制ガイダンスは「業務プロセスの責任者」をシステム側の責任者と分けて扱い、役割と責任を規程で定めることを求めている。システム管理基準は、業務要件と運用の判断を利用部門との合意・判断に置いている。

---

## 5. 検索の記録

| ソース | 検索した語 | 結果 |
|---|---|---|
| IT統制ガイダンス（令和6年）、システム管理基準（令和5年） | 業務プロセスオーナー、プロセスオーナー、オーナー | いずれも0件 |
| 同上 | ユーザ部門、利用部門、IT部門、情報システム部門 | IT統制ガイダンスに「ユーザ部門」、システム管理基準に「利用部門」がある。上記に引用した |
| 金融庁 意見書（2023年） | 業務プロセスオーナー、プロセスオーナー | 0件 |

---

## 改訂履歴

| 版 | 日付 | 改訂内容 | 改訂者 | 承認者 |
|---|---|---|---|---|
| 0.4 | 2026-10-12 | 原文の写し（reference/_sources/）を置かないことにし、写しの行を削除した。原文は各項の入手先で確かめる | 予算移管事務局 | |
| 0.3 | 2026-10-12 | Annex 11 改訂案と厚生労働省のガイドラインを原文で照合し、引用に差し替えた。改訂案が社内 IT部門を SLA・KPI で監督される運用の担い手として扱っていることを加えた | 予算移管事務局 | |
| 0.2 | 2026-10-12 | GxP 側に、Annex 11 改訂案（2025年）、PIC/S PI 011-3、厚生労働省のガイドラインを加えた。GAMP 5 を参考に下げた |
| 0.1 | 2026-10-12 | 初版（案） | 予算移管事務局 | |
