"""
main.py — stage-gating-agent の Python エントリポイント。

パイプライン:
  input/ の生CSV（スキーマは可変）
    -> [adapter]        列マッピングで正規スキーマへ変換     -> mid/canonical_*.csv
    -> [loader]         正規形CSVを読み込み・種別判別・検証
    -> [processor]      正規化 → 審査フラグ → 集計          -> output/normalized.json, output/summary.json
    -> [dashboard_sync] index.html 用データ同期            -> assets/js/data.js

Skills（.claude/commands/）から呼び出される処理の実体。Claude が判断・解釈を行い、
Python はファイル処理・データ変換・集計など決定的な処理を担当する。

使い方:
    .venv/bin/python src/main.py run                     # input/ 配下の CSV を全て処理
    .venv/bin/python src/main.py run --input input/foo.csv
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

# src/ を import パスへ追加し、config / modules をパッケージとして解決する。
SRC_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC_DIR))

from config import settings                                     # noqa: E402
from modules import adapter, loader, processor, dashboard_sync   # noqa: E402


def cmd_run(args: argparse.Namespace) -> int:
    settings.MID_DIR.mkdir(exist_ok=True)
    settings.OUTPUT_DIR.mkdir(exist_ok=True)

    # 1) 生CSV（スキーマ可変）→ 正規形CSV へ変換 -> mid/
    try:
        conv = adapter.convert(Path(args.input))
    except adapter.AdapterError as e:
        print(f"[変換エラー] {e}", file=sys.stderr)
        return 1

    # 2) 正規形CSV（mid/）を読み込み・検証
    try:
        data = loader.load(settings.MID_DIR)
    except loader.InputError as e:
        print(f"[入力エラー] {e}", file=sys.stderr)
        return 1
    data["sources"] = conv["sources"]   # 表示には元の入力ファイル名を使う

    # 3) 正規化・審査・集計 -> output/（集計結果JSON）
    result = processor.process(data)
    settings.NORMALIZED_JSON.write_text(
        json.dumps(result["records"], ensure_ascii=False, indent=2), encoding="utf-8")
    settings.SUMMARY_JSON.write_text(
        json.dumps(result["summary"], ensure_ascii=False, indent=2), encoding="utf-8")

    # 4) ダッシュボード用データを同期 -> assets/js/data.js（HTMLが参照する集計済みJSON）
    data_js_path = dashboard_sync.sync(result)

    # サマリー標準出力
    a = result["summary"]["audit"]
    m = result["summary"]["meta"]
    print(f"完了。投資 {m['investCount']}件・BAU {m['bauCount']}件を処理。"
          f"差し戻し候補 {a['errors']}件・要確認 {a['warnings']}件。")
    mid_files = [p for p in (conv["invest"], conv["bau"]) if p]
    print(f"  mid    -> " + ", ".join(str(p.relative_to(settings.ROOT)) for p in mid_files)
          + "（正規形CSV）")
    print(f"  output -> {settings.NORMALIZED_JSON.relative_to(settings.ROOT)}, "
          f"{settings.SUMMARY_JSON.relative_to(settings.ROOT)}")
    print(f"  dash   -> {data_js_path.relative_to(settings.ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="stage-gating-agent")
    sub = parser.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="パイプラインを実行する")
    p_run.add_argument("--input", default=str(settings.INPUT_DIR),
                       help="処理対象の入力パス（既定: input/ ディレクトリ全体）")
    p_run.set_defaults(func=cmd_run)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
