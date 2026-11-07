# 付録C　Microsoft 365 Copilot エージェントでの利用

> **種別**：導入手順
> **使用場面**：`../../chapters/01_business-process.md` 1.1「契約類型の特定」・1.2「チェックリストによる一次スクリーニング」を、Claude Code を使えない環境で Microsoft 365 Copilot のエージェント（エージェントビルダー／Copilot Studio）により支援する場合
> **参照元**：`../../chapters/01_business-process.md`

## 目的

`03_agents/contract-review-agent`（Claude Code の Skill）の分類・チェック機能を、Microsoft 365 Copilot のエージェントとして再現する手順を示す。指示（Instructions）と、ナレッジに登録するファイルは、すべて本フォルダ内のものを使う。

## エージェントの構成

分類とチェックは、それぞれ別のエージェントとして作成する。

| エージェント | 指示（Instructions）に貼るもの | ナレッジに登録するもの | 利用者が添付・入力するもの |
|---|---|---|---|
| IT契約類型分類 | `classifier-instructions.md` の全文 | `../classification-criteria/B_contract-type-classification-criteria.md` | 契約書ファイル（文書一式） |
| IT契約チェック | `checker-instructions.md` の全文 | `../checklists/*.md`（25件） | 契約書ファイル（文書一式）、類型コード（または分類レポート） |

- 出力の書式は指示の中に含めているため、テンプレートのファイルを別途登録する必要はない
- 判定基準・チェックリストは指示欄に入れず、ナレッジとして登録する

## 利用の流れ

1. 1件の契約を構成する文書（基本契約・個別契約・覚書・別紙など）を、**すべてまとめて**分類エージェントに添付する
2. 分類エージェントが分類レポート（`classify_*.md`）を生成する。返信欄に示された類型コードを確認する
3. 同じ文書一式と類型コード（または分類レポート）をチェックエージェントに渡す
4. チェックエージェントが、文書構成（関係図）と文書別の根拠を含むチェック結果レポート（`check_report_*.md`）を生成する

## ファイル出力について

- 両エージェントとも、レポートをチャットの返信欄ではなく Markdown ファイルとして生成し、ダウンロードリンクで提示するよう指示している。ファイル生成はコードインタープリターの機能を使う（エージェントビルダーでは既定で有効）
- 生成されたファイルはセッション中のみダウンロードできるため、生成後すぐに保存する
- Microsoft のドキュメントでは、生成できる形式として Word・Excel・PowerPoint・PDF・画像が例示されており、Markdown は明記されていない。導入時に .md で出力されることを確認する
- 関係図（Mermaid）は Copilot のチャット上では図として表示されない。保存した .md を Mermaid に対応したビューアー（VS Code 等）で開いて確認する

## 更新時の注意

- 指示の内容は、`contract-review-agent` の Skill（`.claude/commands/it-contract-classifier.md`・`it-contract-checker.md`）と出力テンプレートの手順・書式に合わせている。どちらかを変更したときは、もう一方も合わせて更新する
- 判定基準・チェックリストを更新した場合は、ナレッジに登録したファイルも差し替える

---

**参照**：`classifier-instructions.md`、`checker-instructions.md`、`../classification-criteria/B_contract-type-classification-criteria.md`、`../checklists/`、`../../../../../03_agents/contract-review-agent/`
