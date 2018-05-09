# -*- coding: utf-8 -*-
"""Google Sheet API V4 を用い、スプレッドシートを操作するサンプルです.

認証情報は使用する環境で適切なものに置き換えてください.
"""
import datetime
from typing import Dict, List, Union

import pandas as pd
import requests
from apiclient import discovery
from oauth2client.client import OAuth2Credentials

# 認証情報
CLIENT_ID = "84xxxxxxxxxx.apps.googleusercontent.com"
CLIENT_SECRET = "jpgIxxxxxxxx"
REFRESH_TOKEN = "1/RMxxxxxxxx"


class MySpreadsheet:
    """Google Spreadsheet を操作します."""

    def __init__(self):
        """初期化. OAuth認証もここで行います."""
        refresh_params = {
            "client_id": CLIENT_ID,
            "refresh_token": REFRESH_TOKEN,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token"}

        rs = requests.post('https://accounts.google.com/o/oauth2/token',
                           refresh_params).json()
        expiry = datetime.datetime.now() + datetime.timedelta(seconds=rs['expires_in'])

        cred_params = {
            'access_token': rs['access_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': REFRESH_TOKEN,
            'token_expiry': expiry,
            'token_uri': 'https://accounts.google.com/o/oauth2/token',
            'user_agent': ''}

        self.credentials = OAuth2Credentials(**cred_params)

    def create(self, title: str) -> Dict[str, Union[str, List[str]]]:
        """スプレッドシートを新規作成します.

        :param title: スプレッドシートのタイトル.
        :return: スプレッドシートの属性.
        """
        service = discovery.build('sheets', 'v4', credentials=self.credentials)
        body = {"properties": {"title": title}}
        request = service.spreadsheets().create(body=body)
        response = request.execute()

        return {"id": response["spreadsheetId"],
                "url": response["spreadsheetUrl"],
                "sheets": [x["properties"]["title"] for x in response["sheets"]]}

    def read(self, spreadsheet_id: int, sheet_name: str, sheet_range: str,
             header: bool = True) -> pd.DataFrame:
        """スプレッドシートのテーブルを読込み、pandas DataFrame にして返します.

        :param spreadsheet_id: スプレッドシート ID.
        :param sheet_name: シートの名前.
        :param sheet_range: 読み込む範囲. 例) "A2:C" A2からC行のデータが続くまで.
        :param header: 先頭行は各カラム名ならTrueを指定してください.
        :return: 読み込んだテーブルの情報が入った DataFrame.
        """
        service = discovery.build('sheets', 'v4', credentials=self.credentials)
        _range = f"{sheet_name}!{sheet_range}"
        request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                      range=_range,
                                                      valueRenderOption="UNFORMATTED_VALUE")
        response = request.execute()
        values = response["values"]

        if header:
            columns = values[0]
            values = values[1:]
        else:
            columns = None

        return pd.DataFrame(values, columns=columns)

    def update(self, spreadsheet_id: int, sheet_name: str, sheet_range: str,
               df: pd.DataFrame, header: bool = False) -> None:
        """スプレッドシートのテーブルを更新します.

        :param spreadsheet_id: スプレッドシート ID.
        :param sheet_name: シートの名前.
        :param sheet_range: 読み込む範囲. 例) "A2" 更新する範囲がA2から始まっている.
        :param df: 更新する情報が入っている DataFrame.
        :param header: カラム名を書き込む場合は True を設定してください.
        """
        _range = f"{sheet_name}!{sheet_range}"
        if header:
            dat = [df.columns.tolist()] + df.values.tolist()
        else:
            dat = df.values.tolist()
        body = {"values": dat}

        value_input_option = "USER_ENTERED"
        service = discovery.build('sheets', 'v4', credentials=self.credentials)
        request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id,
                                                         valueInputOption=value_input_option,
                                                         range=_range,
                                                         body=body)
        request.execute()

    def append(self, spreadsheet_id: str, sheet_name: str, sheet_range: str,
               df: pd.DataFrame, header: bool = False) -> None:
        """スプレッドシートのテーブルに情報を加えます.

        :param spreadsheet_id: スプレッドシート ID.
        :param sheet_name: シートの名前.
        :param sheet_range: 読み込む範囲. 例) "A2" 更新するテーブルはA2から始まっている.
        :param df: 更新する情報が入っている DataFrame.
        :param header: カラム名を書き込む場合は True を設定してください.
        """
        _range = f"{sheet_name}!{sheet_range}"
        value_input_option = "USER_ENTERED"
        if header:
            dat = [df.columns.tolist()] + df.values.tolist()
        else:
            dat = df.values.tolist()
        body = {"values": dat}

        service = discovery.build('sheets', 'v4', credentials=self.credentials)
        request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id,
                                                         valueInputOption=value_input_option,
                                                         range=_range,
                                                         body=body)
        request.execute()

    def clear(self, spreadsheet_id: str, sheet_name: str, sheet_range: str) -> None:
        """スプレッドシートのテーブルのうち、指定範囲の情報を削除します.

        :param spreadsheet_id: スプレッドシート ID.
        :param sheet_name: シートの名前.
        :param sheet_range: 読み込む範囲. 例) "A:Z" A列からZ列の全ての情報を削除.
        """
        _range = f"{sheet_name}!{sheet_range}"
        body = {}
        service = discovery.build('sheets', 'v4', credentials=self.credentials)
        request = service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id,
                                                        range=_range,
                                                        body=body)
        request.execute()


if __name__ == "__main__":
    ms = MySpreadsheet()

    # スプレッドシートを新規作成する.
    info = ms.create("Test Spreadsheet")
    s_id = info["id"]
    s_name = info["sheets"][0]

    # clear
    # 全てクリアする.
    ms.clear(s_id, s_name, "A:Z")

    # Append (1)
    # A2以降に新しいテーブルを作る.
    df = pd.DataFrame([[1, 110, 210], [2, 120, 220], [3, 130, 230]],
                      columns=["id", "value1", "value2"])
    ms.append(s_id, s_name, "A2", df, header=True)

    # Append (2)
    # テーブルに情報を追加する.
    df = pd.DataFrame([[4, 140, 240], [5, 150, 250], [6, 150, 250]],
                      columns=["id", "value1", "value2"])
    ms.append(s_id, s_name, "A2", df)

    # update
    # テーブルの一部を更新する.
    df = pd.DataFrame([[7, 170, 270], [8, 180, 280], [9, 190, 290]],
                      columns=["id", "value1", "value2"])
    ms.update(s_id, s_name, "A2", df, header=True)

    # Read
    # テーブルを読み込む.
    df = ms.read(s_id, s_name, "A2:C", header=True)
    print(df)
