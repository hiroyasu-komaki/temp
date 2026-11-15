# 01 IT運用の定義と範囲

## 要旨

IT運用は、作り終えたシステムを**止めずに動かし続け、利用者の依頼と問い合わせに応え、変更を安全に入れる**日々の活動である。システムの一生のほとんどは、作る期間ではなく使われる期間であり、IT運用の質がそのまま利用者の体験と事業の継続を決める。

## 定義

本資料では、IT運用を次の4つの領域で扱う（本資料の整理）。

| 領域 | 内容 | 代表的な仕組み |
|---|---|---|
| IT サービス管理（ITSM） | 問い合わせ・依頼・障害（インシデント）・問題・変更を、決まった手順で受け付けて処理する | サービスデスク、チケット管理（ServiceNow など） |
| 監視（オブザーバビリティ） | システムの稼働・性能・異常を把握し、障害を早く見つける | 監視ツール、ログ・メトリクス・トレースの分析 |
| ジョブ管理 | 夜間のバッチ処理など、決まった処理を決まった順番と時刻に自動で実行する | ジョブスケジューラー（JP1/AJS3 など） |
| バックアップと復旧 | データとシステムを複製し、障害・災害・攻撃から元に戻せるようにする | バックアップ製品、3-2-1 ルール |

IT サービス管理の代表的な指針が ITIL で、現行の ITIL 4 は、サービスバリューシステム、7つの指導原則、4つの側面、6つの活動からなるサービスバリューチェーン、34のプラクティスで構成される。ITIL は任意の指針であり、資格は個人が取る。組織として認証を受ける場合は ISO/IEC 20000-1 が対象になる。

## 成り立ち

| 年 | 出来事 | 意味 |
|---|---|---|
| 2016 | Google が『Site Reliability Engineering』を出版 | 本番のサービスを動かすことの意味と、信頼性をサービスの設計の一部として扱う考え方（SRE）が広く議論される |
| 2019 | AXELOS が ITIL 4 を公開（2月）。ITIL v3 の26のプロセスを34のプラクティスに組み替える | IT サービス管理の指針が、プロセスの手順書から価値を生む仕組みの全体像へ移る |
| 2021 | PeopleCert が AXELOS を買収し、ITIL の所有者になる | — |
| 2023 | Gartner が ITSM の Magic Quadrant を Market Guide に置き換える | ITSM の製品が成熟し、違いが AI などの付加機能に移る |
| 2024〜2026 | Gartner が「AI Applications in IT Service Management」の Magic Quadrant を始める（2024年に初版） | 問い合わせ対応と運用の判断を AI が支援する製品分野ができる |

PeopleCert は ITIL の次の版（ITIL Version 5）も公開し、ITIL 4 の資格保持者向けの移行の講座を用意している。

## 範囲（何であり、何でないか）

| IT運用が扱うもの | 扱わないもの（隣接領域） |
|---|---|
| サービスデスク、インシデント・問題・変更・依頼の管理 | 攻撃の検知と対応（security-operations） |
| システムの稼働と性能の監視 | 基盤の設計と構成（infrastructure） |
| ジョブ管理（バッチ処理の自動実行） | システム間のデータ連携の仕組み（integration） |
| バックアップと復旧、事業継続の技術的な備え | 端末とコラボレーション基盤そのもの（workplace） |

---

**出典**（確認日：2026-11-14）

- ITIL 4 の構成、所有者、ISO/IEC 20000-1 との関係、ITIL Version 5：SmartSuite「What is ITIL?」— https://www.smartsuite.com/what-is/what-is-itil
- ITIL 4 の公開（2019-02）と 26 プロセスからの組み替え：IT Governance — https://www.itgovernance.eu/itil 、University of Utah — https://itil.it.utah.edu/itilv4/index.html
- PeopleCert による AXELOS の買収（2021）：ManageEngine — https://www.manageengine.com/za/products/service-desk/itil-help-desk-smb-whitepaper.html
- SRE 本（2016）：O'Reilly『The Site Reliability Workbook』紹介 — https://oreilly.com/library/view/~/9781492029496
- ITSM の Magic Quadrant から Market Guide への置き換えと、AI Applications in ITSM の初版（2024）：InvGate — https://blog.invgate.com/pt/quadrante-magico-gartner-aplicacoes-ia-itsm
- 4つの領域の分け方は本資料の整理
