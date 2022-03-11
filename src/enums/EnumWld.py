# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：EnumWld.py
@Author  ：jccfc
@Date    ：2021/9/9 10:51 
"""


from enum import Enum, unique


@unique
class WldPathEnum(Enum):
    wldEncryptPath = "/api/v1/secret/thirdEncryptData/WLD"
    wldDecryptPath = "/api/v1/secret/thirdDecryptData/WLD"

class WldApiStatusEnum(Enum):
    SUCCESS = 'S'  # 成功
    TO_DOING = 'P'  # 处理中
    FAIL = 'F'
    QUERY_CREDIT_RESULT_S = '00'  # 授信成功
    QUERY_CREDIT_RESULT_F = '01'  # 授信失败
    QUERY_CREDIT_RESULT_D = '02'  # 授信中
    QUERY_CREDIT_RESULT_N = '03'  # 查无此单

    QUERY_LOAN_RESULT_S = '0'  # 放款成功
    QUERY_LOAN_RESULT_F = '1'  # 放款失败
    QUERY_LOAN_RESULT_N = '2'  # 查无此单
    QUERY_LOAN_RESULT_D = '99'  # 处理中

    QUERY_REPAY_RESULT_S = '1'  # 还款成功
    QUERY_REPAY_RESULT_D = '2'  # 还款中
    QUERY_REPAY_RESULT_F = '3'  # 还款失败




class StatusCodeEnum(Enum):
    """状态码枚举类"""

    SUCCESS = ('000000', '成功')

    # QUERY_CREDIT_RESULT_3 = ("ICE3297", "资料不完善"),
    # QUERY_CREDIT_RESULT_4 = ("ICE3296", "系统异常"),
    # APPLY_CERTIFICATION_1 = ("ICE3719", "系统异常"),
    # APPLY_CERTIFICATION_2 = ("ICE3718", "已鉴权"),
    # APPLY_CERTIFICATION_3 = ("ICE3717", "其他失败"),
    # VERIFY_CODE_1 = ("ICE3729", "系统异常"),
    # VERIFY_CODE_2 = ("ICE3728", "验证码不正确"),
    # VERIFY_CODE_3 = ("ICE3727", "验证码过期"),
    # VERIFY_CODE_4 = ("ICE3726", "其他失败"),
    # CHECK_USER_ACCEPT_1 = ("ICE3101", "非存量用户"),
    # CHECK_USER_ACCEPT_2 = ("ICE3102", "存量用户有余额"),
    # CHECK_USER_ACCEPT_3 = ("ICE3103", "存量用户无余额"),
    # CHECK_USER_REJECT_1 = ("ICE3199", "黑名单"),
    # CHECK_USER_REJECT_2 = ("ICE3198", "内部审批不通过"),
    # CHECK_USER_REJECT_3 = ("ICE3197", "存量用户有余额"),
    # CHECK_USER_REJECT_4 = ("ICE3196", "存量用户无余额"),
    # NOT_PASS = ("ICE3699", "审核不通过"),
    # PASS_WAY_FAIL = ("ICE3698", "通道失败"),
    # NO_HOURLY = ("100003", "请勿频繁请求")

    @property
    def code(self):
        """获取状态码"""
        return self.value[0]

    @property
    def msg(self):
        """获取状态码信息"""
        return self.value[1]
