# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：Enums.py
@Author  ：jccfc
@Date    ：2022/1/7 15:11 
"""

from enum import Enum


# @unique
class EnumStatusCode(Enum):
    SUCCESS = 200
    SYS_ERROR = 500
    FAILED = 400
