import sys
from datetime import datetime, timedelta
from pathlib import Path

import arrow
from traitlets import Int, List, Unicode
from traitlets.config.configurable import Configurable
from traitlets.config.loader import PyFileConfigLoader

# 設定ファイルを保存するディレクトリ
CONFIG_DIR = ".myclock"
# 設定ファイル名
CONFIG_FILE = "config.py"
# 設定内容
CONFIG_CONTENT = """
# Myclock configuration.
c.MyClock.time_zones = [ "Asia/Tokyo", "Europe/London", "America/New_York"]
c.MyClock.time_format = "HH:mm:ss"
c.MyClock.the_day_datetime = "2020-07-24 20:00:00+09:00"
c.MyClock.the_day_title = "Tokyo Olympic"
"""


class MyClock(Configurable):

    # 初期値
    time_zones = List(["Asia/Tokyo"]).tag(config=True)
    time_format = Unicode("YYYY-MM-DD HH:mm:ss ZZ").tag(config=True)
    the_day_datetime = Unicode("2020-07-24 20:00:00+09:00").tag(config=True)
    the_day_title = Unicode("Tokyo Olympic").tag(config=True)

    def __init__(self):
        p = Path.home() / ".myclock" / "config.py"
        if p.exists():
            # 設定ファイルが存在すれば読み込む.
            loader = PyFileConfigLoader(str(p))
            c = loader.load_config()
            # 自身のパラメータを更新する.
            self.update_config(c)

    def show(self):
        # 各ローカル時刻を表示
        utc = arrow.utcnow()
        for zone in self.time_zones:
            s = utc.to(zone).format(self.time_format)
            print(f"{zone.split('/')[1]}\t{s}".expandtabs(16))

        # カウントダウンを表示
        factory = arrow.ArrowFactory(CustomArrow)
        custom = factory.utcnow()
        delta = custom.till_the_day(arrow.get(self.the_day_datetime))
        print(f"{self.the_day_title}\t{str(delta).split('.')[0]}")


class CustomArrow(arrow.Arrow):
    """カウントダウンのためのカスタム Arrow クラス."""

    def till_the_day(self, dt: arrow) -> timedelta:
        """指定日と現在日時との timedelta を返す."""
        return dt - self


def create_config():
    """ホームディレクトリに .myclock/config.py を生成する."""
    d = Path.home() / ".myclock"
    p = Path.home() / ".myclock" / "config.py"
    try:
        d.mkdir()
    except FileExistsError:
        pass
    if not p.exists():
        try:
            with open(p, "w") as f:
                f.write(CONFIG_CONTENT)
        except OSError:
            print("cannot write config file.")


def command():
    """MyClockによる時刻を表示する."""
    mc = MyClock()
    mc.show()


if __name__ == "__main__":
    create_config()
    command()
