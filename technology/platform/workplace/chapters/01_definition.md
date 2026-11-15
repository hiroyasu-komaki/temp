# 01 ワークプレイスの定義と範囲

## 要旨

ワークプレイスは、社員が毎日使う**端末（PC・スマートフォン）**と、**メール・会議・チャット・文書共有などのコラボレーション基盤**、およびそれらを配り、更新し、守る**端末管理**の領域である。全社員に直接届くため、変更の影響が大きく、ベンダーの製品の更新周期・サポート期限・ライセンス体系の変更に強く左右される。

## 定義

本資料では、ワークプレイスを次の3つの要素で扱う（本資料の整理）。

| 要素 | 内容 | 代表的な製品 |
|---|---|---|
| 端末 | PC の OS とハードウェア、スマートフォン、仮想デスクトップ | Windows、macOS、Windows 365、Azure Virtual Desktop |
| コラボレーション基盤 | メール、予定表、会議、チャット、文書の作成・保存・共有 | Microsoft 365、Google Workspace |
| 端末管理（UEM） | 端末の設定・アプリの配布・OS の更新・紛失時の対応を一元的に管理する | Microsoft Intune、Omnissa Workspace ONE |

## 成り立ち

| 年 | 出来事 | 意味 |
|---|---|---|
| 2020 | Microsoft が Office 365 の多くのプランを Microsoft 365 に改称（4月21日）。Google が G Suite を Google Workspace に改称（10月6日） | オフィスソフトの売り切りから、クラウドのサブスクリプションへの移行が完了する |
| 2021 | Microsoft が Windows 365（クラウド PC）を一般提供（8月2日） | OS そのものをクラウドから配る選択肢ができる |
| 2023 | Microsoft 365 Copilot を企業向けに一般提供（11月1日、1ユーザー月額30ドル） | 生成 AI がコラボレーション基盤に組み込まれる（→ ai） |
| 2024 | Microsoft が Teams を Microsoft 365・Office 365 から全世界で切り離す（4月1日）。新規の顧客は Teams を含まない版と Teams 単体を組み合わせる | コラボレーション基盤のライセンス体系が規制の影響で変わる |
| 2025 | Windows 10 のサポート終了（10月14日）。法人は有償の延長セキュリティ更新（ESU）を最長3年購入できる | OS のサポート期限が、端末の更新計画を決める |

## 範囲（何であり、何でないか）

| ワークプレイスが扱うもの | 扱わないもの（隣接領域） |
|---|---|
| PC・スマートフォンの OS とライフサイクル、仮想デスクトップ | ID とログインの基盤（identity） |
| Microsoft 365・Google Workspace などのコラボレーション基盤 | 端末上の攻撃の検知と対応（security-operations の EDR） |
| 端末管理（UEM）、OS とアプリの更新の配布 | サービスデスク・問い合わせ対応の運用（it-operations） |
| | 生成 AI の仕組みとリスク（ai） |

---

**出典**（確認日：2026-11-14）

- Office 365 から Microsoft 365 への改称：Computerworld（2020-03）— https://www.computerworld.com/article/1616773/microsoft-to-shift-smbs-office-subscriptions-to-microsoft-365-brand.html 、Microsoft ドイツのニュース — https://news.microsoft.com/de-de/produktivitaetssuite-fuer-kleine-und-mittelstaendische-unternehmen-heisst-jetzt-microsoft-365/
- G Suite から Google Workspace への改称：Google Workspace Updates（2020-10-06）— https://workspaceupdates.googleblog.com/2020/10/introducing-google-workspace.html
- Windows 365 の一般提供：Microsoft ニュース（2021-07-14）— https://news.microsoft.com/source/2021/07/14/microsoft-unveils-windows-365-ushering-in-a-new-category-of-computing/
- Microsoft 365 Copilot の一般提供と価格：Microsoft 365 ブログ（2023-09-21）— https://www.microsoft.com/en-us/microsoft-365/blog/2023/09/21/announcing-microsoft-365-copilot-general-availability/
- Teams の切り離し：Microsoft Tech Community（2024-04-01）— https://techcommunity.microsoft.com/t5/partner-news/important-notice-changes-to-microsoft-365-office-365-and/ba-p/4100985
- Windows 10 のサポート終了と ESU：Petri — https://petri.com/?p=762768 、TechRepublic — https://www.techrepublic.com/article/news-windows-10-esu-cheat-sheet/
- 3つの要素の分け方は本資料の整理
