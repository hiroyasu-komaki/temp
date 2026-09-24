# 投資委員会 案件管理システム（CMS）開発ドキュメント

- **出典**: `02_concepts/governance/it-materiality-framework/chapters/04_process-redesign.md` ほか（→ [一次資料](./00-overview/03-source-materials.md)）
- **様式**: `04_devdocs/devdoc-template`（使い方は同フォルダの `USAGE-01-tailoring.md` / `USAGE-02-retrofit.md`）
- **最終更新**: 2026-09-23

投資委員会の審議プロセス（Step1〜Step4）を、会議ではなく文書と通知で進めるための案件管理システム。Microsoft 365 で構築する（画面＝Power Apps、ワークフロー＝Power Automate、データ＝SharePoint リスト、文書＝SharePoint ドキュメントライブラリ、通知＝Teams、申請時の自動生成＝AI）。

---

## 1. 着手時の判定（USAGE-01 §8）

**判定日**: 2026-09-23 ／ **判定者**: Hiroyasu ／ **進め方**: 実装なし → 00→08 の順に書く ／ **設計終了**: 2026-09-23（決定ログ #24）

| 軸 | 評価 | 点 |
|---|---|:--:|
| 規模 | ローコード。3〜20人月の見込み（TBD: 工数見積で確定） | 1 |
| 関与人数 | 事務局・IT部門の構築担当で3〜7名 | 1 |
| 想定寿命 | 審議制度の基盤として3年以上 | 2 |
| 変更コスト | データの持ち方（リスト構成）は後から変えにくい | 1 |
| 引継ぎ | IT部門内で運用を引き継ぐ | 1 |
| 規制・監査 | 社内基準（審議の監査証跡） | 1 |
| 契約形態 | 社内・予算管理あり | 1 |
| 段階開発 | 範囲①→②（AIエージェント）→③（伴走・台帳）の拡張が前提 | 2 |
| **合計** | | **10** |

**プロファイル**: **M（標準）**。10点で L との境界にあるため、変更コストの高い章は粒度を上げる。

**標準より粒度を上げる章**:

| 章 | 粒度 | 理由 |
|---|---|---|
| 02-architecture/02-data-model | G3 | SharePointリストの構成は稼働後の変更が難しく、範囲②③の受け口にもなる |
| 03-detail-design/03-state-transitions | G3 | 案件ステータスとSLAが審議プロセスそのもの |
| 01-requirements/05-roles-and-permissions | −（#24 で対象外） | 閲覧範囲は全員公開（#15・#16）となり、ロールと操作はデータモデル §2・状態遷移 §7 に書いたため |
| 00-overview/02-plan-comparison | G2 | 段階開発を採るため（M では △） |

**読み替える章**（Power Platform で構築するため）:

| 章 | 読み替え |
|---|---|
| 02-architecture/03-api-design | 独自APIは持たない。Power Automate フロー一覧・コネクタ・トリガの設計として書く |
| 04-implementation/02-repo-structure | ソリューション構成として、実装方針（04-01）§3 に統合（#24） |
| 04-implementation/03-dev-environment | 本番のみ（#23）。技術スタック §4 と実装方針（04-01）に統合（#24） |

**省略する章**:

| 章 | 理由 | 見直す条件 |
|---|---|---|
| 07-project/01-estimate-wbs | 社内開発で、工数・体制を契約や予算化の根拠として示す必要がない（決定ログ #21） | 外部委託する、または予算申請の根拠が必要になったとき |
| 07-project/02-team-and-skills | 同上 | 同上 |
| 01-02、01-05、02-04、03-02、03-04、04-02〜04、05 全体、06 全体、07-03、08-01 | 社内の業務効率化ツールのため設計を軽くまとめる。内容はほかの章に書いてある（各ファイルに参照先を記載。決定ログ #24） | 外部委託する、または範囲②③に着手するとき |

---

## 2. フォルダ構成と状態

`> 📝 記入ガイド:` が残っているファイル＝未着手・未完成。

| # | フォルダ | 状態 |
|---|---|---|
| 00 | [00-overview](./00-overview/) | 初版 |
| 01 | [01-requirements](./01-requirements/) | [業務ドメイン構造](./01-requirements/01-domain-structure.md)・[機能スコープ](./01-requirements/03-functional-scope.md)・[非機能要件](./01-requirements/04-non-functional.md) 初版 |
| 02 | [02-architecture](./02-architecture/) | [技術スタック](./02-architecture/01-tech-stack.md)・[データモデル](./02-architecture/02-data-model.md)・[フロー設計](./02-architecture/03-api-design.md)・[ADR](./02-architecture/05-adr/) 6本 |
| 03 | [03-detail-design](./03-detail-design/) | [画面設計](./03-detail-design/01-screen-design.md)（審議ワークベンチ、申請用アプリの申請後）・[状態遷移](./03-detail-design/03-state-transitions.md)・[申請画面の紙芝居](./03-detail-design/mockup-application-form/)・[審議ワークベンチの紙芝居](./03-detail-design/mockup-workbench/) |
| 04 | [04-implementation](./04-implementation/) | [実装方針](./04-implementation/01-implementation-policy.md)（構築の順番・作り方・稼働前の確認）1枚 |
| 05〜07 | | 対象外（#24。07 は #21） |
| 08 | [08-operations](./08-operations/) | [運用・引き継ぎ](./08-operations/02-operations-handover.md) 1枚 |
| — | [_templates](./_templates/) | 変数・決定ログ記入済み |

---

## 3. 運用ルール（テンプレートから継承）

- **スコープ判断の正は [機能スコープ](./01-requirements/03-functional-scope.md)**。ここに無い機能を作りたくなったら、先にこのファイルを更新する。
- **設計を変えたら ADR を残す**（[02-architecture/05-adr/](./02-architecture/05-adr/)）。
- **一次資料は改変しない**。一次資料は `02_concepts/governance/it-materiality-framework/` に原本のまま置き、本ドキュメントは二次資料とする。
- **制度（審議ルール）の変更は一次資料側で行う**。CMS側で運用ルールを先に決めたくなったら、決定ログの確認依頼に登録する。
- 各ファイルの冒頭に「出典」と「最終更新」を書く。

**規模を問わず必須の4章**: [機能スコープ](./01-requirements/03-functional-scope.md) ／ [データモデル](./02-architecture/02-data-model.md) ／ 開発環境 → [技術スタック §4](./02-architecture/01-tech-stack.md)・[実装方針](./04-implementation/01-implementation-policy.md) ／ バックログ → [決定ログの保留課題](./_templates/decision-log.md)
