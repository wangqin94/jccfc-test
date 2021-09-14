# -*- coding: utf-8 -*-
# ------------------------------------------
# 分期乐接口数据封装类
# ------------------------------------------
import time
from config.TestEnvInfo import *
from src.impl.common.CommonUtils import *
from src.enums.EnumsCommon import *
from src.enums.EnumFql import *
from utils.Models import *
from src.test_data.module_data import fql


class FqlBizImpl(INIT):
    def __init__(self, *, data=None, credit_amount=30000, loan_amount=600, loan_term=3, encrypt_flag=True):
        super().__init__()

        # 解析项目特性配置
        self.cfg = fql.fql

        self.data = data if data else get_base_data(str(self.env) + ' -> ' + str(ProductEnum.FQL.value), 'applyId')
        self.log.info('用户四要素信息 \n%s', self.data)

        self.encrypt_flag = encrypt_flag
        self.strings = str(int(round(time.time() * 1000)))
        self.times = time.strftime('%Y-%m-%d', time.localtime())
        self.loanAmount = loan_amount
        self.credit_amount = credit_amount
        self.loanTerm = loan_term

        self.sourceCode = '000UC010000006268'
        self.encrypt_url = self.host_fql + FqlPathEnum.fqlEncryptPath.value
        self.decrypt_url = self.host_fql + FqlPathEnum.fqlDecryptPath.value

        # 初始化payload变量
        self.active_payload = {}

        # 初始数据库变量
        self.credit_database_name = '%s_credit' % TEST_ENV_INFO.lower()
        self.asset_database_name = '%s_asset' % TEST_ENV_INFO.lower()

    def set_active_payload(self, payload):
        self.active_payload = payload

    @staticmethod
    def url_encoded_to_json(response):
        data = dict()
        data["content"] = response.split('content=')[1].split('&sign=')[0]
        data["sign"] = response.split('&sign=')[1]
        return data

    # 授信申请payload
    def credit(self, **kwargs):
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

        # 更新 payload 字段值
        credit_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit']['payload'], **credit_data)
        self.active_payload = parser.parser

        # 校验用户是否在系统中已存在
        self.check_user_available(self.data)

        self.log.demsg('开始授信申请...')
        url = self.host_fql + self.cfg['credit']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url, 
                                     encrypt_flag=self.encrypt_flag)
        response['applyId'] = self.data['applyId']
        return response

    # 授信查询payload
    def credit_query(self, **kwargs):
        credit_data = dict()
        # header
        credit_data['requestSerialNo'] = 'SerialNo' + self.strings + "2"

        # body
        credit_data['applyId'] = self.data['applyId']
        credit_data['sourceCode'] = self.sourceCode

        # 更新 payload 字段值
        credit_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit_query']['payload'], **credit_data)
        self.active_payload = parser.parser

        self.log.demsg('开始授信查询...')
        url = self.host_fql + self.cfg['credit_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url, 
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 支用申请payload
    def loan(self, **kwargs):
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
        firstRepayDate, day = loan_and_period_date_parser(date_str=date, period=int(self.loanTerm), flag=False,
                                                          max_bill=28)
        loan_data['firstRepayDate'] = firstRepayDate[0]
        loan_data['fixedRepayDay'] = day
        loan_data['mobileNo'] = self.data['telephone']

        # 更新 payload 字段值
        loan_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan']['payload'], **loan_data)
        self.active_payload = parser.parser

        self.log.demsg('开始支用申请...')
        url = self.host_fql + self.cfg['loan']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url, 
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 支用查询
    def loan_query(self, **kwargs):
        loan_data = dict()
        # header
        loan_data['requestSerialNo'] = 'SerialNo' + self.strings + "2"

        # body
        loan_data['applyId'] = self.data['applyId']
        loan_data['sourceCode'] = self.sourceCode

        # 更新 payload 字段值
        loan_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan_query']['payload'], **loan_data)
        self.active_payload = parser.parser

        self.log.demsg('开始支用查询...')
        url = self.host_fql + self.cfg['loan_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url, 
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 支用查询payload
    def loan_repay_notice(self, **kwargs):
        loan_data = dict()
        # head
        loan_data['requestSerialNo'] = 'SerialNo' + self.strings + "2"

        # body
        loan_data['applyId'] = self.data['applyId']
        loan_data['sourceCode'] = self.sourceCode

        # 更新 payload 字段值
        loan_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit_query']['payload'], **loan_data)
        self.active_payload = parser.parser
        url = self.host + self.cfg['loan_repay_notice']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url, 
                                     encrypt_flag=self.encrypt_flag)
        return response


if __name__ == '__main__':
    info = FqlBizImpl()
