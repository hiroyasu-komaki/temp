# -*- coding: utf-8 -*-
"""
4枚のPNGをまとめて再生成するスクリプト。

処理は2段階:
    1. xlsxを読み込み、中間ファイル(mid/*.json)を書き出す(build_mid.pyと同じ処理)。
    2. 各グラフ生成スクリプトは、xlsxではなくmid/*.jsonだけを参照してPNGを作る。

こうすることで、xlsxからの転記結果をグラフ化する前にJSONとして検証できる。

使い方:
    python3 generate_all.py
        → vmo_impact_model.xlsx (プロジェクト直下のinputフォルダ) を読み込み、
          midフォルダに中間JSONを書き出したうえで、outputフォルダに4枚のPNGを書き出す。

    python3 generate_all.py --from-mid
        → xlsxは読み直さず、既存のmid/*.json(手動編集した内容を含む)を
          そのまま使ってグラフだけを再生成する。

    python3 generate_all.py /path/to/vmo_impact_model.xlsx /path/to/output_dir /path/to/mid_dir
        → xlsxのパス・出力先フォルダ・中間ファイル出力先を明示的に指定する場合。
          (--from-mid と併用する場合、xlsx_pathは無視される)

xlsxの「前提」シート(青字セル・黄色セル)の数値を変更して保存した後、
このスクリプトを再実行すれば、中間JSON・4枚のPNGすべてが最新の数値で作り直される。
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import common
import chart01_facts_sole_source_contracts as chart01
import chart02_hypothesis_impact as chart02
import chart03_npv_irr_3years as chart03
import chart04_vmo_cost_structure as chart04

CHARTS = [chart01, chart02, chart03, chart04]


def main():
    parser = argparse.ArgumentParser(description="4枚のPNGをまとめて再生成する")
    parser.add_argument("xlsx_path", nargs="?", default=common.DEFAULT_XLSX_PATH)
    parser.add_argument("output_dir", nargs="?", default=common.DEFAULT_OUTPUT_DIR)
    parser.add_argument("mid_dir", nargs="?", default=common.DEFAULT_MID_DIR)
    parser.add_argument(
        "--from-mid",
        action="store_true",
        help="xlsxを読み直さず、既存のmid/*.json(手動編集を含む)からグラフだけを再生成する",
    )
    args = parser.parse_args()

    print(f"mid   : {args.mid_dir}")
    print(f"output: {args.output_dir}")

    if args.from_mid:
        inputs_json = os.path.join(args.mid_dir, common.INPUTS_JSON)
        if not os.path.exists(inputs_json):
            print(f"\nエラー: 中間ファイルが見つかりません: {inputs_json}")
            print("先に build_mid.py (または --from-mid を外した generate_all.py) を実行してください。")
            sys.exit(1)
        print("(--from-mid: xlsxは読み直さず、既存の中間JSONをそのまま使用)\n")
    else:
        if not os.path.exists(args.xlsx_path):
            print(f"\nエラー: xlsxファイルが見つかりません: {args.xlsx_path}")
            sys.exit(1)
        print(f"xlsx  : {args.xlsx_path}\n")
        common.build_mid_files(xlsx_path=args.xlsx_path, mid_dir=args.mid_dir)
        print("  ✓ 中間ファイル(JSON)を作成しました\n")

    for mod in CHARTS:
        t0 = time.time()
        out_path = mod.render(mid_dir=args.mid_dir, output_dir=args.output_dir)
        print(f"  ✓ {os.path.basename(out_path)}  ({time.time() - t0:.1f}s)")

    print("\n完了: 4枚のPNGを再生成しました。")


if __name__ == "__main__":
    main()
