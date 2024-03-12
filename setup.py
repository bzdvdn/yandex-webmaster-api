from io import open
from setuptools import setup, find_packages

from yandex_webmaster import __version__


def read(f):
    return open(f, "r", encoding="utf-8").read()


setup(
    name="yandex-webmaster-api",
    version=__version__,
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        "requests",
    ],
    description="wrapper for yandex webmaster api",
    author="bzdvdn",
    author_email="bzdv.dn@gmail.com",
    url="https://github.com/bzdvdn/yandex-webmaster-api",
    license="MIT",
    python_requires=">=3.8",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
)
