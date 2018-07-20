"""挨拶に関する関数が入っているスクリプト."""
from datetime import datetime

from mtools.clock_util.local_time import get_local_time

TIMEZONE_JP = "Asia/Tokyo"
TIMEZONE_NY = "America/New_York"


def get_greeting_message(timezone: str) -> str:
    """指定したタイムゾーンにおける挨拶を返します.

    :timezone: タイムゾーン.
    :return: 指定したタイムゾーンでの現地時刻での挨拶.

    .. Note::

        * 設定できるタイムゾーンは次のタイムゾーンになります.

            * "Asia/Tokyo"
            * "America/New_York"

        * このサンプルでは例外に関しての考慮はしていません.

    :Example:

        >>> from mtools.message_util.greeting import get_greeting_message
        >>> get_greeting_message("Asia/Tokyo")
        'こんにちは。'
    """
    # 各言語でのメッセージ.
    messages = {"jp": {"morning": "おはよう。", "daytime": "こんにちは。", "night": "こんばんは。"},
                "en": {"morning": "Good morning.", "daytime": "Hello.", "night": "Good evening."}}

    # 指定タイムゾーンにおける現在時刻を得る.
    dt = get_local_time(timezone)

    # 言語を設定する.
    if timezone == TIMEZONE_JP:
        lang = "jp"
    elif timezone == TIMEZONE_NY:
        lang = "en"
    else:
        lang = "jp"

    # 時間帯を設定する.
    if 5 <= dt.hour and dt.hour <= 9:
        t = "morning"
    elif (18 <= dt.hour) or (0 <= dt.hour and dt.hour <= 5):
        t = "night"
    else:
        t = "daytime"

    return messages[lang][t]


if __name__ == "__main__":
    # 動作確認用.
    print(get_greeting_message("Asia/Tokyo"))
