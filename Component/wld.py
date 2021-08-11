# -*- coding: utf-8 -*-
# -------------------------------------------
# 我来贷借贷业务类
# -------------------------------------------
import requests
from DataClass.wld import PayloadGenerator


class Component(PayloadGenerator):
    def __init__(self, *, repay_type='1', data=None, repay_term_no="1"):
        super().__init__(data=data, repay_term_no=repay_term_no, repay_type=repay_type)
        self.repay_term_no = repay_term_no
        self.repay_type = repay_type

    # 绑卡
    def bind_card(self, **kwargs):
        # 校验用户是否在系统中已存在
        self.check_user_available(self.data)
        self.log.demsg('开始绑卡...')
        self.bind_card_msg(**kwargs)
        url = self.host + self.cfg['bind_card']['interface']
        print(self.active_payload)
        # 加密
        encrypt_payload = self.encrypt(self.active_payload)
        print(encrypt_payload)
        response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
        # 解密
        response = self.decrypt(response.json())
        self.log.info('业务请求响应：%s', response)
        return response

    # 确认绑卡
    def confirm_bind_card(self, **kwargs):
        self.log.demsg('确认绑卡...')
        self.confirm_bind_card_msg(**kwargs)
        url = self.host + self.cfg['confirm_bind_card']['interface']
        # 加密
        encrypt_payload = self.encrypt(self.active_payload)
        response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
        # 解密
        response = self.decrypt(response.json())
        self.log.info('业务请求响应：%s', response)
        return response

    # 绑卡查询
    def query_bind_card(self, **kwargs):
        self.log.demsg('开始绑卡结果查询...')
        self.query_bind_card_msg(**kwargs)
        url = self.host + self.cfg['query_bind_card']['interface']
        # 加密
        encrypt_payload = self.encrypt(self.active_payload)
        response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
        # 解密
        response = self.decrypt(response.json())
        self.log.info('业务请求响应：%s', response)
        return response

    # 换卡申请
    def update_card(self, **kwargs):
        self.log.demsg('开始换卡申请...')
        self.update_card_msg(**kwargs)
        url = self.host + self.cfg['update_card']['interface']
        # 加密
        encrypt_payload = self.encrypt(self.active_payload)
        response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
        # 解密
        response = self.decrypt(response.json())
        self.log.info('业务请求响应：%s', response)
        return response

    # 授信申请
    def credit(self, **kwargs):
        self.log.demsg('开始授信...')
        self.credit_msg(**kwargs)
        url = self.host + self.cfg['credit']['interface']
        # 加密
        encrypt_payload = self.encrypt(self.active_payload)
        response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
        # 解密
        response = self.decrypt(response.json())
        self.log.info('业务请求响应：%s', response)
        return response

    def credit_query(self, **kwargs):
        self.log.demsg('开始授信查询...')
        self.credit_msg(**kwargs)
        url = self.host + self.cfg['credit_query']['interface']
        # 加密
        encrypt_payload = self.encrypt(self.active_payload)
        response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
        # 解密
        response = self.decrypt(response.json())
        self.log.info('业务请求响应：%s', response)
        return response

    # 支用申请
    def loan(self, **kwargs):
        self.log.demsg('开始支用...')
        self.loan_msg(**kwargs)
        url = self.host + self.cfg['loan']['interface']
        # 加密
        encrypt_payload = self.encrypt(self.active_payload)
        response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
        # 解密
        response = self.decrypt(response.json())
        self.log.info('业务请求响应：%s', response)
        return response

    # 支用查询
    def loan_query(self, **kwargs):
        self.log.demsg('开始支用查询...')
        self.loanquery_msg(**kwargs)
        url = self.host + self.cfg['loan_query']['interface']
        # 加密
        encrypt_payload = self.encrypt(self.active_payload)
        response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
        # 解密
        response = self.decrypt(response.json())
        self.log.info('业务请求响应：%s', response)
        return response

    # 还款
    def repay(self, **kwargs):
        self.log.demsg('还款...')
        self.repay_msg(**kwargs)
        url = self.host + self.cfg['repay']['interface']
        # 加密
        encrypt_payload = self.encrypt(self.active_payload)
        response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
        # 解密
        response = self.decrypt(response.json())
        self.log.info('业务请求响应：%s', response)
        return response


