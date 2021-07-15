# -*- coding: utf-8 -*-
# -------------------------------------------
# 应急支付业务类
# -------------------------------------------
import json

import requests
from DataClass.YingJiZF import PayloadGenerator


class Component(PayloadGenerator):
    def __init__(self, *, data=None):
        super().__init__(data=data)

    # 应急支付渠道查询
    def query_channel(self, **kwargs):
        # 校验用户是否在系统中已存在
        self.log.demsg('开始应急支付渠道查询...')
        self.query_channel_msg(**kwargs)
        url = self.host + self.cfg['queryChannel']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('json格式业务请求响应：%s', json.dumps(response.json()))
        self.log.info('字典格式业务请求响应：%s', response.json())
        return response.json()

    def query_user_list_by_page(self, **kwargs):
        self.log.demsg('批量查询客户借据信息查询...')
        self.query_invoice_list_msg(**kwargs)
        url = self.host + self.cfg['queryInvoiceListByPage']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('json格式业务请求响应：%s', json.dumps(response.json()))
        self.log.info('字典格式业务请求响应：%s', response.json())
        return response.json()

    def loan_bill(self, **kwargs):
        self.log.demsg('查询我的账单...')
        self.loan_bill_msg(**kwargs)
        url = self.host + self.cfg['loan_bill']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('json格式业务请求响应：%s', json.dumps(response.json()))
        self.log.info('字典格式业务请求响应：%s', response.json())
        return response.json()

    def loan_query(self, **kwargs):
        self.log.demsg('贷款列表查询...')
        self.loan_query_msg(**kwargs)
        url = self.host + self.cfg['loan_query']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('json格式业务请求响应：%s', json.dumps(response.json()))
        self.log.info('字典格式业务请求响应：%s', response.json())
        return response.json()

    def loan_details(self, **kwargs):
        self.log.demsg('贷款详情查询...')
        self.loan_details_msg(**kwargs)
        url = self.host + self.cfg['loan_details']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('json格式业务请求响应：%s', json.dumps(response.json()))
        self.log.info('字典格式业务请求响应：%s', response.json())
        return response.json()

    def repay_query(self, **kwargs):
        self.log.demsg('还款记录查询...')
        self.repay_query_msg(**kwargs)
        url = self.host + self.cfg['repay_query']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('json格式业务请求响应：%s', json.dumps(response.json()))
        self.log.info('字典格式业务请求响应：%s', response.json())
        return response.json()

    def plan_query(self, **kwargs):
        self.log.demsg('待还款计划查询...')
        self.plan_query_msg(**kwargs)
        url = self.host + self.cfg['plan_query']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('json格式业务请求响应：%s', json.dumps(response.json()))
        self.log.info('字典格式业务请求响应：%s', response.json())
        return response.json()

    def payment_result(self, **kwargs):
        self.log.demsg('查询订单支付结果...')
        self.payment_result_msg(**kwargs)
        url = self.host + self.cfg['payment_result']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('json格式业务请求响应：%s', json.dumps(response.json()))
        self.log.info('字典格式业务请求响应：%s', response.json())
        return response.json()

    def payment_query(self, **kwargs):
        self.log.demsg('查询订单支付结果...')
        self.payment_query_msg(**kwargs)
        url = self.host + self.cfg['payment_query']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('json格式业务请求响应：%s', json.dumps(response.json()))
        self.log.info('字典格式业务请求响应：%s', response.json())
        return response.json()

    def bankcard_bind(self, **kwargs):
        self.log.demsg('绑定银行卡...')
        self.bankcard_bind_msg(**kwargs)
        url = self.host + self.cfg['bankcard_bind']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('json格式业务请求响应：%s', json.dumps(response.json()))
        self.log.info('字典格式业务请求响应：%s', response.json())
        return response.json()

    def bankcard_modify(self, **kwargs):
        self.log.demsg('修改银行卡...')
        self.bankcard_modify_msg(**kwargs)
        url = self.host + self.cfg['bankcard_modify']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('json格式业务请求响应：%s', json.dumps(response.json()))
        self.log.info('字典格式业务请求响应：%s', response.json())
        return response.json()

    def payment(self, **kwargs):
        self.log.demsg('发起还款申请...')
        self.payment_msg(**kwargs)
        url = self.host + self.cfg['payment']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('json格式业务请求响应：%s', json.dumps(response.json()))
        self.log.info('字典格式业务请求响应：%s', response.json())
        return response.json()