# -*- coding: utf-8 -*-
# ------------------------------------------
# 分期乐接口数据封装类
# ------------------------------------------
import json
import time

from Config.global_config import *
from Engine.Base import INIT
from Component.XieCheng import *
from Config.TestEnvInfo import *
from ComLib.Models import *


class PayloadGenerator(INIT):
    def __init__(self, *, data=None, credit_amount=30000, loan_amount=600, loan_term=3):
        super().__init__()
        self.data = data if data else get_base_data(str(self.env) + ' -> ' + str(self.project), 'applyId')
        self.log.info('用户四要素信息 \n%s', self.data)

        self.strings = str(int(round(time.time() * 1000)))
        self.times = time.strftime('%Y-%m-%d', time.localtime())
        self.loanAmount = loan_amount
        self.credit_amount = credit_amount
        self.loanTerm = loan_term

        self.sourceCode = '000UC010000006268'
        self.encrypt_url = self.host_fql + "/api/fql/v1/encrypt/encryptData"
        self.decrypt_url = self.host_fql + "/api/fql/v1/encrypt/decryptData"

        # 初始化payload变量
        self.active_payload = {}

        # 初始数据库变量
        self.credit_database_name = '%s_credit' % TEST_ENV_INFO.lower()
        self.asset_database_name = '%s_asset' % TEST_ENV_INFO.lower()

    def get_credit_data_info(self, table='credit_loan_apply', key="查询条件"):
        """
        :function: 获取credit数据库表中信息
        table : 表名
        key ： 查询关键字
        """
        sql = "select * from {}.{} where {};".format(self.credit_database_name, table, key)
        # 获取表属性字段名
        keys = self.mysql.select_table_column(table_name=table, database=self.credit_database_name)
        # 获取查询内容
        values = self.mysql.select(sql)
        # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
        data = [dict(zip(keys, item)) for item in values][0]
        return data

    def get_asset_data_info(self, table='asset_loan_apply', key="查询条件"):
        """
        :function: 获取asset数据库表中信息
        table : 表名
        key ： 查询关键字
        """
        sql = "select * from {}.{} where {};".format(self.asset_database_name, table, key)
        # 获取表属性字段名
        keys = self.mysql_asset.select_table_column(table_name=table, database=self.asset_database_name)
        # 获取查询内容
        values = self.mysql_asset.select(sql)
        # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
        data = [dict(zip(keys, item)) for item in values][0]
        return data

    def set_active_payload(self, payload):
        self.active_payload = payload

    def encrypt(self, encrypt_payload):
        print("\n开始加密")
        response = requests.post(url=self.encrypt_url, headers=headers, json=encrypt_payload)
        print("加密status_code:", response.status_code)
        res = response.json()
        res = str(res).replace("'", '''"''').replace(" ", "")
        print(f"加密响应报文如下：\n{res}")
        return json.loads(res)

    def decrypt(self, decrypt_payload):
        print("\n开始解密")
        decrypt_payload = json.dumps(decrypt_payload)
        response = requests.post(url=self.decrypt_url, headers=headers, data=decrypt_payload)
        print("解密status_code:", response.status_code)
        res = response.json()
        res = str(res).replace("'", '''"''').replace(" ", "")
        print(f"解密响应报文如下：\n{res}")
        return res

    @staticmethod
    def url_encoded_to_json(response):
        data = dict()
        data["content"] = response.split('content=')[1].split('&sign=')[0]
        data["sign"] = response.split('&sign=')[1]
        return data

    # 授信申请payload
    def credit_msg(self, **kwargs):
        credit_data = dict()

        # head
        credit_data['requestSerialNo'] = 'SerialNo' + self.strings + "1"
        credit_data['requestTime'] = self.strings
        credit_data['empNo'] = 'empNo' + self.strings
        credit_data['merchantId'] = self.sourceCode
        credit_data['managerId'] = self.sourceCode

        # body
        credit_data['applyId'] = self.data['applyId']
        credit_data['sourceCode'] = self.sourceCode
        credit_data['loanAmount'] = self.credit_amount
        credit_data['creditAmount'] = self.credit_amount
        credit_data['firstOrderDate'] = time.strftime('%Y-%m-%d', time.localtime())

        credit_data['idNo'] = self.data['cer_no']
        credit_data['userBankCardNo'] = self.data['bankid']
        credit_data['name'] = self.data['name']
        credit_data['mobileNo'] = self.data['telephone']

        credit_data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['credit']['payload'], **credit_data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 授信查询payload
    def credit_query_msg(self, **kwargs):
        credit_data = dict()
        # header
        credit_data['requestSerialNo'] = 'SerialNo' + self.strings + "2"

        # body
        credit_data['applyId'] = self.data['applyId']
        credit_data['sourceCode'] = self.sourceCode

        credit_data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['credit_query']['payload'], **credit_data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 支用申请payload
    def loan_msg(self, **kwargs):
        """ # 支用申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        loan_data = dict()
        # head
        loan_data['requestSerialNo'] = 'SerialNo' + self.strings + '3'
        loan_data['requestTime'] = self.strings
        loan_data['empNo'] = 'empNo' + self.strings
        loan_data['merchantId'] = self.sourceCode
        loan_data['managerId'] = self.sourceCode

        # body
        loan_data['applyId'] = self.data['applyId']
        loan_data['sourceCode'] = self.sourceCode
        loan_data['loanAmt'] = self.loanAmount
        loan_data['loanTerm'] = self.loanTerm
        loan_data['name'] = self.data['name']
        loan_data['mobileNo'] = self.data['telephone']
        loan_data['debitAccountNo'] = self.data['bankid']

        date = self.times.split()[0]
        firstRepayDate, day = loan_and_period_date_parser(date_str=date,period=int(self.loanTerm),flag=False,max_bill=28)
        print(firstRepayDate[0])
        loan_data['firstRepayDate'] = firstRepayDate[0]
        loan_data['fixedRepayDay'] = day
        loan_data['mobileNo'] = self.data['telephone']

        # 更新 payload 字段值
        loan_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan']['payload'], **loan_data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 支用查询payload
    def loan_query_msg(self, **kwargs):
        loan_data = dict()
        # head
        loan_data['requestSerialNo'] = 'SerialNo' + self.strings + "2"

        # body
        loan_data['applyId'] = self.data['applyId']
        loan_data['sourceCode'] = self.sourceCode

        loan_data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['credit_query']['payload'], **loan_data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", loan_data)
        self.set_active_payload(self.active_payload)


if __name__ == '__main__':
    info = PayloadGenerator()
