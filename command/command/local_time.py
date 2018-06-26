"""Qiita記事 「pip install で shell で実行可能なコマンドをインストールする」 のサンプルプログラム."""

import argparse

import arrow


class LocalTime():
    """コンソールに各タイムゾーンの現在時刻を表示するクラス."""

    def __init__(self) -> None:
        """クラスの初期化.

        表示するタイムゾーンとフォーマットを設定します.
        """
        self.time_zones = ["Asia/Tokyo", "Europe/London", "America/New_York"]
        self.time_format = "YYYY-MM-DD HH:mm:ss ZZ"
        self.time_format_short = "HH:mm:ss"

    def show(self, full: bool=True) -> None:
        """各タイムゾーンでの現在時刻を表示する.

        :param full: Trueの場合は日付時刻を表示し、Falseの場合は時刻のみ表示します.
        """
        utc = arrow.utcnow()
        for zone in self.time_zones:
            fmt = self.time_format if full else self.time_format_short
            # ローカル時刻に変換する.
            s = utc.to(zone).format(fmt)
            # Asia 等は省いて表示する.
            print(f"{zone.split('/')[1]}\t{s}".expandtabs(16))


def exec() -> None:
    """コマンドのエントリーポイント."""
    parser = argparse.ArgumentParser(
        prog="lt", description="Local times: 各タイムゾーンの現在時刻を表示します.")
    # コマンドラインオプションの設定.
    parser.add_argument("-t", "--time-only",
                        help="時刻のみ表示します.", action="store_true")
    args = vars(parser.parse_args())

    lt = LocalTime()
    is_full = True
    if args["time_only"]:
        is_full = False

    lt.show(is_full)


if __name__ == "__main__":
    exec()
