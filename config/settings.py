"""Qiita記事: 「パッケージの Config をミスなく反映させる方法」 のサンプルプログラム."""

from pathlib import Path

import arrow
from traitlets import Int, List, Unicode
from traitlets.config.configurable import Configurable
from traitlets.config.loader import PyFileConfigLoader

# 外部設定ファイル.
CONFIG_FILE = "config.py"


class Settings(Configurable):
    """設定値を保持するクラス."""

    # 保持しているパラメータ.
    # これらのパラメータは外部設定ファイルから更新できる.
    cpu = Unicode("CORE i5").tag(config=True)
    memory = Int(8).tag(config=True)
    usb_types = List(["USB 2.0", "USB 3.0"]).tag(config=True)

    def __init__(self) -> None:
        """クラスの初期化."""
        pass

    def load_config(self) -> None:
        """設定ファイルを読み込みパラメータを更新する."""
        p = Path(CONFIG_FILE)
        if p.exists():
            # 設定ファイルが存在すれば読み込む.
            loader = PyFileConfigLoader(str(p))
            c = loader.load_config()
            # 自身のパラメータを更新する.
            self.update_config(c)

    def dump(self) -> None:
        """パラメータを辞書にして返す."""
        return {"cpu": self.cpu,
                "memory": self.memory,
                "usb": self.usb_types}


if __name__ == "__main__":
    settings = Settings()
    print(settings.dump())
    settings.load_config()
    print(settings.dump())
