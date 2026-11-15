# 付録D　Veeva 依存度の整理

> **参照元**：[04章](../chapters/04_tradeoffs.md) 論点2

製薬企業が Veeva に依存している機能と、他社で代替可能な機能を整理します。システム選定やリスク評価の参考資料です。

---

## D-1 代替可能性の分類

| 機能・コンポーネント | Veeva依存度 | 代替可能性 | 備考 |
|---|---|---|---|
| Core CRM（活動記録・HCP/HCO管理） | 中 | 可能 | Salesforce・他社CRMで代替可能だが、移行コストが高い |
| Vault CRM（Vault-CRM統合） | 高 | 困難 | PromoMats-CLM連携はVeeva固有。代替時は別途コンテンツ統制基盤が必要 |
| Veeva Network / OpenData | 高 | 部分的 | 日本ではUltmarc直接契約で代替可能だが、グローバル統合は難しい |
| CLM（コンテンツ提示・ログ） | 高 | 困難 | Vault PromoMatsとの連携が前提。他社CLMではGxP保証に課題 |
| Approved Email | 高 | 可能 | MLRレビュー済みテンプレートの配信。別途承認フロー設計が必要 |
| Veeva QualityDocs・QMS | 中〜高 | 可能 | MasterControl・Documentumなどの代替QMS製品が存在する |
| Veeva RIM（Submissions・Registrations） | 高 | 困難 | eCTD申請特化製品（Extedo等）で代替可能だが、統合コストが高い |
| Veeva Safety Suite | 中〜高 | 可能 | Oracle Argus・ARISg等の代替PVシステムが存在する |
| Vault AI・Veeva Falcon | 中 | 可能 | 他社AI（Salesforce Agentforce等）との競合領域 |
| Veeva Link（Key People・Medical Insights 等） | 中〜高 | 部分的 | KOLデータはVeeva独自。インサイト分析は他社製品・自社開発でも可能だが、Medical CRMとの一体性は失われる |
| Veeva 臨床製品（CTMS・eTMF・EDC 等） | 中〜高 | 可能 | Medidata等の代替製品が存在する。依頼者・CRO・施設の連携範囲で判断 |
| Veeva Nitro | 中 | 可能 | 他のデータ基盤で代替可能。Ultmarcデータ自体は直接取得も可能 |
## D-2 日本市場における独自リスク

- **HCP/HCOデータ**：Veeva OpenDataが非対応のため、UltmarcとのVeeva連携に依存。Veeva離脱時はUltmarc直接連携への移行が必要。
- **日本固有データの連携**：Ultmarc などのデータを Veeva の製品（Network・Nitro）経由で取り込んでいる場合、Veeva を離れると、その取り込みを別に作り直す必要がある。
- **業界横断の指標（CRM Pulse など）**：Veeva の CRM 利用データから作られる業界横断のデータ（HCPへのアクセス状況など）は、Veeva を離れると利用できなくなる。
## D-3 総括

- **CRM単体**：他社CRMでも代替可能だが、コンテンツ統制・GxP保証の再設計が必要
- **Vault + CRM一体**：「文書承認→現場配信→活動記録→監査証跡」のエンドツーエンドをVeeva以外で実現するには、複数製品の統合設計が必要
- **日本のHCP/HCOデータ**：Veevaが直接グローバル提供するというより、ローカル提携（Ultmarc）や追加サービスで補う構造であり、データ側の依存はVeevaとUltmarc双方に分散している

---

**出典**（確認日：2026-11-14）

- OpenData が日本で提供されていない点、Ultmarc との提携：付録H を参照
- CRM Pulse：Zacks による Veeva FY2026 Q1 決算の解説 — https://www.zacks.com/stock/news/2586097/
- 代替製品（MasterControl、OpenText Documentum、Extedo、Oracle Argus、ArisGlobal、Medidata など）は、各領域の代表的な製品として一般に知られているもの
- 依存度・代替可能性の評価（D-1 の表）と総括（D-3）は、本資料の評価であり、個別の一次資料はない
