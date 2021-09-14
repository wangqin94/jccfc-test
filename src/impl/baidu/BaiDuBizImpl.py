# -*- coding: utf-8 -*-
# ------------------------------------------
# 百度接口数据封装类
# ------------------------------------------
from src.impl.common.CommonUtils import post_with_encrypt
from utils.Models import *
from engine.Base import INIT
from src.enums.EnumsCommon import *
from src.test_data.moduleData import BaiDu


class BaiDuBizImpl(INIT):
    def __init__(self, *, data=None, type=1, loan_no=None, encrypt_flag=False):
        super().__init__()

        # 解析项目特性配置
        self.cfg = BaiDu.BaiDu

        self.data = data if data else get_base_data(str(self.env) + ' -> ' + str(ProductEnum.BAIDU.value))
        self.log.info('用户四要素信息 \n%s', self.data)

        self.credit_amount = 3000000  # 授信申请金额, 默认3000000  单位分
        self.loan_amount = 1000000  # 支用申请金额, 默认1000000  单位分
        self.period = 3  # 借款期数, 默认3期
        self.loan_no = loan_no
        self.type = type
        self.encrypt_flag = encrypt_flag

        # 初始化payload变量
        self.credit_payload = {}
        self.loan_payload = {}
        self.active_payload = {}

    def set_active_payload(self, payload):
        self.active_payload = payload

    # 授信申请
    def credit(self, **kwargs):
        strings = str(int(round(time.time() * 1000)))
        credit_data = dict()
        credit_data['prcid'] = self.data['cer_no']
        credit_data['bankcard'] = self.data['bankid']
        credit_data['name'] = self.data['name']
        credit_data['phonenumber'] = self.data['telephone']

        credit_data['timestamp'] = time.strftime('%Y%m%d%H%M%S')
        credit_data['reqSn'] = 'Apply_Id' + strings + "1001"
        credit_data['sessionId'] = 'Apply_sid' + strings + "1002"
        credit_data['transactionId'] = 'Apply_tid' + strings + "1003"
        credit_data['initialAmount'] = self.credit_amount  # 授信申请金额, 默认3000000分

        # 更新 payload 字段值
        credit_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit']['payload'], **credit_data)
        self.active_payload = parser.parser

        # 校验用户是否已存在
        self.check_user_available(self.data)

        self.log.demsg('开始授信申请...')
        url = self.host + self.cfg['credit']['interface']
        response = post_with_encrypt(url, self.active_payload, encrypt_flag=self.encrypt_flag)
        response['applyId'] = credit_data['reqSn']
        return response

    # 支用申请
    def loan(self, **kwargs):
        """ # 支用申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        strings = str(int(round(time.time() * 1000)))
        loan_data = dict()
        loan_data['prcid'] = self.data['cer_no']
        loan_data['bankcard'] = self.data['bankid']
        loan_data['name'] = self.data['name']
        loan_data['phonenumber'] = self.data['telephone']

        loan_data['timestamp'] = time.strftime('%Y%m%d%H%M%S')
        loan_data['reqSn'] = 'Loan_req' + strings + "1001"
        loan_data['sessionId'] = 'Loan_sid' + strings + "1002"
        loan_data['transactionId'] = 'Loan_tid' + strings + "1003"
        loan_data['cashAmount'] = self.loan_amount  # 支用申请金额, 默认1000000分
        loan_data['orderId'] = 'orderId' + strings
        loan_data['term'] = self.period

        loan_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan']['payload'], **loan_data)
        self.active_payload = parser.parser

        self.log.demsg('开始支用申请...')
        url = self.host + self.cfg['loan']['interface']
        response = post_with_encrypt(url, self.active_payload, encrypt_flag=self.encrypt_flag)
        response['orderId'] = loan_data['orderId']
        return response

    # 还款通知申请
    def notice(self, **kwargs):
        """ # 还款通知payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        strings = str(int(round(time.time() * 1000)))
        notice_data = dict()
        comment = dict()
        notice_data['order_id'] = "order_id" + strings
        notice_data['seq_no'] = "seq_no" + strings
        notice_data['cur_date'] = time.strftime("%Y%m%d", time.localtime())
        notice_data['tran_time'] = time.strftime("%Y%m%d%H%M%S", time.localtime())
        notice_data['type'] = int(self.type)

        # 根据姓名查询支用信息
        key1 = "user_name = '{}'".format(self.data['name'])
        credit_loan_apply = self.get_credit_data_info(table="credit_loan_apply", key=key1)

        # 借据号默认为空取当前用户第一笔借据号，否则取赋值借据号
        loan_no = self.loan_no if self.loan_no else credit_loan_apply["third_loan_invoice_id"]
        credit_loan_apply = self.get_credit_data_info(table="credit_loan_apply", key=key1)
        notice_data['loan_id'] = loan_no
        comment['amount_total'] = str(int(credit_loan_apply["apply_amount"]) * 100)
        comment['loan_order_id'] = str(credit_loan_apply["thirdpart_order_id"])
        notice_data["comment"] = str(comment)

        notice_data.update(kwargs)
        parser = DataUpdate(self.cfg['notice']['payload'], **notice_data)
        self.active_payload = parser.parser

        self.log.demsg('开始通知申请...')
        url = self.host + self.cfg['notice']['interface']
        response = post_with_encrypt(url, self.active_payload, encrypt_flag=self.encrypt_flag)
        return response
