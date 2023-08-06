# !/usr/bin/env python 
# -*- coding: utf-8 -*-
# file_name: setup.py.py
# author: ScCcWe
# time: 2022/3/6 11:34 下午
import setuptools

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymysql_dao",
    version="0.0.1",
    author="ScCcWe",
    author_email="scccwe@163.com",
    description="A functional enhancement package that focus on crud based PyMySQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ScCcWe/PyMySQLDao",
    project_urls={
        "Bug Tracker": "https://github.com/ScCcWe/PyMySQLDao/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src", exclude=["tests*", "examples*"]),
    python_requires=">=3.7",
)
