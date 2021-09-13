# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：EnumWld.py
@Author  ：jccfc
@Date    ：2021/9/9 10:51 
"""

# @unique
from enum import Enum


class WldPathEnum(Enum):
    wldEncryptPath = "/api/v1/secret/thirdEncryptData/WLD"
    wldDecryptPath = "/api/v1/secret/thirdDecryptData/WLD"
