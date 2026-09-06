# contract — IT契約管理ガイドライン

IT部門が締結・管理するIT関連契約について、契約類型の整理、ANSI/NCMA CMS標準に基づく標準業務プロセスの定義、契約類型別チェックリストの整備をまとめたコンセプト資料です。個別契約書そのものの保管や、契約書レビューを自動化するツール（contract-review-agent）自体の実装はこのフォルダの対象外です。そのツールをどの業務ステップで使うかは `chapters/01_business-process.md` にまとめています（関連プロジェクトとしての詳細は本README末尾）。

構成は `../concept-template/` の標準フォルダ構成に準拠しています。このコンセプトでは社内公開用のHTML版（`index.html` / `html/` / `images/` / `assets/`）は未整備のため作成していません。必要になった時点で `concept-template` から複製してください。

## ディレクトリツリー

```
contract_negotiation/
├── README.md                              このファイル
├── chapters/
│   ├── 00_contract-types.md               IT部門が取り扱う契約類型一覧（A〜H、25小分類）
│   └── 01_business-process.md             CMSのライフサイクル（Pre-Award/Award/Post-Award）に基づく標準業務プロセス定義。contract-review-agentの活用方法（利用シーン・結果の取り扱い）も含む。CMS自体の解説は appendix/cms-standard/ へ分離
├── proposal/
│   ├── contract_negotiation_briefing.pptx  契約交渉の社内共有資料（6枚）。①準備を始めるタイミング（RFP発出以降、交渉できる条件が狭くなること）、②3フェーズと各フェーズの到達状態、③合意できる範囲（双方の限界線と代替手段）、④時間の制約と論点の提示順序
│   ├── contract_negotiation_briefing.pdf   上記のPDF版
│   ├── it-contract-guide.pptx              IT契約チェックリスト導入提案（旧資料、日本語6枚＋英語6枚）。現状の課題／法務・購買・IT部門の業務領域／IT部門が取り扱う契約類型を整理
│   └── it-contract-guide.pdf               上記のPDF版
├── appendix/
│   ├── checklists/                        契約類型別チェックリスト（25件）。ファイル名の接頭辞は chapters/00 の契約類型コード（A-1〜H-3）に対応
│   ├── cms-standard/
│   │   └── A_cms-lifecycle-overview.md    ANSI/NCMA CMS標準の指導原則・ドメイン・コンピテンシーの解説（理論的背景）
│   └── templates/
│       ├── form1_negotiation-points-list.md  交渉論点リストの記入用テンプレート（chapters/01の1.4で使用）
│       └── form2_negotiation-strategy.md     交渉戦略の記入用テンプレート（chapters/01の2.1で使用）
└── sources/
    └── CMS_contract-management-standard.pdf  ANSI/NCMA CMS標準の原本
```

## 正本／読む順序

- 交渉に臨む前に社内で前提をそろえたい → `proposal/contract_negotiation_briefing.pptx`（`chapters/01`のフェーズ定義・2.1・2.2を、交渉学の基本フレームワーク（BATNA／ZOPA）と合わせて説明するもの）
- 契約類型を知りたい → `chapters/00_contract-types.md`
- 契約審査の標準業務プロセス、どこでcontract-review-agentを使うかを知りたい → `chapters/01_business-process.md`
- 個別契約レビュー時に使うチェックリストが欲しい → `appendix/checklists/`
- ANSI/NCMA CMS標準そのものの解説（指導原則・ドメイン・コンピテンシー）を知りたい → `appendix/cms-standard/A_cms-lifecycle-overview.md`（原本PDFは `sources/`）
- 交渉論点リストを作成したい → `appendix/templates/form1_negotiation-points-list.md`
- 交渉戦略（提示順序・時間の制約・撤退条件）をまとめたい → `appendix/templates/form2_negotiation-strategy.md`

分割前の初版ドラフトのうち`it-contract-guide_proposal.md`は、上記への分割が完了したため削除済みです（2026-09-06）。一方`proposal/it-contract-guide.pdf`・`it-contract-guide.pptx`（IT契約チェックリスト導入提案の旧資料）は、まだ参照・流用する可能性があるため削除せず残しています。また、個別事案の分析だった「Lessons Learned」章は、本フォルダが契約に関する標準業務の定義を目的としているため削除済みです。チェックリスト整備の企画提案書（`proposal/contract_proposal.md`）も、25類型分のチェックリストが整備済みで提案としての役割を終えたため削除しました（2026-09-06）。`proposal/` には現在、契約交渉の社内共有資料（`contract_negotiation_briefing.pptx`/`.pdf`、2026-09-06作成）と、上記のIT契約チェックリスト導入提案の旧資料（`it-contract-guide.pptx`/`.pdf`）を置いています。

## 関連プロジェクトとの重複について

`../../03_agents/contract-review-agent/` は本フォルダの内容をもとに開発された契約書レビューエージェントです。`chapters/01_business-process.md` にどの業務ステップでこのエージェントを使うかを定義していますが、以下は独立コピーとして重複しています（2026-09-06時点、今回の整理では未着手）。

- `contract-review-agent/checklists/` — 本フォルダの `appendix/checklists/`（旧 `checklists/`）と現時点で内容が同一（バイト単位で一致）
- `contract-review-agent/direction/it-contract-type-classifier.md` — `chapters/00_contract-types.md` の契約類型一覧と重複する「IT契約類型マスター」を独自に保持

どちらか一方を更新すると、もう一方との間に乖離（ドリフト）が生じる可能性があります。将来的には contract-review-agent 側が本フォルダを参照する形に統合するか、更新時の同期ルールを決めることを推奨します。
