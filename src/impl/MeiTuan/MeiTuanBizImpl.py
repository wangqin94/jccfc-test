# -*- coding: utf-8 -*-
# ------------------------------------------
# 接口数据封装类
# ------------------------------------------

from config.TestEnvInfo import *
from src.test_data.module_data import MeiTuan
from src.enums.EnumMeiTuan import *
from src.impl.common.CommonUtils import *
from src.enums.EnumsCommon import *


class MeiTuanBizImpl(INIT):
    def __init__(self, *, data=None, loan_no=None, term="1", encrypt_flag=True):
        super().__init__()
        self.log.demsg('当前测试环境 %s', TEST_ENV_INFO)
        # 解析项目特性配置
        self.cfg = MeiTuan.MeiTuan

        self.app_no = 'mt_app_no' + str(int(round(time.time() * 1000))) + "1002"
        self.data = data if data else get_base_data(str(self.env) + ' -> ' + str(ProductEnum.MEITUAN.value),
                                                    app_no=self.app_no)
        self.log.info('用户四要素信息 %s: ', self.data)

        # 初始化定义用户apply信息
        self.user_credit_apply_info = {}
        self.user_credit_file_info = {}
        self.user_loan_apply_info = {}

        # 初始化数据库查询公共类
        self.GetSqlData = GetSqlData()
        # 初始换加密标识
        self.encrypt_flag = encrypt_flag

        # 初始借据号,期次
        self.loan_no = loan_no
        self.term = term

        # 初始化定义部分数据值
        self.encrypt_url = self.host + EnumMeiTuanPath.MeiTuanEncryptPath.value
        self.decrypt_url = self.host + EnumMeiTuanPath.MeiTuanDecryptPath.value
        self.credit_amount = 3000000  # 授信申请额度 单位分
        self.loan_amount = 100000  # 支用申请额度 单位分
        self.rate = 980  # 利息 万分之
        self.credit_amount = 3000000  # 授信申请额度 单位分
        self.loan_amount = 100000  # 支用申请额度 单位分
        self.rate = 980  # 利息 万分之
        self.base_data = data

        # 初始化定义所有接口的payload
        self.active_payload = {}

    @staticmethod
    def url_encoded_to_json(response):
        data = dict()
        data["content"] = response.split('content=')[1].split('&sign=')[0]
        data["sign"] = response.split('&sign=')[1]
        return data

    def set_active_payload(self, payload):
        self.active_payload = payload

    # 获取数据库用户授信信息
    def get_user_credit_apply_info(self, sql=None, table='credit_apply', database=None, times=10, interv=5):
        database = self.credit_database_name if not database else database
        if not sql:
            sql = "SELECT * FROM {} WHERE certificate_no='{}';".format(table, self.data['cer_no'])
        keys = self.mysql_credit.select_table_column(table_name=table, database=database)
        res = []
        for _ in range(times):
            res = self.mysql_credit.select(sql)
            if res:
                break
            wait_time(interv)
        else:
            self.log.error('查询用户授信信息失败')
        info = [dict(zip(keys, item)) for item in res]
        self.user_credit_apply_info = info

    def get_user_file_info(self, sql, table='credit', database=None):
        database = self.credit_database_name if not database else database
        # keys = self.mysql_credit.select_table_column(table_name=table, database=database)
        # sql =
        # values = self.mysql_credit.select(sql)
        pass

    # 获取数据库支用申请用户信息
    def get_user_loan_apply_info(self, certificate_no, database=None):
        database = self.credit_database_name if not database else database
        sql = "select * from {}.credit_loan_apply where certificate_no='{}';".format(database, certificate_no)
        keys = self.mysql_credit.select_table_column(table_name='credit_loan_apply', database=database)
        res = self.mysql_credit.select(sql)
        info = [dict(zip(keys, item)) for item in res]
        self.user_loan_apply_info = info

    def init_msg(self):
        self.data = self.base_data

    # 授信申请payload
    def credit(self, **kwargs):
        credit_data = dict()
        strings = str(int(round(time.time() * 1000)))
        credit_data['requestTime'] = time.strftime('%Y%m%d%H%M%S')
        credit_data['requestSerialNo'] = "SerialNo" + strings + "1001"
        credit_data['APP_NO'] = self.app_no
        credit_data['APPLY_AMT'] = self.credit_amount  # 授信申请贷款金额, 默认3000000分
        credit_data['CUSTOMER_NO'] = 'customer_no' + strings + "1002"
        credit_data['CER_NO'] = self.data['cer_no']
        credit_data['NAME'] = self.data['name']
        credit_data['MOBILE_NO'] = self.data['telephone']
        credit_data['CARD_NO'] = self.data['bankid']
        credit_data['PLATFORM_RATE'] = self.rate
        credit_data['PLATFORM_PENALTY_RATE'] = self.rate
        credit_data['ID_NO_OCR'] = self.data['cer_no']
        credit_data['ID_NAME_OCR'] = self.data['name']

        # 更新 payload 字段值
        credit_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit']['payload'], **credit_data)
        self.active_payload = parser.parser

        # 校验用户是否在系统中已存在
        self.check_user_available(self.data)

        self.log.demsg('授信申请...')
        url = self.host + self.cfg['credit']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        response['app_no'] = self.app_no
        return response

    # 美团授信查询payload
    def credit_query(self, app_no=None, **kwargs):
        credit_query_data = dict()
        strings = str(int(round(time.time() * 1000)))
        credit_query_data['requestSerialNo'] = 'SerialNo' + strings + "1001"
        credit_query_data['requestTime'] = time.strftime('%Y%m%d%H%M%S')
        app_no = app_no if app_no else self.data['app_no']
        credit_query_data['APP_NO'] = app_no

        # 更新 payload 字段值
        credit_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit_query']['payload'], **credit_query_data)
        self.active_payload = parser.parser

        self.log.demsg('美团授信查询...')
        url = self.host + self.cfg['credit_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 美团放款申请payload
    def loan(self, app_no=None, **kwargs):
        loan_data = dict()
        strings = str(int(round(time.time() * 1000)))
        loan_data['requestTime'] = time.strftime('%Y%m%d%H%M%S')
        loan_data['requestSerialNo'] = "SerialNo" + strings + "1001"
        loan_data['LOAN_NO'] = 'loan_no' + strings + '1002'
        loan_data['ID_NO'] = self.data['cer_no']
        loan_data['NAME'] = self.data['name']
        loan_data['CARD_NO'] = self.data['bankid']
        loan_data['CARD_BIND_PHONENUMBER'] = self.data['telephone']
        loan_data['CONTRACT_NO'] = 'CONTRACT_NO' + strings + "1002"
        loan_data["TRADE_TIME"] = time.strftime('%Y%m%d%H%M%S')
        loan_data['TRADE_AMOUNT'] = self.loan_amount
        loan_data["TRADE_PERIOD"] = 3  # 默认3期
        loan_data["CREDIT_LIMIT"] = 30000  # 单位元
        loan_data["AVAILABLE_LIMIT"] = 30000  # 单位元
        loan_data["USED_LIMIT"] = 0

        app_no = app_no if app_no else self.data['app_no']
        content = self.GetSqlData.get_credit_apply_info(thirdpart_apply_id=app_no)
        loan_data['APP_NO'] = app_no
        loan_data['CUSTOMER_NO'] = content['thirdpart_user_id']

        # 更新 payload 字段值
        loan_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan']['payload'], **loan_data)
        self.active_payload = parser.parser

        self.log.demsg('美团放款申请...')
        url = self.host + self.cfg['loan']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 美团放款查询payload
    def loan_query(self, app_no=None, **kwargs):
        loan_query_data = dict()
        strings = str(int(round(time.time() * 1000)))
        loan_query_data['requestSerialNo'] = 'SerialNo' + strings + "1001"
        loan_query_data['requestTime'] = time.strftime('%Y%m%d%H%M%S')
        app_no = app_no if app_no else self.data['app_no']
        loan_query_data['APP_NO'] = app_no

        # 更新 payload 字段值
        loan_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan_query']['payload'], **loan_query_data)
        self.active_payload = parser.parser

        self.log.demsg('美团支用查询...')
        url = self.host + self.cfg['loan_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def repay_notice(self, **kwargs):
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

        self.log.demsg('美团还款通知...')
        url = self.host + self.cfg['repay_notice']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def loan_notice(self, **kwargs):
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

        self.log.demsg('美团放款通知...')
        url = self.host + self.cfg['loan_notice']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response


if __name__ == '__main__':
    pass
