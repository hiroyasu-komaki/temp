"""
config パッケージ — Python 側の設定を一元管理する。

- settings.py: パス定数・既定パラメータなど、コード全体で参照する設定。
- ここに JSON / YAML などの設定ファイルを置き、settings.py から読み込んでもよい。

使い方:
    from config import settings
    print(settings.INPUT_DIR)
"""
from . import settings

__all__ = ["settings"]
