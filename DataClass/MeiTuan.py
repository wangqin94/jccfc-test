# -*- coding: utf-8 -*-
# ------------------------------------------
# 接口数据封装类
# ------------------------------------------

import sys
import json
import time
import requests
from ComLib.Models import *
from Config.global_config import *
from Engine.Base import INIT


class PayloadGenerator(INIT):
    def __init__(self, *, data=None, app_no=None, loan_no=None, term="1"):
        super().__init__()
        if not data:
            self.data = get_base_data(TEST_ENV_INFO)
            self.log.info('随机生成客户四要素信息 \n%s', self.data)
        else:
            self.data = data
            self.log.info('自定义用户四要素信息 \n%s', self.data)

        # 检测手机号是否已被注册
        self.check_user_available(self.data)

        # 初始化定义用户apply信息
        self.user_credit_apply_info = {}
        self.user_credit_file_info = {}
        self.user_loan_apply_info = {}

        # 授信申请号 - 授信查询使用
        self.app_no = app_no
        # 初始化授信合同号
        self.BANK_CONTRACT_NO = None

        # 初始借据号,期次
        self.loan_no = loan_no
        self.term = term

        # 初始化定义部分数据值
        self.encrypt_url = self.host + "/api/v1/secret/thirdEncryptData/MEIT"
        self.decrypt_url = self.host + "/api/v1/secret/thirdDecryptData/MEIT"
        self.credit_amount = 3000000  # 授信申请额度 单位分
        self.loan_amount = 100000  # 支用申请额度 单位分
        self.rate = 980  # 利息 万分之
        self.base_data = data
        self.loan_no = str(int(round(time.time() * 1000))) + "1001"

        # 初始化定义所有接口的payload
        self.credit_payload = {}
        self.credit_query_payload = {}
        self.loan_payload = {}
        self.loan_query_payload = {}
        self.credit_invalid_payload = {}
        self.crypt_payload = ''
        self.decrypt_payload = ''
        self.active_payload = {}

    def encrypt(self, encrypt_payload):
        print("\n开始加密")
        response = requests.post(url=self.encrypt_url, headers=headers, json=encrypt_payload)
        print("加密status_code:", response.status_code)
        res = response.json()
        res = str(res).replace("'", '''"''').replace(" ", "")
        # print(f"加密响应报文如下：\n{res}")
        return json.loads(res)

    def decrypt(self, decrypt_payload):
        print("\n开始解密")
        decrypt_payload = json.dumps(decrypt_payload)
        response = requests.post(url=self.decrypt_url, headers=headers, data=decrypt_payload)
        print("解密status_code:", response.status_code)
        res = response.json()
        res = str(res).replace("'", '''"''').replace(" ", "")
        # print(f"解密响应报文如下：\n{res}")
        return res

    @staticmethod
    def url_encoded_to_json(response):
        data = dict()
        data["content"] = response.split('content=')[1].split('&sign=')[0]
        data["sign"] = response.split('&sign=')[1]
        return data

    def check_phone_available(self):
        sql = "select * from credit_apply where user_tel='{}';".format(self.data['telephone'])
        res = self.mysql.select(sql)
        if res:
            if self.data['cer_no'] not in res[0]:
                self.log.error('手机号已被注册, 测试程序退出!')
                sys.exit(168)
            else:
                self.log.warning('提示：用户已存在授信信息\n继续流程...')

    # 动态获取授信申请号，当force为真时，强制替换为授信payload中的APP_NO申请号
    def update_credit_app_no(self, src=True, force=False):
        """
        :param src: 获取app_no的来源 True: user_credit_apply_info, False: credit_payload
        :param force: 是否为强制更新， 默认False
        :return: None
        """
        if force:  # 强制模式
            print('---强制替换刷新授信申请号---')
            if src:
                if self.credit_payload and 'APP_NO' in self.credit_payload['body']:
                    self.app_no = self.credit_payload['body']['APP_NO']
            else:
                if self.user_credit_apply_info and 'thirdpart_apply_id' in self.user_credit_apply_info[0]:
                    self.app_no = self.user_credit_apply_info[0]['thirdpart_apply_id']
        else:  # 非强制模式
            if self.app_no:
                self.log.info('授信申请号存在，本次操作不做替换刷新，若需要强制替换，请置force=True')
            else:
                if self.credit_payload and 'APP_NO' in self.credit_payload['body']:
                    self.app_no = self.credit_payload['body']['APP_NO']
                else:
                    if self.user_credit_apply_info and 'thirdpart_apply_id' in self.user_credit_apply_info[0]:
                        self.app_no = self.user_credit_apply_info[0]['thirdpart_apply_id']

    # 设置授信申请号
    def set_credit_app_no(self, app_no):
        self.app_no = app_no

    def update_bank_contract_no(self):
        self.BANK_CONTRACT_NO = self.user_credit_apply_info[0]['credit_apply_id']

    def set_active_payload(self, payload):
        self.active_payload = payload

    # 获取数据库用户授信信息
    def get_user_credit_apply_info(self, sql=None, table='credit_apply', database=None, times=10, interv=5):
        database = self.credit_database_name if not database else database
        if not sql:
            sql = "SELECT * FROM {} WHERE certificate_no='{}';".format(table, self.data['cer_no'])
        keys = self.mysql.select_table_column(table_name=table, database=database)
        res = []
        for _ in range(times):
            res = self.mysql.select(sql)
            if res:
                break
            wait_time(interv)
        else:
            self.log.error('查询用户授信信息失败')
        info = [dict(zip(keys, item)) for item in res]
        self.user_credit_apply_info = info

    def get_user_file_info(self, sql, table='credit', database=None):
        database = self.credit_database_name if not database else database
        # keys = self.mysql.select_table_column(table_name=table, database=database)
        # sql =
        # values = self.mysql.select(sql)
        pass

    # 获取数据库支用申请用户信息
    def get_user_loan_apply_info(self, certificate_no, database=None):
        database = self.credit_database_name if not database else database
        sql = "select * from {}.credit_loan_apply where certificate_no='{}';".format(database, certificate_no)
        keys = self.mysql.select_table_column(table_name='credit_loan_apply', database=database)
        res = self.mysql.select(sql)
        info = [dict(zip(keys, item)) for item in res]
        self.user_loan_apply_info = info

    def init_msg(self):
        self.data = self.base_data

    # 授信申请payload
    def mt_credit_msg(self, **kwargs):
        credit_data = self.data
        strings = str(int(round(time.time() * 1000)))
        credit_data['tradestamp'] = time.strftime('%Y%m%d%H%M%S')
        credit_data['reqsn'] = strings + "1001"
        credit_data['app_no'] = strings + "1002"
        credit_data['APPLY_AMT'] = self.credit_amount  # 授信申请贷款金额, 默认3000000分
        payload = {
            "head": {
                "merchantId": "F21C01MEIT",
                "channelNo": "01",
                "requestSerialNo": 'SXSN' + credit_data['reqsn'],
                "requestTime": credit_data['tradestamp'],  # 年-月-日 时：分：秒
                "tenantId": "000"
            },  # 202103031119406040001000000009
            "body": {
                "APP_NO": 'SXAN' + credit_data['app_no'],  # '202103021040153690001000000028',  #
                "APPLY_AMT": str(credit_data['APPLY_AMT']),  # N*100
                "CUSTOMER_NO": "CUSTOMER_NO" + credit_data["cer_no"],
                "PRODUCT_NO": "00018",  # 美团产品号
                "BANK_NO": "MT",
                "CER_TYPE": "01",
                "CER_NO": credit_data["cer_no"],
                "CERT_VALID_START_DATE": "20160225",
                "CERT_VALID_END_DATE": "20260225",
                "NAME": credit_data['name'],
                # "NAME": "陈祺",
                "MOBILE_NO": credit_data["telephone"],
                "CARD_NO": credit_data["bankid"],
                "ZM_AUTH_FLAG": "Y",
                "RATE_LISTS": [
                    {
                        "REPAYMENT_TYPE": "ACPI",
                        "PLATFORM_RATE": str(self.rate),
                        "PLATFORM_PENALTY_RATE": str(self.rate)
                    }
                ],
                "OCR": {
                    "ID_NO_OCR": credit_data["cer_no"],
                    "ID_NAME_OCR": credit_data["name"],
                    # "ID_NAME_OCR": "陈祺",
                    "ID_VALIDITY_OCR": "20160225-20260225",
                    "ID_FACE_PIC_PATH": "/hj/xdgl/meituan/cqid1.png",  # /hj/xdgl/meituan/cqid1
                    "ID_BACK_PIC_PATH": "/hj/xdgl/meituan/cqid2.png",
                    # /hj/xdgl/meituan/cqid2.png  /hj/xdgl/meituan/owxbackerror.jpg
                    # "ID_FACE_PIC_PATH": "/hj/xdgl/meituan/wymid1.png",
                    # "ID_BACK_PIC_PATH": "",
                    "ID_ADDRESS_OCR": "成都莆田街133号-4-5",  # 深圳莆田街133号-4-5
                    "NATION": "回族",
                    "ISSUER": "四川省成都市"
                },
                "HAS_JB_ADMIT": "Y",
                "RISK_INFO": {
                    "platform_consuming_ability_level": "1002",
                    "platform_consuming_frequency_level": "1002",
                    "platform_consuming_scene_number_level": "1002",
                    "predicted_age_level": "1002",
                    "predicted_marital_status_level": "1002",
                    "active_city_number_level_last_90d": "1002",
                    "predicted_gender_level": "1002",
                    "account_register_time_level": "1002",
                    "job_category_code": "1002",
                    "resident_province_name": "1002",
                    "user_order_count_level_in_last_180d": "1002",
                    "user_order_count_level_in_last_360d": "1002",
                    "user_order_count_level_in_last_90d": "1002",
                    "user_order_days_level_in_last_180d": "1002",
                    "user_order_days_level_in_last_360d": "1002",
                    "user_order_days_level_in_last_90d": "1002",
                    "user_successful_order_amount_level_in_last_180d": "1002",
                    "user_successful_order_amount_level_in_last_360d": "1002",
                    "user_successful_order_amount_level_in_last_90d": "1002",
                    "user_successful_order_count_level_in_last_180d": "1002",
                    "user_successful_order_count_level_in_last_360d": "1002",
                    "user_successful_order_count_level_in_last_90d": "1002",
                    "user_successful_waimai_order_count_level_in_last_180d": "1002",
                    "user_successful_waimai_order_count_level_in_last_360d": "1002",
                    "user_successful_waimai_order_count_level_in_last_90d": "1002",
                    "user_visit_bg_count_level_in_last_90d": "1002",
                    "user_active_days_in_last_180d_level": "1002",
                    "user_active_days_in_last_360d_level": "1002",
                    "user_active_days_in_last_90d_level": "1002",
                    "user_visit_waimai_days_in_last_180d": "1002",
                    "user_visit_waimai_days_in_last_360d": "1002",
                    "user_visit_waimai_days_in_last_90d": "1002",
                    "user_active_tag_in_1y": "1002",
                    "user_visit_group_buy_days_in_last_180d": "1002",
                    "user_visit_group_buy_days_in_last_360d": "1002",
                    "user_visit_group_buy_days_in_last_90d": "1002",
                    "mt_creditscore_level_v4_0_1": "1002"
                },
                "Signature_date": "20160225",
                # "FACE_PIC_PATH": "/hj/xdgl/meituan/wymface.png",
                "FACE_PIC_PATH": "/hj/xdgl/meituan/cqface",  # /hj/xdgl/meituan/cqface.png
            }
        }
        self.credit_payload = payload
        if kwargs:
            parser = DataUpdate(payload, **kwargs)
            self.credit_payload = parser.parser
        self.set_active_payload(self.credit_payload)

    # 美团授信查询payload
    def mt_credit_query_msg(self, **kwargs):
        print('------开始授信结果查询-------')
        credit_query_data = self.data
        credit_query_data['reqsn'] = str(int(round(time.time() * 1000))) + "1001"
        if not self.app_no:
            self.update_credit_app_no()  # 获取授信申请号
        payload = {
            "head": {
                "merchantId": "F21C01MEIT",
                "channelNo": "01",
                "requestSerialNo": self.app_no,
                "requestTime": credit_query_data['reqsn'],  # 年-月-日 时：分：秒
                "tenantId": "000",
                "token": "111"
            },
            "body": {
                "APP_NO": self.app_no,
            }
        }
        self.credit_query_payload = payload
        if kwargs:
            parser = DataUpdate(payload, **kwargs)
            self.credit_query_payload = parser.parser
        self.set_active_payload(self.credit_query_payload)

    # 美团放款申请payload
    def mt_loan_msg(self, **kwargs):
        loan_data = self.data
        strings = str(int(round(time.time() * 1000)))
        loan_data['tradestamp'] = time.strftime('%Y%m%d%H%M%S')
        loan_data['reqsn'] = strings + "1001"
        loan_data['app_no'] = strings + '1002'
        loan_data['loanNo'] = strings + "1003"
        loan_data["contractno"] = self.BANK_CONTRACT_NO
        loan_data['TRADE_AMOUNT'] = self.loan_amount
        loan_data["TRADE_PERIOD"] = 3  # 默认3期
        loan_data["CREDIT_LIMIT"] = 30000  # 单位元
        loan_data["AVAILABLE_LIMIT"] = 30000  # 单位元
        loan_data["USED_LIMIT"] = 0
        payload = {
            "head": {
                "merchantId": "F21C01MEIT",
                "channelNo": "01",
                "requestSerialNo": 'ZYSN' + loan_data['reqsn'],
                "requestTime": loan_data['tradestamp'],
                "tenantId": "000"
            },
            "body": {
                "APP_NO": 'appNo' + loan_data['reqsn'],  # self.app_no,
                "LOAN_NO": 'loanNo' + loan_data['loanNo'],
                "APP_ID": "MT",
                "CARD_NO": loan_data["bankid"],
                "NAME": loan_data['name'],
                # "NAME": "陈祺",
                "CAREER_TYPE": "",
                "ID_TYPE": "01",
                "ID_NO": loan_data["cer_no"],
                "CERT_VALID_START_DATE": "20151212",
                "CERT_VALID_END_DATE": "20251212",
                "CARD_BIND_PHONENUMBER": loan_data["telephone"],
                "CUSTOMER_NO": "CUSTOMER_NO" + loan_data["cer_no"],
                "CONTRACT_NO": loan_data["contractno"],
                "TRADE_TIME": loan_data["tradestamp"],
                "TRADE_AMOUNT": loan_data['TRADE_AMOUNT'],
                "TRADE_PERIOD": loan_data['TRADE_PERIOD'],
                "TENANT_NO": "DL-GDXT",
                "TENANT_NAME": "DL-GDXT",
                "STATEMENT_DATE": 20210408,
                "REPAYMENT_DATE": 20210408,
                "CONNECT_NAME_1": "夔琦萍",
                "CONNECT_PHONENUMBER_1": "16100000446",
                "CONNECT_RELATION_1": "1",
                "CONNECT_NAME_2": "卜慧巧",
                "CONNECT_PHONENUMBER_2": "14300003500",
                "CONNECT_RELATION_2": "2",
                "PURPOSE": "旅游",
                "CREDIT_LIMIT": loan_data["CREDIT_LIMIT"],
                "AVAILABLE_LIMIT": loan_data["AVAILABLE_LIMIT"],
                "FUNDPARTY": "TLJR-GDXT",
                "USED_LIMIT": loan_data["USED_LIMIT"],
                "REPAYMENT_TYPE": "ACPI",
                "RATE": "0.000980",
                "LIVING_VERIFY_PASS": "Y",
                "LIVING_VERIFY_TIMES": "3",
                "LIVING_VERIFY_FAILED": "1",
                "RISK_INFO": {
                    "platform_consuming_ability_level": "1002",
                    "platform_consuming_frequency_level": "1002",
                    "platform_consuming_scene_number_level": "1002",
                    "predicted_age_level": "1002",
                    "predicted_marital_status_level": "1002",
                    "active_city_number_level_last_90d": "1002",
                    "predicted_gender_level": "1002",
                    "account_register_time_level": "1002",
                    "job_category_code": "1002",
                    "resident_province_name": "1002",
                    "user_order_count_level_in_last_180d": "1002",
                    "user_order_count_level_in_last_360d": "1002",
                    "user_order_count_level_in_last_90d": "1002",
                    "user_order_days_level_in_last_180d": "1002",
                    "user_order_days_level_in_last_360d": "1002",
                    "user_order_days_level_in_last_90d": "1002",
                    "user_successful_order_amount_level_in_last_180d": "1002",
                    "user_successful_order_amount_level_in_last_360d": "1002",
                    "user_successful_order_amount_level_in_last_90d": "1002",
                    "user_successful_order_count_level_in_last_180d": "1002",
                    "user_successful_order_count_level_in_last_360d": "1002",
                    "user_successful_order_count_level_in_last_90d": "1002",
                    "user_successful_waimai_order_count_level_in_last_180d": "1002",
                    "user_successful_waimai_order_count_level_in_last_360d": "1002",
                    "user_successful_waimai_order_count_level_in_last_90d": "1002",
                    "user_visit_bg_count_level_in_last_90d": "1002",
                    "user_active_days_in_last_180d_level": "1002",
                    "user_active_days_in_last_360d_level": "1002",
                    "user_active_days_in_last_90d_level": "1002",
                    "user_visit_waimai_days_in_last_180d": "1002",
                    "user_visit_waimai_days_in_last_360d": "1002",
                    "user_visit_waimai_days_in_last_90d": "1002",
                    "user_active_tag_in_1y": "1002",
                    "user_visit_group_buy_days_in_last_180d": "1002",
                    "user_visit_group_buy_days_in_last_360d": "1002",
                    "user_visit_group_buy_days_in_last_90d": "1002",
                    "mt_creditscore_level_v4_0_1": "1002"
                }
            }
        }
        self.loan_payload = payload
        if kwargs:
            parser = DataUpdate(payload, **kwargs)
            self.loan_payload = parser.parser
        self.set_active_payload(self.loan_payload)

    # 美团放款查询payload
    def mt_loan_query_msg(self, **kwargs):
        loan_data = self.data
        loan_data['nowtime'] = time.strftime('%Y%m%d%H%M%S')
        loan_data['reqsn'] = str(int(round(time.time() * 1000))) + "1001"
        loan_data['app_no'] = self.user_loan_apply_info[0]['thirdpart_apply_id']
        payload = {
            "head": {
                "merchantId": "F21C01MEIT",
                "channelNo": "01",
                "requestSerialNo": 'ZYCX' + loan_data['reqsn'],
                "requestTime": loan_data['nowtime'],
                "tenantId": "000"
            },
            "body": {
                "APP_NO": loan_data['app_no'],
            }
        }
        self.loan_query_payload = payload
        if kwargs:
            parser = DataUpdate(payload, **kwargs)
            self.loan_query_payload = parser.parser
        self.set_active_payload(self.loan_query_payload)

    # 用户额度失效payload
    def mt_credit_invalid_msg(self, **kwargs):
        payload = {
            "productId": "F21C011",  # F20B021
            "certificateNo": self.data['cer_no'],  # '210900198109124838',
            "userName": self.data['name'],  # '郝健翔',
            "reason": "1",
            "remark": "测试操作",
            "limitId": "",
            "voucherUrl": ""
        }
        self.credit_invalid_payload = payload
        if kwargs:
            parser = DataUpdate(payload, **kwargs)
            self.credit_invalid_payload = parser.parser
        self.set_active_payload(self.credit_invalid_payload)

    def mt_repay_notice_msg(self, **kwargs):
        strings = str(int(round(time.time() * 1000)))
        repay_notice = dict()
        repay_notice['requestSerialNo'] = "reqNo" + strings
        repay_notice['CONTRACT_NO'] = "CONTRACT_NO" + strings
        repay_notice['BIZ_SERIAL_NO'] = "BIZ_SERIAL_NO" + strings

        # 根据姓名查询支用信息
        key1 = "user_name = '{}'".format(self.data['name'])
        credit_loan_apply = self.get_credit_data_info(table="credit_loan_apply", key=key1)
        repay_notice['RATE'] = str(int(credit_loan_apply["apply_rate"]) / 36000)
        repay_notice['TRADE_PERIOD'] = credit_loan_apply["apply_term"]

        # 借据号默认为空取当前用户第一笔借据号，否则取赋值借据号
        loan_no = self.loan_no if self.loan_no else credit_loan_apply["third_loan_invoice_id"]

        key2 = "third_loan_no = '{}' and repay_term_no = '{}'".format(loan_no, self.term)
        credit_ctrip_repay_notice_info = self.get_credit_data_info(table="credit_ctrip_repay_notice_info", key=key2)

        key3 = "certificate_no = '{}'".format(self.data['cer_no'])
        credit_personal_limit_detail = self.get_credit_data_info(table="credit_personal_limit_detail", key=key3)
        repay_notice['CREDIT_LIMIT'] = str(int(credit_personal_limit_detail["total_amount"]))
        repay_notice['AVALIABLE_LIMIT'] = str(int(credit_personal_limit_detail["total_amount"]) * 100)
        repay_notice['USED_LIMIT'] = str(int(credit_personal_limit_detail["total_amount"]) * 100 - int(
            credit_personal_limit_detail["total_amount"]) * 100)

        repay_notice['LOAN_NO'] = loan_no
        repay_notice['REPAYMENT_AMOUNT'] = str(int(credit_ctrip_repay_notice_info["actual_repay_amount"]) * 100)
        repay_notice['PRINCIPAL'] = str(int(credit_ctrip_repay_notice_info["repay_principal"]) * 100)
        repay_notice['INTEREST'] = str(int(credit_ctrip_repay_notice_info["repay_interest"]) * 100)
        repay_notice['D_INTEREST'] = str(int(credit_ctrip_repay_notice_info["repay_penalty_amount"]) * 100)
        repay_notice['REPAY_TYPE'] = int(credit_ctrip_repay_notice_info["repay_type"])
        repay_notice['PERIOD_NOW'] = str(credit_ctrip_repay_notice_info["repay_term_no"])
        repay_notice['REPAYMENT_DATE'] = str(credit_ctrip_repay_notice_info["finish_time"])

        repay_notice['REPAYMENT_NAME'] = self.data['name']
        repay_notice['REPAYMENT_CARD'] = self.data['bankid']
        repay_notice['REPAYMENT_TIME'] = str(credit_ctrip_repay_notice_info["finish_time"])

        repay_notice.update(kwargs)

        parser = DataUpdate(self.cfg['repay_notice']['payload'], **repay_notice)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", json.dumps(self.active_payload))
        self.set_active_payload(self.active_payload)

    def mt_loan_notice_msg(self, **kwargs):
        strings = str(int(round(time.time() * 1000)))
        loan_notice = dict()
        loan_notice['requestSerialNo'] = "reqNo" + strings
        loan_notice['CONTRACT_NO'] = "CONTRACT_NO" + strings

        # 根据姓名查询支用信息
        key1 = "user_name = '{}'".format(self.data['name'])
        credit_loan_apply = self.get_credit_data_info(table="credit_loan_apply", key=key1)
        loan_notice['RATE'] = str(int(credit_loan_apply["apply_rate"]) / 36000)
        loan_notice['TRADE_PERIOD'] = str(credit_loan_apply["apply_term"])
        loan_notice['PAYMENT_CONFIRM_TIME'] = str(credit_loan_apply["loan_pay_time"])
        loan_notice['LOAN_AMOUNT'] = str(int(credit_loan_apply["apply_amount"]) * 100)
        loan_notice['REPAYMENT_DATE'] = str(credit_loan_apply["repay_day"])

        # 借据号默认为空取当前用户第一笔借据号，否则取赋值借据号
        loan_no = self.loan_no if self.loan_no else credit_loan_apply["third_loan_invoice_id"]
        loan_notice['LOAN_NO'] = loan_no

        loan_notice.update(kwargs)

        parser = DataUpdate(self.cfg['loan_notice']['payload'], **loan_notice)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", json.dumps(self.active_payload))
        self.set_active_payload(self.active_payload)


if __name__ == '__main__':
    pass
