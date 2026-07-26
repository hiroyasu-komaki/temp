# 開発環境セットアップ

- **出典**: 実装の棚卸し `[実装]` / procspec README `[実装]`
- **最終更新**: 2026-07-25

> **合格条件は「新しく参加した開発者が、この手順だけで動く状態にできること」。**
> ⚠️ **本手順はまだ第三者による検証を受けていない** `[未確認]`。新メンバーが参加したら、この手順だけでセットアップしてもらい、詰まった箇所をその場で追記すること。**書いた本人は自分の環境で動くので気づけない。**

---

## 1. 前提ソフトウェア

| ソフトウェア | バージョン | 必須 | 備考 |
|---|---|:--:|---|
| Node.js | **未指定** `[実装]` | ✅ | Next 16 / React 19 / NestJS 11 が動作する版が必要 |
| npm | Node.js 同梱 | ✅ | workspaces を使用 |

> ⚠️ **Node.js のバージョンが固定されていない** `[実装]`。`.node-version` / `.tool-versions` / `package.json` の `engines` いずれも無い。
> **環境差による不具合の温床。** → [バックログ](../06-roadmap/02-backlog.md)

**DB は不要** — 開発は SQLite（ファイル）を使うため `[実装]`（→ [ADR-0004](../02-architecture/05-adr/0004-sqlite-for-development.md)）。

---

## 2. 初回セットアップ

### 2-1. Claude Code スキルを使う場合（推奨）

```
/server-start
```

依存インストール（初回）・schema ビルド・DB初期化（初回）・API/Web の起動をまとめて行う `[実装]`。

### 2-2. 手動で行う場合（上記と等価）

```bash
# 1. 依存関係のインストール
npm install

# 2. 共有スキーマのビルド（★必須。FE/BE が dist を参照する）
npm run build:schema

# 3. データベースの初期化（初回のみ）
cd apps/api
npx prisma migrate dev --name init     # dev.db を作成
npx ts-node prisma/seed.ts             # デモユーザーを作成
cd ../..
```

> ⚠️ **環境変数の設定手順が抜けている** `[実装]`。`.env.example` が存在しないため、
> `apps/api/.env`（`DATABASE_URL`）と `apps/web/.env.local`（`NEXT_PUBLIC_API_BASE`）を**手で作る必要があるか、既定値で動くかが不明** `[未確認]`。
> リポジトリには `.env` が存在するが Git 管理外のため、**clone した状態では無い。**
> → [バックログ](../06-roadmap/02-backlog.md)。必要な内容は [リポジトリ構成 §7](./02-repo-structure.md)。

---

## 3. 起動

```bash
npm run dev:api   # http://localhost:3001
npm run dev:web   # http://localhost:3000
```

| サービス | URL | 実体 |
|---|---|---|
| Web（Next.js） | http://localhost:3000 | `apps/web` |
| API（NestJS） | http://localhost:3001 | `apps/api`。`PORT` で変更可 |

**起動確認**: http://localhost:3000 を開き、案件一覧が表示されれば成功 `[実装]`。

---

## 4. 動作確認シナリオ

> **「起動した」ではなく「主要フローが通った」まで確認する。**

1. `/` を開く → 案件一覧（初回は空）
2. 「＋ 新規案件」→ 件名を入力し、契約類型を選択 → 作成
3. ウィザードで各ステップに入力 → **ヘッダに「保存しました」が出る**
4. **ブラウザをリロード** → 入力内容が復元される（← 本システムの中核価値）
5. ステップ11で配点を入力 → 合計100 で「✓ 適正」が出る
6. ステップ5で予算を入力 → 合計が自動計算される
7. 「プレビュー」→ 全体が1枚で表示される → 印刷ダイアログが開く
8. `/` に戻る → 作成した案件が一覧に出る

---

## 5. よく使うコマンド

| コマンド | 内容 | 出所 |
|---|---|---|
| `npm run dev:api` | API を start:dev で起動 | `[実装]` |
| `npm run dev:web` | Web を dev で起動 | `[実装]` |
| `npm run build:schema` | `packages/schema` をビルド | `[実装]` |
| `npx prisma migrate dev` | DBスキーマ変更の反映（`apps/api` で実行） | `[実装]` |
| `npx prisma studio` | DBの中身をGUIで確認（`apps/api` で実行） | `[推定]` |
| **テスト** | **存在しない** | `[実装]` |
| **リント・フォーマット** | **設定されていない** | `[実装]` |
| **型チェック（単体）** | ルートスクリプトなし | `[実装]` |

> ⚠️ **リンタ・フォーマッタが設定されていない** `[実装]`。コードスタイルの統一が人力に依存する。
> → [コーディング規約](./04-coding-standards.md)、[バックログ](../06-roadmap/02-backlog.md)

---

## 6. 開発時の注意 ★

| 状況 | 必要な操作 | 忘れると |
|---|---|---|
| **`packages/schema` を変更した** | **`npm run build:schema` を再実行** | FE/BE が古い定義を参照し、原因不明の型エラー・検証エラーになる |
| `prisma/schema.prisma` を変更した | `npx prisma migrate dev` | Prisma Client が古いまま |
| 依存関係が更新された | `npm install` ＋ `npm run build:schema` | — |

> **1つ目が最も踏みやすい。** `packages/schema` は FE/BE 双方が `dist` を参照しているため、ソースを直しただけでは反映されない `[実装]`。

---

## 7. トラブルシューティング

| 症状 | 原因 | 対処 |
|---|---|---|
| 型エラー／`@procspec/schema` が見つからない | schema 未ビルド | `npm run build:schema` |
| 401 「未知のユーザーです」 | seed 未実行、または `x-user-email` が未登録 | `npx ts-node prisma/seed.ts` を実行 |
| DBが見つからない | `prisma migrate dev` 未実行 | `apps/api` で実行 |
| ポートが使用中 | 前回のプロセスが残留 | `/server-stop`、または該当ポートのプロセスを停止 |
| API に繋がらない | `NEXT_PUBLIC_API_BASE` の不一致 | `apps/web/.env.local` を確認 |

> 本表は実装から推測したもので、**実際に踏まれた事象の記録ではない** `[推定]`。詰まった事象があれば都度追記すること。

---

## 8. 開発時の認証・テストデータ

| 項目 | 内容 | 出所 |
|---|---|---|
| 既定ユーザー | `demo.creator@example.com`（役割 `creator`） | `[実装]` |
| ユーザーの切り替え | リクエストの `x-user-email` ヘッダを変更。未知のメールは 401 | `[実装]` |
| **他ロールでの動作確認** | **seed に `creator` 1名しかいない。** 他ロールのユーザーは手動作成が必要 | `[実装]` |
| テストデータの投入 | `prisma/seed.ts`（ユーザーのみ。案件データは無し） | `[実装]` |
| データのリセット | `apps/api/prisma/dev.db` を削除 → `prisma migrate dev` `[推定]` | — |

> ⚠️ **`dept_head` / `vmo` / `viewer` のユーザーが seed に無い** `[実装]`。
> 認可を実装する際、**ロール別の動作確認ができない。** seed の拡充が必要 `[推定]`。

---

## 9. ログの確認場所

| 対象 | 場所 | 出所 |
|---|---|---|
| API（スキル起動時） | `.dev-logs/api.log` | `[実装]` |
| Web（スキル起動時） | `.dev-logs/web.log` | `[実装]` |
| API（手動起動時） | 標準出力 | `[実装]` |

---

## 10. 未整備の環境

| 項目 | 状態 | 出所 |
|---|---|---|
| CI/CD | **なし**（WBS 1.1・14人日が未着手） | `[資料]` |
| ステージング環境 | **なし** | `[実装]` |
| 本番環境 | **なし**（クラウド環境が未払い出し） | `[未確認]` |
| Docker / devcontainer | **なし** | `[実装]` |
| リンタ・フォーマッタ | **なし** | `[実装]` |
| テスト実行環境 | **なし** | `[実装]` |

→ [バックログ](../06-roadmap/02-backlog.md)、[技術スタック §5](../02-architecture/01-tech-stack.md)
