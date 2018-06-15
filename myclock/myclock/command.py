# -*- coding: utf-8 -*-
"""このモジュールには次のクラスと関数が入っています.

- MyClock class: 指定したタイムゾーンの日時および指定日のカウントダウンを表示するためのクラス.
- CustomArrow class: カウントダウンの日時を生成するヘルパークラス.
- create_config function: 設定ファイルをホームディレクトリの .myclock 以下に生成する関数.
- command function: MyClock を実行するための関数.

このモジュールは次の外部モジュールを使用しています.

- 外部設定ファイルのよる更新に Traitlets を使用しています.
- タイムゾーンの変換に Arrow を使用しています.
"""
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
# 設定ファイルに書き込む内容
CONFIG_CONTENT = """
# Myclock configuration.
# 表示する各タイムゾーン.
c.MyClock.time_zones = [ "Asia/Tokyo", "Europe/London", "America/New_York"]
# 日時のフォーマット.
c.MyClock.time_format = "HH:mm:ss"
# カウントダウンを行う日時.
c.MyClock.the_day_datetime = "2020-07-24 20:00:00+09:00"
# カウントダウンの日時の名称.
c.MyClock.the_day_title = "Tokyo Olympic"
"""


class MyClock(Configurable):
    """コンソールに各タイムゾーンの時刻と指定日へのカウントダウンを表示するクラス.

    各タイムゾーンとカウントダウン用の指定日は外部ファイルから設定することができます.
    外部設定ファイルはモジュールのインストール時にホームディレクトリの .myclock ディレクトリ以下に生成されます.
    外部設定ファイルがない場合は内部のデフォルト値が使用されます.
    モジュールをアンインストールしても設定ファイルは残ります.
    """

    # 初期値
    time_zones = List(["Asia/Tokyo"]).tag(config=True)
    time_format = Unicode("YYYY-MM-DD HH:mm:ss ZZ").tag(config=True)
    the_day_datetime = Unicode("2020-07-24 20:00:00+09:00").tag(config=True)
    the_day_title = Unicode("Tokyo Olympic").tag(config=True)

    def __init__(self) -> None:
        """コンストラクタ.

        - 外部設定ファイルが存在する場合は読込み、このクラスのプロパティを更新します.
        """
        p = Path.home() / ".myclock" / "config.py"
        if p.exists():
            # 設定ファイルが存在すれば読み込む.
            loader = PyFileConfigLoader(str(p))
            c = loader.load_config()
            # 自身のパラメータを更新する.
            self.update_config(c)

    def show(self) -> None:
        """ローカル時刻とカウントダウンを表示します."""
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
        """指定日と現在日時との timedelta を返す.

        :params dt: カウントダウンの対象となる指定日.
        """
        return dt - self


def create_config() -> None:
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


def command() -> None:
    """MyClockによる時刻を表示する.

    - ターミナルから実行される myclock コマンドのエントリーポイント.

    :Example:

        >>> myclock
        Tokyo           16:14:17
        London          08:14:17
        New_York        03:14:17
        Tokyo Olympic	770 days, 3:45:42

    """
    mc = MyClock()
    mc.show()


if __name__ == "__main__":
    create_config()
    command()
