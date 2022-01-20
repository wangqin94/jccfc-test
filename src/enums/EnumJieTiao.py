# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test
@File    ：EnumFql.py
@Author  ：jccfc
@Date    ：2021/9/9 10:49
"""

# @unique
from enum import Enum


class EnumJieTiaoPath(Enum):
    JieTiaoEncryptPath = "/api/v1/secret/thirdEncryptData/JieTiao"
    JieTiaoDecryptPath = "/api/v1/secret/thirdDecryptData/JieTiao"
