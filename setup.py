#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "click>=7.0.0",
    "fsspec>=0.7.0",
    "gcsfs>=0.7.0",
    "xarray>=0.15.0",
    "zarr>=2.3.0",
]

test_requirements = ["pytest"]

setup(
    author="Oliver Watt-Meyer",
    author_email="oliverwatt@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Describe zarr stores from the command line.",
    long_description="Describe zarr stores from the command line.",
    entry_points={
        "console_scripts": [
            "zarrdump=zarrdump.core:dump",
        ]
    },
    install_requires=requirements,
    license="BSD 3-Clause license",
    include_package_data=True,
    keywords="zarr",
    name="zarrdump",
    packages=find_packages(),
    test_suite="tests",
    tests_require=test_requirements,
    version="0.2.0",
)