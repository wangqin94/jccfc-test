# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：EnumYingJiZF.py
@Author  ：jccfc
@Date    ：2022/1/29 16:17 
"""
# @unique
from enum import Enum


class ApiPaymentResultStatusCodeEnum(Enum):
    """状态码枚举类"""

    SUCCESS = ('2', '还款成功')
    FAIL = ("-9999", "还款失败")
    TO_DOING = ("4", "还款处理中，请稍后")

    @property
    def code(self):
        """获取状态码"""
        return self.value[0]

    @property
    def msg(self):
        """获取状态码信息"""
        return self.value[1]