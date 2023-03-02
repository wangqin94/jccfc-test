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
    JIKE = 'jike'
    JIEBEI = 'jiebei'
    XIAOX = 'xiaoxiang'
    YINLIU = 'yinliu'


@unique
class ProductIdEnum(Enum):
    BAIDU = 'F21C021'
    MEITUAN = 'F21C011'
    ctrip = 'F20B021'
    FQL = 'F021108'
    WLD = 'F21E031'
    ZHIXIN = 'F21E041'
    JieTiao = 'F22E011'
    JieBei = 'F22C021'


@unique
class EnumMerchantId(Enum):
    BAIDU = 'F21C02BAID'
    MEITUAN = 'F21C01MEIT'
    FQL = '000UC010000006268'
    WLD = 'F21E03WOLD'


@unique
class EnumCreditStatus(Enum):
    SUCCESS = '03'  # 成功
    TO_CREDIT = '02'  # 审批中
    FAIL = '04'       # 失败
    AUDITING = '00'    # 待审核


@unique
class EnumLoanStatus(Enum):
    TO_LOAN = '15'  # 待放款
    ON_USE = '17'  # 使用中
    LOAN_PAY_FAILED = '21'  # 放款失败
    DEAL_FAILED = '10'  # 处理失败
    REJECT = '07'  # 拒绝
    OVERDUE = '30'  # 逾期
    AUDITING = '06'  # 审核中
    LOANING = '16'  # 放款中
    LOAN_AUDITING = '23'  # 放款审核中
    INITIALIZATION = '01'  # 初始化


@unique
class EnumChannelRepayStatus(Enum):
    TO_REPAY = '01'  # 处理中
    SUCCESS = '03'  # 成功
    CHECK_FAIL = '02'  # 信贷校验失败
    FAIL = '04'   # 资产校验失败


@unique
class EnumCustomPaymentStatus(Enum):
    TO_REPAY = '01'  # 处理中
    SUCCESS = '03'  # 成功
    FAIL = '02'  # 信贷校验失败
    TO_DO = '00'   # 待处理


@unique
class EnumHjLoanDealStatus(Enum):
    INIT = '00'  # 待处理
    PROCESS = '01'  # 处理中
    VALIDATE_FAIL = '02'  # 校验失败
    LOAN_SUCCESS = '03'   # 放款成功
    LOAN_FAIL = '04'   # 放款失败


@unique
class EnumHjRepayNoticeStatus(Enum):
    INIT = '00'  # 待处理
    PROCESS = '01'  # 处理中
    VALIDATE_FAIL = '02'  # 校验失败
    REPAY_SUCCESS = '03'   # 放款成功
    REPAY_FAIL = '04'   # 放款失败


# @unique
class EnumH5PaymentStatus(Enum):
    SUCCESS = "000000"  # 成功
    TO_DOING = 'P'  # 处理中
    FAIL = "999999"


@unique
class EnumLoanInvoiceStatus(Enum):
    NORMAL = '1'  # 正常
    OVERDUE = '2'  # 逾期
    SETTLE = '3'  # 结清


@unique
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
