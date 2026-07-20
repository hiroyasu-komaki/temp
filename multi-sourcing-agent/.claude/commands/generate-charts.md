---
description: vmo_impact_model.xlsx から4枚のグラフ(PNG)を再生成する
---

まず、次の2択をそのままユーザーに提示する(他の説明は不要):

1. Excelから最新化してグラフを作成する(input/vmo_impact_model.xlsx → mid/*.json を作り直してからグラフ生成)
2. 今のmid/*.json(手動編集を含む)をそのまま使ってグラフだけ作成する(Excelは読み直さない)

ユーザーが選択した場合のみ、対応するコマンドをBashツールで実行する。

選択肢1の場合:
```bash
cd /Users/hiroyasukomaki/Documents/03_agents/multi-sourcing-agent/src && /Users/hiroyasukomaki/Documents/03_agents/multi-sourcing-agent/.venv/bin/python main.py
```

選択肢2の場合:
```bash
cd /Users/hiroyasukomaki/Documents/03_agents/multi-sourcing-agent/src && /Users/hiroyasukomaki/Documents/03_agents/multi-sourcing-agent/.venv/bin/python main.py --from-mid
```

どちらも拒否した場合は何も実行せず終了する。実行した場合は、生成されたPNGファイル名を簡潔に報告する。
