
from setuptools import setup

microlib_name = 'mtools.message_util'
setup(
    name="mtools_message_util",
    version="0.1.0",
    author="yourname",
    author_email="yourname@email.com",
    description="Your microlib descriton",
    namespace_packages=['mtools'],
    packages=[microlib_name],
    install_requires=[
        # PyPi からインストールするパッケージ.
    ],
)
