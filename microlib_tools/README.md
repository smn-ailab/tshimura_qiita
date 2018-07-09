# mtools

```Python
>>> from mtools.clock_util.local_time import get_local_time
>>> dt = get_local_time("Asia/Tokyo")
>>> dt.strftime('%Y/%m/%d %H:%M:%S')
'2018/07/09 17:09:51'

>>> from mtools.message_util.greeting import get_greeting_message
>>> get_greeting_message("Asia/Tokyo")
'こんにちは。'
```

## 概要
- このプロジェクトは次のブログ記事
[Python microlibs](https://blog.shazam.com/python-microlibs-5be9461ad979) の内容を基に、 `microlib` を用いたプロジェクト構成を紹介する Qiita 用サンプルプロジェクトです.
- 単一リポジトリ内に複数のマイクロライブラリを保持しています.
- 上記記事中の `macrolib` はここでは説明のため `mtools` に置き換えています.
- 各マイクロライブラリはそれぞれ独立した存在です.
- 各マイクロライブラリは Python 名前空間の仕組みにより `mtools` にまとめられています.
- 依存関係を持たせた構成も可能です. 例) マイクロライブラリA は　マイクロライブラリB の関数を使用する.


## インストール
- このディレクトリで `pip install .` を実行してください。


## 実行できるモジュール
- 次のモジュールと関数が使用できるようになります。
  - clock_util モジュール
    - get_local_time
      - 各タイムゾーンでの現地時刻を返します.

  - message_util モジュール
    - get_greeting_message
      - 各タイムゾーンでの挨拶を返します.
      - 内部で clock_util モジュールの get_local_time を使用しています.

## アンインストール
- `pip uninstall mtools` を実行することによりアンインストールできます.

## 参考
- [Python microlibs](https://blog.shazam.com/python-microlibs-5be9461ad979)
