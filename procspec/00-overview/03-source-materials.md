# 一次資料との対応

- **最終更新**: 2026-07-25
- **注記**: 本ファイルは後追い文書化の **Step 1**（最初に作成）。以降の全記述の出所の基準になる。

---

## 1. 一次資料の一覧

一次資料は [`00-overview/requirement/`](./requirement/) に原本のまま置く。**改変しない。**

> **配置についての注記**: 一次資料は本ドキュメント群と同階層（`04_devdocs/requirement/`）ではなく、
> **本章の配下**に置いている。文書の入口（00-overview）で資料に到達できる利点がある一方、
> **「原本は派生文書と分離して置く」という一般的な原則からは外れる**配置である。
> 参照する側（`01-requirements/` 以降）からは `../00-overview/requirement/` となる点に注意。

**格納場所**: [`00-overview/requirement/`](./requirement/)

| # | ファイル | 種別 | 内容 | 出所 |
|---|---|---|---|---|
| 1 | `Form2_本番実装_設計アドバイス.md` | 設計助言 | UI/UX・アーキテクチャアドバイザーによる本番化提言。診断→UX方針→技術選定→データモデル→AI→ロードマップ | `[資料]` |
| 2 | `Form2_概算見積書.xlsx` | 見積 | 5シート（サマリ・プラン比較／WBS・工数明細／体制・SFIA／SFIA参照／前提・除外・リスク） | `[資料]` |
| 3 | `Form2_Prototype_Improved.html` | プロトタイプ | 610行の単一HTML。ウィザード・localStorage保存・AIパネルのUIモック | `[資料]` |
| 4 | `開発方針.md` | 二次資料 | 上記1〜3をプランAスコープに絞り込んだ開発方針。**procspec リポジトリ側にある** | `[資料]` |

> `開発方針.md` は一次資料ではなく、資料1〜3から作られた二次資料。本ドキュメント群と同じ層にあたる。内容は本ドキュメント群に再構成済み。

---

## 2. 一次資料 → 本ドキュメントの対応

| 一次資料・該当箇所 | 本ドキュメントの対応先 | 扱い |
|---|---|---|
| 助言 §0・§1（診断） | [プロダクトビジョン §2](./01-product-vision.md) | 全面反映 |
| 助言 §2（UI/UX方針） | [UX設計原則](../01-requirements/02-ux-design-principles.md) | 全面反映 |
| 助言 §3（技術選定） | [技術スタック](../02-architecture/01-tech-stack.md)、[ADR-0002](../02-architecture/05-adr/0002-schema-single-source.md) | 反映＋一部差異（→ §4） |
| 助言 §3-6（autosave設計） | [API設計 §4](../02-architecture/03-api-design.md)、[ADR-0003](../02-architecture/05-adr/0003-optimistic-lock-append-version.md) | 全面反映 |
| 助言 §4（データモデル） | [データモデル](../02-architecture/02-data-model.md)、[ADR-0001](../02-architecture/05-adr/0001-jsonb-hybrid-data-model.md) | 反映＋一部未実装（→ §4） |
| 助言 §5（AI設計） | [プランC](../06-roadmap/03-future-plans.md) | プランA対象外として持ち越し |
| 助言 §6（ロードマップ） | [フェーズ計画](../06-roadmap/01-phase-plan.md) | 見積WBSの区分を優先して再構成 |
| 助言 §7（チェックリスト） | [バックログ](../06-roadmap/02-backlog.md) | 未達項目を転記 |
| 見積 サマリ・プラン比較 | [プラン比較](./02-plan-comparison.md) | 転記 |
| 見積 WBS・工数明細 | [WBS・工数明細](../07-project/01-estimate-wbs.md) | 転記 |
| 見積 体制・SFIA／SFIA参照 | [体制・スキル](../07-project/02-team-and-skills.md) | 転記 |
| 見積 前提・除外・リスク | [前提・除外・リスク](../07-project/03-assumptions-risks.md) | 転記 |
| プロトタイプ `TYPES` `RULES` `STEPS` | [業務ドメイン構造](../01-requirements/01-domain-structure.md) | 定義として資産化 |
| プロトタイプ 入力部品 | [入力部品仕様](../03-detail-design/02-input-components.md) | 反映 |
| プロトタイプ AIパネル | — | ⛔ プランA対象外。UIモックのまま残置 `[資料]` |

---

## 3. 資料の欠落

| 欠落しているもの | 影響 |
|---|---|
| **設計助言が対象とする `Form2_Procurement_Specification.html`（原本モック）** | 助言 §1 の診断内容を実物で確認できない。`requirement/` にあるのは `Form2_Prototype_Improved.html`（改善版） |
| **様式2 の原本（14セクションの定義）** | 助言・見積・開発方針が「14セクション」を前提とするが、その定義書が無い。**プランB/Cでセクションを追加する際に必須** → [decision-log](../_templates/decision-log.md) |
| **トライアルのフィードバック原文** | 4つの不満は助言 §1 の要約でしか読めない。UATのベースライン値も無い |
| **標準条項・評価テンプレのマスタ** | プランBのテンプレ管理画面の実装に必要 |
| **議事録・意思決定の記録** | 技術選定の経緯が一切残っていない。→ ADRの復元が推測に依存する原因 |

---

## 4. 資料と実装／資料間の食い違い ★重要

> **後追い文書化で最も価値のある発見。** 読み進める前に必ず目を通すこと。

| # | 食い違い | 詳細 | 判断 | 出所 |
|---|---|---|---|---|
| **1** | **助言の診断対象と、残っているプロトタイプが別物** | 助言は「`Form2_Procurement_Specification.html` を対象」と明記。`requirement/` にあるのは `Form2_Prototype_Improved.html` | Improved は診断後に作られた改善版と思われる。**助言 §1 の診断は Improved には当てはまらない** | `[推定]` |
| **2** | **「途中保存できない」の診断が Improved では解消済み** | 助言 §1 は「`localStorage` も `fetch` も無い。リロードで全消失」と診断。しかし Improved には localStorage 保存（デバウンス700ms）が実装されている | 診断→改善版作成、の順と思われる。**プランAが解く課題は「localStorage ではなくサーバ状態を持つこと」**（複数端末・監査・競合制御） | `[推定]` |
| **3** | **`data-ja/data-en` が存在しない** | 助言 §1・§3-2 は「多言語は DOM の `data-ja/data-en` で実装済み、辞書へ移行が必要」とする。Improved 内の該当属性は **0件** | 原本モックには存在し、Improved で削除された可能性。**プランBのi18n着手時に「移行元が無い」ことになる** | `[未確認]` |
| **4** | **セクション数の不一致** | 助言・見積・開発方針は「14セクション」前提。Improved のセクションは 0／1／2／3／4／4-2／5／11 の **8つのみ** | Improved の時点で既に絞り込み済み。**procspec は「14のうちA分を抜粋」したのではなく「Improved をそのまま実装」したのが実態** | `[推定]` |
| **5** | **開発方針が挙げるテーブルの一部が未実装** | 開発方針 §4 は `evaluations`（`locked` 列）・`clauses`・`secondary_types`・`roles`/`case_roles` を挙げるが、実装は5モデルのみ | 意図的な見送りか実装漏れか不明。**評価配点は `case_answers.data.eval` に内包されている** | `[未確認]` |

### この食い違いが意味すること

**#4 が最も重要。** 「14セクションのうちプランA分を実装した」のではなく、「既に8セクションに絞られた Improved 版を実装した」のが実態である。

→ **プランB/Cで「残りのセクションを追加する」際、追加対象の定義が一次資料に存在しない**（§3 の欠落）。セクション追加は「定義追加で済む」設計になっている（→ [拡張性](../02-architecture/04-extensibility.md)）が、**追加する内容そのものが未定**。これは設計の問題ではなく、要件の問題として [前提条件](../07-project/03-assumptions-risks.md) に登録している。

---

## 5. 一次資料から変更した点

| 一次資料の記述 | 実装での扱い | 理由 | 合意 | 記録 |
|---|---|---|---|---|
| DB は PostgreSQL（助言 §4） | 開発は SQLite | ゼロセットアップ性 `[推定]` | 不明 | [ADR-0004](../02-architecture/05-adr/0004-sqlite-for-development.md) |
| 認証は OIDC/SSO（助言 §3-4） | `x-user-email` ヘッダの仮認証 | 実IdP接続情報が未提供 `[実装]`（コードコメントに明記） | — | [ADR-0005](../02-architecture/05-adr/0005-dev-auth-guard.md) |
| OpenAPI で契約を先に定義（助言 §3-3） | 未作成。コード先行 | 不明 | 不明 | [バックログ](../06-roadmap/02-backlog.md) |
| `evaluations` テーブル（助言 §4） | `case_answers.data.eval` に内包 | 不明 | 不明 | [ADR-0001](../02-architecture/05-adr/0001-jsonb-hybrid-data-model.md) |
| autosave はフィールド単位の差分PATCH（助言 §3-6） | フォーム全体をマージ送信 | 不明 | 不明 | [バックログ](../06-roadmap/02-backlog.md) |
| デバウンス 1〜2秒（助言 §2-3）／プロトタイプ 700ms | 800ms | **根拠不明** | — | [ADR-0003](../02-architecture/05-adr/0003-optimistic-lock-append-version.md) |

**いずれも発注元の合意記録が残っていない。** `[未確認]` として [decision-log](../_templates/decision-log.md) に登録済み。

---

## 6. 優先順位のルール

| 対象 | 正とするもの |
|---|---|
| スコープ判断 | [機能スコープ](../01-requirements/03-functional-scope.md) |
| 設計判断 | [ADR](../02-architecture/05-adr/) |
| 工数・体制・契約条件 | **一次資料（見積書）**。本ドキュメントで変えない |
| 現時点の実装挙動 | **実装コード**（本ドキュメントが「正」になるまでの暫定。→ [README §5](../README.md)） |
