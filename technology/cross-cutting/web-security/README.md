# web-security — Webアプリケーションのセキュリティ

**一言でいうと**：Webアプリケーションに対する脅威の変遷と、それに対抗する設計原則・アーキテクチャ・暗号化・認証・認可を整理するトピック。

- **扱うこと**：脅威の変遷と具体例、セキュリティ設計の5原則、セキュアアーキテクチャ、TLS と証明書、アプリから見た認証（IdP への委譲）・認可、アプリ利用者向けの IDaaS（CIAM）
- **扱わないこと**：社員向けの ID 基盤と運用（IdP・SSO・ID のライフサイクル・特権 ID → identity）、攻撃の検知と対応・脆弱性管理の運用（→ security-operations）、設計原則を開発の工程に組み込む仕組み（→ app-development）、広く使われる部品の重大脆弱性への組織的な対処（→ governance/zero-day-response）
- 当社固有の情報は 06章にだけ書く（未作成）

## ディレクトリ構成

```
web-security/
├── README.md
├── chapters/
│   ├── 01_definition.md   定義と範囲：脅威と対策の変遷、各時代の脅威と防御の具体例
│   ├── 02_structure.md    構造：設計の5原則、セキュアアーキテクチャ、1回のアクセスの全体像、TLS、証明書、認証、認可
│   └── 03_landscape.md    製品と提供形態：CIAM（Auth0・Cognito・Firebase など）、WAF・WAAP、TLS の証明書、国内の製品、市場の動き
└── appendix/
    └── A_saml-vs-oidc.md  SAML とは（OAuth2/OIDC との比較）
```

## 読み方

- 隣接領域との境界（どのシステムが何を持つか）は [function-allocation](../../cross-cutting/function-allocation/function-allocation.md) にまとめている。
- 01 → 02 → 03 の順に読む。
- 正本は `chapters/` と `appendix/` の Markdown。
- 「要確認」は裏付けが取れていない記述。

## 章の作成状況

| 章 | 状態 | 最終確認日 |
|---|---|---|
| 01〜03、付録A | 作成済み（旧 Part 1・Part 2 を5つの観点に組み替え）。出典を追記し、誤りを修正（実例3件、証明書・TLS・OIDCの流れなど）。03章の社員向け IdP（Entra ID・Okta）は identity 03章へ移した。03章は記入要領に沿って書き直し、WAF・WAAP と TLS の証明書を加えた（2026-11-14） | 2026-11-14 |
| 04・05・06 | 素材がないため未作成 | — |
