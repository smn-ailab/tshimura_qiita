
from setuptools import find_packages, setup

setup(
    name="my_command",
    packages=find_packages(),
    entry_points={
        'console_scripts': ['my_command=my_command.command_line:main']}
)
