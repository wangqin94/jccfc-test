# -*- coding: utf-8 -*-
# # -----------------------------------------
# # - Common enum 枚举值管理
# # -----------------------------------------

from enum import Enum, unique


@unique
class ProductEnum(Enum):
    BAIDU = 'BaiDu'
    MEITUAN = 'MeiTuan'
    ctrip = 'ctrip'
    FQL = 'fql'
    YINGJF = 'YingJiZF'
    WLD = 'wld'
    ZHIXIN = 'zhixin'


@unique
class EnumCreditStatus(Enum):
    SUCCESS = '03'  # 成功
    TO_CREDIT = '02'
    FAIL = '04'


@unique
class EnumLoanStatus(Enum):
    TO_LOAN = '15'  # 待放款
    ON_USE = '17'  # 使用中
    LOAN_PAY_FAILED = '21'  # 放款失败


@unique
class EnumChannelRepayStatus(Enum):
    TO_REPAY = '01'  # 处理中
    SUCCESS = '03'  # 成功
    CHECK_FAIL = '02'  # 信贷校验失败
    FAIL = '04'   # 资产校验失败


if __name__ == "__main__":
    print(ProductEnum.BAIDU.value)
