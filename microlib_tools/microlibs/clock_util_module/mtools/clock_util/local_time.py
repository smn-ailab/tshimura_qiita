"""時刻とタイムゾーンに関する関数が入っているスクリプト."""
import argparse
import sys
from datetime import datetime
from pathlib import Path

import arrow


def get_local_time(timezone: str) -> datetime:
    """指定したタイムゾーンにおける現在時刻を返します.

    :timezone: タイムゾーン. 例) Asia/Tokyo
    :return: 指定したタイムゾーンでの現地時刻.

    :Example:

        >>> from mtools.clock_util.local_time import get_local_time
        >>> get_local_time('Asia/Tokyo')
        datetime.datetime(2018, 7, 9, 15, 50, 30, 831248, tzinfo=tzfile('/usr/share/zoneinfo/Asia/Tokyo'))
    """
    utc = arrow.utcnow()
    return utc.to(timezone).datetime


if __name__ == "__main__":
    # 動作確認用.
    print(get_local_time("Asia/Tokyo"))
