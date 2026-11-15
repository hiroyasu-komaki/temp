# veeva-platform — Veeva の製品群

**一言でいうと**：製薬などライフサイエンス業界に特化したクラウドソフトウェアと業界データの製品群。共通基盤（Vault Platform）の上に、R&D（臨床・薬事・品質・安全性）とコマーシャル（メディカル・営業・マーケティング）のアプリケーションを揃えている。

- **扱うこと**：Veeva の定義と成り立ち、製薬バリューチェーンとの対応、Vault Platform の構造（データ構造、ライフサイクル、API、AI、監査証跡）、全製品の位置づけ、Veeva に本質的に伴う論点、System of Record と隣接領域との境界、日本固有の HCP/HCO データ事情（Ultmarc）
- **扱わないこと**：製品の導入・設定手順、個別プロジェクトの要件定義や見積、Vault のアカウント管理（→ governance/vault-access-management）
- 当社の現状は 06章にだけ書く

## ディレクトリ構成

```
veeva-platform/
├── README.md
├── chapters/
│   ├── 01_definition.md   定義と範囲：Veeva とは、CRM の基盤移行、製薬バリューチェーンと製品の対応、用語集
│   ├── 02_structure.md    構造：3層構成、Vault Platform、データ構造、ライフサイクル同期、API、AI、監査証跡
│   ├── 03_landscape.md    製品と提供形態：全製品マップ、業務と製品の早見表、領域別の付録への索引
│   ├── 04_tradeoffs.md    主要な論点：業界特化か汎用か、Veeva でそろえるか組み合わせるか
│   ├── 05_business-requirements.md   ビジネス要件：ファンクションに決めてもらうこと
│   └── 06_our-company.md  当社の現状：Veeva CRM の置き換え、Vault の維持
├── appendix/
│   ├── A_drug-development-and-cmc.md    医薬品開発と CMC、CRO、PMDA/FDA、CTD の詳細
│   ├── B_ultmarc-and-japan-hcp-data.md  Ultmarc の沿革と MDB の詳細
│   ├── C_veeva-vs-salesforce.md         Veeva と Salesforce Life Sciences Cloud の比較
│   ├── D_veeva-dependency.md            Veeva 依存度と代替可能性
│   ├── E_rd-products.md                 R&D 領域の製品：臨床・薬事（RIM）・品質・安全性
│   ├── F_medical-products.md            メディカル領域の製品：Medical Suite、Veeva Link
│   ├── G_commercial-products.md         コマーシャル領域の製品：Vault CRM Suite、PromoMats/MLR、KAM、KPI
│   ├── H_data-products.md               データ領域の製品：Network、OpenData、Ultmarc、識別子、Nitro・Compass
│   └── I_system-of-record.md            データ責任分界（System of Record）、R&D とコマーシャルの接続点、CRUD・RACI
└── images/                図版（ファイル名の先頭は使っている章の番号）
```

## 読み方

- 隣接領域との境界（どのシステムが何を持つか）は [function-allocation](../../cross-cutting/function-allocation/function-allocation.md) にまとめている。
- 01 → 02 → 03 → 04 → 05 の順に読む。03 の製品マップが全製品の索引で、領域ごとの詳細は付録E〜Hにある。
- 製薬業務そのものを知りたいときは、01 → 付録A。
- 正本は `chapters/` と `appendix/` の Markdown。
- 製品構成・名称は Veeva 公式サイト（2026年10月時点）に基づく。Veeva は製品の追加・改称が多いため、更新時は各章末の出典を再確認する。
- 「要確認」は裏付けが取れていない記述。

## 章の作成状況

| 章 | 状態 | 最終確認日 |
|---|---|---|
| 01〜03、05 | 作成済み（旧 00〜06章を5つの観点に組み替え）。03章に提供形態・市場の動きを加えた（2026-11-14）。05章はビジネス要件の章に改めた（2026-11-15） | 2026-11-14 |
| 04 | 作成済み（付録C・Dから論点を抽出） | 2026-11-14 |
| 06 | 作成済み | 2026-11-14 |
| 付録A・B | 出典を追記し、誤りを修正 | 2026-11-14 |
| 付録E〜H | 作成済み（付録Hの日本の HCP/HCO データは 2026-11-14 に修正） | 2026-10 |
| 付録C・D | 出典を追記し、誤りを修正（Salesforce の投入時期、IQVIA との関係など）。評価の部分は本資料の評価と明記 | 2026-11-14 |
