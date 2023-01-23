#!/usr/bin/env python
"""
@author jacobi petrucciani
@desc pip setup file
"""
from setuptools import setup, find_packages


__library__ = "gamble"
__version__ = "VERSION"
__user__ = "https://github.com/jpetrucciani"


with open("README.md", encoding="UTF-8") as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name=__library__,
    version=__version__,
    description=("a collection of gambling classes/tools"),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Jacobi Petrucciani",
    author_email="j@cobi.dev",
    url=f"{__user__}/{__library__}.git",
    download_url=f"{__user__}/{__library__}.git",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    zip_safe=False,
)
