# -*- coding: utf-8 -*-
# -------------------------------------------
# 携程借贷业务类
# -------------------------------------------
import requests
from ComLib.Models import *
from DataClass.XieCheng import PayloadGenerator


class Component(PayloadGenerator):
    def __init__(self, *, data=None, repay_term_no="1"):
        super().__init__(data=data, repay_term_no=repay_term_no)

    # 携程预授信申请
    def pre_credit(self, **kwargs):
        self.log.demsg('开始授信申请...')
        self.pre_credit_msg(**kwargs)
        url = self.host + self.cfg['pre_credit']['interface']
        print(self.active_payload)
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('业务请求响应：%s', str(response.json()))
        return response.json()

    # 携程授信激活
    def credit(self, **kwargs):
        self.log.demsg('开始授信激活...')
        self.credit_msg(**kwargs)
        url = self.host + self.cfg['credit']['interface']
        print(self.active_payload)
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('业务请求响应：%s', str(response.json()))
        return response.json()

    def credit_query(self):
        pass

    def loan(self, **kwargs):
        self.log.demsg('开始支用申请...')
        self.loan_msg(**kwargs)
        url = self.host + self.cfg['loan']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('业务请求响应：%s', response.json())
        return response.json()

    def notice(self, **kwargs):
        self.log.demsg('开始还款通知...')
        self.repay_notice_msg(**kwargs)
        url = self.host + self.cfg['loan_repay_notice']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('业务请求响应：%s', response.json())
        return response.json()

    def loan_query(self):
        pass
