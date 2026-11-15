# 01 ID・アクセス管理の定義と範囲

## 要旨

ID・アクセス管理（IAM：Identity and Access Management）は、**誰が（ID）**、**本人であることをどう確かめ（認証）**、**何にアクセスしてよいか（権限）**を、入社から退職まで一貫して管理する仕組みである。個々のアプリの中で作る認証・認可（→ web-security）と違い、IAM は**組織全体で共通に使う基盤と、その運用の手順**を扱う。

## 定義

本資料では、IAM を次の4つの機能の組み合わせとして扱う（本資料の整理）。

| 機能 | 何をするか | 代表的な仕組み |
|---|---|---|
| ディレクトリ | ID と属性（所属、役職など）の正本を持つ | Active Directory、Microsoft Entra ID |
| アクセス管理（認証・SSO） | 本人確認をして、各アプリへのログインを1か所にまとめる | IdP、SAML・OIDC によるフェデレーション、MFA |
| ID ガバナンス（IGA） | ID のライフサイクルと権限の付与・見直しを管理する | 入社・異動・退職の自動化、アクセス申請、アクセスレビュー |
| 特権アクセス管理（PAM） | 管理者権限など、影響の大きい権限を特別に守る | 一時的な権限付与（JIT）、認証情報の保管、操作の記録 |

Gartner は IGA を、ID のライフサイクルを管理し、オンプレミスとクラウドの両方でアクセスの付与と権限の管理を行うソリューションと定義している。PAM は、システムの管理・設定に使うアカウント・認証情報・コマンドを管理・保護することで、高い権限でのアクセスを提供するツールと定義している。

## 成り立ち

| 年 | 出来事 | 意味 |
|---|---|---|
| 2000 | Windows 2000 Server とともに Active Directory が登場。LDAP・Kerberos・DNS などの標準技術を採用 | 社内の ID と認証を1か所で管理する基盤が普及する |
| 2015 | SCIM 2.0 が IETF の RFC（7643・7644）になる | クラウドのアプリへの ID の作成・変更・削除（プロビジョニング）を標準の API で行えるようになる |
| 2023 | Microsoft が Azure AD を Microsoft Entra ID に改称 | クラウドの IdP が、社内 ID 管理の中心になる |
| 2025 | NIST SP 800-63-4（デジタル ID ガイドライン）の最終版が公開 | 本人確認・認証・フェデレーションの強さを、リスクに応じて別々に選ぶ考え方を引き継ぎつつ、要件を更新 |

認証プロトコル（SAML・OAuth 2.0・OIDC）の仕組みは web-security の 02章と付録A で扱う。

## 範囲（何であり、何でないか）

| IAM が扱うもの | IAM が扱わないもの（隣接領域） |
|---|---|
| 社員・委託先などの ID のライフサイクル（入社・異動・退職） | アプリの中の認証・認可の作り方（web-security） |
| IdP と SSO、MFA、条件付きアクセスの方針 | 顧客・利用者向けにアプリへ組み込む認証（CIAM。web-security 03章） |
| アクセス申請・承認、定期的なアクセスレビュー | 不正なログインや攻撃の検知・対応（security-operations） |
| 特権 ID の管理 | 人事情報そのもの（HCM。人事は ID の起点になる → 05章） |
| アプリへのプロビジョニング（SCIM など） | PC などの端末の管理（workplace） |

---

**出典**（確認日：2026-11-14）

- IGA の定義：Gartner「Market Guide for Identity Governance and Administration」の定義の引用（SailPoint・Pathlock の紹介記事経由）— https://pathlock.com/blog/2026-gartner-iga-market-guide-top-findings/ 、https://veza.com/?p=14326
- PAM の定義：Gartner「Magic Quadrant for Privileged Access Management」（2025-10-13）の市場定義の要約 — https://research.oz.spotlightar.com/reports/magic-quadrant-privileged-access-management-2025/market-definition
- Active Directory の登場と採用技術：@IT「Active Directory 25周年に寄せて」（2025-06）— https://atmarkit.itmedia.co.jp/ait/articles/2506/06/news005.html
- SCIM：IETF RFC 7644（2015-09）— https://datatracker.ietf.org/doc/rfc7644/ 、RFC Editor「SCIM」— https://www.rfc-editor.org/subjects/scim/
- Entra ID への改称：Azure 更新情報「Azure AD is becoming Microsoft Entra ID」（2023-07-11）— https://azure.microsoft.com/ja-jp/updates/azure-ad-is-becoming-microsoft-entra-id/
- NIST SP 800-63-4：NIST CSRC（最終版 2025-07-31）— https://csrc.nist.gov/pubs/sp/800/63/4/final
- 4つの機能の分け方は、上記をもとにした本資料の整理
