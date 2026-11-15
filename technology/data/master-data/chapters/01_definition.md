# 01 マスタデータ管理の定義と範囲

## 要旨

マスタデータは、取引の「誰と・何を・どこで」を表す、**多くのシステムが共通に使う基準のデータ**（品目・取引先・顧客・従業員・拠点など）である。マスタデータ管理（MDM）は、それぞれのマスタについて**どのシステムが正本（System of Record）か**、**誰が登録・変更してよいか**、**どう品質を保ち、どう配るか**を決めて守り続ける取り組みである。製品を入れることより、**業務部門と IT の役割分担を決めること**が中心になる。

## 定義

Gartner は MDM を、業務部門と IT が協力して、企業の公式な共有マスタデータ資産の統一性・正確性・管理（スチュワードシップ）・意味の一貫性・説明責任を確保する、技術に支えられた規律と定義している。

| 用語 | 内容 |
|---|---|
| マスタデータ | 取引の対象となる事業上の実体（顧客・仕入先・従業員・製品・コストセンターなど）のデータ |
| 参照データ | 分類や区分のための、取りうる値の一覧（国コード、単位、剤形など）。マスタデータの一部と見なされることもあり、変わることは少ない |
| System of Record（SoR） | ある項目について正本を持つシステム（本資料の整理） |
| ゴールデンレコード | 複数のシステムの記録を突き合わせてまとめた、1つの実体についての最も信頼できる記録 |
| データスチュワード | マスタの登録・変更の判断と品質に責任を持つ担当者 |

MDM の技術の基本は、源泉のシステムのデータを集める **MDM ハブ**、源泉からハブへデータを運ぶ**データ連携**、**データ品質のツール**の3つとされる。

## 業界特有の例：医薬品の識別（IDMP）

医薬品では、製品・物質のマスタが規制の対象になる。ISO の IDMP（Identification of Medicinal Products）は、医薬品を一意に識別し情報を交換するための5つの規格（物質 ISO 11238、剤形・単位・投与経路・包装 ISO 11239、単位 ISO 11240、医薬品の製品 ISO 11616、承認された医薬品 ISO 11615）からなる。欧州医薬品庁（EMA）は、これを物質・製品・組織・参照（SPOR）の4つのマスタデータの領域に分けて段階的に導入している。

## 範囲（何であり、何でないか）

| MDM が扱うもの | 扱わないもの（隣接領域） |
|---|---|
| マスタの項目ごとの正本（SoR）と、登録・変更の権限 | マスタを配る仕組みそのもの（integration） |
| マスタの品質（重複・欠落・表記の揺れ）の管理 | 取引データ（受注・出荷など）の処理（erp など） |
| マスタの照合・統合（ゴールデンレコード） | 分析用のデータの蓄積と可視化（analytics） |
| データスチュワードの役割と、マスタの管理の手順 | ID・アカウントの管理（identity。従業員マスタとは接する） |

---

**出典**（確認日：2026-11-14）

- MDM の定義（Gartner）：Pimcore による引用 — https://pimcore.com/en/resources/blog/master-data-management-essentials-you-can-t-afford-to-get-wrong_a54096
- マスタデータ・参照データ、MDM の技術の3要素：CIO.com — https://www.cio.com/article/191827/what-is-master-data-management-ensuring-a-single-source-of-truth.html 、https://www.cio.com/article/3620430/what-is-master-data-management-ensuring-a-single-source-of-truth.html
- ゴールデンレコード：Pimcore — https://pimcore.com/en/resources/insights/what-is-master-data-management
- IDMP と SPOR：EMA「Data on medicines (ISO IDMP standards): Overview」— https://www.ema.europa.eu/en/human-regulatory/overview/data-medicines-iso-idmp-standards
- System of Record の定義と範囲の分け方は本資料の整理
