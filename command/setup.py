# -*- coding: utf-8 -*-
"""モジュールをインストールし、コマンドとして使用できるようにする setup.py."""
from setuptools import find_packages, setup

setup(
    name="lt",
    packages=find_packages(),
    install_requires=[
        "arrow"],
    # lt コマンドはここで設定.
    entry_points={
        'console_scripts': ['lt=command.local_time:exec']})
