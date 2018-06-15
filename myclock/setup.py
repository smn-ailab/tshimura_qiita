
from setuptools import find_packages, setup

from myclock.command import create_config

setup(
    name="myclock",
    packages=find_packages(),
    install_requires=[
        "arrow"],
    # myclock コマンドはここで設定.
    entry_points={
        'console_scripts': ['myclock=myclock.command:command']}
)

# 設定ファイルをホームディレクトリに生成する.
create_config()
