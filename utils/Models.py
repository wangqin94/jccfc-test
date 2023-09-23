# -*- coding: utf-8 -*-

# # -----------------------------------------------------------
# # - 公共模块函数变量
# # -----------------------------------------------------------
import base64
import datetime as datetimes
import hashlib
import json
import os
import random
import string
import time
from datetime import datetime
from functools import wraps
from inspect import getcallargs

import demjson as demjson
import requests
from dateutil.relativedelta import relativedelta

from config.TestEnvInfo import TEST_ENV_INFO
from utils.BankNo import BankNo
from utils.GenName import get_name
from utils.Identity import IdNumber
from utils.Logger import MyLog

_log = MyLog.get_log()


# __all__ = ['output_format', 'wait_time', 'get_day', 'get_base_data',
#            'loan_and_period_date_parser', 'ciphertext',
#            'encrypt', 'decrypt', 'DataUpdate', 'loanByAvgAmt', 'get_telephone', 'project_dir', 'get_read_json',
#            'get_next_month_today', 'get_before_month_today']


# # -----------------------------------------------------------
# # - 结果展示装饰器, 不写入日志文件
# # -----------------------------------------------------------
def output_format(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("# --------------------- Divide Line --------------------------- #")
        func(*args, **kwargs)
        print("# --------------------- Divide Line --------------------------- #")

    return wrapper


# # -----------------------------------------------------------
# # - 等待时间
# # -----------------------------------------------------------
def wait_time(sec):
    _log.info('sleep %s seconds...', sec)
    time.sleep(int(sec))


# # -----------------------------------------------------------
# # - 用户四要素生成
# # -----------------------------------------------------------
def get_base_data(env, *project, back=20, age=None, bankName=None, **kwargs):
    """
    用户基础信息生成
    @param bankName: 银行名称 eg:bankName='中国银行'; None:随机银行
    @param env: 环境变量
    @param project: 添加随机数
    @param back: person文件存放数据最大条数 默认20
    @param age: eg: age='2020-01-01'； age=None 随机生成大于18岁生日
    @param kwargs: data字典中添加指定key-value值
    @return:
    """
    data = {}
    strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
    # res = requests.get('http://10.10.100.153:8081/getTestData')
    # bank = BankNo()
    data['name'] = get_name()
    data['cer_no'] = IdNumber.generate_id(age=age)
    # 获取随机生成的手机号
    data['telephone'] = get_telephone()
    bankName = bankName if bankName else '中国银行'
    data['bankid'] = BankNo().get_bank_card(bankName=bankName)[0]
    data['bankcode'] = BankNo().get_bank_card(bankName=bankName)[1]

    if os.path.exists("person.py"):
        pass
    else:
        file = open("person.py", "w")
        file.close()
    # 读取文件行数，超过20行删除历史数据
    with open('person.py', "r", encoding='utf-8') as f:  # 打开文件
        back_data = f.readlines()  # 读取文件
        count = len(back_data)  # 获取txt文件的行数
        if count > back:
            start = count - back
            back_data = back_data[start:count]  # 只读取最后20行的内容
            f = open('person.py', "w", encoding='utf-8')  # 以写入的形式打开txt文件
            f.writelines(back_data)  # 将修改后的文本内容写入
            f.close()  # 关闭文件

    # project赋值后天从到data中
    if project:
        for item in project:
            data[item] = str(item) + strings

    if kwargs:
        for key, value in kwargs.items():
            data[key] = str(value)

    with open('person.py', 'a', encoding='utf-8') as f:
        f.write('\n')
        f.write('data = {}  # {}'.format(str(data), env))
    _log.demsg('当前测试环境: {}'.format(TEST_ENV_INFO))
    _log.info('用户四要素信息: {}'.format(data))
    return data


# # -----------------------------------------------------------
# # - 用户四要素生成（临时数据，不保存到文件）
# # -----------------------------------------------------------
def get_base_data_temp(*project, age=None, bankName=None, **kwargs):
    """
    用户基础信息生成
    @param bankName: 银行名称 eg:bankName='中国银行'; None:随机银行
    @param project: 添加随机数
    @param age: eg: age='2020-01-01'； age=None 随机生成大于16岁生日
    @param kwargs: data字典中添加指定key-value值
    @return:
    """
    data = {}
    strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
    # res = requests.get('http://10.10.100.153:8081/getTestData')
    data['name'] = get_name()
    data['cer_no'] = IdNumber.generate_id(age=age)
    # 获取随机生成的手机号
    data['telephone'] = get_telephone()
    bank = BankNo()
    bankName = bankName if bankName else '工商银行'
    data['bankid'] = bank.get_bank_card(bankName=bankName)[0]
    data['bankcode'] = bank.get_bank_card(bankName=bankName)[1]

    # project赋值后天从到data中
    if project:
        for item in project:
            data[item] = str(item) + strings

    if kwargs:
        for key, value in kwargs.items():
            data[key] = str(value)
    _log.demsg('当前测试环境: {}'.format(TEST_ENV_INFO))
    _log.info('用户四要素信息: {}'.format(data))
    return data


# 更新person文件指定行数数据
def update_user_info(newData, item=-1, model="a"):
    """
    @param newData: 待更新用户数据
    @param item: 待更新第N行数据，默认最后一行
    @param model: model="a" 追加一条新数据， model="w"更新数据
    @return:
    """
    # 读取文件第item行数进行数据更新
    with open('person.py', "r", encoding='utf-8') as f:  # 打开文件
        back_data = f.readlines()  # 读取文件
        if model == "a":
            f = open('person.py', model, encoding='utf-8')  # 以写入的形式打开txt文件
            f.write('\n')
            f.write('data = {}'.format(newData))  # 将修改后的文本内容写入
        elif model == "w":
            back_data[item] = 'data = {}'.format(newData)  # 只更新第item行
            f = open('person.py', model, encoding='utf-8')  # 以写入的形式打开txt文件
            f.writelines(back_data)  # 将修改后的文本内容写入
        f.close()  # 关闭文件


# 计算还款时间和放款时间差，天为单位
def get_day(time1, time2):
    """
    @param time1: 时间1
    @param time2: 时间2
    :return: 差异天数time2-time1
    """
    try:
        day1 = time.strptime(str(time1), '%Y-%m-%d')
        day2 = time.strptime(str(time2), '%Y-%m-%d')
        day_num = (int(time.mktime(day2)) - int(time.mktime(day1))) / (24 * 60 * 60)
        # 2022-03-03修改： 去掉绝对值
        return int(day_num)
    except Exception as e:
        _log.error("系统错误: {}".format(e))


# # -----------------------------------------------------------
# # - 数据库查询语句组装
# # -----------------------------------------------------------
def get_sql_qurey_str(table, *args, db=None, **kwargs):
    """ # 数据库查询sql
    @param table:       表名
    @param db:          数据库名
    @param args:        查询表子项 tuple
    @param kwargs:      where 筛选条件
    :return:            sql语句
    """
    table = table if not db else '%s.%s' % (db, table)
    attr = '*' if not args else ', '.join(args)
    sql_str = ["select", attr, "from", table]
    if kwargs:
        filters = 'where ' + ' and '.join(["%s='%s'" % (k, v) for k, v in kwargs.items()]) + ';'
        sql_str.append(filters)
    return ' '.join(sql_str)


# # -----------------------------------------------------------
# # - 数据库更新语句组装
# # -----------------------------------------------------------
def update_sql_qurey_str(table, db=None, attr=None, **kwargs):
    """ # 数据库更新sql
    @param attr:        where 条件
    @param table:       表名
    @param db:          数据库名
    @param kwargs:      更新字段
    :return:            sql语句
    """
    table = table if not db else '%s.%s' % (db, table)
    sql_str = ["UPDATE", table, "SET"]
    if kwargs:
        filters = ','.join(["%s='%s'" % (k, v) for k, v in kwargs.items()])
        sql_str.append(filters)
    attr = 'where ' + attr + ';'
    sql_str.append(attr)
    return ' '.join(sql_str)


# # -----------------------------------------------------------
# # - 数据库插入语句组装
# # -----------------------------------------------------------
def insert_sql_qurey_str(table, db=None):
    """ # 数据库更新sql
    @param table:       表名
    @param db:          数据库名
    :return:            表名
    """
    table = table if not db else '%s.%s' % (db, table)
    return table


# # -----------------------------------------------------------
# # - 数据库删除语句组装
# # -----------------------------------------------------------
def delete_sql_qurey_str(table, db=None, **kwargs):
    """ # 数据库更新sql
    @param table:       表名
    @param db:          数据库名
    @param kwargs:      更新字段
    :return:            sql语句
    """
    table = table if not db else '%s.%s' % (db, table)
    sql_str = ["DELETE", "FROM", table]
    if kwargs:
        filters = 'where ' + ' and '.join(["%s='%s'" % (k, v) for k, v in kwargs.items()]) + ';'
        sql_str.append(filters)
    return ' '.join(sql_str)


# # -----------------------------------------------------------
# # - 等额本息计算
# # -----------------------------------------------------------
def loanByAvgAmt(loanamt, term, year_rate):
    repayment_plan = []
    # 月利率
    month_rate = year_rate / 1200
    # 每月还款总额
    amtpermonth = loanamt * month_rate * pow((1 + month_rate), term) / (pow((1 + month_rate), term) - 1)
    for i in range(1, term + 1):
        if i == 1:
            # 第一个月还款利息
            month_interest = loanamt * month_rate
        else:
            # 第2-n个月还款利息
            month_interest = (loanamt * month_rate - amtpermonth) * pow((1 + month_rate), (i - 1)) + amtpermonth
        # 应还本金
        month_principal = amtpermonth - month_interest
        month_principal = round(month_principal, 2)
        month_interest = round(month_interest, 2)
        repayment_plan.append((int(month_principal * 100), int(month_interest * 100)))
    return repayment_plan


# # -----------------------------------------------------------
# # - 还款日/账单日计算
# # -----------------------------------------------------------
def loan_and_period_date_parser(*, date_str, period=1, flag=False, max_bill=25):
    """ # tips: 入参时须带关键字
    @param date_str:    (str)借款日期  eg: '2020-01-09'
    @param period:      (int)分期数  eg: 3， 默认为 1
    @param flag:        返回首期还款日、账单日
    @param max_bill:    (int) 最大账单日, 默认25号
    :return:
    """
    date_list = date_str.split('-')
    bill_year = int(date_list[0])
    bill_month = int(date_list[1])
    bill_day = int(date_list[-1])
    period_date_list = []
    if bill_day > max_bill:
        bill_day -= max_bill
        bill_month += 1
    for _ in range(int(period)):
        bill_month += 1
        if bill_month > 12:
            bill_year += 1
            bill_month -= 12
        period_date_list.append("%d-%02d-%02d" % (bill_year, bill_month, bill_day))
    if flag:
        return period_date_list[0], "%02d" % bill_day

    return period_date_list, "%02d" % bill_day


# # -----------------------------------------------------------
# # - 接口数据加密
# # -----------------------------------------------------------
def encrypt(encrypt_url, headers, encrypt_payload):
    """ # 接口数据payload加密
    @param encrypt_url:     加密请求地址
    @param headers:         加密请求报文头部
    @param encrypt_payload: 待加密数据
    :return: 加密后的payload
    """
    _log.info("开始请求加密接口对报文进行加密操作...")
    response = requests.post(url=encrypt_url, headers=headers, json=encrypt_payload)
    _log.info("报文加密操作结束！status code: %s", response.status_code)
    res = demjson.encode(response.json())  # 将 Python 对象编码成 JSON 字符串
    # res = str(res).replace("'", '''"''').replace(" ", "")
    _log.info(f"加密后的报文：{res}")
    return json.loads(res)


# # -----------------------------------------------------------
# # - 接口数据解密
# # -----------------------------------------------------------
def decrypt(decrypt_url, headers, decrypt_payload):
    """ # 接口数据payload解密
    @param decrypt_url:     解密请求地址
    @param headers:         解密请求报文头部
    @param decrypt_payload: 待解密数据
    :return:                解密后的报文
    """
    _log.info("开始请求解密接口对报文进行解密操作...")
    # decrypt_payload = json.dumps(decrypt_payload)
    response = requests.post(url=decrypt_url, headers=headers, json=decrypt_payload)
    _log.info("报文解密操作结束！status code: %s", response.status_code)
    res = response.json()
    res1 = str(res).replace("'", '''"''').replace(" ", "")
    _log.info(f"解密后的报文：{res1}")
    return res


# # -----------------------------------------------------------
# # - 接口数据加解密装饰器
# # -----------------------------------------------------------
def ciphertext(func):
    @wraps(func)
    def inner(*args, **kwargs):
        paramater = getcallargs(func, *args, **kwargs)
        self = paramater['self']
        print('in en:', self.active_payload)
        if paramater['encrypt']:
            _log.info("开始请求加密接口对报文进行加密操作...")
            response = requests.post(url=self.encrypt_url, headers=self.headers, json=self.active_payload)
            _log.info("报文加密操作结束！status code: %s", response.status_code)
            res = str(response.json()).replace("'", '''"''').replace(" ", "")
            _log.info(f"加密后的报文：\n{res}")
            self.active_payload = json.loads(res)
            print('加加密', self.active_payload)

        func(*args, **kwargs)

        if paramater['encrypt']:
            _log.info("开始请求解密接口对报文进行解密操作...")
            # self.active_payload = json.dumps(self.active_payload)
            print('加加密1', self.active_payload)
            response = requests.post(url=self.decrypt_url, headers=self.headers, data=json.dumps(self.active_payload))
            _log.info("报文解密操作结束！status code: %s", response.status_code)
            res = str(response.json()).replace("'", '''"''').replace(" ", "")
            _log.info(f"解密后的报文：\n{res}")

    return inner


# # -----------------------------------------------------------
# # - 接口字段参数更新类
# # -----------------------------------------------------------
class DataUpdate(object):
    def __init__(self, data, unique=True, **kwargs):
        self.data = data
        self.unique = unique
        self.dict_update = kwargs

    @property
    def parser(self):
        for key, value in self.dict_update.items():
            self.data = self._update_data(self.data, key, value)
        return self.data

    def _update_data(self, data, key, value):
        """ # 遍历嵌套字典或list并替换字典的key """
        if isinstance(data, dict):  # 使用isinstance检测数据类型，如果是字典
            if key in data.keys():  # 替换字典中所有key与传参一致的key
                if isinstance(value, dict):
                    for itemKey in value.keys():
                        data[key] = self._update_data(data[key], itemKey, value[itemKey])
                else:
                    data[key] = value
                if self.unique:
                    return data
            # # TODO:
            # # 遍历字典的所有子层级，将子层级赋值为变量chdict，
            # # 分别替换子层级第一层中所有key对应的value，
            # # 最后在把替换后的子层级赋值给当前处理的key
            for child_key in data.keys():
                child_dict = data[child_key]
                self._update_data(child_dict, key, value)
                data[child_key] = child_dict
        elif isinstance(data, list):  # list
            for element in data:  # 遍历list元素，以下重复上面的操作
                if isinstance(element, dict):
                    if key in element.keys():
                        element[key] = value
                        if self.unique:
                            return data
                    for child_key in element.keys():
                        child_dict = element[child_key]
                        self._update_data(child_dict, key, value)
                        element[child_key] = child_dict
        return data


# # -----------------------------------------------------------
# # - 生成随机手机号
# # -----------------------------------------------------------

# 运营商的号码前缀
prefix = [
    '130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
    '145', '147', '149', '150', '151', '152', '153', '155', '156', '157',
    '158', '159', '165', '171', '172', '173', '174', '175', '176', '177',
    '178', '180', '181', '182', '183', '184', '185', '186', '187', '188',
    '189', '191'
]


def get_telephone():
    # 随机取一个手机号前缀
    pos = random.randint(0, len(prefix) - 1)
    # 随机生成后8位数字，string.digits是数字0到9，可以参考源码
    suffix = ''.join(random.sample(string.digits, 8))
    # 拼接返回11位手机号
    return prefix[pos] + suffix


# # -----------------------------------------------------------
# # - 获取项目根路径
# # -----------------------------------------------------------
def project_dir():
    """
    get project dir
    :return:
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# # -----------------------------------------------------------
# # - 解析json文件
# # -----------------------------------------------------------
def get_read_json(json_file_name):
    """
    @param json_file_name: json文件名
    :return: 返回json文件的内容
    """
    with open(os.path.join(project_dir(), "XXX", json_file_name),
              encoding='utf-8') as f:
        return json.load(f)


# # -----------------------------------------------------------
# # - 获取当前时间的后N月
# # -----------------------------------------------------------
def get_next_month_today(n):
    today = datetimes.date.today()
    next_month_today = today - relativedelta(months=-int(n))
    return next_month_today


# # -----------------------------------------------------------
# # - 获取当前时间的前N月
# # -----------------------------------------------------------
def get_before_month_today(n):
    today = datetimes.date.today()
    before_month_today = today - relativedelta(months=+int(n))
    return before_month_today


# # -----------------------------------------------------------
# # - 获取指定日期的前N月
# # -----------------------------------------------------------
def get_custom_month(month=3, date='2021-11-13'):
    """
    @param month: 跳转月份数
    @param date: 指定时间
    @return:
    """
    date = datetime.strptime(date, '%Y-%m-%d').date()
    date = str(date - relativedelta(months=-int(month)))
    return date


# # -----------------------------------------------------------
# # - 获取当前时间的后N天
# # -----------------------------------------------------------
def get_next_day(n):
    today = datetimes.date.today()
    next_month_today = today - relativedelta(days=-int(n))
    return next_month_today


# # -----------------------------------------------------------
# # - 获取当前时间的后N天
# # -----------------------------------------------------------
def get_before_day(n):
    today = datetimes.date.today()
    before_month_today = today - relativedelta(days=+int(n))
    return before_month_today


# # -----------------------------------------------------------
# # - 获取指定日期的前N月
# # -----------------------------------------------------------
def get_custom_day(day=0, date='2021-11-13'):
    """
    @param day: 跳转月天数
    @param date: 指定时间
    @return:
    """
    date = datetime.strptime(date, '%Y-%m-%d').date()
    date = str(date - relativedelta(days=-int(day)))
    return date


# # -----------------------------------------------------------
# # - 获取指定日期的前N年
# # -----------------------------------------------------------
def get_custom_year(year=0, date=None):
    """
    @param year: 跳转年数
    @param date: 指定时间 '2021-11-13'
    @return:
    """
    if not date:
        date = time.strftime('%Y-%m-%d', time.localtime())
    date = datetime.strptime(date, '%Y-%m-%d').date()
    date = str(date - relativedelta(years=-int(year)))
    return date


# # -----------------------------------------------------------
# # - 图片转为base64字符串
# # -----------------------------------------------------------
def get_base64_from_img(img_path):
    """
    @param img_path: 图片存储路径
    @return: response 接口响应参数 数据类型：json
    """
    with open(img_path, "rb") as f:  # 转为二进制格式
        base64_data = base64.b64encode(f.read())  # 使用base64进行加密
        return base64_data.decode()


# # -----------------------------------------------------------
# # - 字符串转MD5
# # -----------------------------------------------------------
def computeMD5(message):
    m = hashlib.md5()
    m.update(message.encode(encoding='utf-8'))
    return m.hexdigest()


def format_path(path):
    """
    @param path: 待格式化路径
    @return: response 返回标准化路径 eg: /hj/xdgl/meituan/bank_loan_create/20220401
    """
    return path.replace('\\', '/').replace('\\\\', '/').replace('..', '.').replace('/./', '/')


def assetAnnuity(loanAmt, term, yearRate, billDate):
    """
    非最后一期，每期期供是用等额本息的公式计算出来的，然后对应的利息是等于剩余本金*月利率，本金=期供-利息；只有最后一期，是用的剩余本金+利息，计算的期供
    @param loanAmt:         借款金额
    @param term:            期数
    @param yearRate:        锦程实收利率
    @param billDate:       用户首期账单日
    @return:还款计划表
    """
    repayment_plan = []
    # 月利率
    jcMonthRate = round(yearRate / 1200, 6)
    # 剩余应还本金
    jcLeftPrePrincipal = loanAmt
    for i in range(1, term + 1):
        repaymentPlans = {}
        # 每月还款总额
        if i == term:
            jcAmtpermonth = jcLeftPrePrincipal + jcLeftPrePrincipal * jcMonthRate
        else:
            jcAmtpermonth = round(
                loanAmt * jcMonthRate * pow((1 + jcMonthRate), term) / (pow((1 + jcMonthRate), term) - 1), 2)

        # 每期应还利息
        jcMonthInterest = jcLeftPrePrincipal * jcMonthRate
        # 每期应还本金
        jcMonthPrincipal = jcAmtpermonth - jcMonthInterest
        # 剩余还款本金
        jcLeftPrePrincipal = jcLeftPrePrincipal - jcMonthPrincipal

        repaymentPlans['period'] = i
        repaymentPlans['billDate'] = get_custom_month(i - 1, billDate)
        repaymentPlans['principalAmt'] = round(jcMonthPrincipal, 2)
        repaymentPlans['interestAmt'] = round(jcMonthInterest, 2)
        repayment_plan.append(repaymentPlans)
    return repayment_plan


# # -----------------------------------------------------------
# # - 老核心等额本息还款计划计算
# # -----------------------------------------------------------
def yinLiuRepayPlanByAvgAmt(loanAmt, term, yearRate, billDate, guaranteeAmt=1.11):
    """
    非最后一期，每期期供是用等额本息的公式计算出来的，然后对应的利息是等于剩余本金*月利率，本金=期供-利息；只有最后一期，是用的剩余本金+利息，计算的期供
    @param loanAmt:         借款金额
    @param term:            期数
    @param yearRate:        锦程实收利率
    @param billDate:        用户首期账单日
    @param guaranteeAmt:    服务费
    @return:还款计划表
    """
    repayment_plan = []
    # 月利率
    jcMonthRate = round(yearRate / 1200, 6)
    # 剩余应还本金
    jcLeftPrePrincipal = loanAmt
    for i in range(1, term + 1):
        repaymentPlans = {}
        isLastPeriod = i == term
        # 每月还款总额
        if isLastPeriod:
            jcAmtpermonth = jcLeftPrePrincipal + jcLeftPrePrincipal * jcMonthRate
        else:
            jcAmtpermonth = round(
                loanAmt * jcMonthRate * pow((1 + jcMonthRate), term) / (pow((1 + jcMonthRate), term) - 1), 2)

        # 每期应还利息
        jcMonthInterest = round(jcLeftPrePrincipal * jcMonthRate, 2)
        # 每期应还本金
        jcMonthPrincipal = jcLeftPrePrincipal if isLastPeriod else jcAmtpermonth - jcMonthInterest
        # 剩余还款本金
        jcLeftPrePrincipal = round((jcLeftPrePrincipal - jcMonthPrincipal), 2)

        repaymentPlans['period'] = i  # 期次
        repaymentPlans['billDate'] = get_custom_month(i - 1, billDate)  # 还款日
        repaymentPlans['principalAmt'] = round(jcMonthPrincipal, 2)  # 本金
        repaymentPlans['interestAmt'] = round(jcMonthInterest, 2)  # 利息
        repaymentPlans['guaranteeAmt'] = guaranteeAmt  # 服务费
        repayment_plan.append(repaymentPlans)
    # repayment_plan[0]['principalAmt'] += 0.01
    return repayment_plan


# # -----------------------------------------------------------
# # - 老核心等额本金还款计划计算
# # -----------------------------------------------------------
def yinLiuRepayPlanByAvgPrincipal(loanAmt, term, yearRate, billDate, guaranteeAmt=1.11):
    """
    利息=期初余额×年贴息率（9.3%）/12
    @param loanAmt:         借款金额
    @param term:            期数
    @param yearRate:        锦程实收利率
    @param billDate:        用户首期账单日
    @param guaranteeAmt:    服务费
    @return:还款计划表
    """
    repayment_plan = []
    # 月利率
    jcMonthRate = yearRate / 1200
    # 月应还本金
    jcMonthPrincipal = round(loanAmt / term, 2)
    # 剩余应还本金
    jcLeftPrePrincipal = loanAmt
    for i in range(1, term + 1):
        repaymentPlans = {}
        # 是否最后一期
        isLastPeriod = i == term
        # 每期应还利息
        jcMonthInterest = round(jcLeftPrePrincipal * jcMonthRate, 2)
        repaymentPlans['period'] = i  # 期次
        repaymentPlans['billDate'] = get_custom_month(i - 1, billDate)  # 还款日
        if isLastPeriod:
            repaymentPlans['principalAmt'] = jcLeftPrePrincipal
        else:
            repaymentPlans['principalAmt'] = round(jcMonthPrincipal, 2)  # 本金
        repaymentPlans['interestAmt'] = round(jcMonthInterest, 2)  # 利息
        repaymentPlans['guaranteeAmt'] = guaranteeAmt  # 服务费
        jcLeftPrePrincipal = round((jcLeftPrePrincipal - jcMonthPrincipal), 2)  # 剩余还款本金
        repayment_plan.append(repaymentPlans)
    return repayment_plan


def get_bill_day(loan_date=None):
    """
    引流通用账单日计算规则
    @param loan_date: 放款时间，如果放款时间空，则默认当前时间 eg:2022-01-01
    @return: 返回首期账单日
    """
    if not loan_date:
        loan_date = time.strftime('%Y-%m-%d', time.localtime())  # 当前时间
    date_list = str(loan_date).split('-')
    bill_year, bill_month, bill_day = map(int, date_list)
    bill_month += 1
    if bill_month > 12:
        bill_year += 1
        bill_month -= 12
    bill_day = 28 if bill_day > 27 else bill_day
    bill_data = '{}-{}-{}'.format(str(bill_year), str("%02d" % bill_month), str("%02d" % bill_day))
    return bill_data


if __name__ == "__main__":
    # img_path = os.path.join(project_dir(), r'src\\test_data\\testFile\\idCardFile\\cqid2.png')
    # r = get_base64_from_img(img_path)
    # r = get_before_month(2, date='2021-11-13')
    # r = update_sql_qurey_str(table='table', db='db', attr='a=b', a=1, b=2)
    # r = get_custom_year(-16)
    # r = get_custom_month(0, '2022-02-03')
    # print(r)
    # r = get_sql_qurey_str('table', 'a', 'b', db='base')

    # r = format_path("/hj/xdgl/meituan/bank_loan_create\\20220401")
    # print(r)

    # print(OldSysLoanByAvgAmt(10000, 12, 24, '2021-07-01', guaranteeAmt=0))
    print(json.dumps(yinLiuRepayPlanByAvgPrincipal(5200, 6, 9.3, '2023-07-02', guaranteeAmt=0)))
