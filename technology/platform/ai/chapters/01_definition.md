# 01 AI の定義と範囲

## 要旨

本トピックが扱う AI は、主に**生成 AI**（文章・画像・コードなどを作る AI）と、その中心にある**大規模言語モデル（LLM）**、および LLM が外部の道具を使って作業を進める **AI エージェント**である。企業にとっての論点は、モデルそのものの性能より、**自社のデータとどうつなぐか**と、**誤り・情報漏えい・攻撃のリスクをどう抑えるか**にある（本資料の整理）。

## 定義

| 用語 | 内容（本資料の整理） |
|---|---|
| 生成 AI | 学習したデータをもとに、新しい文章・画像・音声・コードなどを生成する AI |
| 大規模言語モデル（LLM） | 大量の文章で学習し、次に来る言葉を予測することで文章を生成するモデル。現在の主なモデルは Transformer という構造に基づく |
| RAG（検索拡張生成） | 質問に関係する文書を検索して LLM に渡し、その内容に基づいて回答させる方式。モデルを学習し直さずに、自社のデータを使える |
| AI エージェント | LLM が、検索・ファイル操作・業務システムの操作などの道具を自分で選んで使い、複数の手順を進めて目的を達成する仕組み |

## 成り立ち

| 年 | 出来事 | 意味 |
|---|---|---|
| 2017 | Google の研究者が論文「Attention Is All You Need」で Transformer を発表 | 現在の主要な LLM の土台になる構造が生まれる |
| 2020 | Patrick Lewis らが RAG（Retrieval-Augmented Generation）の論文を発表 | 外部の文書を検索して回答に使う方式が提案される |
| 2022 | OpenAI が ChatGPT を公開（11月30日） | 生成 AI が一般の利用者に広がる |
| 2023 | NIST が AI リスクマネジメントフレームワーク（AI RMF 1.0）を公開（1月）。Microsoft 365 Copilot が企業向けに一般提供（11月） | AI のリスク管理の枠組みと、業務ソフトへの組み込みが始まる |
| 2024 | EU AI 法が発効（8月1日）。NIST が生成 AI プロファイル（AI 600-1）を公開（7月）。Anthropic が Model Context Protocol（MCP）を公開（11月） | 規制と、AI を外部のシステムにつなぐ標準が出てくる |
| 2025 | 日本の AI 法（人工知能関連技術の研究開発及び活用の推進に関する法律）が成立（5月28日）、9月1日に全面施行。12月に AI 基本計画を閣議決定。MCP を Linux Foundation の Agentic AI Foundation に寄贈（12月） | 国内の推進の枠組みができる。AI エージェントの接続の標準が中立な団体に移る |
| 2026 | EU の Digital Omnibus on AI が発効（7月27日）。高リスク AI の義務の適用が2027年12月2日に延期される | 規制の適用時期が動く |

## 範囲（何であり、何でないか）

| AI が扱うもの | 扱わないもの（隣接領域） |
|---|---|
| 生成 AI・LLM・RAG・AI エージェントの仕組み | AI の利用に関する社内のルールとガバナンス（governance/ai-security-framework） |
| AI の基盤（モデルの提供サービス、接続の標準） | GPU などの計算基盤そのもの（infrastructure） |
| AI に固有のリスク（誤り、プロンプトインジェクションなど）と、その技術的な対策 | 業務ソフトに組み込まれた AI のライセンスと配布（workplace） |
| 国内外の規制の概要 | 従来型の機械学習・統計分析（→ [analytics](../../../data/analytics/README.md)） |

## 社内のルールとの違い

AI の利用に関する社内のルールと体制（何に使ってよいか、誰が承認するか、リスクをどう評価するか）は、ガバナンスの資料（governance/ai-security-framework）で扱う。本トピックは、そのルールの対象になる**仕組みとリスクの中身**を扱う。

---

**出典**（確認日：2026-11-14）

- Transformer（2017）：Towards AI — https://pub.towardsai.net/the-nine-page-paper-that-rewired-artificial-intelligence-da4819389822 、IntuitionLabs — https://intuitionlabs.ai/articles/key-innovations-behind-chatgpt
- RAG（2020）と ChatGPT（2022-11-30）：解説記事 — https://luckyplz.pages.dev/blog/ai-evo-08-rag-en/
- NIST AI RMF 1.0（2023-01-26）と AI 600-1（2024-07-26）：NordLayer — https://nordlayer.com/learn/ai-security/nist-ai-risk-management-framework/ 、arc42 — https://quality.arc42.org/standards/nist-ai-rmf 、NIST AI 600-1 — https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- Microsoft 365 Copilot の一般提供：Redmond Channel Partner（2023-11-01）— https://rcpmag.com/articles/2023/11/01/microsoft-365-copilot-at-ga.aspx
- EU AI 法と Digital Omnibus：Cooley（2026-07）— https://cdp.cooley.com/digital-ai-omnibus-delays-key-deadlines-introduces-new-rules/ 、IBM — https://www.ibm.com/think/topics/ai-act-timeline-implementation
- MCP の公開と寄贈：Anthropic — https://www.anthropic.com/news/donating%2Dthe%2Dmodel%2Dcontext%2Dprotocol%2Dand%2Destablishing%2Dof%2Dthe%2Dagentic%2Dai%2Dfoundation 、Linux Foundation — https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation 、The New Stack（2025-12-09）— https://thenewstack.io/anthropic-donates-the-mcp-protocol-to-the-agentic-ai-foundation/
- 日本の AI 法：内閣府資料 — https://www8.cao.go.jp/cstp/gaiyo/yusikisha/20251120/siryo1.pdf 、BUSINESS LAWYERS — https://businesslawyers.jp/articles/1475
- 用語の定義と範囲の分け方は本資料の整理
