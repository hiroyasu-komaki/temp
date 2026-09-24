# プレースホルダ変数一覧

- **最終更新**: 2026-09-23

各ドキュメントで使う `{{変数名}}` の定義。値はこの表を正とする。

## 置換手順

```bash
cd cms
grep -rl '{{PRODUCT_NAME}}' . | xargs sed -i '' 's/{{PRODUCT_NAME}}/実際の名前/g'
# 未置換の変数が残っていないか確認
grep -rno '{{[A-Z_]\{2,\}}}' . | sort -u
```

## 変数定義

| 変数 | 意味 | 本プロジェクトの値 |
|---|---|---|
| `{{PRODUCT_NAME}}` | プロダクト名 | 投資委員会 案件管理システム（CMS） |
| `{{REPO_NAME}}` | リポジトリ名／ソリューション名 | cms（Power Platform ソリューション名：TBD） |
| `{{CLIENT_NAME}}` | 依頼部門 | 投資委員会 事務局 |
| `{{TARGET_USERS}}` | 主たる利用者 | 起案者（事業部門）、事務局、審査担当者、投資委員会メンバー、PPM |
| `{{PLAN_LABELS}}` | 段階プランの呼称 | ① 案件管理・ワークフロー ／ ② AIエージェント事務局 ／ ③ 伴走・台帳 |
| `{{CURRENT_PLAN}}` | 今回のスコープ | ① |
| `{{PHASE_LABELS}}` | フェーズ区分 | TBD（06-roadmap で決める） |
| `{{FE_FRAMEWORK}}` | 画面 | Power Apps キャンバスアプリ（申請・事務局・委員会・担当者） |
| `{{BE_FRAMEWORK}}` | 処理 | Power Automate（標準コネクタのみ） |
| `{{DATABASE}}` | データ | SharePoint Online（リスト＋ドキュメントライブラリ） |
| `{{AUTH_METHOD}}` | 認証 | Microsoft Entra ID（M365 サインイン）。権限は M365 グループ／SharePoint 権限で制御 |
| `{{SHARED_PACKAGE}}` | 共有定義 | 対象外（Power Platform 環境変数・選択肢列で代替） |
| `{{WEB_PORT}}` / `{{API_PORT}}` | 開発時ポート | 対象外 |
| `{{TOTAL_EFFORT}}` / `{{DURATION}}` | 工数・期間 | TBD |
| `{{PM_NAME}}` 他 | 担当者名 | TBD |

## 汎用プレースホルダ（一括置換の対象外）

| 記法 | 意味 |
|---|---|
| `{{N}}` | 任意の数値 |
| `{{}}` | その場で埋める自由記述 |
| `{{日本語の説明}}` | 何を書くかの指示 |

## プロジェクト固有で追加した変数

| 変数 | 意味 | 値 |
|---|---|---|
| `{{SITE_NAME}}` | CMS の SharePoint サイト | TBD |
| `{{SLA_*}}` | 各ステップの期限（営業日） | 作成・回付 3／確認 3／審議 3／回答書確認 2／議論要請 3（決定ログ #12） |
