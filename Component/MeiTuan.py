# -*- coding: utf-8 -*-
# -------------------------------------------
# 美团借贷业务类
# -------------------------------------------

import pprint
import requests
from ComLib.Models import *
from DataClass.MeiTuan import PayloadGenerator


class Component(PayloadGenerator):
    def __init__(self, *, data=None, app_no=None, encrypt_flag=True, loan_no=None, term="1"):
        super(Component, self).__init__(data=data, app_no=app_no)

        self.encrypt_flag = encrypt_flag
        self.loan_no = loan_no
        self.term = term

    # 美团授信申请
    @ciphertext
    def mt_credit_test(self, encrypt=False):
        self.log.info('开始授信申请!')
        interface = "/api/v1/meit/credit"
        url = "{}{}".format(self.host, interface)
        # 加密
        encrypt_payload = self.encrypt(self.credit_payload)
        response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
        self.active_payload = response.json()
        self.log.info('业务请求响应：%s', self.active_payload)
        # 解密
        response = self.decrypt(self.active_payload)
        return response

    @output_format
    def mt_credit_result(self):
        self.user_credit_apply_info()
        if self.user_credit_apply_info:
            pprint.pprint(f'授信通过，用户数据已入库 \n{self.user_credit_apply_info}')
        else:
            pprint.pprint('授信结果查询失败，无用户授信数据')

    # 美团授信查询
    def mt_credit_query_test(self):
        interface = '/api/v1/meit/credit/resultQuery'
        url = "{}{}".format(self.host, interface)
        pprint.pprint(self.credit_query_payload)
        self.credit_query_payload['body']['APP_NO'] = 'error123456'
        pprint.pprint(self.credit_query_payload)
        # 加密
        encrypt_payload = self.encrypt(self.credit_query_payload)
        for _ in range(10):
            response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
            wait_time(5)
            # 解密
            res = self.decrypt(response.json())
            res = eval(res)
            pprint.pprint(f"授信查询响应报文如下：\n{res}")
            if res['body'] and res['body']['BANK_CONTRACT_NO']:
                break
        else:
            print('授信查询失败...')
            return
        self.BANK_CONTRACT_NO = res['body']['BANK_CONTRACT_NO']
        print(f"授信合同号：\n{self.BANK_CONTRACT_NO}")
        pprint.pprint(f"授信查询响应报文如下：\n{res}")

    # 美团支用申请
    def mt_loan_test(self):
        print('------------------ 开始放款申请 --------------------')
        interface = "/api/v1/meit/loan/apply"
        url = "{}{}".format(self.host, interface)
        # 加密
        encrypt_payload = self.encrypt(self.loan_payload)
        #encrypt_payload = self.loan_payload
        response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
        print(u'接口返回: ', response)
        # 解密
        #res = response.json()
        res = self.decrypt(response.json())
        return res

    # 支用查询
    def mt_loan_query_test(self):
        print('------------------ 开始放款申请查询 --------------------')
        interface = "/api/v1/meit/loan/resultQuery"
        url = "{}{}".format(self.host, interface)
        # 加密
        encrypt_payload = self.encrypt(self.loan_query_payload)
        response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
        print(u'接口返回: ', response)
        # 解密
        res = self.decrypt(response.json())
        print(f"响应报文如下：\n{res}")

    # 额度失败
    def mt_credit_invalid_test(self):
        print('------------------ 额度失效配置 --------------------')
        url = 'https://credit-hsit.corp.jccfc.com/hsjry/credit/v1/limit/operate/invalid'
        response = requests.post(url=url, headers=self.headers, json=self.credit_invalid_payload)
        print(u'接口返回: ', response)
        print(f"响应报文如下：\n{response}")

    def mt_repay_notice_test(self, **kwargs):
        self.log.demsg('还款通知...')
        self.mt_repay_notice_msg(**kwargs)
        url = self.host + self.cfg['repay_notice']['interface']
        if self.encrypt_flag:
            # 加密
            encrypt_payload = self.encrypt(self.active_payload)
            response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
            print(u'接口返回: ', response)
            # 解密
            res = self.decrypt(response.json())
            print(f"响应报文如下：\n{res}")
        else:
            response = requests.post(url=url, headers=self.headers, json=self.active_payload)
            res = self.decrypt(response.json())
            print(f"响应报文如下：\n{res}")
        return response.json()

    def mt_loan_notice_test(self, **kwargs):
        self.log.demsg('还款通知...')
        self.mt_loan_notice_msg(**kwargs)
        url = self.host + self.cfg['loan_notice']['interface']
        if self.encrypt_flag:
            # 加密
            encrypt_payload = self.encrypt(self.active_payload)
            response = requests.post(url=url, headers=self.headers, json=encrypt_payload)
            print(u'接口返回: ', response)
            # 解密
            res = self.decrypt(response.json())
            print(f"响应报文如下：\n{res}")
        else:
            response = requests.post(url=url, headers=self.headers, json=self.active_payload)
            res = self.decrypt(response.json())
            print(f"响应报文如下：\n{res}")
        return response.json()