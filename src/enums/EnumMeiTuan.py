# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test
@File    ：EnumFql.py
@Author  ：jccfc
@Date    ：2021/9/9 10:49
"""

# @unique
from enum import Enum


class EnumMeiTuanPath(Enum):
    MeiTuanEncryptPath = "/api/v1/secret/thirdEncryptData/MEIT"
    MeiTuanDecryptPath = "/api/v1/secret/thirdDecryptData/MEIT"
