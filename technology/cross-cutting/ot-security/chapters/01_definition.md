# 01 OT セキュリティの定義と範囲

## 要旨

OT セキュリティは、工場の制御システムなどの OT を守る取り組みである。IT のセキュリティとの違いは、**安全と可用性を最優先にすること**と、**10年以上使い続ける、更新しにくい機器を前提にすること**にある（→ manufacturing 05章）。工場がネットワークやクラウドとつながるにつれて、**IT 側から入った攻撃が生産を止める**ことが現実の問題になっている。

## 定義

NIST は OT を、物理的な環境とやり取りする（または、そうした機器を管理する）プログラム可能なシステムと機器の総称とし、産業制御システム、ビルの自動制御、輸送のシステム、物理的な入退室の管理、環境の監視・計測のシステムなどを例に挙げる。

## 成り立ち

| 時期 | できごと |
|---|---|
| 1990年代 | パデュー大学が製造の統合のための階層モデルを作る。工場の制御系は、外のネットワークにつながらないことを前提に設計されていた |
| 2006年 | NIST SP 800-82 の初版（産業制御システムのセキュリティ） |
| 2007年〜 | IEC 62443 シリーズの発行が始まる |
| 2010年代 | IT と OT の接続が進み、パデューモデルに産業用 DMZ（Level 3.5）が加えられる |
| 2020年代 | IoT・クラウド・遠隔保守によるスマート工場化で、外とつながる経路が増える。NIST SP 800-82 Rev. 3（2023年）、経済産業省の工場セキュリティガイドライン（2022年）が出る |

## 用語集

| 用語 | 意味 |
|---|---|
| ICS（産業制御システム） | 工場やプラントの物理的な工程を監視・制御するシステムの総称 |
| PLC | 機器を直接制御する小型の制御装置 |
| DCS | プラント全体を分散して制御するシステム |
| SCADA | 離れた設備の状態を集めて監視・制御するシステム |
| HMI | 運転員が制御システムを操作する画面 |
| エンジニアリングワークステーション | PLC などのプログラムや設定を作成・書き込む端末 |
| ヒストリアン | 制御システムのデータを時系列で蓄積するサーバ。IT と OT の橋渡しになりやすい |
| CPS（サイバーフィジカルシステム） | 計算・通信と物理的な工程が結びついたシステム。OT・IoT・ロボットなどを含む |
| IACS | IEC 62443 での呼び方。産業用の自動化・制御システム |
| ゾーン／コンジット | 同じセキュリティ要求を持つ資産のまとまり／ゾーン間の通信路（→ 02章） |
| 補償的な対策 | 本来の対策（パッチなど）がとれないときに、別の手段でリスクを下げる対策 |

## 標準とガイドライン

| 名称 | 発行元 | 内容 |
|---|---|---|
| IEC 62443 シリーズ | IEC・ISA（ISA99 委員会） | OT・IACS のセキュリティの国際標準。総論（1-x）、組織の方針と手順（2-x）、システム（3-x）、部品（4-x）の4群からなる。工場をゾーンとコンジットに分け、ゾーンごとに目標のセキュリティレベル（SL 1〜4）を決める |
| NIST SP 800-82 Rev. 3「Guide to Operational Technology (OT) Security」 | 米国 NIST（2023年9月28日） | 対象を ICS から OT に広げた改訂。OT の脅威と脆弱性、推奨の対策、アーキテクチャを示し、SP 800-53 Rev. 5 の管理策を OT 向けに絞った基準（OT オーバーレイ）を加えた |
| 工場システムにおけるサイバー・フィジカル・セキュリティ対策ガイドライン Ver 1.0 | 経済産業省（2022年11月16日） | 工場のセキュリティ対策を企画・導入するための3つのステップを示す。2024年4月には、スマート化を進めるときのポイントをまとめた別冊を公開 |
| パデューモデル | 米国パデュー大学（1990年代） | 製造の統合のための階層モデル。もともとセキュリティの管理策として作られたものではないが、OT のネットワークを分ける基準として広く使われる（→ 02章） |

## 主な事例

| 時期 | 事例 | 何が起きたか |
|---|---|---|
| 2017年 | Merck（米国の製薬企業）と NotPetya | 世界的に広がったマルウェアで、製造・研究・営業を含む世界の業務が止まった。同社は約14億ドルを保険で請求し、戦争の免責の適用をめぐる裁判を経て、2024年1月に保険会社と和解した |
| 2022年2〜3月 | 小島プレス工業とトヨタ自動車 | 部品の仕入先がランサムウェアとみられる攻撃を受け、ネットワークを遮断してすべてのシステムを止めた。受発注のシステムが使えなくなり、トヨタは国内14工場28ラインの稼働を1日止めた |

どちらも、制御システムそのものではなく **IT 側の被害が生産を止めた**例である（本資料の整理）。

## 範囲（何であり、何でないか）

| 含むもの | 含まないもの（隣接領域） |
|---|---|
| OT の資産を守る考え方・標準・対策・製品 | 製造のシステムの機能と、IT と OT の管掌の区分（→ manufacturing） |
| IT と OT の境界（産業用 DMZ）の設計 | 全社の検知と対応、脆弱性管理の運用（→ security-operations） |
| 保守ベンダーのリモートアクセスの守り方 | 製造の記録の信頼性とバリデーション（→ gxp-compliance） |
| | 製品（自動車・医療機器など）に組み込まれたソフトウェアのセキュリティ |

---

**出典**（確認日：2026-11-14）

- OT の定義と NIST SP 800-82 Rev. 3：NIST（2023-09）— https://www.nist.gov/news-events/news/2023/09/guide-operational-technology-ot-security-nist-publishes-sp-800-82-revision 、CSRC（2023-09-28）— https://csrc.nist.gov/news/2023/nist-publishes-sp-800-82-revision-3
- IEC 62443 の構成：IEC — https://syc-se.iec.ch/deliveries/cybersecurity-guidelines/security-standards-and-best-practices/iec-62443/ 、Encryption Consulting — https://www.encryptionconsulting.com/education-center/iec-62443/
- 工場セキュリティガイドライン：MONOist（2023-05）— https://monoist.itmedia.co.jp/mn/articles/2305/09/news017.html 、別冊：MONOist（2024-05）— https://monoist.itmedia.co.jp/mn/spv/2405/30/news009_2.html
- パデューモデルの成り立ち：Trout — https://www.trout.software/resources/purdue-model
- Merck と NotPetya：Security Affairs（2024-01-06）— https://securityaffairs.com/156994/laws-and-regulations/merck-settles-notpetya-insurance.html 、Dark Reading — https://darkreading.com/cyber-risk/war-or-not-cyber-insurers-still-hashing-out-exclusion
- 小島プレス工業とトヨタ自動車：時事通信（ビジネス+IT、2022-03-01）— https://www.sbbit.jp/article/refers/82094 、https://www.sbbit.jp/article/refers/82195
- CPS の範囲：Gartner — https://www.gartner.com/en/documents/7540249
- NIST SP 800-82 の初版（2006年）：TechXplore（NIST の転載）— https://techxplore.com/news/2023-09-technology-ot-published.amp
- IEC 62443 の最初の発行（2007年）：SmartSuite — https://www.smartsuite.com/frameworks/iec-62443-series-security-industrial-automation-control-systems
- 工場の制御系が外とつながらない前提で設計されてきたこと：MONOist（2023-06）— https://monoist.itmedia.co.jp/mn/articles/2306/22/news025.html
- 産業用 DMZ が後から加えられたこと：SentinelOne — https://www.sentinelone.com/tw/cybersecurity-101/cybersecurity/what-is-the-purdue-model/
- 用語の説明、事例の位置づけ、成り立ちの「2010年代」の時期の目安は本資料の整理
