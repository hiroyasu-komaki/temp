# 付録H　データ領域の製品 — 顧客マスタと業界データ

> **参照元**：[03章](../chapters/03_landscape.md)

本付録は、コマーシャル活動の土台となる **顧客（HCP/HCO）マスタ** と、Veeva が提供する **業界データ・分析基盤** を扱います。日本はグローバルと仕組みが異なる（OpenData が提供されず Ultmarc を使う）ため、その違いを重点的に説明します。

---

## H-1 全体像

| 区分 | 製品 | 役割 | 日本での扱い |
|------|------|------|-------------|
| マスタ管理 | **Veeva Network（Network MDM）** | HCP/HCO マスタの統合・重複排除・変更管理。CRM 等が参照する単一ソース | 利用可 |
| リファレンスデータ | **Veeva OpenData Commercial** | Veeva が整備する HCP/HCO のプロファイルデータ | **提供なし**（Ultmarc で代替） |
| | Veeva OpenData Clinical | 治験責任医師・施設のデータ（[付録E](E_rd-products.md)） | — |
| アクセス指標 | **Veeva HCP Access** | Veeva CRM 利用企業の活動を集計した、医療従事者への業界横断アクセス指標 | 提供あり |
| アカウントデータ | **Veeva Link Key Accounts** | 主要アカウントと意思決定者の詳細 | 米国向け |
| KOL データ | Veeva Link Key People | KOL の詳細（[付録F](F_medical-products.md)） | — |
| 患者・処方データ | **Veeva Compass**（Patient / Prescriber / National） | 匿名化された患者の長期データ、処方医・地域別の推計データ | 米国中心 |
| 分析基盤 | **Veeva Nitro** | CRM 活動データと外部データを統合するコマーシャルデータウェアハウス（Amazon Redshift） | 日本企業の導入事例あり |
| | **Marketing Analytics** | キャンペーン効果測定・顧客インサイト | — |

---
## H-2 Veeva Network — 顧客マスタ管理

Veeva Network は HCP/HCO マスタデータ管理（MDM）の製品です。CRM・メディカル・イベント等のアプリが参照する医師・施設データの **正本（System of Record）** になります。

| 機能 | 内容 |
|------|------|
| 統合 | 外部データ（OpenData・Ultmarc 等）と自社データを統合 |
| 重複排除 | 同一人物・同一施設の重複レコードを検出・統合 |
| 変更管理 | 現場からの変更申請（異動・新規施設）を受け付け、データ提供元に照会して反映 |
| 配信 | CRM 等の下流システムへマスタを配信 |

**設計原則**：CRM 側の医師・施設情報は参照専用とし、変更は Network で行います（[02章](../chapters/02_structure.md)「API と連携方式」）。

---
## H-3 グローバル：Veeva OpenData

OpenData は、Veeva 自らが整備・更新する HCP/HCO のリファレンスデータです。

- データ例：Veeva ID（一意識別子）、氏名、住所、電話番号、免許番号、専門分野、所属関係
- CDA（Common Data Architecture）に準拠した標準フィールドで提供
- レコード数と対象国数に基づく **有料のサブスクリプション**（「Open」は無料の意味ではなく、第三者と共有しやすい契約形態を指す）
- アジア太平洋では、東南アジア・オーストラリア・韓国・インド・ニュージーランド・台湾など11か国で提供

---
## H-4 日本：Ultmarc（日本アルトマーク）

**OpenData は日本では提供されていません。** Veeva は日本では現地のデータ提供元である Ultmarc と提携しています。

### Ultmarc のマスタファイル（MDB）

| ファイル | 正式名称 | 範囲 |
|---------|---------|------|
| **DCF** | Doctor Computer File | 全国の医療施設（病院・診療所）と所属医師 |
| **DSF** | Drug Store File | 全国の薬局・薬店 |
| **PCF** | Pharmacist Computer File | 病院薬剤師 |

- 全国の医療機関と、そこに勤務する医師・薬剤師などのマスターデータ
- 会員企業が情報を提供し、データの正確さと網羅性を共同で維持する **業界共同メンテナンスモデル**（会員は2019年時点で約250の企業・行政機関）
- 有料の会員制。Veeva 経由で使う場合も Ultmarc の利用料は別途発生
- 沿革・料金体系の詳細は [付録B](B_ultmarc-and-japan-hcp-data.md)

### 日本の HCP/HCO データの入手経路

| 経路 | 内容 |
|------|------|
| Ultmarc（Veeva 提携） | HCP/HCO の基本プロファイル。Network 経由で CRM に配信 |
| Veeva CRM Pulse（Pulse データ） | Veeva CRM 利用企業の活動を集計した、HCP へのアクセスとチャネル別エンゲージメントのデータ。四半期ごとに、国・診療科・ブリック（小地域）単位で集計して提供（21か国）。日本が対象国に含まれるかは公式ページで確認できなかった |
| 自社データ | CRM に蓄積された面談・反応データ |

> 旧資料にあった「Veeva Jitsushoka」は、公式サイトで製品として確認できなかったため、本資料では扱わない。

### 具体例：大学病院のデータ

| 種別 | 内容 |
|------|------|
| HCO（施設） | DCF 施設コード、施設名、住所、電話番号、診療科目、二次医療圏、DPC 対象病院フラグ、がん診療連携拠点病院フラグ、病床数、特定機能病院フラグ |
| HCP（医師） | DCF 医師コード、氏名、役職（教授・講師等）、所属部科、勤務先施設コードによる紐づけ |

---
## H-5 識別子 — 同じ人・同じ施設をどう突き合わせるか

医師・施設は、複数のデータ源とシステムに登場します。氏名で突き合わせるのではなく、**一意識別子** で結びつけることが前提です。

| 識別子 | 付与元 | 使われる場面 |
|--------|-------|-------------|
| Veeva ID | Veeva（OpenData・Network） | グローバルの HCP/HCO 識別 |
| DCF 施設コード・医師コード | Ultmarc | 日本の HCP/HCO 識別 |
| NPI・免許番号 | 各国当局 | 米国等の公的識別 |
| Network ID / CRM Account ID | 自社の Network / CRM | 社内システム間の突き合わせ |
| External ID | 他の自社システム | ERP・データ基盤との連携 |

識別子の対応ルールを事前に決めておかないと、グローバルとローカル、CRM とメディカル（Link）の間でデータがずれます。

---
## H-6 分析基盤 — Nitro と Compass

| 製品 | 中身 | 使い方 |
|------|------|-------|
| Veeva Nitro | CRM の活動データ＋外部データ（売上・処方等）を統合したデータウェアハウス。業界向けの事前構築済みコネクタとデータモデルを持つ | KPI 分析、ターゲティング、活動と成果の関係分析 |
| Veeva Compass | 匿名化された患者データ・処方データ（米国中心） | 市場分析、ターゲティング |
| Marketing Analytics | キャンペーンの効果測定 | マーケティング施策の評価 |

---

**出典**（確認日：2026-10。H-4 と日本のデータ入手経路は 2026-11-14 に再確認）

- Veeva CRM Pulse：Veeva「Veeva Commercial Pulse」— https://veeva.com/?p=100335
- Ultmarc の MDB：付録B の出典を参照

- [Veeva OpenData Asia Pacific](https://www.veeva.com/products/opendata-asia-pacific/)
- [Veeva Nitro（日本）](https://www.veeva.com/jp/products/crm-suite/nitro/)
- [Veeva Link Overview](https://www.veeva.com/products/veeva-link/overview/)
- [Veeva Products（製品一覧）](https://www.veeva.com/products/)
