# -*- coding: utf-8 -*-

# # -----------------------------------------------------------
# # - 公共模块函数变量
# # -----------------------------------------------------------
import random
import string

from Engine.Logger import Logs, getcallargs, wraps, requests, json, time

_log = Logs()
__all__ = ['output_format', 'wait_time', 'get_base_data',
           'loan_and_period_date_parser', 'ciphertext',
           'encrypt', 'decrypt', 'DataUpdate', 'get_telephone']


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
def get_base_data(env, *project):
    strings = str(int(round(time.time() * 1000)))
    data = {}
    res = requests.get('http://10.10.100.153:8081/getTestData')
    data['name'] = eval(res.text)["姓名"]
    data['cer_no'] = eval(res.text)["身份证号"]
    data['bankid'] = eval(res.text)["银行卡号"]
    # 获取随机生成的手机号
    data['telephone'] = get_telephone()

    # project赋值后天从到data中
    if project:
        for item in project:
            data[item] = str(item) + strings

    with open('person.py', 'a', encoding='utf-8') as f:
        f.write('\n')
        f.write('data = {}  # {}'.format(str(data), env))
    return data


# # -----------------------------------------------------------
# # - 数据库查询语句组装
# # -----------------------------------------------------------
def get_sql_qurey_str(table, db=None, attr=None, **kwargs):
    """ # 数据库查询sql
    :param table:       表名
    :param db:          数据库名
    :param attr:        查询表子项
    :param kwargs:      where 筛选条件
    :return:            sql语句
    """
    table = table if not db else '%s.%s' % (db, table)
    attr = '*' if not attr else ', '.join(attr)
    sql_str = ["select", attr, "from", table]
    if kwargs:
        filters = 'where' + 'and'.join(["%s='%s'" % (k, v) for k, v in kwargs.items()]) + ';'
        sql_str.append(filters)
    return ' '.join(sql_str)


# # -----------------------------------------------------------
# # - 还款日/账单日计算
# # -----------------------------------------------------------
def loan_and_period_date_parser(*, date_str, period=1, flag=False, max_bill=25):
    """ # tips: 入参时须带关键字
    :param date_str:    (str)借款日期  eg: '2020-01-09'
    :param period:      (int)分期数  eg: 3， 默认为 1
    :param flag:        返回首期还款日、账单日
    :param max_bill:    (int) 最大账单日, 默认25号
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
    :param encrypt_url:     加密请求地址
    :param headers:         加密请求报文头部
    :param encrypt_payload: 待加密数据
    :return: 加密后的payload
    """
    _log.info("开始请求加密接口对报文进行加密操作...")
    response = requests.post(url=encrypt_url, headers=headers, json=encrypt_payload)
    _log.info("报文加密操作结束！status code: %s", response.status_code)
    res = response.json()
    res = str(res).replace("'", '''"''').replace(" ", "")
    _log.info(f"加密后的报文：\n{res}")
    return json.loads(res)


# # -----------------------------------------------------------
# # - 接口数据解密
# # -----------------------------------------------------------
def decrypt(decrypt_url, headers, decrypt_payload):
    """ # 接口数据payload解密
    :param decrypt_url:     解密请求地址
    :param headers:         解密请求报文头部
    :param decrypt_payload: 待解密数据
    :return:                解密后的报文
    """
    _log.info("开始请求解密接口对报文进行解密操作...")
    decrypt_payload = json.dumps(decrypt_payload)
    response = requests.post(url=decrypt_url, headers=headers, data=decrypt_payload)
    _log.info("报文解密操作结束！status code: %s", response.status_code)
    res = response.json()
    res = str(res).replace("'", '''"''').replace(" ", "")
    _log.info(f"解密后的报文：\n{res}")
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
            if key in data.keys():  # 替换字典第一层中所有key与传参一致的key
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


if __name__ == "__main__":
    print(DataUpdate)
