# -*- coding: utf-8 -*-
# ------------------------------------------
# 应急支付接口数据封装类
# ------------------------------------------
import hashlib
import time

from ComLib.Models import *
from Engine.Base import INIT
from Config.TestEnvInfo import *


def encrypt_md5(data):
    # 创建md5对象
    hl = hashlib.md5()
    # 此处必须声明encode
    # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    hl.update(data.encode(encoding='utf-8'))
    # print("加密响应报文如下：{}".format(hl.hexdigest()))
    return hl.hexdigest()


class PayloadGenerator(INIT):
    def __init__(self, *, data=None, payment_type="5"):
        super().__init__()
        self.data = data if data else get_base_data(str(self.env) + ' -> ' + str(self.project))
        self.log.info('用户四要素信息 \n%s', self.data)

        self.strings = str(int(round(time.time() * 1000)))
        self.times = time.strftime('%Y-%m-%d', time.localtime())
        self.jcSystemCode = 'loan-web'
        self.paymentType = payment_type

        # 初始化payload变量
        self.active_payload = {}

        # 初始数据库变量
        self.credit_database_name = '%s_credit' % TEST_ENV_INFO.lower()
        self.asset_database_name = '%s_asset' % TEST_ENV_INFO.lower()

    def set_active_payload(self, payload):
        self.active_payload = payload

    # 应急支付渠道查询payload
    def query_channel_msg(self, **kwargs):
        """ # 应急支付渠道查询payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        data = dict()
        # head
        requestSerialNo = 'SerialNo' + self.strings + "1"
        data['requestSerialNo'] = requestSerialNo
        data['jcSystemCode'] = self.jcSystemCode
        data['jcSystemEncry'] = encrypt_md5(requestSerialNo + self.jcSystemCode)

        data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['queryChannel']['payload'], **data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 批量查询客户借据信息payload
    def query_invoice_list_msg(self, **kwargs):
        """ # 批量查询客户借据信息payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        data = dict()
        # header
        requestSerialNo = 'SerialNo' + self.strings + "2"
        data['requestSerialNo'] = requestSerialNo
        data['jcSystemCode'] = self.jcSystemCode
        data['jcSystemEncry'] = encrypt_md5(requestSerialNo + self.jcSystemCode)

        data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['queryInvoiceListByPage']['payload'], **data)
        self.active_payload = parser.parser
        self.active_payload["head"]["channelNo"] = "21"
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 我的账单查询payload
    def loan_bill_msg(self, **kwargs):
        """ # 我的账单查询payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        data = dict()
        # head
        requestSerialNo = 'SerialNo' + self.strings + "2"
        data['requestSerialNo'] = requestSerialNo
        data['jcSystemCode'] = self.jcSystemCode
        data['jcSystemEncry'] = encrypt_md5(requestSerialNo + self.jcSystemCode)

        # 更新 payload 字段值
        data.update(kwargs)
        parser = DataUpdate(self.cfg['loan_bill']['payload'], **data)
        self.active_payload = parser.parser
        self.active_payload["head"]["channelNo"] = "21"
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 支付记录查询payload
    def payment_query_msg(self, **kwargs):
        """ # 支付记录查询payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        data = dict()
        # head
        requestSerialNo = 'SerialNo' + self.strings + "2"
        data['requestSerialNo'] = requestSerialNo
        data['jcSystemCode'] = self.jcSystemCode
        data['jcSystemEncry'] = encrypt_md5(requestSerialNo + self.jcSystemCode)

        # 更新 payload 字段值
        data.update(kwargs)
        parser = DataUpdate(self.cfg['payment_query']['payload'], **data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 贷款列表查询payload
    def loan_query_msg(self, **kwargs):
        """ # 贷款列表查询payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        data = dict()
        # head
        requestSerialNo = 'SerialNo' + self.strings + "2"
        data['requestSerialNo'] = requestSerialNo
        data['jcSystemCode'] = self.jcSystemCode
        data['jcSystemEncry'] = encrypt_md5(requestSerialNo + self.jcSystemCode)

        # 更新 payload 字段值
        data.update(kwargs)
        parser = DataUpdate(self.cfg['loan_query']['payload'], **data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 贷款详情查询payload
    def loan_details_msg(self, **kwargs):
        """ # 贷款详情查询payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        data = dict()
        # head
        requestSerialNo = 'SerialNo' + self.strings + "2"
        data['requestSerialNo'] = requestSerialNo
        data['jcSystemCode'] = self.jcSystemCode
        data['jcSystemEncry'] = encrypt_md5(requestSerialNo + self.jcSystemCode)

        # 更新 payload 字段值
        data.update(kwargs)
        parser = DataUpdate(self.cfg['loan_details']['payload'], **data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 还款记录查询payload
    def repay_query_msg(self, **kwargs):
        """ # 还款记录查询payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        data = dict()
        # head
        requestSerialNo = 'SerialNo' + self.strings + "2"
        data['requestSerialNo'] = requestSerialNo
        data['jcSystemCode'] = self.jcSystemCode
        data['jcSystemEncry'] = encrypt_md5(requestSerialNo + self.jcSystemCode)

        # 更新 payload 字段值
        data.update(kwargs)
        parser = DataUpdate(self.cfg['repay_query']['payload'], **data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 待还款计划查询payload
    def plan_query_msg(self, **kwargs):
        """ # 待还款计划查询payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        data = dict()
        # head
        requestSerialNo = 'SerialNo' + self.strings + "2"
        data['requestSerialNo'] = requestSerialNo
        data['jcSystemCode'] = self.jcSystemCode
        data['jcSystemEncry'] = encrypt_md5(requestSerialNo + self.jcSystemCode)

        # 更新 payload 字段值
        data.update(kwargs)
        parser = DataUpdate(self.cfg['plan_query']['payload'], **data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 查询订单支付结果payload
    def payment_result_msg(self, **kwargs):
        """ # 查询订单支付结果payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        data = dict()
        # head
        requestSerialNo = 'SerialNo' + self.strings + "2"
        data['requestSerialNo'] = requestSerialNo
        data['jcSystemCode'] = self.jcSystemCode
        data['jcSystemEncry'] = encrypt_md5(requestSerialNo + self.jcSystemCode)

        # 更新 payload 字段值
        data.update(kwargs)
        parser = DataUpdate(self.cfg['payment_result']['payload'], **data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 绑定银行卡payload
    def bankcard_bind_msg(self, **kwargs):
        """ # 绑定银行卡payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        data = dict()
        # head
        requestSerialNo = 'SerialNo' + self.strings + "2"
        data['requestSerialNo'] = requestSerialNo
        data['jcSystemCode'] = self.jcSystemCode
        data['jcSystemEncry'] = encrypt_md5(requestSerialNo + self.jcSystemCode)

        # 更新 payload 字段值
        data.update(kwargs)
        parser = DataUpdate(self.cfg['bankcard_bind']['payload'], **data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 更换银行卡payload
    def bankcard_modify_msg(self, **kwargs):
        """ # 更换银行卡payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        data = dict()
        # head
        requestSerialNo = 'SerialNo' + self.strings + "2"
        data['requestSerialNo'] = requestSerialNo
        data['jcSystemCode'] = self.jcSystemCode
        data['jcSystemEncry'] = encrypt_md5(requestSerialNo + self.jcSystemCode)

        # 更新 payload 字段值
        data.update(kwargs)
        parser = DataUpdate(self.cfg['bankcard_modify']['payload'], **data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 还款申请payload
    def payment_msg(self, **kwargs):
        """ # 还款申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        data = dict()
        # head
        requestSerialNo = 'SerialNo' + self.strings + "2"
        data['requestSerialNo'] = requestSerialNo
        data['jcSystemCode'] = self.jcSystemCode
        data['jcSystemEncry'] = encrypt_md5(requestSerialNo + self.jcSystemCode)

        # body
        # 根据用户名称查询借据信息
        key1 = "user_name = '{}'".format(self.data['name'])
        credit_loan_invoice = self.get_credit_data_info(table="credit_loan_invoice", key=key1)
        loan_invoice_id = credit_loan_invoice["loan_invoice_id"]
        data['loanInvoiceId'] = loan_invoice_id
        data['paymentType'] = self.paymentType

        data['appOrderNo'] = 'appOrderNo' + self.strings + "3"
        if self.paymentType == "5":
            data['idNo'] = self.data['cer_no']
            data['bankAcctNo'] = self.data['bankid']
            data['bankAcctName'] = self.data['name']
            data['phoneNum'] = self.data['telephone']

        # 更新 payload 字段值
        data.update(kwargs)
        parser = DataUpdate(self.cfg['payment']['payload'], **data)
        self.active_payload = parser.parser
        self.active_payload["head"]["channelNo"] = "21"
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)


if __name__ == '__main__':
    info = PayloadGenerator()
