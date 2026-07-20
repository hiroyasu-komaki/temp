"""
Main.py — VMO ベンダー切替投資エージェントのエントリポイント。

パイプライン:
  input/contracts.csv + input/scenario.json
    -> [loader]     読み込み・検証
    -> [scoring]    V×U×R と束ね評価 -> mid/scored.json
    -> [allocation] 予算配分         -> output/allocation.json
    -> [reporter]   説明レポート     -> output/report.md
    -> [dashboard_sync] index.html用データ同期 -> assets/js/data.js

使い方:
  python src/Main.py
  python src/Main.py --scenario input/scenario_conservative.json
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

# src/modules をパッケージとして解決するため src/ を import パスへ
SRC_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC_DIR))

from modules import loader, scoring, allocation, reporter, dashboard_sync  # noqa: E402

ROOT = SRC_DIR.parent
INPUT_DIR = ROOT / "input"
MID_DIR = ROOT / "mid"
OUTPUT_DIR = ROOT / "output"


def main() -> int:
    ap = argparse.ArgumentParser(description="VMO ベンダー切替投資エージェント")
    ap.add_argument("--contracts", default=str(INPUT_DIR / "contracts.csv"),
                    help="契約CSVのパス")
    ap.add_argument("--scenario", default=str(INPUT_DIR / "scenario.json"),
                    help="シナリオJSONのパス")
    args = ap.parse_args()

    MID_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 1) 読み込み・検証
    try:
        scenario = loader.load_scenario(Path(args.scenario))
        contracts = loader.load_contracts(Path(args.contracts))
    except loader.InputError as e:
        print(f"[入力エラー] {e}", file=sys.stderr)
        return 1

    print(f"読み込み: 契約 {len(contracts)} 件 / シナリオ '{scenario.get('scenario_name','?')}'")

    contracts_d = loader.contracts_to_dicts(contracts)

    # 2) スコアリング -> mid/scored.json
    scored = scoring.score_all(contracts_d, scenario)
    (MID_DIR / "scored.json").write_text(
        json.dumps(scored, ensure_ascii=False, indent=2), encoding="utf-8")
    n_act = sum(1 for c in scored["candidates"] if c["verdict"] == "即着手")
    print(f"スコアリング完了: 候補 {len(scored['candidates'])} 件（即着手 {n_act} 件）"
          f" -> mid/scored.json")

    # 3) 予算配分 -> output/allocation.json
    alloc = allocation.allocate(scored)
    (OUTPUT_DIR / "allocation.json").write_text(
        json.dumps(alloc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"予算配分完了: 本コミット {alloc['committed_m']}M / "
          f"予算不足 {alloc['blocked_m']}M -> output/allocation.json")

    # 4) レポート -> output/report.md
    report = reporter.build_report(scored, alloc)
    (OUTPUT_DIR / "report.md").write_text(report, encoding="utf-8")
    print("レポート生成完了 -> output/report.md")

    # 5) ダッシュボード用データを同期 -> assets/js/data.js
    data_js_path = dashboard_sync.sync(contracts_d, scenario, ROOT)
    print(f"ダッシュボードデータ同期完了 -> {data_js_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
