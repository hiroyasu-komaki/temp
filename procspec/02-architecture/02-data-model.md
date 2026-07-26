# データモデル

- **出典**: 設計助言 §4 `[資料]` / 実装の棚卸し `[実装]`
- **最終更新**: 2026-07-25

---

## 1. モデリング方針

**基本方針**: 案件・提出のメタは列で正規化、回答本体は JSON で柔軟に持つハイブリッド `[資料]`（助言 §4）。

**狙い** `[資料]`

- 様式改訂・項目追加を**マイグレーション不要**で吸収する
- 集計・検索が必要な値（予算合計・類型など）は生成列／ビューで別途抽出する

**列に持つ / JSONに持つ の判断基準** `[推定]`

> 資料に明示的な基準はない。実装から読み取った実際の切り分けは以下。

| JSONに持つ（`case_answers.data`） | 列に持つ（`cases`） |
|---|---|
| 様式のセクション回答すべて | 一覧・検索に使う値（`title`, `contractPeriod`, `primaryType`） |
| 可変長リスト（`sla[]`, `eval[]`） | 状態（`status`）、発番（`caseNo`） |
| 条件付きで現れる項目（非機能のチェック配下） | 所有者（`createdById`）、部門（`dept`） |

> **注意: 一部の値が二重に保持されている** `[実装]`。`title`／`period`／`primary` は JSON 側と `cases` 列の両方にあり、`PATCH /drafts/:caseId` の中で同期している。
> 一覧表示のための非正規化と思われる `[推定]`。**同期漏れが起きうる構造**であり、`cases` を直接更新する経路が将来増えると破綻する。→ [ADR-0001](./05-adr/0001-jsonb-hybrid-data-model.md)

---

## 2. ER概要

```
User 1 ──< CaseRecord 1 ──< CaseAnswer   （版管理。isCurrent=true が現在版）
              │        1 ──< Attachment  （テーブルのみ。機能未実装）
              │        1 ──< AuditLog
User 1 ──────────────────< AuditLog
```

---

## 3. エンティティ定義

出所: `apps/api/prisma/schema.prisma` `[実装]`

### User

| 列 | 型 | 説明 | 今回使用 |
|---|---|---|:--:|
| `id` | uuid | | ✅ |
| `name` | String | | ✅ |
| `email` | String (unique) | 仮認証のキー | ✅ |
| `role` | `UserRole` | `creator`/`dept_head`/`vmo`/`viewer`。既定 `creator` | **❌** |
| `createdAt` | DateTime | | ✅ |

> **`role` は定義のみで、認可判定に一度も使われていない** `[実装]`。将来の RBAC 実装のための先取りと思われる `[推定]`。
> → [ロールと権限 §5](../01-requirements/05-roles-and-permissions.md)

### CaseRecord（`cases`）

| 列 | 型 | 説明 | 今回使用 |
|---|---|---|:--:|
| `id` | uuid | | ✅ |
| `caseNo` | String (unique) | サーバ発番。形式 `C-YYYY-NNNN` | ✅ |
| `title` | String | JSON側と二重保持 | ✅ |
| `contractPeriod` | String | 同上 | ✅ |
| `primaryType` | String? | 同上。例 `"A-2"` | ✅ |
| `status` | `CaseStatus` | 既定 `draft`。**遷移APIが無いため常に `draft`** | ◐ |
| `createdById` | FK → User | | ✅ |
| `dept` | String | **常に空文字**（入力経路が無い） | **❌** |
| `createdAt` / `updatedAt` | DateTime | | ✅ |

> **`dept` が使われていない** `[実装]`。`CreateCaseSchema` に項目はあるが、UI から送られていない。
> 助言 §3-4 の RBAC「部門単位の閲覧」に必要になる列 `[推定]`。**先取りではなく実装漏れの可能性がある** `[未確認]`。

**助言 §4 が挙げるが未実装の列**: `secondary_types`（`text[]`・副類型）`[資料]`

### CaseAnswer（`case_answers`）★版管理の要

| 列 | 型 | 説明 |
|---|---|---|
| `id` | uuid | |
| `caseId` | FK → CaseRecord | |
| `version` | Int | 楽観ロックのキー。1 起点 |
| `data` | **String** | JSON文字列。**Postgres移行時は `Json`(jsonb) に変更** `[実装]`（コードコメントに明記） |
| `isCurrent` | Boolean | 現在版フラグ |
| `updatedById` | String | **FK制約なし**（`User` へのリレーション未定義）`[実装]` |
| `updatedAt` | DateTime | |

**インデックス**: `@@index([caseId, isCurrent])` `[実装]`

> `updatedById` に FK 制約が無いのは実装漏れと思われる `[推定]`。`CaseRecord.createdById` や `AuditLog.actorId` には制約がある。

### Attachment（`attachments`）

| 列 | 型 | 今回使用 |
|---|---|:--:|
| `id` / `caseId` / `sectionKey` | | ❌ |
| `fileName` / `sizeBytes` / `mime` / `storageKey` | | ❌ |
| **`scanStatus`** | String? (`pending`\|`clean`\|`infected`) | ❌ **先取り** |
| **`provisionCondition`** | String? (`unconditional`\|`nda_required`) | ❌ **先取り** |
| `uploadedById` / `uploadedAt` | | ❌ |

> **テーブル全体が未使用** `[実装]`。添付機能そのものが未実装のため。
> `scanStatus` / `provisionCondition` は**明示的な先取り**（コードコメントに「B/C向けの拡張列（Aでは未使用。§6 拡張性への配慮に基づき先取りして確保）」と記載）`[実装]`。**これは意図が明確に残っている数少ない例。**

### AuditLog（`audit_log`）

| 列 | 型 | 説明 |
|---|---|---|
| `id` / `caseId` / `actorId` | | |
| `action` | String | `case.create` / `draft.patch` のみ記録 `[実装]` |
| `fieldPath` | String? | `draft.patch` 時は変更キーをカンマ連結 |
| `before` / `after` | String? | **JSON全体**を保存（差分ではない） |
| `at` | DateTime | |

> **`before`/`after` に回答本体の全体が入る** `[実装]`。autosave のたびに記録されるため、**監査ログのサイズが版と同じ速度で増える。**
> 助言 §4 は「誰が・いつ・どの項目を・どう変えたか」を想定しており `[資料]`、全体スナップショットは意図とずれる `[推定]`。→ [バックログ](../06-roadmap/02-backlog.md)

---

## 4. 回答本体（`case_answers.data`）の構造

Zod スキーマ `CaseAnswerDataSchema` が単一ソース `[実装]`。**autosave で部分入力を許すため全項目 optional** `[実装]`。

| セクション | キー |
|---|---|
| 0. 案件情報 | `title` / `period` / `primary` |
| 1〜3. 自由記述 | `s1_text` / `s2_text` / `s3_text` |
| 4. 非機能要件 | `ck_perf`,`nf_perf`,`nf_perf_u` / `ck_avail`,`nf_avail`,`nf_rto`,`nf_rpo` / `ck_sec`,`nf_sso`,`nf_log` / `ck_reg`,`reg_gxp`,`reg_pi`,`reg_sox` / `nf_note` |
| 4-2. SLA | `sla: SlaRow[]`（`metric`/`target`/`measure`/`penalty`） |
| 5. 制約・予算 | `b_init`/`b_run`/`b_lic` / `d_rfp`/`d_go` / `s5_text` |
| 11. 評価配点 | `eval: EvalRow[]`（`criterion`/`weight`/`viewpoint`） |

詳細は [業務ドメイン構造 §4](../01-requirements/01-domain-structure.md)。

> **全項目 optional の副作用** `[推定]`: 提出時の必須チェックを行う仕組みが**別途必要**だが、実装されていない。
> 「下書きでは緩く、提出時は厳しく」の二段構えが原則（→ [検証・エラー設計](../03-detail-design/04-validation-and-errors.md)）だが、**後段が存在しない。**

---

## 5. 版管理と楽観ロック

**方式**: 追記型。autosave のたびに新版（`version+1`）を `isCurrent=true` で作成し、旧版を `isCurrent=false` にする `[実装]`。

**狙い** `[資料]`: 誤操作の復元・監査差分・差戻し時の比較（助言 §3-6「サーバは各PATCHをバージョン付きで履歴保存」）。

**楽観ロックの流れ** `[実装]`（`DraftsService.patch`、トランザクション内）

1. 現在版（`isCurrent=true`）を取得
2. クライアントの `version` と不一致なら **409 Conflict**（`currentVersion` を返す）
3. 一致すれば既存データに `patch.data` をマージ（JSON Merge Patch 相当）
4. 旧版を `isCurrent=false` にし、`version+1` の新版を作成
5. `cases` のメタ列（`title`/`contractPeriod`/`primaryType`）を同期
6. 監査ログ（`draft.patch`）を記録

> ⚠️ **版が無制限に増える** `[実装]`。デバウンス800ms の autosave ごとに1版が作られるため、
> 1件の仕様書を1時間編集すると**数百〜千版**に達しうる。刈り込み・世代管理の仕組みは無い。
> 助言に版数の管理方針の記載は無く、**意図的な設計か検討漏れかは不明** `[未確認]`。
> → [ADR-0003](./05-adr/0003-optimistic-lock-append-version.md)、[バックログ](../06-roadmap/02-backlog.md)

---

## 6. 現行（SQLite）と本番（PostgreSQL）の差分

| 観点 | 開発（SQLite） | 本番（PostgreSQL） | 切替 |
|---|---|---|---|
| provider | `sqlite` | `postgresql` | `schema.prisma` |
| `data` 型 | `String`（`JSON.parse`/`stringify`） | `Json`（jsonb） | 型変更＋マイグレーション |
| 接続 | `file:./dev.db` | 接続文字列 | `DATABASE_URL` |
| 集計 | アプリ側で計算 | 生成列/ビューで抽出可能 `[資料]` | — |

`schema.prisma` 冒頭に移行方法のコメントあり `[実装]`。→ [ADR-0004](./05-adr/0004-sqlite-for-development.md)

> **移行の未検証リスク** `[推定]`: `data` を `String` から `Json` に変えると、アプリ側の `JSON.parse`/`stringify` が不要になる。
> **この呼び出しは `CasesService.toDto` / `DraftsService.patch` に散在しており**、移行時に全て見直す必要がある。移行手順書は存在しない。

---

## 7. 助言が想定するが未実装のテーブル

| テーブル | 用途 | 出所 | 判断 |
|---|---|---|---|
| `evaluations` | 評価項目・配点（`locked` 列で凍結） | `[資料]` 助言 §4 | 現在は `data.eval` に内包。→ [ADR-0001](./05-adr/0001-jsonb-hybrid-data-model.md) |
| `clauses` | 標準条項の適用状態 | `[資料]` 助言 §4 | プランB（条項管理）で必要 |
| `roles` / `case_roles` | 案件単位の権限 | `[資料]` 助言 §4 | RBAC 本実装で必要 |
| `secondary_types` | 副類型（`cases` の列） | `[資料]` 助言 §4 | 未実装 |

> **開発方針 §4 は `evaluations` の `locked` 列を「Aでは将来拡張用に持つ」と書いているが、テーブル自体が存在しない** `[実装]`。
> → [一次資料との対応 §4-5](../00-overview/03-source-materials.md)。**開発方針の記述が実態と食い違っている。**

---

## 8. データ量見積

| エンティティ | 想定 |
|---|---|
| `cases` | **未定義** `[未確認]` |
| `case_answers` | **案件数 × 編集操作数**。§5 の通り無制限に増える |
| `audit_log` | `case_answers` と同数以上（全体スナップショット付き） |
| `attachments` | 未実装 |

> **性能要件が未定義のため、データ量の妥当性を判断できない** `[未確認]`。→ [非機能要件](../01-requirements/04-non-functional.md)
> ただし §5 の版増加は、**要件値が何であれ問題になる可能性が高い** `[推定]`。

---

## 9. マイグレーション運用

| 項目 | 現状 | 出所 |
|---|---|---|
| ツール | Prisma Migrate | `[実装]` |
| 既存マイグレーション | `20260724123008_init` の1件のみ | `[実装]` |
| 命名規則 | **未定義** `[未確認]` | — |
| 本番適用の手順・承認 | **未定義** `[未確認]` | — |
| ロールバック方針 | **未定義** `[未確認]` | — |
| シードデータ | `prisma/seed.ts`（デモユーザー1名のみ） | `[実装]` |

---

## 10. 拡張時の指針

- **列を先取りする** — `Attachment.scanStatus`/`provisionCondition` の先例に倣う。ただし**先取りの理由をコメントで残すこと**（残っていない列は削除されうる）。
- **集計・検索が必要になった項目は、JSONから生成列/ビューへ抽出する** `[資料]`。`data` の柔軟さと検索性を両立させる。
- **`cases` への非正規化コピーを増やさない** `[推定]` — §1 の二重保持は既に同期処理を必要としている。増やすほど破綻しやすくなる。

→ 判断基準は [拡張性への配慮](./04-extensibility.md)。
