# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：Identity.py
@Author  ：jccfc
@Date    ：2022/4/8 9:43 
"""
import random
import re
# 导入某个模块的部分类或方法
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# 导入常量并重命名
from config.IdConstant import *


class IdNumber(str):

    def __init__(self, id_number):
        super(IdNumber, self).__init__()
        self.id = id_number
        self.area_id = int(self.id[0:6])
        self.birth_year = int(self.id[6:10])
        self.birth_month = int(self.id[10:12])
        self.birth_day = int(self.id[12:14])

    def get_area_name(self):
        """根据区域编号取出区域名称"""
        return AREA_INFO[self.area_id]

    def get_birthday(self):
        """通过身份证号获取出生日期"""
        return "{0}-{1}-{2}".format(self.birth_year, self.birth_month, self.birth_day)

    def get_age(self):
        """通过身份证号获取年龄"""
        now = (datetime.now() + timedelta(days=1))
        year, month, day = now.year, now.month, now.day

        if year == self.birth_year:
            return 0
        else:
            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):
                return year - self.birth_year - 1
            else:
                return year - self.birth_year

    def get_sex(self):
        """通过身份证号获取性别， 女生：0，男生：1"""
        return int(self.id[16:17]) % 2

    def get_check_digit(self):
        """通过身份证号获取校验码"""
        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * int(self.id[i])
        check_digit = (12 - (check_sum % 11)) % 11
        return check_digit if check_digit < 10 else 'X'

    @classmethod
    def verify_id(cls, id_number):
        """校验身份证是否正确"""
        if re.match(ID_NUMBER_18_REGEX, id_number):
            check_digit = cls(id_number).get_check_digit()
            return str(check_digit) == id_number[-1]
        else:
            return bool(re.match(ID_NUMBER_15_REGEX, id_number))

    @classmethod
    def generate_id(cls, sex=None, age=None):
        """
        随机生成身份证号
        @param sex:  sex = 0表示女性，sex = 1表示男性
        @param age:  eg: age='2020-01-01'； age=None 随机生成大于16岁生日
        @return:
        """
        # 随机生成一个区域码(6位数)
        id_number = str(random.choice(list(AREA_INFO.keys())))
        # 限定出生日期范围(8位数)
        now_date = datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
        if age:
            age = datetime.strptime(age, "%Y-%m-%d")
            assert now_date > age + relativedelta(years=int(17)), '支付要求用户最小年龄不能小于16岁'
            birth_days = datetime.strftime(age, "%Y%m%d")
        else:
            min_age = datetime.strftime(now_date - relativedelta(years=int(16)), "%Y-%m-%d")
            start, end = datetime.strptime("1975-01-01", "%Y-%m-%d"), datetime.strptime(min_age, "%Y-%m-%d")
            birth_days = datetime.strftime(start + timedelta(random.randint(0, (end - start).days + 1)), "%Y%m%d")
        id_number += str(birth_days)
        # 顺序码(2位数)
        id_number += str(random.randint(10, 99))
        # 性别码(1位数)
        sex = sex if sex else random.randint(0, 1)  # 随机生成男(1)或女(0)
        id_number += str(random.randrange(sex, 10, step=2))
        # 校验码(1位数)
        return id_number + str(cls(id_number).get_check_digit())


if __name__ == '__main__':
    # random_sex = random.randint(0, 1)  # 随机生成男(1)或女(0)
    id1 = IdNumber.generate_id(age=None)
    print(id1)  # 随机生成身份证号
    # print(IdNumber('410326199507103197').area_id)  # 地址编码:410326
    # print(IdNumber('410326199507103197').get_area_name())  # 地址:河南省洛阳市汝阳县
    # print(IdNumber('410326199507103197').get_birthday())  # 生日:1995-7-10
    # print(IdNumber('410326199507103197').get_age())  # 年龄:23(岁)
    # print(IdNumber('410326199507103197').get_sex())  # 性别:1(男)
    # print(IdNumber('410326199507103197').get_check_digit())  # 校验码:7
    print(IdNumber.verify_id(id1))  # 检验身份证是否正确:False
