# 02 Webアプリケーションセキュリティの構造

## 要旨

セキュリティは、5つの設計原則（最小権限・多層防御・フェイルセキュア・セキュアデフォルト・オープン設計）を土台に、レイヤード構造・ゼロトラスト・WAF と TLS・ネットワーク分離を組み合わせたアーキテクチャとして組み立てます。1回のアクセスは、TLS による暗号化と通信相手の確認、認証（あなたは誰か）、認可（何をしてよいか）という関門を順に通ります。

## セキュリティ設計の5原則

「安全なシステム」は後付けの対策だけでは実現できません。設計の段階から組み込むべき考え方が5つあります。

### 最小権限（Least Privilege）

#### 考え方
ユーザーやシステムには、**その業務に必要な最小限の権限だけを与える**という原則です。「使わないかもしれないから念のため広めに」は禁物です。

#### 具体例
```
❌ 悪い例: アプリがデータベースに接続する際、管理者権限を使う
           → アプリが乗っ取られると、DB全体を削除・改ざん可能

✅ 良い例: アプリに「読み取り専用」権限だけを付与する
           → 乗っ取られても、データを盗まれる被害にとどまる
```

#### 守らなかった実例
2017年のEquifax情報漏洩では、最初に侵入されたシステムが、動作に必要なのは3つのデータベースだけなのに、40以上のデータベースにアクセスできる状態でした。攻撃者はそこから社内の複数のシステムへ侵入を広げ、約1億4,800万人分の個人情報が流出しました。

---

### 多層防御（Defense in Depth）

#### 考え方
セキュリティを「一枚の壁」で守ろうとするのではなく、**複数の独立した防御層を重ねる**という原則です。1層が突破されることを前提に設計します。

#### 具体例
```
攻撃者
  ↓
【第1層】 WAF（不正リクエストをブロック）
  ↓ 突破されたとしても…
【第2層】 アプリの入力検証（不正データを拒否）
  ↓ 突破されたとしても…
【第3層】 DBのアクセス制御（権限外の操作を拒否）
  ↓ 突破されたとしても…
【第4層】 ログ・監視（異常を検知してアラート）
```

#### 守らなかった実例
2021年のColonial Pipeline攻撃では、使われなくなったのに無効化されていなかったVPNアカウントのパスワードが漏れており、多要素認証（MFA）もなかったため、パスワード1つで社内ネットワークに侵入されました。守りがパスワードという1層しかなかった例です。同社は被害の拡大を防ぐためにパイプラインを約6日間止め、米国東海岸の燃料供給が混乱しました。

---

### フェイルセキュア（Fail Secure）

#### 考え方
エラーや予期しない障害が発生したとき、**「失敗した場合は拒否する」をデフォルトにする**という原則です。また、エラーメッセージに内部情報を含めないことも重要です。

#### 具体例
```
❌ 悪い例（失敗時に情報を漏らす）
   ログイン失敗 → 「そのメールアドレスは登録されていません」
                    ↑ 攻撃者が「有効なアカウント」を特定するヒントになる

✅ 良い例（失敗時に何も教えない）
   ログイン失敗 → 「メールアドレスまたはパスワードが正しくありません」
                    ↑ 有効かどうかを判断できない

❌ 悪い例（エラーに内部情報を含める）
   エラー発生 → スタックトレース（エラーの詳細）をそのままブラウザに表示
                 ↑ SQLのテーブル名・コードの構造が攻撃者に筒抜け
```

---

### セキュアデフォルト（Secure Defaults）

#### 考え方
システムの初期設定を「最も安全な状態」にしておくという原則です。**セキュリティを有効にするために設定変更が必要、ではなく、無効にするために設定変更が必要**という設計にします。

#### 具体例
```
❌ 悪い例: デフォルトでHTTP（暗号化なし）で動作する
           → 設定を知らない管理者が放置すると、通信が丸見えになる

✅ 良い例: 最初からHTTPSで動作し、HSTSを有効にしておく
           → 管理者が何もしなくても、暗号化された通信が使われる
```

#### 守らなかった実例
2016年のMiraiボットネットは、工場出荷時のユーザー名とパスワード（60組あまり）のままインターネットにつながっていたカメラやルーターなどのIoT機器を乗っ取り、数十万台規模に広がりました。乗っ取った機器から大規模なDDoS攻撃を行い、DNS事業者Dynへの攻撃では多くの大手Webサービスが一時的に使えなくなりました。

---

### オープン設計（Open Design）

#### 考え方
「仕組みを秘密にすることでセキュリティを保つ」という設計に頼らないという原則です。**暗号化アルゴリズムなどは公開・検証済みの標準規格を使う**ことで、より堅牢な安全性を実現します。

#### 具体例
```
❌ 悪い例: 自社オリジナルの暗号方式を使う
           → 公開検証を経ていないため、見落とした欠陥を突かれやすい
           → 設計者が退職・情報漏洩すると全て無効化される

✅ 良い例: OpenSSL、OAuth2などの公開・標準化された仕組みを使う
           → 世界中の専門家が検証・改善し続けているため、信頼性が高い
```

---

### まとめ

| 原則 | 一言で言うと | 守らないとどうなるか |
|------|------------|-------------------|
| 最小権限 | 必要なものだけ渡す | 侵害が全体に波及する |
| 多層防御 | 一枚の壁に頼らない | 1箇所の突破で全滅する |
| フェイルセキュア | 失敗時は閉じる | エラーが攻撃の手がかりになる |
| セキュアデフォルト | 最初から安全にしておく | 設定ミスが即脆弱性になる |
| オープン設計 | 秘密主義に頼らない | 独自実装が簡単に破られる |

これら5つの原則は独立したものではなく、組み合わせて実践することで初めて「設計レベルで安全なシステム」が実現します。

## セキュアアーキテクチャ設計

### レイヤード構造

フロントエンド・バックエンド・データ・インフラを論理的・物理的に分離します。1つの層が侵害されても、他の層への影響を最小限に抑えることが目的です。各層ではそれぞれ独立した認証・検証を行います。

```mermaid
flowchart LR
    User["👤 ユーザー"]

    subgraph Front["第1層：フロントエンド"]
        SPA["SPA（React）"]
    end

    subgraph Gateway["第2層：ゲートウェイ"]
        AG["API Gateway（App Gateway + WAF）"]
    end

    subgraph Back["第3層：バックエンド"]
        MS1["マイクロサービスA（認証）"]
        MS2["マイクロサービスB（ビジネスロジック）"]
        MS3["マイクロサービスC（ファイル処理）"]
    end

    subgraph Data["第4層：データ"]
        DB["DB（Private）"]
        Cache["キャッシュ"]
        Storage["ストレージ"]
    end

    User -->|"HTTPS"| SPA
    SPA -->|"HTTPS + 認証トークン"| AG
    AG -->|"検証済みリクエストのみ通過"| MS1
    AG -->|"検証済みリクエストのみ通過"| MS2
    AG -->|"検証済みリクエストのみ通過"| MS3
    MS1 & MS2 & MS3 -->|"Private接続のみ"| DB
    MS2 --> Cache
    MS3 --> Storage
```

> 各層の間に検証ポイントを設けることで、1層突破が即全体の崩壊につながらない構造を実現します。

---

### ゼロトラストモデル

「社内ネットワークだから安全」「認証済みだから信頼する」という前提を排除し、**すべての通信を毎回検証する**モデルです。
内部サービス間の通信であっても例外はありません。

```mermaid
flowchart LR
    User["👤 ユーザー"]

    subgraph ZT["ゼロトラスト検証"]
        direction TB
        MFA["① MFA認証"]
        Token["② JWTトークン発行"]
        Policy["③ アクセスポリシー確認（役割・デバイス・場所）"]
    end

    subgraph Services["サービス群"]
        direction TB
        SvcA["サービスA"]
        SvcB["サービスB"]
        DB["DB"]
    end

    User --> MFA --> Token --> Policy
    Policy -->|"許可された場合のみ"| SvcA
    Policy -->|"許可された場合のみ"| SvcB
    SvcA -->|"再検証"| SvcB
    SvcB -->|"再検証"| DB

    style ZT fill:#fff3cd,stroke:#ffc107
```

> サービスAが侵害されても、そこからDBへ直接アクセスすることはできません。横方向への侵害拡大（ラテラルムーブメント）を防ぎます。

---

### 通信保護とWAF

外部からの通信はすべてWAFで検査し、内部通信はTLS暗号化を徹底します。WAFは中身を検査するため、TLSを終端（復号）した後のリクエストを検査します（WAF自身がTLSを終端する製品も多い）。公開するエンドポイントを最小限に絞ることも重要です。

```mermaid
flowchart LR
    Internet["🌐 インターネット"]

    subgraph Edge["エッジ保護"]
        TLS["TLS終端（HTTPS強制・HSTSヘッダ）"]
        WAF["WAF・SQLi検知・XSS検知・OWASP CRSルール"]
    end

    subgraph Internal["内部通信（非公開）"]
        App["アプリサーバー"]
        DB["DBPrivate Endpointのみ"]
    end

    Blocked["❌ 不正リクエストブロック"]

    Internet -->|"HTTPS"| TLS
    TLS -->|"復号したリクエスト"| WAF
    WAF -->|"検知した場合"| Blocked
    WAF -->|"正常な場合・再暗号化"| App
    App -->|"Private接続のみ"| DB

    style Blocked fill:#f8d7da,stroke:#dc3545,color:#000
    style Edge fill:#d1ecf1,stroke:#17a2b8,color:#000
```

---

### ネットワーク分離とセグメンテーション

ネットワークをサブネット（区画）に分割し、区画間の通信を厳密に制御します。侵害が発生した場合でも、該当区画だけを隔離することで被害を封じ込めます。

```mermaid
flowchart LR
    Internet["🌐 インターネット"]

    subgraph VNet["仮想ネットワーク（VNet）"]

        subgraph PublicSubnet["パブリックサブネット（外部公開あり）"]
            WAF["WAF / ロードバランサー"]
            Web["Webサーバー"]
        end

        subgraph PrivateSubnet["プライベートサブネット（外部公開なし）"]
            API["APIサーバー"]
            DB["DB（内部アクセスのみ）"]
        end

        NSG["NSG（ネットワークセキュリティグループ）・DBへの直接アクセスを拒否・APIへはWebサーバーからのみ許可"]
    end

    Internet --> WAF --> Web
    Web -->|"NSGで制御"| API
    API -->|"NSGで制御"| DB
    NSG -.->|"監視・制御"| PrivateSubnet

    style PublicSubnet fill:#fff3cd,stroke:#ffc107,color:#000
    style PrivateSubnet fill:#d4edda,stroke:#28a745,color:#000
```

---

### 一般構成 vs セキュア構成の比較

```mermaid
flowchart LR
    subgraph Insecure["❌ 一般的な構成（危険）"]
        direction LR
        U1["ユーザー"]
        App1["Appサーバー（直接公開）"]
        DB1["DB（パブリック接続）"]
        Log1["アプリログのみ"]

        U1 -->|"HTTP可"| App1
        App1 -->|"平文・信頼前提"| DB1
    end

    subgraph Secure["✅ セキュアな構成"]
        direction LR
        U2["ユーザー"]
        GW["WAF＋API Gateway"]
        App2["Appサーバー（非公開）"]
        DB2["DB（Private接続のみ）"]
        Monitor["統合監視（ログ＋異常検知）"]

        U2 -->|"HTTPS強制"| GW
        GW -->|"JWT認証済みのみ"| App2
        App2 -->|"Private Endpoint"| DB2
        App2 & DB2 --> Monitor
    end

    style Insecure fill:#f8d7da,stroke:#dc3545,color:#000
    style Secure fill:#d4edda,stroke:#28a745,color:#000
```

---

### まとめ

これら4つの設計アプローチは、それぞれ独立して機能しますが、組み合わせることで真に堅牢なアーキテクチャになります。

| 設計アプローチ | 守るもの | 侵害時の効果 |
|--------------|---------|------------|
| レイヤード構造 | 層をまたいだ侵害拡大 | 被害を1層内に封じ込める |
| ゼロトラスト | 横方向への侵害拡大 | サービス間の不正移動を防ぐ |
| WAF・TLS | 外部からの攻撃通信 | 既知の攻撃パターンを入口で遮断 |
| ネットワーク分離 | 区画をまたいだアクセス | 侵害区画だけを即座に隔離できる |

## 全体像：1回のアクセスで何が起きているか

以下で扱う概念（ハンドシェイク・証明書・認証・認可）は、それぞれ独立したトピックではなく、**1回のアクセスの中で順番に積み重なる関門**です。まず全体の流れを把握してから、各関門の詳細に入ります。

---

### 4つの関門と役割

```mermaid
sequenceDiagram
    actor User as 👤 ユーザー
    participant Browser as ブラウザ
    participant TLS as TLS証明書の検証
    participant AuthN as 認証（Authentication）
    participant AuthZ as 認可（Authorization）
    participant Resource as 🗂️ リソース

    Note over Browser,TLS: ① まず「通信路を安全に確立する」
    Browser->>TLS: ハンドシェイク → サーバー証明書を検証
    TLS-->>Browser: ✅ 本物のサーバーと確認・暗号化通信を確立

    Note over Browser,AuthN: ② 次に「あなたは誰か」を確認
    Browser->>AuthN: ログイン情報 or クライアント証明書を提示
    AuthN-->>Browser: ✅ 本人確認OK → JWTトークン発行

    Note over Browser,AuthZ: ③ 最後に「何をしてよいか」を確認
    Browser->>AuthZ: JWTトークン付きでリクエスト
    AuthZ-->>Browser: ✅ 権限あり → アクセス許可
    AuthZ->>Resource: データを返す
```

| 関門 | 問い | 使う技術 | 突破されると |
|------|------|---------|------------|
| **① ハンドシェイク・TLS** | 通信相手は本物か？通信路は安全か？ | TLS証明書（CA発行） | 通信内容が盗まれる・偽サイトに誘導される |
| **② 認証** | あなたは誰か？ | パスワード・MFA・クライアント証明書 | 不正ログインが成立する |
| **③ 認可** | 何をしてよいか？ | RBAC・ABAC・JWT | 権限外のデータにアクセスされる |

---

### 積み重なる防御の構造

```mermaid
flowchart LR
    Internet["🌐 インターネット"]

    G1["🤝 関門①ハンドシェイク＋TLS通信路を確立・保護"]
    G2["🪪 関門②認証本人確認"]
    G3["🔑 関門③認可権限確認"]
    Resource["🗂️ リソース"]

    Deny1["❌ 偽サイト・盗聴を遮断"]
    Deny2["❌ 不正ログインを遮断"]
    Deny3["❌ 権限外アクセスを遮断"]

    Internet --> G1 --> G2 --> G3 --> Resource
    G1 --> Deny1
    G2 --> Deny2
    G3 --> Deny3

    style Deny1 fill:#f8d7da,stroke:#dc3545,color:#000
    style Deny2 fill:#f8d7da,stroke:#dc3545,color:#000
    style Deny3 fill:#f8d7da,stroke:#dc3545,color:#000
    style Resource fill:#d4edda,stroke:#28a745,color:#000
```

> どれか一つが欠けても安全な通信は成立しません。以降の章ではこの順番に沿って各関門を掘り下げます。

## ハンドシェイクとTLS暗号化

### ハンドシェイクとは

「ハンドシェイク（握手）」とは、**実際のデータ通信を始める前に、双方が「安全に話せる状態か」を確認し合う準備手続き**のことです。

人間に例えると、電話をかけたときに「もしもし、聞こえますか？」「聞こえます、どうぞ」とやり取りしてから本題に入るのと同じです。

ハンドシェイクは認証・認可よりも**さらに手前の「土台」**にあたります。この土台があって初めて、認証情報（パスワードやトークン）を安全にやり取りできます。逆に言えば、**ハンドシェイクが成立しない＝そもそも安全に通信できない**状態です。

```mermaid
flowchart LR
    H["🤝 ハンドシェイク通信路を安全に確立"]
    T["🔒 TLS暗号化通信盗聴・改ざんを防ぐ"]
    A["🪪 認証本人確認"]
    Z["🔑 認可権限確認"]

    H -->|"安全な通信路の上で"| T
    T -->|"安全な通信路の上で"| A
    A -->|"確認済みの上で"| Z

    style H fill:#d1ecf1,stroke:#17a2b8,color:#000
```

---

### TLSハンドシェイクの流れ

```mermaid
sequenceDiagram
    actor Client as 👤 ブラウザ（Client）
    participant Server as 🖥️ Webサーバー（Server）

    Note over Client,Server: ① 挨拶と鍵の材料の交換（ClientHello / ServerHello）
    Client->>Server: 「TLS1.3使えます。暗号方式はAES/ChaCha20に対応。鍵の材料はこれです」
    Server->>Client: 「TLS1.3・AESを使いましょう。こちらの鍵の材料はこれです」
    Client->>Client: 共通の暗号化鍵を生成
    Server->>Server: 共通の暗号化鍵を生成

    Note over Client,Server: ② サーバーの身元確認（ここから暗号化されている）
    Server->>Client: TLS証明書を提示「私はexample.comです（CA署名付き）」＋秘密鍵を持っている証明
    Client->>Client: 証明書の署名を手元のルート証明書で検証✅ 本物のサーバーと確認

    Note over Client,Server: ③ 暗号化通信の開始（Finished）
    Server->>Client: 「準備完了です🔒」
    Client->>Server: 「準備完了です🔒」
    Client->>Server: 暗号化されたHTTPリクエスト
    Server->>Client: 暗号化されたHTTPレスポンス
```

TLS 1.3 では、最初の往復で鍵の材料を交換するため、証明書のやり取りから先はすでに暗号化されています（TLS 1.2 では、証明書を受け取った後に鍵を交換していました）。

### まとめ

| | **内容** | **もし省略すると** |
|---|---|---|
| **ハンドシェイク** | 通信相手の確認・暗号化方式の合意・鍵の共有 | 偽サーバーと通信・通信内容が丸見え |
| **TLS暗号化** | ハンドシェイクで決めた鍵で通信を暗号化 | パスワードや個人情報が盗まれる |

## 証明書の基礎：公開鍵暗号の仕組み

証明書を理解するには、まず前提となる「公開鍵暗号」を押さえる必要があります。

```mermaid
flowchart LR
    subgraph KeyPair["鍵ペア（セットで生成）"]
        Pub["🔓 公開鍵誰にでも配布してよい"]
        Pri["🔐 秘密鍵絶対に外に出さない"]
    end

    Encrypt["暗号化：公開鍵で施錠→ 秘密鍵を持つ人しか開けられない"]
    Sign["署名：秘密鍵で署名→ 公開鍵で「本物か」確認できる"]

    Pub --> Encrypt
    Pri --> Sign
```

証明書とは「**この公開鍵は確かに本物です**」と第三者機関（CA）が保証した文書です。

---

### TLS/SSL証明書（HTTPS通信の基盤）

#### 何のためにある？

ブラウザが「今通信している相手は本物のサーバーか」を確認するための仕組みです。これがないと、偽サイトへの誘導（中間者攻撃）を検知できません。

```mermaid
sequenceDiagram
    actor User as 👤 ブラウザ
    participant Server as Webサーバー
    participant CA as 認証局（CA）例：Let's Encrypt

    Note over Server,CA: 事前準備（証明書の取得）
    Server->>CA: 「example.comの証明書をください」
    CA->>CA: ドメイン所有者であることを確認
    CA->>Server: TLS証明書を発行（CAの署名付き）

    Note over User,Server: 実際の通信時
    User->>Server: ① HTTPSでアクセス
    Server->>User: ② TLS証明書を提示
    User->>User: ③ 手元のルート証明書でCAの署名を検証（CAに問い合わせるわけではない）
    User->>Server: ④ 暗号化通信を開始 🔒
```

> ブラウザは、OSやブラウザに組み込まれたルート証明書を使って、署名を手元で検証します。CAの情報を参照するのは、失効の確認（CRL・OCSP）を行う場合などに限られます。

#### 証明書の種類

| 種類 | 検証レベル | 取得難易度 | 向いている用途 |
|------|----------|----------|--------------|
| **DV（ドメイン認証）** | ドメイン所有のみ確認 | 簡単・無料（Let's Encrypt）| 個人サイト・開発環境 |
| **OV（組織認証）** | 組織の実在を確認 | 中程度 | 企業サイト・業務システム |
| **EV（拡張認証）** | 組織を厳格に審査 | 高い・有償 | 金融・ECなど信頼性が重要なサービス（主要ブラウザは2019年ごろからアドレスバーでのEV表示をやめており、利用者から見た違いは小さい） |

#### 有効期限と失効の注意点

```mermaid
flowchart LR
    Issue["証明書発行"]
    Valid["✅ 有効期間（最大200日。2027年3月から100日、2029年3月から47日）"]
    Expire["❌ 期限切れブラウザが警告表示"]
    Revoke["❌ 失効（CRL/OCSP）秘密鍵漏洩時など緊急無効化"]
    Renew["🔄 更新"]

    Issue --> Valid --> Expire --> Renew --> Valid
    Valid --> Revoke
```

> 証明書の期限切れはサービス停止に直結します。公開証明書の最大有効期間は、CA/Browser Forum の決定（Ballot SC-081v3）により、398日から2026年3月に200日、2027年3月に100日、2029年3月に47日へと段階的に短くなります。手作業での更新は現実的でなくなるため、ACMEなどによる自動更新を前提にし、期限監視も設定しましょう。

---

### クライアント証明書（デバイス・ユーザー認証）

#### 何のためにある？

TLS証明書が「サーバーの身元証明」であるのに対し、クライアント証明書は**「接続してきた端末・ユーザーの身元証明」**です。パスワードを使わずに、デバイス自体を認証できます。

```mermaid
sequenceDiagram
    actor User as 👤 ユーザー（端末）
    participant Server as 社内システム
    participant IdP as 社内IdP / MDM

    Note over User,IdP: 事前準備（証明書のインストール）
    IdP->>User: クライアント証明書を発行・端末にインストール

    Note over User,Server: アクセス時
    User->>Server: ① アクセス要求
    Server->>User: ② 「クライアント証明書を提示してください」
    User->>Server: ③ 端末の証明書を提示
    Server->>Server: ④ 証明書を検証（有効期限・失効・発行元）
    Server->>User: ⑤ 認証OK → アクセス許可 ✅
```

#### パスワード認証との比較

| | **パスワード認証** | **クライアント証明書認証** |
|---|---|---|
| **盗難リスク** | フィッシングで盗まれる | 秘密鍵をTPMなどに取り出せない形で保存すれば、盗難は困難（取り出し可能な形で保存すると、コピーされうる） |
| **フィッシング耐性** | 低い | 高い（秘密鍵は送信されず、署名はその接続にしか使えないため、偽サイトが受け取っても使い回せない） |
| **管理コスト** | 低い | 高い（証明書の発行・失効管理が必要） |
| **ユーザー体験** | パスワード入力が必要 | 透過的（意識せずに認証される） |
| **向いている場面** | 一般ユーザー向けサービス | 社内システム・ゼロトラスト環境 |

#### ゼロトラストにおける役割

```mermaid
flowchart LR
    Device["💻 端末"]

    subgraph ZeroTrust["ゼロトラスト検証"]
        C1{"クライアント証明書あり？"}
        C2{"証明書は有効期限内？"}
        C3{"MDM管理済みデバイス？"}
    end

    Allow["✅ アクセス許可"]
    Deny["❌ アクセス拒否"]

    Device --> C1
    C1 -->|"YES"| C2
    C2 -->|"YES"| C3
    C3 -->|"YES"| Allow
    C1 & C2 & C3 -->|"NO"| Deny

    style Allow fill:#d4edda,stroke:#28a745,color:#000
    style Deny fill:#f8d7da,stroke:#dc3545,color:#000
```

#### まとめ：2つの証明書の役割の違い

| | **TLS/SSL証明書** | **クライアント証明書** |
|---|---|---|
| **誰の証明？** | サーバー | 端末・ユーザー |
| **誰が検証？** | ブラウザ | サーバー |
| **主な目的** | 通信の暗号化・サーバー正当性確認 | デバイス認証・不正端末の排除 |
| **失効時の影響** | ブラウザ警告・サービス停止 | その端末のアクセスが即遮断 |

---

### クライアント証明書は認証を兼ねる

ここが混乱しやすいポイントです。TLS証明書は常に「通信路の保護」ですが、クライアント証明書は**認証のステップを担う**こともできます。

```mermaid
flowchart TD
    subgraph Pattern1["パターン①：一般的なWebアプリ"]
        direction LR
        P1_TLS["TLS証明書通信を暗号化"]
        P1_PW["パスワード＋MFA認証"]
        P1_JWT["JWTトークン認可"]
        P1_TLS --> P1_PW --> P1_JWT
    end

    subgraph Pattern2["パターン②：ゼロトラスト・社内システム"]
        direction LR
        P2_TLS["TLS証明書通信を暗号化"]
        P2_CERT["クライアント証明書認証（パスワード不要）"]
        P2_JWT["JWTトークン認可"]
        P2_TLS --> P2_CERT --> P2_JWT
    end

    style Pattern1 fill:#fff3cd,stroke:#ffc107
    style Pattern2 fill:#d4edda,stroke:#28a745
```

## 認証

### 認証とは？

「あなたは誰ですか？」を確認するステップです。本人確認に成功するとトークン（JWT）が発行され、次の関門である認可（次節）へと引き渡されます。

```mermaid
flowchart LR
    User["👤 ユーザー"]
    AuthN["認証（Authentication）<br>「あなたは誰ですか？」<br>本人確認"]
    Token["JWTトークン発行<br>→ 認可ステップへ"]
    DenyAuthN["❌ 401 Unauthorized<br>認証失敗（本人確認できず）"]

    User -->|"ID・パスワード・MFAなど"| AuthN
    AuthN -->|"本人確認OK"| Token
    AuthN -->|"本人確認NG"| DenyAuthN

    style AuthN fill:#d1ecf1,stroke:#17a2b8,color:#000
    style Token fill:#d4edda,stroke:#28a745,color:#000
    style DenyAuthN fill:#f8d7da,stroke:#dc3545,color:#000
```

### 認証設計：自前管理をやめてIdPに委譲する（OAuth2/OIDC）

#### 考え方
パスワードの保管・MFAの実装・ブルートフォース対策などを自前で実装するのは、コストが高く脆弱性を生みやすいです。OAuth2/OpenID Connect（OIDC）を基盤に、実績あるIdP（Identity Provider）に認証を委譲するのが現代のベストプラクティスです。

> SAMLを使った認証フローについては[付録A](../appendix/A_saml-vs-oidc.md)で同じ登場人物を使って比較しています。

> 委譲先となる社員向けの IdP そのもの（ID のライフサイクル、MFA の方針、特権 ID の管理）は [identity](../../identity/README.md) で、認証ログの監視と不審なログインへの対応は [security-operations](../../security-operations/README.md) で扱います。

#### 認証フロー（OAuth2/OIDC）

```mermaid
sequenceDiagram
    actor User as 👤 ユーザー
    participant App as Webアプリ
    participant IdP as IdP（Entra ID / Auth0 など）
    participant API as APIサーバー
    participant Log as 監視ログ

    User->>App: ① ログインボタンをクリック
    App->>User: ② IdPへリダイレクト（認可リクエスト＋PKCE）
    User->>IdP: ③ ログイン画面で認証情報＋MFAを入力
    IdP->>User: ④ 認可コードを付けてアプリへリダイレクト
    User->>App: ⑤ ブラウザが認可コードをアプリへ渡す
    App->>IdP: ⑥ 認可コードでトークンを要求（アプリとIdPの直接通信）
    IdP->>App: ⑦ IDトークン（JWT）・アクセストークンを発行
    App->>API: ⑧ APIリクエスト（Authorizationヘッダにアクセストークン）
    API->>API: ⑨ トークン検証・権限チェック
    API->>App: ⑩ レスポンス
    IdP->>Log: ⑪ 全認証イベントをログ記録
```

> これは OAuth2 の「認可コードフロー＋PKCE」で、Webアプリ・モバイルアプリの標準的な方式です。ブラウザが中継するのは短時間しか使えない認可コードだけで、トークン本体はアプリがIdPから直接受け取ります。IDトークンはJWT形式と決まっていますが、アクセストークンの形式はIdPによって異なります（JWTの場合が多い）。

#### 自前実装 vs IdP委譲の比較

| 項目 | 自前認証 | IdP委譲（推奨） |
|------|---------|--------------|
| MFA対応 | 自分で実装が必要 | 標準サポート |
| ブルートフォース対策 | 自分で実装が必要 | IdP側で自動対処 |
| ログ・監視 | 自前で構築 | 統合監視に直結 |
| 侵害時の対応 | セッションやトークンの無効化を自前で実装 | IdP側でセッション・リフレッシュトークンを一括失効できる（発行済みのアクセストークンは、有効期限まで使える場合がある） |

### まとめ

| 設計ポイント | やること | やってはいけないこと |
|------------|---------|-----------------|
| 認証方式 | IdP（OAuth2/OIDC）に委譲 | パスワードを自前で保管・管理 |
| MFA | 原則すべての利用者に必須化（可能ならフィッシング耐性のある方式） | パスワードのみで認証を完結させる |
| 監視 | 全認証イベントをログに記録 | エラー時だけログを取る |

## 認可

### 認可とは？

「何をしてよいですか？」を確認するステップです。前節の認証でトークンが発行された後、APIリクエストのたびにサーバー側でこのトークンを検証し、要求された操作の権限があるかを確認します。

```mermaid
flowchart LR
    Token["JWTトークン<br>（認証済み）"]
    AuthZ["認可（Authorization）<br>「何をしてよいですか？」<br>権限確認"]
    Resource["🗂️ リソース"]
    DenyAuthZ["❌ 403 Forbidden<br>認可失敗（権限なし）"]

    Token -->|"APIリクエストのたびに"| AuthZ
    AuthZ -->|"権限あり → アクセス許可"| Resource
    AuthZ -->|"権限なし"| DenyAuthZ

    style AuthZ fill:#d4edda,stroke:#28a745,color:#000
    style Resource fill:#d4edda,stroke:#28a745,color:#000
    style DenyAuthZ fill:#f8d7da,stroke:#dc3545,color:#000
```

---

### 認可設計：「何ができるか」はサーバー側で必ず確認する

#### 考え方
認可（権限チェック）はサーバー側で行うことが絶対条件です。フロントエンドだけで「管理者メニューを非表示にする」といった制御は、開発者ツールで簡単に書き換えられてしまいます。

```mermaid
flowchart TB
    subgraph NG["❌ フロントのみの制御（危険）"]
        direction LR
        F1["フロントで管理者ボタンを非表示"]
        Hack["攻撃者がDevToolsでHTMLを書き換え"]
        F2["管理者APIに直接アクセス成功"]
        F1 --> Hack --> F2
    end

    subgraph OK["✅ サーバー側での制御（正しい）"]
        direction LR
        S1["フロントで管理者ボタンを非表示（UIのみ）"]
        S2["APIサーバーで権限チェック"]
        S3["権限なし → 403拒否権限あり → 処理実行"]
        S1 --> S2 --> S3
    end

    style NG fill:#f8d7da,stroke:#dc3545,color:#000
    style OK fill:#d4edda,stroke:#28a745,color:#000
```

#### RBACとABACの使い分け

| | RBAC（ロールベース） | ABAC（属性ベース） |
|---|---|---|
| **制御の基準** | ユーザーの「役割」で判断 | 役割に加え、場所・時間・デバイスなど複数の「属性」で判断 |
| **具体例** | `admin`は全操作可、`user`は閲覧のみ | 日本国内・社内デバイス・営業時間内の場合のみ承認 |
| **✅ Pros** | シンプルで管理しやすい／導入コストが低い／監査しやすい | きめ細かい制御が可能／条件の組み合わせで柔軟に対応できる |
| **❌ Cons** | 条件が複雑になるとロールが爆発的に増える／状況に応じた動的制御が苦手 | 設計・管理が複雑／条件が増えるほどデバッグが難しくなる |
| **向いている場面** | 社内システム・管理画面など役割が明確なシステム | グローバルサービス・ゼロトラスト環境など状況に応じた制御が必要なシステム |

一般的には**まずRBACで設計し、より細かい制御が必要な箇所にABACを組み合わせる**のが現実的なアプローチです。

---

### まとめ

| 設計ポイント | やること | やってはいけないこと |
|------------|---------|-----------------|
| 認可の実施場所 | サーバー側でロール・属性を検証 | フロントエンドの表示制御だけに頼る |
| ロール設計 | まずRBACで設計し、必要に応じてABACを追加 | 最初からABACで複雑に設計しすぎる |
| 監視 | APIリクエストごとに権限チェック結果をログに記録 | エラー時だけログを取る |

---

**出典**（確認日：2026-11-14）

- Equifax：米下院 監視・政府改革委員会「The Equifax Data Breach」（2018-12）— https://oversight.house.gov/wp-content/uploads/2018/12/Equifax-Report.pdf 。40以上のデータベースにアクセスできた点は Crowell & Moring による同報告書の要約 — https://crowell.com/en/insights/client-alerts/lessons-from-the-house-report-on-the-equifax-breach-tRBKUpg6sU8gxxy6uRxaKo
- Colonial Pipeline：同社CEOの米上院での証言（2021-06-08）の報道 — https://amp.insurancejournal.com/news/national/2021/06/09/617870.htm 、Mandiant による侵入経路の説明の報道 — https://www.bangordailynews.com/2021/06/05/nation/hackers-breached-colonial-pipeline-using-compromised-password/
- Mirai：Antonakakis ほか「Understanding the Mirai Botnet」（USENIX Security 2017）— https://zakird.com/papers/mirai.pdf
- 証明書の最大有効期間：CA/Browser Forum Ballot SC-081v3（2025-04 可決）。要点は DNSimple の解説 — https://support.dnsimple.com/articles/announcement-ssl-certificate-validity-changes/
- TLS 1.3 のハンドシェイク：RFC 8446 — https://datatracker.ietf.org/doc/html/rfc8446
- 認可コードフローと PKCE：RFC 6749、RFC 7636、OpenID Connect Core 1.0（付録Aの出典を参照）
- 設計の5原則、アーキテクチャ、RBAC/ABAC：一般的な考え方をまとめた本資料の整理
