# -*- coding: utf-8 -*-
"""モジュールをインストールし、コマンドとして使用できるようにする setup.py."""
from setuptools import find_packages, setup

setup(
    name="weather",
    packages=find_packages(),
    test_suite='nose.collector',
    python_requires=">=3.6",
    # インストール時に PyPi から取得される外部パッケージ.
    install_requires=[
        "requests"],
    # ユーザーが指定した場合にインストールされる外部パッケージ.
    extras_require={
        "test": ["nose"],
        "doc": ["sphinx"]},
    # コマンドが実行されたときのエントリーポイント.
    entry_points={
        'console_scripts': ['weather=weather_checker.checker:entry_point']}
)
