# -*- coding: utf-8 -*-
"""天気予報と天気概況を取得します.

天気の情報の取得には以下の Web API を使用しています.
- お天気Webサービス（Livedoor Weather Web Service / LWWS）
http://weather.livedoor.com/weather_hacks/webservice
"""

import argparse
from typing import Dict, Sequence, Union

import requests

URL_BASE = "http://weather.livedoor.com/forecast/webservice/json/v1"
PLACESS = {
    "Hokkaido": "016010",
    "Aomori": "020010",
    "Miyagi": "040010",
    "Akita": "050010",
    "Yamagata": "060010",
    "Fukushima": "070010",
    "Ibaraki": "080010",
    "Tochigi": "090010",
    "Gunma": "100010",
    "Saitama": "110010",
    "Chiba": "120010",
    "Tokyo": "130010",
    "Kanagawa": "140010",
    "Niigata": "150010",
    "Toyama": "160010",
    "Ishikawa": "170010",
    "Fukui": "180010",
    "Yamanashi": "190010",
    "Nagano": "200010",
    "Gifu": "210010",
    "Shizuoka": "220010",
    "Aichi": "230010",
    "Mie": "240010",
    "Shiga": "250010",
    "Kyoto": "260010",
    "Osaka": "270000",
    "Hyogo": "280010",
    "Nara": "290010",
    "Wakayama": "300010",
    "Tottori": "310010",
    "Shimane": "320010",
    "Okayama": "330010",
    "Hiroshima": "340010",
    "Yamaguchi": "350010",
    "Tokushima": "360010",
    "Kagawa": "370000",
    "Ehime": "380010",
    "Kochi": "390010",
    "Fukuoka": "400010",
    "Saga": "410010",
    "Nagasaki": "420010",
    "Kumamoto": "430010",
    "Oita": "440010",
    "Miyazaki": "450010",
    "Kagoshima": "460010",
    "Okinawa": "471010"}


def get_information(place: str) -> Dict[str, Union[str, Sequence[Dict[str, str]]]]:
    """Web API から天気と天気概況を取得します.

    :params place: 都道府県名(ローマ字)
    :return: 天気予報と天気概況の文字列が入った辞書.
    """
    if place not in PLACESS.keys():
        raise ValueError(f"Unknown place: {place}")

    # Web サービスから情報を取得する.
    args = f"?city={PLACESS[place]}"
    url = URL_BASE + args
    ret = requests.get(url)
    dat = ret.json()

    # 必要な情報を辞書にして返す.
    return {
        # 地名
        "place": dat["title"].split(" ")[0],
        # 天気概況
        "description": dat["description"]["text"],
        # 予報
        "forecasts": [
            # 今日
            {"weather": dat["forecasts"][0]["telop"],
             "temp_min": dat["forecasts"][0]["temperature"]["min"],
             "temp_max": dat["forecasts"][0]["temperature"]["max"]},
            # 明日
            {"weather": dat["forecasts"][1]["telop"],
             "temp_min": dat["forecasts"][1]["temperature"]["min"],
             "temp_max": dat["forecasts"][1]["temperature"]["max"]},
            # 明後日
            {"weather": dat["forecasts"][2]["telop"],
             "temp_min": dat["forecasts"][2]["temperature"]["min"],
             "temp_max": dat["forecasts"][2]["temperature"]["max"]}]}


def create_message(weather_info: Dict[str, Union[str, Sequence[Dict[str, str]]]]) -> str:
    """表示するためのメッセージを作る.

    :param weather_info: 天気の情報が入った辞書.
    :return: 表示要文字列.
    """
    dat = weather_info
    d1_w = dat["forecasts"][0]["weather"]
    d2_w = dat["forecasts"][1]["weather"]
    d3_w = dat["forecasts"][2]["weather"]
    # None の場合は -- にしておく.
    d1_min = dat["forecasts"][0]["temp_min"]["celsius"] if dat["forecasts"][0]["temp_min"] else "--"
    d1_max = dat["forecasts"][0]["temp_max"]["celsius"] if dat["forecasts"][0]["temp_max"] else "--"
    d2_min = dat["forecasts"][1]["temp_min"]["celsius"] if dat["forecasts"][1]["temp_min"] else "--"
    d2_max = dat["forecasts"][1]["temp_max"]["celsius"] if dat["forecasts"][1]["temp_max"] else "--"
    d3_min = dat["forecasts"][2]["temp_min"]["celsius"] if dat["forecasts"][2]["temp_min"] else "--"
    d3_max = dat["forecasts"][2]["temp_max"]["celsius"] if dat["forecasts"][2]["temp_max"] else "--"
    desc = dat["description"]

    # 書式を整えた文字列を返す.
    return f"""{dat["place"]} の天気
-------------------------------------------------------------------
今日　: {d1_w}{" "*(8-len(d1_w*2))}    最低気温:{d1_min:>3}℃    最高気温:{d1_max:>3}℃
明日　: {d2_w}{" "*(8-len(d2_w*2))}    最低気温:{d2_min:>3}℃    最高気温:{d2_max:>3}℃
明後日: {d3_w}{" "*(8-len(d3_w*2))}    最低気温:{d3_min:>3}℃    最高気温:{d3_max:>3}℃
-------------------------------------------------------------------
{desc}"""


def entry_point() -> int:
    """コマンドラインからのエントリーポイント."""
    parser = argparse.ArgumentParser(
        prog="weather", description="指定地域の天気と天気概況を表示します.")
    # コマンドラインオプションの設定.
    parser.add_argument("-p", "--place", help="都道府県名を指定します.")
    args = vars(parser.parse_args())
    # 指定がない場合は Tokyo をデフォルトとしておく.
    place = args["place"] if args["place"] else "Tokyo"
    try:
        info = get_information(place)
        mes = create_message(info)
        #  結果を表示.
        print(mes)

        return 0
    except ValueError:
        print(f"地名エラー: {place}")
        return -1


if __name__ == "__main__":
    # 動作確認
    entry_point()
