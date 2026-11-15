# quality-regulatory — 品質・薬事・安全性

**一言でいうと**：医薬品の品質の記録（QMS）、承認の取得と維持（RIM）、市販後の安全性の監視（PV）を支える仕組み。

- **扱うこと**：QMS・RIM・PV の機能、eCTD v4.0・E2B(R3)・CSA などの標準と規制、変更と有害事象の流れ、主要製品、論点、隣接領域との境界
- **扱わないこと**：Veeva の製品の詳細（→ veeva-platform 付録E）、臨床試験（→ rd）、製造の実行（→ manufacturing）、CSV・データインテグリティの要件の全体（→ gxp-compliance）
- 当社固有の情報は 06章にだけ書く（未作成）

## ディレクトリ構成

```
quality-regulatory/
├── README.md
└── chapters/
    ├── 01_definition.md   定義と範囲：3つのシステム、標準と規制
    ├── 02_structure.md    構造：品質と薬事のつながり、有害事象の流れ、正本
    ├── 03_landscape.md    製品と提供形態：QMS、PV、RIM、国内の要素、提供形態、市場の動き
    ├── 04_tradeoffs.md    主要な論点：5つの軸
    └── 05_business-requirements.md   ビジネス要件：ファンクションに決めてもらうこと
```

## 読み方

- 隣接領域との境界（どのシステムが何を持つか）は [function-allocation](../../cross-cutting/function-allocation/function-allocation.md) にまとめている。
- 01 → 02 → 03 → 04 → 05 の順に読む。
- 出典と確認日は各章末に記載。「本資料の整理」と書いた箇所は出典をもとにした見解。

## 章の作成状況

| 章 | 状態 | 最終確認日 |
|---|---|---|
| 01〜05 | 作成済み。03章は記入要領に沿って書き直した（2026-11-14）。Veeva・ArisGlobal 以外の RIM 製品、国内の製品と採用状況、文書管理の専用製品、eCTD v4.0 の国内移行の実際の状況は未調査。05章はビジネス要件の章に改めた（2026-11-15） | 2026-11-14 |
| 06 | 素材がないため未作成 | — |
