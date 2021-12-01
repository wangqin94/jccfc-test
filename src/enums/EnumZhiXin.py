# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：EnumZhiXin.py
@Author  ：jccfc
@Date    ：2021/10/21
"""

# @unique
from enum import Enum


class StatusCodeEnum(Enum):
    """状态码枚举类"""

    SUCCESS = ('200', 'success')
    QUERY_CREDIT_RESULT_1 = ("ICE3299", "黑名单"),
    QUERY_CREDIT_RESULT_2 = ("ICE3298", "审核不通过"),
    QUERY_CREDIT_RESULT_3 = ("ICE3297", "资料不完善"),
    QUERY_CREDIT_RESULT_4 = ("ICE3296", "系统异常"),
    APPLY_CERTIFICATION_1 = ("ICE3719", "系统异常"),
    APPLY_CERTIFICATION_2 = ("ICE3718", "已鉴权"),
    APPLY_CERTIFICATION_3 = ("ICE3717", "其他失败"),
    VERIFY_CODE_1 = ("ICE3729", "系统异常"),
    VERIFY_CODE_2 = ("ICE3728", "验证码不正确"),
    VERIFY_CODE_3 = ("ICE3727", "验证码过期"),
    VERIFY_CODE_4 = ("ICE3726", "其他失败"),
    CHECK_USER_ACCEPT_1 = ("ICE3101", "非存量用户"),
    CHECK_USER_ACCEPT_2 = ("ICE3102", "存量用户有余额"),
    CHECK_USER_ACCEPT_3 = ("ICE3103", "存量用户无余额"),
    CHECK_USER_REJECT_1 = ("ICE3199", "黑名单"),
    CHECK_USER_REJECT_2 = ("ICE3198", "内部审批不通过"),
    CHECK_USER_REJECT_3 = ("ICE3197", "存量用户有余额"),
    CHECK_USER_REJECT_4 = ("ICE3196", "存量用户无余额"),
    NOT_PASS = ("ICE3699", "审核不通过"),
    PASS_WAY_FAIL = ("ICE3698", "通道失败"),
    NO_HOURLY = ("100003", "请勿频繁请求")

    @property
    def code(self):
        """获取状态码"""
        return self.value[0]

    @property
    def msg(self):
        """获取状态码信息"""
        return self.value[1]


# @unique
class ZhiXinApiStatusEnum(Enum):
    SUCCESS = 'S'  # 成功
    TO_DOING = 'P'  # 处理中
    FAIL = 'F'


# @unique
class JopEnum(Enum):
    JOP0 = "0"  # 国家机关、党群组织、企业、事业单位负责人
    JOP1 = "1"  # 专业技术人员
    JOP3 = "3"  # 办事人员和有关人员
    JOP4 = "4"  # 商业、服务业人员
    JOP5 = "5"  # 农、林、牧、渔、水利业生产人员
    JOP6 = "6"  # 生产、运输设备操作人员及有关人员
    JOPX = "X"  # 军人
    JOPY = "Y"  # 不便分类的其他从业人员
    JOPZ = "Z"  # 未知


# @unique
class EducationEnum(Enum):
    GRADUATE = "10"  # 研究生
    BACHELOR = "20"  # 大学本科（简称“大学”）
    COLLEGE = "30"  # 大学专科和专科学校（简称“大 专”）
    HIGH = "60"  # 高中
    JUNIOR = "70"  # 初中
    PRIMARY = "80"  # 小学
    ILLITERACY = "90"  # 文盲或半文盲
    OTHER = "99"  # 未知


# @unique
class MonthlyIncomeEnum(Enum):
    MONTHLYINCOME01 = "1"  # 5000 以下
    MONTHLYINCOME02 = "2"  # 5001-10000
    MONTHLYINCOME03 = "3"  # 10001-20000
    MONTHLYINCOME04 = "4"  # 20001 以上


# @unique
class MarriageEnum(Enum):
    UNMARRIED = "10"  # 未婚
    MARRIED = "20"  # 已婚
    DEATH_OF_SPOUSE = "30"  # 丧偶
    DIVORCE = "40"  # 离婚
    OTHER = "90"  # 未知


# @unique
class SexEnum(Enum):
    MAN = "M"  # 男人
    WOMAN = "F"  # 女人


# @unique
class RelationshipEnum(Enum):
    PARENTS = "10"  # 父母
    SPOUSE = "20"  # 配偶
    CHILDREN = "30"  # 子女
    RELATIVES = "40"  # 亲戚
    CLASSMATE = "50"  # 同学
    COLLEAGUES = "60"  # 同事
    FRIEND = "70"  # 朋友


# @unique
class BankCodeEnum(Enum):
    CODE_0001 = "0001"  # 中国银行
    CODE_0002 = "0002"  # 农业银行
    CODE_0003 = "0003"  # 工商银行
    CODE_0004 = "0004"  # 建设银行
    CODE_0005 = "0005"  # 交通银行
    CODE_0006 = "0006"  # 光大银行
    CODE_0007 = "0007"  # 民生银行
    CODE_0008 = "0008"  # 平安银行
    CODE_0009 = "0009"  # 邮储银行
    CODE_0010 = "0010"  # 广发银行
    CODE_0011 = "0011"  # 中信银行
    CODE_0012 = "0012"  # 华夏银行
    CODE_0013 = "0013"  # 浦发银行
    CODE_0014 = "0014"  # 兴业银行
    CODE_0015 = "0015"  # 招商银行
    CODE_0017 = "0017"  # 杭州银行
    CODE_0018 = "0018"  # 上海银行
    CODE_0019 = "0019"  # 北京银行


# @unique
class StatusEnum(Enum):
    SUCCESS = "S"  # 授信成功
    FAIL = "F"  # 申请失败
    REJECT = "R"  # 授信拒绝
    DOING = "P"  # 处理中
    CANCEL = "C"  # 取消


# @unique
class ResultCodeEnum(Enum):
    BLACK_LIST = "ICE3299"  # 黑名单
    AUDIT_FAILED = "ICE3298"  # 审核不通过
    IMPERFECT_DATA = "ICE3297"  # 资料不完善（具体）
    EXCEPTION_SYSTEM = "ICE3296"  # 系统异常

