"""Qiita記事: 「パッケージの Config をミスなく反映させる方法」 のサンプルプログラム."""

from pathlib import Path

from traitlets import Int, List, Unicode
from traitlets.config import Application
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


# 追記分.
class Settings2(Application):
    """設定ファイルを自動生成するためのサンプルクラス.

    Traitlets の Application クラスを継承します.
    自動生成は generate_config_file() を実行してください.
    """
    cpu = Unicode("CORE i3").tag(config=True)
    memory = Int(2).tag(config=True)
    usb_types = List(["USB 1.1", "USB 2.0"]).tag(config=True)


if __name__ == "__main__":
    settings = Settings()
    print(settings.dump())
    settings.load_config()
    print(settings.dump())

    # 設定ファイルの自動生成を行う場合のコードはこちら.
    # s2 = Settings2()
    # ret = s2.generate_config_file()
    # Path("auto_generated_config.py").write_text(ret)
