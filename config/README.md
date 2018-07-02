## 概要
- Qiita記事 「PythonパッケージのConfigを簡単に管理・反映する方法」 のサンプルプログラムです.
- 外部設定ファイルを読込み、実行中の Python スクリプトの動的な設定変更を行います.

## 依存ライブラリ
- 設定の取り込みには外部モジュール `Traitlets` を使用しています. (Jupyter Notebook と同じ方式です.)

## 設定ファイル
`config.py` に設定が書かれています.

## 設定の更新
`settings.py` には設定値を保持するクラス `Settings` が定義されています.

このクラスのメソッド `load_config` で設定ファイルを読み込み、設定値の更新を行っています.

## 実行
`settings.py` を実行することにより、設定ファイルの内容を読込みと更新を行います.
下記実行例では2回めのprint の前に config.py を読み込んだため、設定値が更新されています.

```Bash
python settings.py
{'cpu': 'CORE i5', 'memory': 8, 'usb': ['USB 2.0', 'USB 3.0']}
{'cpu': 'CORE i7', 'memory': 16, 'usb': ['USB 3.0', 'USB Type-C']}
```
