# -*- coding: utf-8 -*-
# -------------------------------------------
# 携程借贷业务类
# -------------------------------------------
import requests
from DataClass.XieCheng import PayloadGenerator

class Component(PayloadGenerator):
    def __init__(self, *, repay_mode='1', data=None, repay_term_no="1", loan_invoice_id=None, repay_date='2021-08-09'):
        super().__init__(data=data, repay_term_no=repay_term_no, repay_mode=repay_mode, loan_invoice_id=loan_invoice_id,
                         repay_date=repay_date)

    # 携程预授信申请
    def pre_credit(self, **kwargs):
        # 校验用户是否在系统中已存在
        self.check_user_available(self.data)
        self.log.demsg('开始授信申请...')
        self.pre_credit_msg(**kwargs)
        url = self.host + self.cfg['pre_credit']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('业务请求响应：%s', str(response.json()))
        return response.json()

    # 携程授信激活
    def credit(self, **kwargs):
        self.log.demsg('开始授信激活...')
        self.credit_msg(**kwargs)
        url = self.host + self.cfg['credit']['interface']
        response = requests.post(url=url, headers=self.headers, json=self.active_payload)
        self.log.info('业务请求响应：%s', str(response.json()))
        return response.json()

    def credit_query(self):
        key = "certificate_no = '" + self.data['cer_no'] + "'"
        info = self.get_credit_data_info(table="credit_apply", key=key)
        try:
            status = info['status']
        except (IndexError, Exception):
            status = "x"
        return status

    def credit_to_loan(self):
        key = "certificate_no = '" + self.data['cer_no'] + "'"
        info = self.get_credit_data_info(table="credit_apply", key=key)
        try:
            status = info['status']
        except (IndexError, Exception):
            status = "x"
            self.log.info("未查询到数据")
        return status

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
