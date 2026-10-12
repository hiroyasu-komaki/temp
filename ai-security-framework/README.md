# ai-security-framework — 生成AIセキュリティガバナンス（NIST AI RMF × OWASP GenAI）

NIST を前提としたセキュリティガバナンス（CSF 2.0 導入済み）のもとで、生成AI（LLM・RAG・AIエージェント）のセキュリティケイパビリティを導入し、ガバナンスを安定させるためのコンセプト資料です。NIST AI RMF 1.0／AI 600-1 をガバナンス層として既存のガバナンスに追加し、OWASP Top 10 for LLM Applications 2026／Agentic Top 10 2026 を技術対策層として案件に適用します。NIST（経営の言葉）と OWASP（現場の言葉）を OWASP 公式の対応表でつなぎ、経営と現場の目線を合わせることも狙いです。

扱わないもの：基盤モデルの開発、AI倫理全般（公平性・環境影響）の詳細、個別製品の選定、AIを使ったサイバー防御（SOCでのAI活用）。

## ディレクトリ構成

```
ai-security-framework/
├── README.md                              ← このファイル
├── .gitignore
├── chapters/                              ← 【本体・正本】
│   ├── 01_purpose-and-positioning.md      目的、前提（CSF導入済み）、安定した状態の定義、二層構造と目線合わせ
│   ├── 02_nist-framework-family.md        CSF 2.0／AI RMF 1.0（19カテゴリ）／Playbook／AI 600-1（12リスク）／草案段階の文書
│   ├── 03_owasp-genai-project.md          OWASP GenAI Security Project の成果物、2026年版の改訂点
│   ├── 04_llm-top10-2026.md               LLM01〜LLM10 の定義・典型例・主要対策
│   ├── 05_agentic-top10-2026.md           ASI01〜ASI10 と設計原則、適用条件
│   ├── 06_nist-owasp-integration.md       二層の役割分担、公式対応表（AI 600-1／AI RMF／CSF 2.0）、関連枠組み
│   ├── 07_usecase-risk-checks.md          RAG型・エージェント型のチェックシート
│   ├── 08_risk-assessment-template.md     評価テンプレートの設計（事前分類・Tier・設問・報告）
│   └── 09_roadmap.md                      Phase 1〜3 と外部動向の追跡
├── proposal/
│   ├── ai-security-framework_proposal.md  全章を網羅した概要提案（IT部門内向け、正本）
│   └── ai-security-framework_proposal.pptx 同内容の説明スライド（25枚）
└── appendix/
    └── A_framework-sources.md             参照した枠組みの版・入手先、改訂時の見直し先
```

## 正本とどこから読むか

- 正本は `chapters/` の Markdown です。`proposal/` は意思決定者向けの要約で、章を更新したら提案書も追随させます。HTML版は作成していません。スライド（.pptx）を作る場合は `proposal/` に同じベース名で置きます。
- 経営層・CISO は 01 → 06 → 09、セキュリティガバナンス担当は 02 → 06 → 08 → 09、案件担当・アーキテクトは 04 → 05 → 07 の順を推奨します。
- 依拠する枠組みの版は `appendix/A_framework-sources.md` で固定しています。枠組みの改訂時は同ファイルの「改訂時の見直し先」に沿って更新してください。
- AI RMF の訳語は NIST AI 100-1 の公式日本語訳に合わせています。
