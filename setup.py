#!/usr/bin/env python
"""
@author jacobi petrucciani
@desc pip setup file
"""
from setuptools import setup, find_packages


__library__ = "gamble"
__version__ = "VERSION"

with open("README.md") as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name=__library__,
    version=__version__,
    description=("a collection of gambling classes/tools"),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    zip_safe=False,
)
