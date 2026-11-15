# security-operations — セキュリティ運用

**一言でいうと**：攻撃や不正を見つけ、被害を食い止めて元に戻し、狙われる弱点を減らし続ける、日々の監視と対応の活動。

- **扱うこと**：定義と成り立ち（NIST CSF 2.0 の検知・対応・復旧）、SIEM・EDR・XDR・SOAR、SOC・CSIRT・MDR、インシデント対応（NIST SP 800-61 第3版）、脆弱性管理（CVSS・KEV）、主要製品、論点、隣接領域との境界
- **扱わないこと**：防御の設計（→ web-security）、権限の付与と見直し（→ identity）、広く使われる部品の重大脆弱性への組織的な対処（→ governance/zero-day-response）、制御系（OT）に固有の守り方（→ ot-security）
- 当社固有の情報は 06章にだけ書く（未作成）

## ディレクトリ構成

```
security-operations/
├── README.md
└── chapters/
    ├── 01_definition.md   定義と範囲：CSF 2.0 との対応、成り立ち（SIEM→EDR→KEV→CVSS v4.0→800-61r3）、扱う／扱わないもの
    ├── 02_structure.md    構造：検知と対応の流れ、検知の仕組み、SOC・CSIRT・MDR、インシデント対応、脆弱性管理
    ├── 03_landscape.md    製品と提供形態：SIEM、端末の保護（防御だけ／EDR を含む段階）、脆弱性管理（EAP）、単一ベンダーにまとめる動き
    ├── 04_tradeoffs.md    主要な論点：5つの軸
    └── 05_business-requirements.md   ビジネス要件：ファンクションに決めてもらうこと
```

## 読み方

- 隣接領域との境界（どのシステムが何を持つか）は [function-allocation](../../cross-cutting/function-allocation/function-allocation.md) にまとめている。
- 01 → 02 → 03 → 04 → 05 の順に読む。
- 正本は `chapters/` の Markdown。
- 出典と確認日は各章末に記載。「本資料の整理」と書いた箇所は出典をもとにした見解。「要確認」は裏付けが取れていない記述。

## 章の作成状況

| 章 | 状態 | 最終確認日 |
|---|---|---|
| 01〜05 | 作成済み。03章は記入要領に沿って書き直した（2026-11-14）。03章に端末保護（6社の製品と段階）と脆弱性管理（EAP、Tenable・Qualys・Rapid7）を追記。Sophos・TrendAI の段階の区分は未確認。05章はビジネス要件の章に改めた（2026-11-15） | 2026-11-14 |
| 06 | 素材がないため未作成 | — |
