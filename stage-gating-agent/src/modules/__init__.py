"""
modules パッケージ — main.py のパイプラインを構成する処理単位。

    adapter        input/ の生CSV（可変スキーマ）→ 正規形CSV へ変換（mid/）
    loader         正規形CSV（mid/）の読み込み・種別判別・検証
    processor      正規化・審査・集計（結果は output/*.json にも保存）
    dashboard_sync ブラウザ用 assets/js/data.js の同期

各モジュールは単機能に保ち、main.py が input → mid → output → assets/js/data.js の
順に呼び出す。
"""
from . import adapter, loader, processor, dashboard_sync

__all__ = ["adapter", "loader", "processor", "dashboard_sync"]
