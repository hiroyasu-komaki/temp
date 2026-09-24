# フロー設計（API設計の読み替え）

- **出典**: [状態遷移](../03-detail-design/03-state-transitions.md) §4・§5・§7 / [データモデル](./02-data-model.md) / [ADR-0005](./05-adr/0005-writes-via-flows-and-private-drafts.md)
- **最終更新**: 2026-09-23
- **状態**: 初版

CMS は独自の API を持たない。**画面の操作 → Power Automate のフロー → 検証 → 書き込み → 記録 → 通知** の組み合わせを、ここでは API として定義する（README §1 の読み替え）。

---

## 1. 設計方針

| 項目 | 方針 |
|---|---|
| 呼び出し方 | Power Apps からフローを呼ぶ（トリガー：Power Apps (V2)）。画面は結果を待って表示を更新する |
| 読み取り | 画面は SharePoint のリストを **直接読む**（全員に閲覧権限がある）。フローを通すのは書き込みだけ |
| 書き込みの主体 | フローがサービスアカウントの接続で書く（ADR-0005）。利用者の接続では書かない。例外は下書き（Drafts）だけ |
| 呼び出した人の特定 | トリガーが受け取る呼び出し元の利用者情報（メールアドレス・ID）を使う。画面から送られた「実行者」の値は信用しない |
| 命名 | `CMS-Fnn-操作名`（例：`CMS-F11-RegisterBrief`）。子フローは `CMS-Cnn-`、定期実行は `CMS-Snn-` |
| 日時 | 保存は UTC、表示は日本時間。期限は日付（営業日）で持つ |
| 応答の形 | すべてのフローが `{ ok, code, message, data }` を返す（§5） |
| 同じ案件の同時処理 | 1つの案件への書き込みは直列にする（フローの同時実行数の設定、または Cases の処理中フラグ）。方式は実装で決める |
| 使うコネクタ | 標準コネクタのみ（SharePoint、Office 365 Outlook、Microsoft Teams、Office 365 Users、承認）。AI の呼び出しだけは #T5 で確定 |

---

## 2. フロー一覧

**遷移**は [状態遷移 §4](../03-detail-design/03-state-transitions.md) の番号。★ は通知先にも送る。

### 2.1 申請（起案者）

| # | フロー | 画面の操作 | 遷移 | 実行できる人 | 今回 |
|---|---|---|---|---|:--:|
| F01 | UploadTempFile | 資料添付の「ファイルを選択」 | − | 本人の下書き | ✅ |
| F02 | GenerateSummary | 「案件概要書を自動生成／再生成」 | − | 本人の下書き | ✅ |
| F03 | SubmitCase | 「申請する」 | S02 | 本人の下書き | ✅ |
| F04 | ExportSummaryPdf | 「PDF出力」 | − | 本人（下書き）／全員（申請後） | ✅（方式は #T14） |
| F05 | UpdateRecipients | 通知先の追加・削除（申請後） | − | 起案担当者 | ✅ |
| F06 | WithdrawCase | 「取り下げ」 | S20 | 起案担当者 | ✅ |

下書きの保存・再開は F なし（画面が Drafts に直接書く）。

### 2.2 Step1（事務局・起案者・審査担当者）

| # | フロー | 画面の操作 | 遷移 | 実行できる人 | 今回 |
|---|---|---|---|---|:--:|
| F10 | AssignSecretariat | 担当者の割当 | S03 | 事務局 | ✅ |
| F11 | RegisterBrief | 論点整理書の登録・回付（初版／修正版） | S04・S07 | 事務局 | ✅ |
| F12 | PostComment | 疑義・意見の登録／論点の追加依頼 | S05・S06 | 起案者／審査担当者 | ✅ |
| F13 | SelectReviewCheck | 確認表の選択・リスクの記載 | S06 | 審査担当者（担当ケイパビリティのみ） | ✅ |
| F14 | ConfirmBrief | 確認完了の登録 | S08 | 起案担当者 | ✅ |
| C01 | EvaluateStep2 | （F13・F14 の最後に呼ぶ） | S09 | − | ✅ |

### 2.3 Step2〜4（事務局・委員会）

| # | フロー | 画面の操作 | 遷移 | 実行できる人 | 今回 |
|---|---|---|---|---|:--:|
| F15 | RequestDeliberation | 回答依頼の登録 | S10 | 事務局 | ✅ |
| F16 | RegisterResult | 審議結果の登録 | S11 | 委員長（代理可） | ✅ |
| F17 | RegisterAnswerDraft | 回答書（案）の登録（修正版も） | S12 | 事務局 | ✅ |
| F18 | RequestAnswerRevision | 回答書の修正依頼 | S13 | 委員 | ✅ |
| F19 | CheckAnswer | 内容確認完了 | S14 | 委員長（代理可） | ✅ |
| F20 | FinalizeAnswer | 回答書の確定 | S15 | 事務局 | ✅ |
| F21 | RequestConsultation | 議論要請 | S17 | 起案担当者／委員 | ✅ |
| F22 | RegisterMeeting | 招集情報の登録 | S19a | 事務局 | ✅ |
| F23 | FinalizeResult | 審議結果・承認条件の確定登録／議事録と最終結果の登録 | S18・S19b（＋S21） | 事務局 | ✅ |

### 2.4 定期実行

| # | フロー | 実行 | 内容 | 今回 |
|---|---|---|---|:--:|
| S01 | DailyDueCheck | 毎朝（営業日） | 期限の前日・当日のリマインド、超過の判定（IsOverdue）と上位者への通知、議論要請の受付終了（S16） | ✅ |
| S02 | CleanupTempUploads | 毎日 | 作成から1日を過ぎた一時保管ファイルを削除 | ✅ |
| S03 | AnnualRetention | 年1回 | 結果確定・取り下げから3年を過ぎた案件の一覧を作り、CMS 管理者の承認後に削除 | ✅ |

### 2.5 子フロー（共通部品）

| # | フロー | 役割 |
|---|---|---|
| C01 | EvaluateStep2 | 起案者確認＝確認完了 かつ 保留＝0 なら審議待ちへ（S09） |
| C02 | GuardCase | 案件の状態・更新日時・実行者のロールを確かめる（§3） |
| C03 | AddBusinessDays | Holidays を見て営業日で期限日を出す |
| C04 | Notify | Teams とメールで通知。★ の場合は通知先・起案担当者・提案責任者を足す |
| C05 | WriteEvent | CaseEvents に1行追記 |
| C06 | SetDue | Cases の DueType・DueDate・IsOverdue を更新 |

---

## 3. 全フロー共通の処理順

```
1. 呼び出した人を特定する（トリガーの利用者情報）
2. C02 GuardCase
   a. 案件を読む（Status、Modified）
   b. 画面が送ってきた Status・Modified と一致するか   → 違えば E_CONFLICT
   c. その状態で、その操作が許されているか              → 違えば E_STATE
   d. 実行者がその操作をしてよいロールか               → 違えば E_FORBIDDEN
3. 入力を検証する                                     → 不足・不正は E_VALIDATION
4. 書き込む（Cases → 関連リスト → 文書の順）
5. C05 WriteEvent（遷移番号、前後の状態、実行者、代理か、詳細）
6. C06 SetDue（期限の開始・終了）
7. C04 Notify
8. 応答を返す { ok: true, data: { status, modified, … } }
```

4 の途中で失敗したら、それまでの書き込みを取り消せない場合がある（SharePoint にはまとめて取り消す仕組みがない）。**状態（Status）の更新を最後に行う**ことで、途中で失敗しても案件が次の状態に進まないようにする。

**ロールの判定**：SharePoint グループ（事務局、審査担当者、投資委員会、PPM、CMS 管理者）の所属で判定する。委員長・代理は Settings の `CHAIR`・`CHAIR_DEPUTY`、審査担当者の担当範囲は Capabilities.Reviewers で判定する。起案担当者かどうかは Cases.Submitter と照合する。

---

## 4. 主要フローの詳細

### F01 UploadTempFile

| 項目 | 内容 |
|---|---|
| 入力 | ファイル、ファイル名、資料の種類、DraftId |
| 検証 | DraftId の下書きが呼び出した本人のものか。形式（#T10）・サイズ |
| 処理 | TempUploads に保存（Uploader、DraftId を記録） |
| 出力 | TempUploadId |
| 注意 | 画面は返ってきた ID を Drafts.TempUploadIds に足す。ファイルの中身は画面に返さない |

### F02 GenerateSummary

| 項目 | 内容 |
|---|---|
| 入力 | DraftId、TempUploadIds |
| 検証 | 本人の下書きか。ファイルが残っているか（1日で消える） → 無ければ `E_TEMP_EXPIRED`（再添付を案内） |
| 処理 | ファイルを読み、AI に案件概要書の項目を抽出させる（呼び出し方式は #T5）。AI への指示は「資料に書かれていることだけ」「選択肢は選択肢の中から」「出所を付ける」「食い違いは両方返す」（業務ドメイン構造 §5 G1〜G6） |
| 出力 | 項目ごとの値・出所・候補（FieldMetaJson と同じ形）、表形式の項目（TablesJson と同じ形） |
| 書き込み | なし（画面が受け取って Drafts に保存する） |
| 時間 | 数十秒かかることがある。画面は待機表示を出す |

### F03 SubmitCase（S02）

| 項目 | 内容 |
|---|---|
| 入力 | DraftId、AttachPolicy（`INCLUDE`／`EXCLUDE`） |
| 検証 | 本人の下書きか。**必須項目を画面と同じ規則でもう一度確かめる**（業務ドメイン構造 §5）。内容確認が ON |
| 処理 | ① 案件IDを採番（年ごとの連番。採番は同時に1本だけ動かす） ② Cases を作成（Status＝`RECEIVED`） ③ CaseSummaries を作成（Drafts.FormJson から項目・TablesJson・FieldMetaJson を移す） ④ `INCLUDE` なら一時保管のファイルを CaseDocuments/{案件ID}/01_submitted へ移す ⑤ Drafts の項目を削除 |
| 記録・期限 | WriteEvent（S02）。SetDue（DRAFTING、3営業日） |
| 通知 | 事務局、★受付 |
| 出力 | CaseNo |

### F11 RegisterBrief（S04・S07）

| 項目 | 内容 |
|---|---|
| 入力 | CaseId、論点整理書ファイル、（修正版のとき）保留に戻す確認表の行 |
| 検証 | 初版：Status＝`RECEIVED` かつ担当が割り当て済み。修正版：Status＝`BRIEFING`。実行者が事務局 |
| 処理 | ファイルを CaseDocuments/{案件ID}/02_issue-brief に保存（同名で上書きし版を積む）。BriefVersion を+1。ApplicantCheck＝`UNCHECKED`。初版なら ReviewChecks を14行作成（すべて `PENDING`）、修正版なら選ばれた行だけ `PENDING` に戻す。PendingCount を数え直す。初版なら Status＝`BRIEFING` |
| 記録・期限 | WriteEvent（S04／S07）。SetDue（CONFIRM、3営業日） |
| 通知 | 起案者、審査担当者（担当するケイパビリティがある人）、★（初版のみ） |

### F13 SelectReviewCheck（S06）＋ C01（S09）

| 項目 | 内容 |
|---|---|
| 入力 | ReviewCheckId、Selection、RiskNote |
| 検証 | Status＝`BRIEFING`。実行者がその行のケイパビリティの担当（Capabilities.Reviewers） |
| 処理 | 行を更新（Reviewer、SelectedAt、BriefVersionAtSelection）。PendingCount を数え直す。C01 を呼ぶ |
| C01 | ApplicantCheck＝`CONFIRMED` かつ PendingCount＝0 なら Status＝`AWAITING_REVIEW`、WriteEvent（S09）、SetDue（なし）、事務局へ通知 |

### F16 RegisterResult（S11）

| 項目 | 内容 |
|---|---|
| 入力 | CaseId、ReviewResult、ApprovalConditions |
| 検証 | Status＝`UNDER_REVIEW`。実行者が委員長または代理（Settings） |
| 処理 | Cases に結果・承認条件・登録者・代理かを書く |
| 記録・期限 | WriteEvent（S11、代理なら OnBehalf）。SetDue（審議を終了） |
| 通知 | 事務局 |

### F23 FinalizeResult（S18・S19b・S21）

| 項目 | 内容 |
|---|---|
| 入力 | CaseId、（協議時）議事録ファイル |
| 検証 | 回答済み：議論要請の受付期間が終了している。協議中：議事録がある。実行者が事務局 |
| 処理 | 協議時は議事録を 04_meeting に保存。Status＝`APPROVED`／`REJECTED`（ReviewResult から決める。条件付き承認は `APPROVED`）。FinalizedAt。承認なら HandedOffToPPMAt を記録 |
| 記録 | WriteEvent（S18／S19b、承認なら S21 も） |
| 通知 | 起案者、委員会、★承認結果。承認なら PPM に承認案件と承認条件 |

### S01 DailyDueCheck

| 項目 | 内容 |
|---|---|
| 対象 | DueDate が入っている案件（索引付きの列で絞り込む） |
| 処理 | 期限の前営業日と当日：担当へリマインド。期限超過：IsOverdue＝はい、上位者（作成・確認は事務局、審議・回答書確認は委員長）へ通知。受付期限を過ぎた回答済み案件：受付を締め（S16）、事務局へ確定登録を依頼 |
| 実行時刻 | 毎朝（営業日のみ）。時刻は運用で決める |

その他のフロー（F04〜F06、F10、F12、F14、F15、F17〜F22、S02、S03）は、[状態遷移 §4](../03-detail-design/03-state-transitions.md) の各行（前提条件・処理・通知）をそのまま実装する。

---

## 5. 応答とエラー

```json
{ "ok": false, "code": "E_CONFLICT", "message": "ほかの人が先に更新しました。最新の内容を表示します。", "data": { "status": "BRIEFING", "modified": "…" } }
```

| code | 意味 | 画面の動き |
|---|---|---|
| `OK` | 成功 | 返ってきた状態で表示を更新 |
| `E_CONFLICT` | 画面が見ていた内容のあとに、誰かが更新した | 最新を読み直して表示 |
| `E_STATE` | 今の状態ではその操作ができない | メッセージを出して読み直す |
| `E_FORBIDDEN` | その人には操作の権限がない | メッセージを出す |
| `E_VALIDATION` | 入力の不足・不正（項目名の一覧を data に返す） | 該当欄を赤くする |
| `E_TEMP_EXPIRED` | 一時保管のファイルが削除済み | 再添付を案内 |
| `E_AI` | 自動生成に失敗した | 再試行を案内（手入力は続けられる） |
| `E_SYSTEM` | そのほかの失敗 | 管理者への連絡を案内。フローの実行履歴に残す |

メッセージの文言と表示方法は [検証・エラー設計](../03-detail-design/04-validation-and-errors.md) で定める（日英）。

---

## 6. 認証・認可

| 項目 | 方針 |
|---|---|
| 認証 | Microsoft 365 のサインイン（Entra ID）。CMS 独自の認証は持たない |
| 認可の判定位置 | **フローの C02 GuardCase**。画面はボタンの表示・非表示に同じ規則を使うが、それだけには頼らない |
| サービスアカウント | CMS 専用。フローの所有者とし、SharePoint への書き込み・メール送信に使う。利用者の操作は CaseEvents.Actor に本人として記録する |
| 閲覧 | SharePoint の権限（全員閲覧。Drafts は本人のみ、TempUploads は利用者なし） |

---

## 7. 監査ログ

すべての F フローと、状態を変える S フローが CaseEvents に1行を追記する（C05）。

| 記録項目 | 内容 |
|---|---|
| 遷移 | 遷移番号（S02 など） |
| 前後の状態 | FromStatus → ToStatus（状態が変わらない操作は同じ値） |
| 実行者・代理 | Actor、OnBehalf |
| 日時 | OccurredAt |
| 詳細 | 版、選んだ確認表の行、変更した通知先、ファイル名など（DetailJson） |

下書き段階の操作（保存、自動生成）は記録しない。

---

## 8. 外部連携

| 連携先 | 方式 | 用途 | 障害時の挙動 |
|---|---|---|---|
| AI（自動生成） | #T5 で確定（AI Builder のプロンプト等） | F02 | `E_AI`。手入力で続けられる |
| Teams・メール | 標準コネクタ | 通知 | 通知に失敗しても書き込みは取り消さない。失敗は CaseEvents に記録し、S01 で再送を試みる |
| PDF 生成 | #T14 で確定 | F04 | 失敗しても画面の内容は変わらない |

---

## 9. 将来追加するフロー

| フロー | 用途 | 時期 | 今の設計に足せるか |
|---|---|---|---|
| Triage | トリアージ（軽／重レーン） | ② | F11 の前に挟める（Cases.TriageLane を確保済み） |
| DraftBrief | 論点整理書の草案を CMS から自動生成 | ② | F11 の入力を作る子フローとして足せる |
| Monitoring 系 | 定期チェックイン、エスカレーション、レビューゲート | ③ | F23 の S21 を起点に足せる |
| ExportLedger | 連携システム・保守期限の台帳化 | ③ | CaseSummaries.TablesJson から展開 |
