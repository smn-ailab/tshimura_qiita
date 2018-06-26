"""Qiita記事: 「設定ファイルを使用した Python スクリプトの初期化」 のサンプルプログラム."""

from pathlib import Path

import arrow
from traitlets import Int, List, Unicode
from traitlets.config.configurable import Configurable
from traitlets.config.loader import PyFileConfigLoader


class LocalTime(Configurable):
    """コンソールに各タイムゾーンの現在時刻を表示するクラス."""

    # 外部設定ファイル `config.py` から更新できるパラメータ.
    time_zones = List(["Asia/Tokyo"]).tag(config=True)
    time_format = Unicode("YYYY-MM-DD HH:mm:ss ZZ").tag(config=True)

    def __init__(self) -> None:
        """クラスの初期化."""
        p = Path("config.py")
        if p.exists():
            # 設定ファイルが存在すれば読み込む.
            loader = PyFileConfigLoader(str(p))
            c = loader.load_config()
            # 自身のパラメータを更新する.
            self.update_config(c)

    def show(self) -> None:
        """各タイムゾーンの現在時刻を表示する."""
        utc = arrow.utcnow()
        for zone in self.time_zones:
            s = utc.to(zone).format(self.time_format)
            print(f"{zone.split('/')[1]}\t{s}".expandtabs(16))


def exec() -> None:
    """日付時刻を表示する."""
    lt = LocalTime()
    lt.show()


if __name__ == "__main__":
    exec()
