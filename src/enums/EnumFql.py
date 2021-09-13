# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test
@File    ：EnumFql.py
@Author  ：jccfc
@Date    ：2021/9/9 10:49
"""

# @unique
from enum import Enum


class FqlPathEnum(Enum):
    fqlEncryptPath = "/api/fql/v1/encrypt/encryptData"
    fqlDecryptPath = "/api/fql/v1/encrypt/decryptData"
