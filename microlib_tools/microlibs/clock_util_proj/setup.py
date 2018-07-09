
from setuptools import setup

microlib_name = 'mtools.clock_util'
setup(
    name="mtools_clock_util",
    version="0.1.0",
    author="yourname",
    author_email="yourname@email.com",
    description="Your microlib descriton",
    namespace_packages=['mtools'],
    packages=[microlib_name],
    install_requires=[
        # add more packages if needed
    ],
)
