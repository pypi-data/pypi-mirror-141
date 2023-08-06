#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: lidongdong
# Mail: 927052521@qq.com
# Created Time: 2021.10.19  19.50
############################################


from setuptools import setup, find_packages

setup(
    name = "lddya",
    version = "1.2.9",
    keywords = ("pip", "license","licensetool", "tool", "gm"),
    description = "修复了栅格图类无法直接获取地图数据(之前必须读取文件得到数据)的bug。",
    long_description = "具体功能，请自行挖掘。",
    license = "MIT Licence",

    url = "https://github.com/not_define/please_wait",
    author = "lidongdong",
    author_email = "927052521@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['chardet']
)
