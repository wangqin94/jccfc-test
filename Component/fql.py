# -*- coding: utf-8 -*-
# -------------------------------------------
# 分期乐借贷业务类
# -------------------------------------------
import requests
from ComLib.Models import *
from DataClass.fql import PayloadGenerator


class Component(PayloadGenerator):
    def __init__(self, *, data=None, credit_amount=30000, loan_amount=600, loan_term=3):
        super().__init__(data=data, credit_amount=credit_amount, loan_amount=loan_amount, loan_term=loan_term)

    # 分期乐授信申请
    def credit(self, **kwargs):
        # 校验用户是否在系统中已存在
        self.check_user_available(self.data)
        self.log.demsg('开始授信申请...')
        self.credit_msg(**kwargs)
        url = self.host_fql + self.cfg['credit']['interface']
        encrypt_payload = self.encrypt(self.active_payload)
        response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
        response = self.decrypt(response.json())
        return response

    def credit_query(self, **kwargs):
        self.log.demsg('开始授信查询...')
        self.credit_query_msg(**kwargs)
        url = self.host_fql + self.cfg['credit_query']['interface']
        encrypt_payload = self.encrypt(self.active_payload)
        response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
        response = self.decrypt(response.json())
        return response

    def loan(self, **kwargs):
        self.log.demsg('开始支用申请...')
        self.loan_msg(**kwargs)
        url = self.host_fql + self.cfg['loan']['interface']
        encrypt_payload = self.encrypt(self.active_payload)
        response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
        response = self.decrypt(response.json())
        return response

    def notice(self, **kwargs):
        self.log.demsg('开始还款通知...')
        self.repay_notice_msg(**kwargs)
        url = self.host + self.cfg['loan_repay_notice']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('业务请求响应：%s', response.json())
        return response.json()

    def loan_query(self):
        pass
