# 付録A　セゾンテクノロジーの連携製品

> **参照元**：03_landscape.md

セゾンテクノロジー（旧 セゾン情報システムズ）は、ファイル転送とデータ連携の国産製品を持つ。製品名が似ているため、違いを整理する。

| 製品 | 種類 | 提供形態 | 中身 |
|---|---|---|---|
| HULFT | ファイル転送 | 自社管理（ソフトウェア） | 30年以上使われてきたファイル連携ツール |
| DataSpider Servista | データ連携 | 自社管理（ソフトウェア） | ノーコードでデータの抽出・変換・連携を設計するミドルウェア。自社のサーバやクラウド上に導入する |
| DataSpider Cloud | データ連携 | クラウド | DataSpider Servista の SaaS 版。AWS 上で提供され、2017年に 1.1、2019年に 1.3 が出ている。2021年にアシストも販売を始めた。2026年時点の位置づけ（後継製品やサポート期限）は、今回の確認では公式情報を見つけられなかった |
| HULFT Square | iPaaS | フルマネージド | HULFT と DataSpider Servista に、環境設定・ユーザー管理・ジョブ設定・サポート・監視などの運用管理機能を加えたクラウド型の連携基盤。2023年2月リリース。Basic・Standard・Enterprise の3プラン |

- 同社が現在 iPaaS として前面に出しているのは HULFT Square である。DataSpider Cloud を選ぶ場合は、製品のロードマップを確認する必要がある。
- HULFT Square には、運用監視を代行するサービス（2024年1月）、SFTPサービスやトリガー機能（2024年6月）、JP1 のジョブ管理との連携（2026年3月）などが追加されている。

---

**出典**（確認日：2026-11-14）

- IT Leaders, アシストが販売開始した「HULFT Square」 — https://it.impress.co.jp/articles/-/25812
- クラウド Watch, アシスト、セゾン情報システムのiPaaS「HULFT Square」を提供（2024-01-10） — https://cloud.watch.impress.co.jp/docs/news/1559757.html
- クラウド Watch, HULFT Square 関連記事一覧 — https://cloud.watch.impress.co.jp/img/clw/docs/1564/529/html/07_o.jpg.html
- セブン銀行の導入事例（HULFT・DataSpider の技術を搭載） — https://www.hulft.com/download_file/23000
- DataSpider Cloud：IT Leaders（2017-11）— https://it.impress.co.jp/articles/-/15358 、日本経済新聞（2019-04、1.3 の提供開始）— https://www.nikkei.com/article/DGXLRSP507638_V10C19A4000000/ 、クラウド Watch（2021-02、アシストの販売開始）— https://cloud.watch.impress.co.jp/docs/news/1305141.html
