# -*- coding: utf-8 -*-
# ------------------------------------------
# 借条接口数据封装类
# ------------------------------------------
from datetime import datetime

from engine.EnvInit import EnvInit
from src.enums.EnumJieTiao import JieTiaoEnum
from src.impl.common.CommonBizImpl import post_with_encrypt
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from src.test_data.module_data import JieTiao
from utils.Models import *
from src.enums.EnumsCommon import *


class JieTiaoBizImpl(EnvInit):
    def __init__(self, *, data=None, encrypt_flag=True):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()
        # 解析项目特性配置
        self.cfg = JieTiao.JieTiao

        self.data = data if data else get_base_data(str(self.env) + ' -> ' + str(ProductEnum.JieTiao.value), "applyid")

        self.encrypt_flag = encrypt_flag
        self.strings = str(int(round(time.time() * 1000)))

        self.encrypt_url = self.host + JieTiaoEnum.JieTiaoEncryptPath.value
        self.decrypt_url = self.host + JieTiaoEnum.JieTiaoDecryptPath.value

        # 初始化payload变量
        self.active_payload = {}

    def loan(self, **kwargs):
        loan_data = dict()

        loan_data['loanReqNo'] = 'loanReqNo' + self.strings + "2"
        loan_data['custName'] ,loan_data['dbAcctName'] = self.data['name'],self.data['name']
        loan_data['id'] = self.data['cer_no']
        loan_data['dbAcct'] = self.data['bankid']
        loan_data['mobileNo'] = self.data['telephone']

        # 更新 payload 字段值
        loan_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan']['payload'], **loan_data)
        self.active_payload = parser.parser
        
        self.log.demsg('放款请求接口...')
        url = self.host + self.cfg['loan']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def loan_query(self, **kwargs):
        loan_query_data = dict()

        # 更新 payload 字段值
        loan_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan_query']['payload'], **loan_query_data)
        self.active_payload = parser.parser

        self.log.demsg('放款结果查询接口...')
        url = self.host + self.cfg['loan_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def payment(self, **kwargs):
        payment_data = dict()
        payment_data['repayCstname'] = self.data['name']
        payment_data['repayRelcard'] = self.data['cer_no']

        # 更新 payload 字段值
        payment_data.update(kwargs)
        parser = DataUpdate(self.cfg['payment']['payload'], **payment_data)
        self.active_payload = parser.parser

        self.log.demsg('代扣接口...')
        url = self.host + self.cfg['payment']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response


    def payment_query(self, **kwargs):
        payment_query_data = dict()

        # 更新 payload 字段值
        payment_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['payment_query']['payload'], **payment_query_data)
        self.active_payload = parser.parser

        self.log.demsg('代扣结果查询接口...')
        url = self.host + self.cfg['payment_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response


    def repay_notice(self, **kwargs):
        repay_notice_data = dict()

        # 更新 payload 字段值
        repay_notice_data.update(kwargs)
        parser = DataUpdate(self.cfg['repay_notice']['payload'], **repay_notice_data)
        self.active_payload = parser.parser

        self.log.demsg('还款通知接口...')
        url = self.host + self.cfg['repay_notice']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def repay_query(self, **kwargs):
        repay_query_data = dict()

        # 更新 payload 字段值
        repay_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['repay_query']['payload'], **repay_query_data)
        self.active_payload = parser.parser

        self.log.demsg('还款查询接口...')
        url = self.host + self.cfg['repay_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response