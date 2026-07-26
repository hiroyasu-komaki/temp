# リポジトリ構成

- **出典**: 実装の棚卸し `[実装]`
- **最終更新**: 2026-07-25

> **本ファイルは、本ドキュメント群で唯一「実装ファイルの場所」を記述する場所である。**
> 設計章（01〜03）にはファイルパスを書かない。リファクタリング時に更新するのはここだけで済むようにするため。

---

## 1. リポジトリ方針

| 項目 | 方針 | 出所 |
|---|---|---|
| リポジトリ分割 | **モノレポ** | `[実装]` |
| パッケージ管理 | npm workspaces（`apps/*` + `packages/*`） | `[実装]` |
| 共有コード | `packages/schema` に集約 | `[資料]` → [ADR-0002](../02-architecture/05-adr/0002-schema-single-source.md) |

> モノレポ／npm workspaces の選定理由は**記録なし** `[未確認]`。
> ただし [ADR-0002](../02-architecture/05-adr/0002-schema-single-source.md)（スキーマ単一ソース）を実現するには、フロント・APIが同じパッケージを参照できる構成が必要であり、**モノレポは自然な帰結** `[推定]`。

---

## 2. ディレクトリ構成

```
procspec/
├─ apps/
│  ├─ api/                     NestJS + Prisma。案件API・ドラフトAPI
│  │  ├─ src/
│  │  │  ├─ cases/             案件CRUD・発番・初版作成・監査記録
│  │  │  ├─ drafts/            PATCH autosave・楽観ロック
│  │  │  ├─ auth/              DevAuthGuard（仮認証）・CurrentUser デコレータ
│  │  │  ├─ audit/             監査ログ記録サービス
│  │  │  ├─ common/            ZodValidationPipe
│  │  │  ├─ prisma/            PrismaService（Global モジュール）
│  │  │  └─ main.ts / app.module.ts
│  │  ├─ prisma/               schema.prisma・migrations・seed.ts・dev.db
│  │  └─ .env                  DATABASE_URL
│  └─ web/                     Next.js（App Router）
│     ├─ src/
│     │  ├─ app/               ルーティング（/、/cases/new、/cases/[id]、/cases/[id]/preview）
│     │  ├─ components/        step-fields.tsx（入力部品）
│     │  └─ lib/               api.ts・step-status.ts・providers.tsx
│     └─ .env.local            NEXT_PUBLIC_API_BASE
├─ packages/
│  └─ schema/                  ★ フロント/API共有の単一ソース
│     └─ src/                  contract-types / steps / case-answer.schema
│                              / case-status / case-input.schema / index
├─ .claude/skills/             server-start / server-stop / server-status
├─ .dev-logs/                  開発サーバのログ（Git管理外）
├─ .gitignore
├─ package.json                npm workspaces のルート
└─ README.md                   リポジトリ入口
```

### ⚠️ ドキュメント・一次資料はリポジトリ外にある

**procspec リポジトリに `requirement/` `devdocs/` `開発方針.md` は存在しない** `[実装]`。
これらは別の場所（`04_devdocs/`）にあり、本ドキュメント群もそこに置かれている。

| 対象 | 実際の場所 |
|---|---|
| 開発ドキュメント（本フォルダ） | `04_devdocs/devdoc-procspec/` |
| 一次資料（原本） | `04_devdocs/devdoc-procspec/00-overview/requirement/` |
| 旧・開発ドキュメント | `04_devdocs/devdoc/` |
| 旧・開発方針 | 一次資料と同階層 |

> ⚠️ **procspec の `README.md` は `./devdocs/` `./requirement/` `./開発方針.md` へリンクしているが、いずれも存在しない** `[実装]`。
> **リポジトリ入口のリンクが全て切れている状態。** → [バックログ](../06-roadmap/02-backlog.md)
>
> **判断が必要** `[未確認]`: ドキュメントをリポジトリに同梱するか、外部管理を正とするか。
> 同梱すればコードと版が揃い、実装変更と同時にドキュメントを更新できる（→ [README §5](../README.md) の「正」への切り替えと整合）。
> 外部管理のままなら、procspec の README を実態に合わせて直す必要がある。

---

## 3. 設計章 → 実装ファイルの対応

> **設計を実装で確認したいときの索引。** 設計章から実装を辿る唯一の経路。

| 設計章 | 対応する実装 |
|---|---|
| [業務ドメイン構造](../01-requirements/01-domain-structure.md) | `packages/schema/src/contract-types.ts`, `steps.ts` |
| [データモデル](../02-architecture/02-data-model.md) | `apps/api/prisma/schema.prisma` |
| [データモデル §4（JSON構造）](../02-architecture/02-data-model.md) | `packages/schema/src/case-answer.schema.ts` |
| [API設計](../02-architecture/03-api-design.md) | `apps/api/src/cases/`, `apps/api/src/drafts/` |
| [API設計 §5（認証）](../02-architecture/03-api-design.md) | `apps/api/src/auth/dev-auth.guard.ts` |
| [API設計 §6（監査）](../02-architecture/03-api-design.md) | `apps/api/src/audit/audit.service.ts` |
| [検証・エラー設計](../03-detail-design/04-validation-and-errors.md) | `apps/api/src/common/zod-validation.pipe.ts` |
| [画面設計](../03-detail-design/01-screen-design.md) | `apps/web/src/app/` |
| [画面設計 §4（状態バッジ）](../03-detail-design/01-screen-design.md) | `apps/web/src/lib/step-status.ts` |
| [入力部品仕様](../03-detail-design/02-input-components.md) | `apps/web/src/components/step-fields.tsx` |
| [状態遷移設計](../03-detail-design/03-state-transitions.md) | `packages/schema/src/case-status.ts`（定義のみ） |

---

## 4. 依存の向き

```
packages/schema  ←  apps/api   （@procspec/schema を検証・型に使用）
packages/schema  ←  apps/web   （@procspec/schema を型・検証・定義に使用）
```

**禁止する依存** `[推定]`

| 禁止 | 理由 |
|---|---|
| `apps/api` → `apps/web` | アプリ間の直接依存。共有が必要なら `packages/` へ |
| `apps/web` → `apps/api` | 同上（API呼び出しは HTTP 経由） |
| `packages/schema` → `apps/*` | 共有パッケージが個別アプリに依存すると循環する |

**現状**: 守られている `[実装]`。

> ⚠️ **`packages/schema` を変更したら `npm run build:schema` が必要** `[実装]`。
> `dist` を FE/BE が参照するため、忘れると古い定義で動く。**開発時の典型的なつまずき。**

---

## 5. レイヤー構成

### バックエンド（NestJS）

| レイヤー | 置くもの | 置かないもの | 遵守 |
|---|---|---|:--:|
| コントローラ | ルーティング、入出力の変換、`ZodValidationPipe` の適用、`CurrentUser` の取得 | ビジネスロジック、DB操作 | ✅ |
| サービス | ビジネスロジック、トランザクション境界、監査記録 | HTTP固有の処理 | ✅ |
| データアクセス | `PrismaService`（Global モジュール） | — | ✅ |

**この分離は [ADR-0007 以外で唯一、資料に明示された設計原則](../02-architecture/01-tech-stack.md)** `[資料]`。プランCのAI差し込みの受け口として機能する。

### フロントエンド（Next.js App Router）

| レイヤー | 置くもの | 現状 |
|---|---|---|
| `app/` | ルーティング、ページコンポーネント | ページに状態管理・autosave ロジックが集中 `[実装]` |
| `components/` | 入力部品 | `step-fields.tsx` に全ステップ分（404行） `[実装]` |
| `lib/` | API クライアント、状態判定、Provider | ✅ |

> ⚠️ **`app/cases/[id]/page.tsx` にウィザードの状態管理・autosave・競合処理が集中している** `[実装]`。
> フックへの切り出しがされていない。**テストを書きにくい構造** `[推定]`。→ [バックログ](../06-roadmap/02-backlog.md)
>
> ⚠️ **`step-fields.tsx` が404行で全ステップ分を含む** `[実装]`。セクション追加のたびに肥大する。
> → [拡張性への配慮 §4-1](../02-architecture/04-extensibility.md)

---

## 6. ファイル命名規則

| 対象 | 現状の規則 | 出所 |
|---|---|---|
| ディレクトリ | ケバブケース（`step-fields`, `dev-auth.guard`） | `[実装]` |
| NestJS ファイル | `{name}.{role}.ts`（`cases.service.ts`, `dev-auth.guard.ts`）※NestJS 慣例 | `[実装]` |
| React コンポーネント | ケバブケースのファイル名、PascalCase のエクスポート | `[実装]` |
| スキーマ | `{name}.schema.ts` または `{name}.ts` | `[実装]` |
| テスト | **規則なし**（テストが存在しない） | `[実装]` |

**明文化された規約は存在しない** `[未確認]`。上記は実装から読み取ったもの。

---

## 7. 設定ファイル・環境変数

| ファイル | 用途 | Git管理 |
|---|---|:--:|
| `apps/api/.env` | `DATABASE_URL` | ❌ |
| `apps/web/.env.local` | `NEXT_PUBLIC_API_BASE` | ❌ |
| **`.env.example`** | — | **存在しない** ⚠️ |

> ⚠️ **`.env.example` が無い** `[実装]`。`.gitignore` には `!.env.local.example` という除外の除外があるが、**該当ファイルが存在しない。**
> 新規参加者が「どの環境変数が必要か」を知る手段が無い。→ [バックログ](../06-roadmap/02-backlog.md)

**環境変数一覧** `[実装]`

| 変数名 | 用途 | 必須 | 既定値 |
|---|---|:--:|---|
| `DATABASE_URL` | Prisma の接続先 | ✅ | `file:./dev.db` |
| `NEXT_PUBLIC_API_BASE` | Web → API のベースURL | − | `http://localhost:3001` |
| `PORT` | API のポート | − | `3001` |

---

## 8. Git 管理外

```
node_modules/
dist/
.next/
*.tsbuildinfo
apps/api/prisma/dev.db          ローカルDB
apps/api/prisma/dev.db-journal
.env / .env.local
.dev-logs/                      開発サーバのログ
npm-debug.log*
```

出所: `.gitignore` `[実装]`。**秘匿情報を含みうるファイルは適切に除外されている** ✅

---

## 9. Claude Code スキル

`.claude/skills/` に開発サーバの操作スキルがある `[実装]`。

| スキル | 内容 |
|---|---|
| `server-start` | 依存インストール（初回）・schemaビルド・DB初期化（初回）・API/Web 起動 |
| `server-status` | API/Web の起動状況（pid・応答）を確認 |
| `server-stop` | ポート 3000/3001 の待受プロセスを停止 |

> **これらは開発補助であり、CI/CD の代替ではない** `[推定]`。CI/CD は未整備（WBS 1.1・14人日）`[資料]`。
> 詳細は [開発環境](./03-dev-environment.md)。

---

## 10. ドキュメントの配置

| 対象 | 場所 |
|---|---|
| 開発ドキュメント | `04_devdocs/devdoc-procspec/`（本フォルダ）※**リポジトリ外**（→ §2） |
| 一次資料（原本） | [`00-overview/requirement/`](../00-overview/requirement/) ※同上 |
| **API仕様（OpenAPI）** | **存在しない** ⚠️ → [バックログ](../06-roadmap/02-backlog.md) |
| リポジトリ入口 | `README.md`（devdocs へ誘導） |
| 旧・開発方針 | `開発方針.md`（内容は本ドキュメント群に再構成済み） |

> ⚠️ **`README.md` と `開発方針.md` が旧ドキュメント構成（`devdocs/00-overview/02-plan-abc-comparison.md` 等）を参照している** `[実装]`。
> 本ドキュメント群に差し替える際、**リンクの更新が必要。** → [バックログ](../06-roadmap/02-backlog.md)
