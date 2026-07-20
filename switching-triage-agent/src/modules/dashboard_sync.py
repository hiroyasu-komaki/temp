"""
dashboard_sync — ブラウザダッシュボード（index.html）用の assets/js/data.js を
Main.py のパイプライン実行と同時に再生成する。

以前は scripts/gen_dashboard_data.py が input/contracts.csv を独自にパースして
いたが、loader.py の検証を経ていない生データを二重にパースする形だった。
ここでは Main.py がすでに loader で読み込み・検証した contracts / scenario を
そのまま受け取って書き出すため、パースロジックの重複や検証漏れが起きない。

Main.py 実行のたびに自動的に呼ばれるので、`assets/js/data.js` を手動で
再生成するコマンドはもう不要（`python src/Main.py` を実行すれば同期される）。
"""
from __future__ import annotations
import json
from pathlib import Path


def _contract_to_js(c: dict) -> dict:
    return {
        "id": c["contract_id"],
        "name": c["contract_name"],
        "type": c["contract_type"],
        "vendor": c["vendor"],
        "expiryM": c["expiry_months"],
        "spend": c["annual_spend_m"],
        "lead": c["switch_lead_months"],
        "cost": c["switch_cost_m"],
        "costSigma": c["switch_cost_sigma"],
        "ret": c["est_return_m"],
        "retSigma": c["return_sigma"],
        "execProbability": c["exec_probability"],
        "contestProb": c.get("contestability_prob"),
        "execProb": c.get("execution_prob"),
        "extCount": int(c.get("extension_count") or 0),
        "active": int(c.get("is_active", 1)),
    }


def sync(contracts_d: list[dict], scenario: dict, root: Path) -> Path:
    """assets/js/data.js を再生成し、書き込んだパスを返す。"""
    out_path = root / "assets" / "js" / "data.js"

    fixed = {
        "lambdaRisk": scenario["lambda_risk"],
        "leadTimeHMonths": scenario["lead_time_h_months"],
    }
    defaults = {
        "budgetM": scenario["budget_m"],
        "safetyMargin": scenario["safety_margin"],
        "useBundle": scenario["use_bundle"],
        "betaBundle": scenario["beta_bundle"],
        "extThreshold": scenario["ext_threshold"],
        "extPenalty": scenario["ext_penalty"],
        "extPenaltyCap": scenario["ext_penalty_cap"],
        "asOfDate": scenario["as_of_date"],
    }
    contracts_js = [_contract_to_js(c) for c in contracts_d]

    lines = [
        "// このファイルは src/modules/dashboard_sync.py が",
        "// `python src/Main.py` の実行時に input/contracts.csv と input/scenario.json",
        "// から自動生成したものです。直接編集しないでください。",
        f"// 生成元シナリオ: {scenario.get('scenario_name', '?')}",
        "",
        f"const BASE_AS_OF = {json.dumps(defaults['asOfDate'])};",
        f"const FIXED_PARAMS = {json.dumps(fixed, ensure_ascii=False, indent=2)};",
        f"const DEFAULT_PARAMS = {json.dumps(defaults, ensure_ascii=False, indent=2)};",
        f"const CONTRACTS = {json.dumps(contracts_js, ensure_ascii=False, indent=2)};",
        "",
    ]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path
