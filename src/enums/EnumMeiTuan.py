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


# @unique
class ApiStatusCodeEnum(Enum):
    """状态码枚举类"""

    SUCCESS = ('000000', '成功')
    PASS = ("A", "通过")
    TO_DOING = ("U", "处理中")
    FAIL = ("R", "拒绝")
    NOT_EXIST = ("W", "不存在")
    NO_HOURLY = ("999999", "系统异常")

    @property
    def code(self):
        """获取状态码"""
        return self.value[0]

    @property
    def msg(self):
        """获取状态码信息"""
        return self.value[1]