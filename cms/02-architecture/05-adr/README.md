# ADR（Architecture Decision Records）

重要な設計判断の記録。書き方は [`_templates/adr-template.md`](../../_templates/adr-template.md)。既存ADRは書き換えず、覆すときは新しいADRを起こして旧ADRを「置換済み」にする。

## 一覧

| # | 決定 | ステータス | 決定日 | 関連 |
|---|---|---|---|---|
| [0001](./0001-platform-microsoft-365.md) | Microsoft 365（SharePoint／Power Apps／Power Automate／Teams）で構築する | 承認 | 2026-09-23 | 技術スタック |
| [0002](./0002-scope-case-management-and-workflow-only.md) | 今回は案件管理とワークフローに限り、AIエージェントと Step4 伴走は作らない | 承認 | 2026-09-23 | 機能スコープ |
| [0003](./0003-intake-forms-and-copilot-precheck.md) | 申請は Forms＋手元資料の添付とし、提出前に Copilot で不足を確認する | 置換済み（→ 0004） | 2026-09-23 | 機能スコープ、入力部品 |
| [0004](./0004-intake-power-apps-and-ai-generated-proposal.md) | 申請画面は Power Apps とし、添付資料から案件概要書の入力項目を AI で自動生成する | 承認 | 2026-09-23 | 機能スコープ、画面設計、入力部品 |
| [0005](./0005-writes-via-flows-and-private-drafts.md) | 書き込みはすべてフロー（サービスアカウント）経由とし、下書きは本人専用のリストに置く | 承認 | 2026-09-23 | データモデル |
| [0006](./0006-two-apps-intake-and-workbench.md) | アプリを「IT投資 申請」と「審議ワークベンチ」の2本に分ける | 承認 | 2026-09-23 | 技術スタック |
