# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：EnumZhiXin.py
@Author  ：jccfc
@Date    ：2021/10/21
"""

# @unique
from enum import Enum


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

