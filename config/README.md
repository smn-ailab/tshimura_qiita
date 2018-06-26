## 概要
- Qiita記事 「設定ファイルを使用した Python スクリプトの初期化」 のサンプルプログラムです.
- 外部設定ファイルを読込み、実行中の Python スクリプトの動的な設定変更を行います.

## 依存ライブラリ
- 設定の取り込みには外部モジュール `Traitlets` を使用しています. (Jupyter Notebook と同じ方式です.)

## 設定ファイル
`config.py` に設定が書かれています.

## 実行
`command.py` を実行することにより、設定ファイルの内容を読込み、実行します.

```Bash
$ python command.py
Tokyo           15:19:18
London          07:19:18
New_York        02:19:18
```
