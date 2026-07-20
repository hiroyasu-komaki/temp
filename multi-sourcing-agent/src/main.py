# -*- coding: utf-8 -*-
"""
エントリポイント。Skill(`.claude/commands/generate-charts.md`)はこのファイルを呼び出す。

実際の処理は src/modules/generate_all.py に委譲する。
使い方は generate_all.py と同じ:

    python3 main.py                # xlsxから最新化して4枚のPNGを再生成
    python3 main.py --from-mid     # xlsxは読み直さず、mid/*.json からPNGだけ再生成
"""
import os
import sys

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SRC_DIR, "modules"))

import generate_all

if __name__ == "__main__":
    generate_all.main()
