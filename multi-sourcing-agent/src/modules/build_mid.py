# -*- coding: utf-8 -*-
"""
vmo_impact_model.xlsx を読み込み、中間ファイル(mid/*.json)を書き出すスクリプト。

グラフ生成(generate_all.py / chart0X.py)はxlsxを直接読まず、ここで作成した
mid/inputs.json, mid/calc.json, mid/investment_eval.json だけを参照する。
xlsxからの転記結果を、グラフを作る前にJSONとして目視・diffで検証できるようにするため。

使い方:
    python3 build_mid.py
        → vmo_impact_model.xlsx (プロジェクト直下のinputフォルダ) を読み込み、
          midフォルダ(プロジェクト直下)に中間JSONを書き出す。

    python3 build_mid.py /path/to/vmo_impact_model.xlsx /path/to/mid_dir
        → xlsxのパスと中間ファイル出力先を明示的に指定する場合。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import common


def main():
    xlsx_path = sys.argv[1] if len(sys.argv) > 1 else common.DEFAULT_XLSX_PATH
    mid_dir = sys.argv[2] if len(sys.argv) > 2 else common.DEFAULT_MID_DIR

    if not os.path.exists(xlsx_path):
        print(f"エラー: xlsxファイルが見つかりません: {xlsx_path}")
        sys.exit(1)

    print(f"xlsx: {xlsx_path}")
    print(f"mid : {mid_dir}\n")

    paths = common.build_mid_files(xlsx_path=xlsx_path, mid_dir=mid_dir)
    for name, path in paths.items():
        print(f"  ✓ {name}: {path}")

    print("\n完了: 中間ファイル(JSON)を作成しました。")


if __name__ == "__main__":
    main()
