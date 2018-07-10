# -*- coding: utf-8 -*-
import os
import sys

import pip
from pip.req import parse_requirements
from setuptools import find_packages, setup

# requirements.txt のパッケージを読み込む.

with open('requirements.txt') as f:
    requirements = f.read().strip().split('\n')

# PyPi からインストールできるもの.
requirements_pypi = [x for x in requirements if not "github" in x]

setup(
    name="mapp",
    version="0.1.0",
    author="yourname",
    author_email="yourname@email.com",
    description="Your microlib descriton",
    packages=find_packages(),
    install_requires=requirements_pypi,
)

# # GitHub からインストールするもの.
# requirements_github = [x for x in requirements if "github" in x]
# for x in requirements_github:
#     pip.main(['install', x])
