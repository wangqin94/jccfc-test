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
    JieTiao = 'jietiao'


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
    DEAL_FAILED = '10'  # 处理失败
    REJECT = '07'  # 拒绝


@unique
class EnumChannelRepayStatus(Enum):
    TO_REPAY = '01'  # 处理中
    SUCCESS = '03'  # 成功
    CHECK_FAIL = '02'  # 信贷校验失败
    FAIL = '04'   # 资产校验失败


class EnumLoanInvoiceStatus(Enum):
    NORMAL = '1'  # 正常
    OVERDUE = '2'  # 逾期
    SETTLE = '3'  # 结清


class EnumRepayPlanStatus(Enum):
    UNREPAY = '1'  # 待还款
    PART_REPAY = '2'  # 部分还款
    REPAY = '3'  # 已还款
    OVERDUE = '4'  # 逾期
    OVERDUE_PART_REPAY = '5'  # 逾期部分还款
    OVERDUE_REPAY = '6'  # 逾期已还款
    SETTLE = '7'  # 已结清

if __name__ == "__main__":
    print(ProductEnum.BAIDU.value)
