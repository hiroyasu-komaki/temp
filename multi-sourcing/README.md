# 競争調達フレームワーク／VMO Value Create施策

当社IT調達における随意契約80%の構造を、非対称情報の経済学を土台に診断し、競争調達方式の導入を制度として設計するプロジェクトです。理論・診断・提言を三部構成でまとめた公開用フレームワーク（HTML）と、経営会議向けの投資提案書、実務で使う申請様式一式で構成されています。

## プロジェクト構成

```
multi-sourcing/
├── index.html                              ← 公開用トップページ（フレームワーク00〜02への入口）
├── html/                                    ← index.html からリンクされる公開ページ
│   ├── 00_Information_Asymmetry.html         理論編：情報の非対称性
│   ├── 01_Sole_Source_Market_Failure.html     診断編：随意契約8割構造下の症状
│   ├── 02_Competitive_Sourcing_Proposal.html  提言編：競争調達フレームワーク
│   ├── Form1_Justification.html               様式1：随意契約理由書（02から参照）
│   └── Form2_Procurement_Specification.html    様式2：調達仕様書（02から参照）
├── appendix/                                ← 様式・解説の原稿（Markdown）
│   ├── Form1_Justification.md                 様式1の原稿
│   ├── Form2_Procurement_Specification.md      様式2の原稿
│   ├── Framework_Commentary.md                 様式1・2の設計思想解説（VMO内部用）
│   └── VMO_Decision_Sheet.md                   VMOが記入する判定書
├── proposal/                                ← 経営会議向け投資提案
│   ├── 施策企画書.md                           企画提案書本体（image/ の図版を参照）
│   └── vmo_impact_model.xlsx                   効果試算モデル（NPV/IRR等の根拠）
├── image/                                   ← 施策企画書.md に埋め込むグラフ4枚
└── README.md
```

## 各ファイルの役割

- **index.html / html/** — 社内外に公開するフレームワーク本体。情報の非対称性の理論（00）→随意契約構造の診断（01）→競争調達の提言（02）の順に読む前提でリンクされています。様式1・2のHTML版（`html/Form1_Justification.html` / `html/Form2_Procurement_Specification.html`）はこのサイトから実際に参照されている正本です。
- **appendix/** — 様式1・2の原稿（Markdown）と、VMOの内部運用資料（判定書・設計思想解説）。`html/` 側の様式と内容を変更する際は、原稿側も合わせて更新してください。
- **proposal/施策企画書.md** — 経営会議に提出する投資提案書。`image/` 配下の4枚のグラフを相対パスで参照しています。
- **proposal/vmo_impact_model.xlsx** — 効果試算・投資評価（NPV/IRR/PI等）の根拠となるExcelモデル。

## 閲覧方法

- フレームワーク全体を読む場合は `index.html` をブラウザで開いてください。
- 投資提案の本体を読む場合は `proposal/施策企画書.md` を開いてください（Markdown対応ビューア推奨）。
