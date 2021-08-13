# -*- coding: utf-8 -*-
# -------------------------------------------
# 百度借贷业务类
# -------------------------------------------
import requests
from ComLib.Models import *
from DataClass.BaiDu import PayloadGenerator


class Component(PayloadGenerator):
    def __init__(self, *, data=None, app_no=None, type=1, loan_no=None):
        super().__init__(data=data, app_no=app_no)
        self.loan_no = loan_no
        self.type = type

    # 百度授信申请
    def credit(self, **kwargs):
        # 校验用户是否已存在
        self.check_user_available(self.data)
        self.log.demsg('开始授信申请...')
        self.credit_msg(**kwargs)
        url = self.host + self.cfg['credit']['interface']
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
        self.log.demsg('开始通知申请...')
        self.notice_msg(**kwargs)
        url = self.host + self.cfg['notice']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('业务请求响应：%s', response.json())
        return response.json()

    def loan_query(self):
        pass

    def limitrestore(self, **kwargs):
        self.log.demsg('开始额度恢复...')
        self.limit_msg(**kwargs)
        url = self.host + self.cfg['limitrestore']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('业务请求响应：%s', response.json())
        return response.json()
