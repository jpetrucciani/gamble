#!/usr/bin/env python
"""
pip setup file
"""
from setuptools import setup, find_packages
from gamble.globals import __library__, __version__


with open("README.rst") as readme:
    LONG_DESCRIPTION = readme.read()


setup(
    name=__library__,
    version=__version__,
    description=(""),
    long_description=LONG_DESCRIPTION,
    author="Jacobi Petrucciani",
    author_email="jacobi@mimirhq.com",
    url="https://github.com/jpetrucciani/{}.git".format(__library__),
    download_url="https://github.com/jpetrucciani/{}.git".format(__library__),
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    zip_safe=False,
)
