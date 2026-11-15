# 01 セキュリティ運用の定義と範囲

## 要旨

セキュリティ運用（SecOps）は、**攻撃や不正を見つけ（検知）、被害を食い止めて元に戻し（対応・復旧）、狙われる弱点を減らし続ける（脆弱性管理）**日々の活動である。防御の仕組みを設計すること（web-security）や、権限を与えること（identity）と違い、**動いているシステムを監視し、起きたことに手を打つ**ことを扱う。

## 定義

NIST サイバーセキュリティフレームワーク（CSF）2.0 は、サイバーセキュリティの活動を6つの機能（統治・識別・防御・検知・対応・復旧）に分ける。本資料では、このうち主に**検知・対応・復旧**と、識別に含まれる脆弱性の把握を、セキュリティ運用の範囲とする（本資料の整理）。

| CSF 2.0 の機能 | 内容 | 本資料での扱い |
|---|---|---|
| 統治（Govern） | 方針・役割・リスク管理の決定（2.0 で追加） | 対象外（組織・ガバナンスの領域） |
| 識別（Identify） | 資産・リスクの把握 | 脆弱性の把握のみ扱う |
| 防御（Protect） | アクセス制御、データ保護など | 対象外（identity・web-security） |
| 検知（Detect） | 攻撃や異常を見つけて分析する | 扱う |
| 対応（Respond） | 見つけたインシデントに手を打つ | 扱う |
| 復旧（Recover） | 影響を受けた資産と業務を元に戻す | 扱う |

NIST SP 800-61 第3版（2025年）は、インシデント対応を独立した手順ではなく、CSF 2.0 の6つの機能すべてに組み込むものとして整理し直している。

## 成り立ち

| 年 | 出来事 | 意味 |
|---|---|---|
| 2005 | Gartner のアナリストが SIEM という言葉を提唱。ログの長期保管・分析（SIM）と、リアルタイムの監視・相関分析（SEM）を1つにまとめた | ログを集めて攻撃を見つける製品分野ができる |
| 2013 | Gartner のアナリストが、端末上の不審な動きの検知と調査に使うツールを ETDR（後の EDR）と名付ける | ウイルス対策（既知のマルウェアを防ぐ）から、端末で起きたことを記録して調べる方向へ広がる |
| 2021 | 米 CISA が BOD 22-01 を出し、「悪用が確認された脆弱性（KEV）」のカタログを公開 | 脆弱性の優先度を、深刻度の点数だけでなく、実際に悪用されているかで決める考え方が広まる |
| 2023 | FIRST が CVSS v4.0 を公開 | 深刻度の点数（基本評価）だけでリスクを判断しないことが、命名の段階で明確になる |
| 2024 | NIST CSF 2.0 を公開（統治の機能を追加） | — |
| 2025 | NIST SP 800-61 第3版を公開（2012年の第2版を置き換え） | — |

国内では、IPA の「情報セキュリティ10大脅威 2026」（組織編）で、1位が「ランサム攻撃による被害」、4位が「システムの脆弱性を悪用した攻撃」だった。

## 範囲（何であり、何でないか）

| セキュリティ運用が扱うもの | 扱わないもの（隣接領域） |
|---|---|
| ログの収集と検知（SIEM）、端末での検知と対応（EDR・XDR） | アプリの脅威と設計の原則（web-security） |
| 監視と対応の体制（SOC・CSIRT）、外部委託（MDR） | ID と権限の付与・見直し（identity） |
| インシデント対応と復旧 | システムの稼働監視・障害対応（it-operations） |
| 脆弱性管理（把握・優先順位付け・修正の確認） | 広く使われる部品の重大脆弱性への組織としての対処（governance/zero-day-response） |

## 組織の対処との違い

広く使われる部品（PHP・Node.js など）に重大な脆弱性が見つかったときの**組織としての対処**（誰が影響を調べ、誰が判断し、どう報告するか）は、ガバナンスの資料（governance/zero-day-response）で扱う。本トピックは、その対処の中で使う**仕組み（脆弱性の把握、検知、対応）**を扱う。

---

**出典**（確認日：2026-11-14）

- NIST CSF 2.0（2024-02-26、6つの機能）：NIST — https://www.nist.gov/news-events/news/2024/02/nist-releases-version-20-landmark-cybersecurity-framework
- NIST SP 800-61r3（2025-04-03）：NIST CSRC — https://csrc.nist.gov/pubs/sp/800/61/r3/final 、NIST ニュース — https://nist.gov/news-events/news/2025/04/nist-revises-sp-800-61-incident-response-recommendations-and-considerations
- SIEM の名称（2005）：Wikipedia「Security information and event management」— https://www.Wikipedia.org/wiki/SIEM 、Solutions Review — https://solutionsreview.com/security-information-event-management/whats-changed-gartners-2015-security-information-and-event-management-siem-magic-quadrant-report
- EDR の名称（2013）：Fortra「What is Endpoint Detection and Response?」— https://www.fortra.com/resources/knowledge-base/endpoint-detection-and-response-edr
- BOD 22-01 と KEV（2021-11-03）：CISA プレスリリース — https://www.cisa.gov/news/2021/11/03/cisa-releases-directive-reducing-significant-risk-known-exploited-vulnerabilities 、ファクトシート — https://www.cisa.gov/sites/default/files/publications/Reducing_the_Significant_Risk_of_Known_Exploited_Vulnerabilities_211103.pdf
- CVSS v4.0（2023-11-01）：@IT — https://atmarkit.itmedia.co.jp/ait/articles/2311/10/news048.html
- 情報セキュリティ10大脅威 2026：@IT（2026-03-03）— https://atmarkit.itmedia.co.jp/ait/articles/2603/03/news057.html
- CSF の機能と本資料の範囲の対応は、本資料の整理
