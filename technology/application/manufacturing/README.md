# manufacturing — 生産系IT（ERP・MES・SCADA・PLC）

**一言でいうと**：製造業のITを、ISA-95 の階層（経営 → 製造オペレーション → 制御 → 機器）で捉え、MES を中心とした Level 3（製造オペレーション管理）の構成と、IT と OT の境界を整理するトピック。

- **扱うこと**：ISA-95 の5階層、MOM の4領域（MES・LIMS/QMS・CMMS/EAM・WMS）、MESA-11、生産管理システムの位置づけ、各階層の主要製品、IT/OT の区分基準
- **扱わないこと**：制御系（OT）の守り方（→ ot-security）、製造の記録の信頼性とバリデーション（→ gxp-compliance）
- 当社の現状と、それに対する打ち手（責任分解・データガバナンス・投資承認ルーティング）は 06章と付録A〜Cにだけ書く

## ディレクトリ構成

```
manufacturing/
├── README.md
├── chapters/
│   ├── 01_definition.md   定義と範囲：生産管理の管理対象と目的（QCD）、「生産管理システム」の位置づけ
│   ├── 02_structure.md    構造：ISA-95 の5階層、MOM の4領域、MESA-11、生産計画・BOM・製造指図の階層対応、IT と OT の区分基準
│   ├── 03_landscape.md    製品と提供形態：階層別・MOM 領域別の主要製品
│   ├── 04_tradeoffs.md    主要な論点：6つの軸（ERPかMESか、MOMの製品構成、標準化、管掌、マスタ、現場の接続）
│   ├── 05_business-requirements.md   ビジネス要件：ファンクションに決めてもらうこと
│   └── 06_our-company.md  当社の現状：システム構成、mcframe の経緯、責任の重なり、マスタ多重管理、課題への打ち手（提言）
├── appendix/              06章の補足（当社固有）
│   ├── A_decision-criteria.md           判断基準：MESA-11×運用主管マッピング、投資案件の追加項目、承認ルートの判定フロー
│   ├── B_routing-operation.md           運用：プロンプトを用いた2段階の判定フロー
│   └── C_investment-approval-prompts.md 承認ルーティング判定プロンプト集
└── images/                図版（ファイル名の先頭は使っている章の番号）
```

## 読み方

- 隣接領域との境界（どのシステムが何を持つか）は [function-allocation](../../cross-cutting/function-allocation/function-allocation.md) にまとめている。
- 01 → 02 → 03 → 04 → 05 の順に読み、当社の状況は 06 → 付録A → B → C の順に読む。
- 正本は `chapters/` と `appendix/` の Markdown。プロンプトの正本は付録C。
- 「要確認」は裏付けが取れていない記述。

## 章の作成状況

| 章 | 状態 | 最終確認日 |
|---|---|---|
| 01〜03、05 | 作成済み（旧 00_framework を5つの観点に組み替え）。出典を追記し、記述を出典に合わせて修正。03章は記入要領に沿って書き直した（2026-11-14）。03章の品質・保全・在庫の国内製品、Level0 の製品は未調査。05章はビジネス要件の章に改めた（2026-11-15） | 2026-11-14 |
| 04 | 作成済み（01〜03・05章と06章の事例から一般化） | 2026-11-14 |
| 06 | 作成済み。ERP・mcframe の現状は 2026-11-14 に更新、それ以外は 2026-08 時点。提言は旧 governance/ot-governance から統合 | 2026-11-14 |
| 付録A〜C | 旧 governance/ot-governance の 03・04章・付録1 を移設。当社向けの提言のため外部の出典はない | 2026-08 |
