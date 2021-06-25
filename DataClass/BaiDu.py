# -*- coding: utf-8 -*-
# ------------------------------------------
# 百度接口数据封装类
# ------------------------------------------

import time
from pprint import pprint
from ComLib.Models import *
from Engine.Base import INIT


class PayloadGenerator(INIT):
    def __init__(self, *, data=None, app_no=None):
        super().__init__()
        self.data = data if data else get_base_data(str(self.env) + ' -> ' + str(self.project))
        self.log.info('用户四要素信息 \n%s', self.data)

        self.credit_amount = 3000000    # 授信申请金额, 默认3000000  单位分
        self.loan_amount = 1000000      # 支用申请金额, 默认1000000  单位分
        self.period = 3                 # 借款期数, 默认3期

        # 初始化payload变量
        self.credit_payload = {}
        self.loan_payload = {}
        self.active_payload = {}

    def set_active_payload(self, payload):
        self.active_payload = payload

    # 授信申请payload
    def credit_msg(self, **kwargs):
        strings = str(int(round(time.time() * 1000)))
        credit_data = dict()
        credit_data['prcid'] = self.data['cer_no']
        credit_data['bankcard'] = self.data['bankid']
        credit_data['name'] = self.data['name']
        credit_data['phonenumber'] = self.data['telephone']

        credit_data['timestamp'] = time.strftime('%Y%m%d%H%M%S')
        credit_data['reqSn'] = 'Apply_req' + strings + "1001"
        credit_data['sessionId'] = 'Apply_sid' + strings + "1002"
        credit_data['transactionId'] = 'Apply_tid' + strings + "1003"
        credit_data['initialAmount'] = self.credit_amount               # 授信申请金额, 默认3000000分

        credit_data.update(kwargs)
        self.log.info("data数据: %s", credit_data)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['credit']['payload'], **credit_data)
        self.credit_payload = parser.parser
        self.set_active_payload(self.credit_payload)

    # 支用申请payload
    def loan_msg(self, **kwargs):
        """ # 支用申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        strings = str(int(round(time.time() * 1000)))
        loan_data = dict()
        loan_data['prcid'] = self.data['cer_no']
        loan_data['bankcard'] = self.data['bankid']
        loan_data['name'] = self.data['name']
        loan_data['phonenumber'] = self.data['telephone']

        loan_data['timestamp'] = time.strftime('%Y%m%d%H%M%S')
        loan_data['reqSn'] = 'Loan_req' + strings + "1001"
        loan_data['sessionId'] = 'Loan_sid' + strings + "1002"
        loan_data['transactionId'] = 'Loan_tid' + strings + "1003"
        loan_data['cashAmount'] = self.loan_amount                      # 支用申请金额, 默认1000000分
        loan_data['orderId'] = 'Ord' + strings
        loan_data['term'] = self.period

        loan_data.update(kwargs)
        self.log.info("data数据: %s", loan_data)

        parser = DataUpdate(self.cfg['loan']['payload'], **loan_data)
        self.loan_payload = parser.parser
        self.set_active_payload(self.loan_payload)
