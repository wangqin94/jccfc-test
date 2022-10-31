# -*- coding: utf-8 -*-
# ------------------------------------------
# 百度接口数据封装类
# ------------------------------------------
from src.impl.common.CommonBizImpl import post_with_encrypt_baidu
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils.Apollo import Apollo
from utils.Models import *
from engine.EnvInit import EnvInit
from src.enums.EnumsCommon import *
from src.enums.EnumBaiDu import *
from src.test_data.module_data import BaiDu
from config.globalConfig import *


class BaiDuBizImpl(EnvInit):
    def __init__(self, data=None, type=1, repay_mode='02', loan_no=None, encrypt_flag=False):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()
        # 解析项目特性配置
        self.cfg = BaiDu.BaiDu
        self.data = data if data else get_base_data(str(self.env) + ' -> ' + str(ProductEnum.BAIDU.value))
        self.credit_amount = 3000000  # 授信申请金额, 默认3000000  单位分
        self.loan_amount = 1000000  # 支用申请金额, 默认1000000  单位分
        self.period = 3  # 借款期数, 默认3期
        self.loan_no = loan_no
        self.type = type
        self.repay_mode = repay_mode  # repay_mode='02'随借随还，repay_mode='05'等额本息
        self.encrypt_flag = encrypt_flag

        self.encrypt_url = self.host + EnumBaiDuPath.BaiDuEncryptPath.value
        self.decrypt_url = self.host + EnumBaiDuPath.BaiDuDecryptPath.value

        # 初始化payload变量
        self.credit_payload = {}
        self.loan_payload = {}
        self.active_payload = {}

    def set_active_payload(self, payload):
        self.active_payload = payload

    # 结清证明
    def settlement(self, **kwargs):
        settlement_data = dict()
        strings = str(int(round(time.time() * 1000)))
        settlement_data['requestTime'] = time.strftime('%Y%m%d%H%M%S')
        settlement_data['requestSerialNo'] = "SerialNo" + strings + "1001"
        # 更新 payload 字段值
        settlement_data['reqsn'] = time.strftime('%Y%m%d%H%M%S')
        settlement_data.update(kwargs)
        parser = DataUpdate(self.cfg['settlement']['payload'], **settlement_data)
        self.active_payload = parser.parser

        self.log.demsg('开始支用申请...')
        url = self.host + self.cfg['settlement']['interface']
        response = post_with_encrypt_baidu(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                           encrypt_flag=True)
        # response = post_with_encrypt(url, self.active_payload, encrypt_flag=self.encrypt_flag)
        response['orderId'] = settlement_data['orderId']
        return response

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

        # 配置风控mock返回建议额度与授信额度一致
        apollo_data = dict()
        apollo_data['hj.channel.risk.credit.line.amt.mock'] = self.active_payload['message']['expanding']['initialAmount']
        Apollo().update_config(appId='loan2.1-jcxf-credit', **apollo_data)

        # 校验用户是否已存在
        self.MysqlBizImpl.check_user_available(self.data)

        self.log.demsg('开始授信申请...')
        url = self.host + self.cfg['credit']['interface']
        response = post_with_encrypt_baidu(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                           encrypt_flag=True)
        # response = post_with_encrypt(url, self.active_payload, encrypt_flag=self.encrypt_flag)
        response['credit_apply_id'] = credit_data['reqSn']
        return response

    # 授信查询
    def credit_query(self, credit_apply_id, **kwargs):
        strings = str(int(round(time.time() * 1000)))
        credit_query_data = dict()
        credit_query_data['prcid'] = self.data['cer_no']
        credit_query_data['bankcard'] = self.data['bankid']
        credit_query_data['name'] = self.data['name']
        credit_query_data['phonenumber'] = self.data['telephone']

        credit_query_data['timestamp'] = time.strftime('%Y%m%d%H%M%S')
        credit_query_data['reqSn'] = 'reqSn' + strings + "1001"
        credit_query_data['sessionId'] = 'sid' + strings + "1002"
        credit_query_data['transactionId'] = 'tid' + strings + "1003"
        credit_query_data['expanding'] = {'reqSn': credit_apply_id}

        # 更新 payload 字段值
        credit_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit_query']['payload'], **credit_query_data)
        self.active_payload = parser.parser

        self.log.demsg('开始授信查询...')
        url = self.host + self.cfg['credit_query']['interface']
        response = post_with_encrypt_baidu(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                           encrypt_flag=True)
        # response = post_with_encrypt(url, self.active_payload, encrypt_flag=self.encrypt_flag)
        return response

    # 支用申请
    def loan(self, **kwargs):
        """ # 支用申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json response 接口响应参数 数据类型：json
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
        # 随借随还
        if self.repay_mode == '02':
            loan_data['repayMode'] = '22'
            loan_data['dailyInterestRate'] = '6.5'
            loan_data['compreAnnualInterestRate'] = '2340'
        # 等额本息
        elif self.repay_mode == '05':
            loan_data['repayMode'] = '32'
            loan_data['dailyInterestRate'] = '6.2'
            loan_data['compreAnnualInterestRate'] = '2232'
        loan_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan']['payload'], **loan_data)
        self.active_payload = parser.parser

        self.log.demsg('开始支用申请...')
        url = self.host + self.cfg['loan']['interface']
        response = post_with_encrypt_baidu(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                           encrypt_flag=True)
        # response = post_with_encrypt(url, self.active_payload, encrypt_flag=self.encrypt_flag)
        response['loan_apply_id'] = loan_data['reqSn']
        return response

    # 支用查询
    def loan_query(self, loan_apply_id, **kwargs):
        strings = str(int(round(time.time() * 1000)))
        loan_query_data = dict()
        loan_query_data['prcid'] = self.data['cer_no']
        loan_query_data['bankcard'] = self.data['bankid']
        loan_query_data['name'] = self.data['name']
        loan_query_data['phonenumber'] = self.data['telephone']

        loan_query_data['timestamp'] = time.strftime('%Y%m%d%H%M%S')
        loan_query_data['reqSn'] = 'reqSn' + strings + "1001"
        loan_query_data['sessionId'] = 'sid' + strings + "1002"
        loan_query_data['transactionId'] = 'tid' + strings + "1003"
        loan_query_data['expanding'] = {'reqSn': loan_apply_id}

        # 更新 payload 字段值
        loan_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit_query']['payload'], **loan_query_data)
        self.active_payload = parser.parser

        self.log.demsg('开始支用查询...')
        url = self.host + self.cfg['loan_query']['interface']
        response = post_with_encrypt_baidu(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                           encrypt_flag=True)
        # response = post_with_encrypt(url, self.active_payload, encrypt_flag=self.encrypt_flag)
        return response

    # 还款通知申请
    def notice(self, **kwargs):
        """ # 还款通知payload字段装填
        注意：键名必须与接口原始数据的键名一致
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000)))
        notice_data = dict()
        comment = dict()
        # notice_data['order_id'] = "order_id" + strings
        notice_data['seq_no'] = "seq_no" + strings
        notice_data['cur_date'] = time.strftime("%Y%m%d", time.localtime())
        notice_data['tran_time'] = time.strftime("%Y%m%d%H%M%S", time.localtime())
        notice_data['type'] = int(self.type)

        # 根据姓名查询支用信息
        key1 = "user_name = '{}'".format(self.data['name'])
        credit_loan_apply = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_apply", key=key1)

        # 借据号默认为空取当前用户第一笔借据号，否则取赋值借据号
        loan_no = self.loan_no if self.loan_no else credit_loan_apply["third_loan_invoice_id"]
        credit_loan_apply = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_apply", key=key1)
        notice_data['loan_id'] = loan_no
        notice_data['order_id'] = loan_no
        comment['amount_total'] = str(int(credit_loan_apply["apply_amount"]) * 100)
        comment['loan_order_id'] = str(credit_loan_apply["thirdpart_order_id"])
        notice_data["comment"] = str(comment)

        notice_data.update(kwargs)
        parser = DataUpdate(self.cfg['notice']['payload'], **notice_data)
        self.active_payload = parser.parser

        self.log.demsg('开始通知申请...')
        url = self.host + self.cfg['notice']['interface']
        response = post_with_encrypt_baidu(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                           encrypt_flag=True)
        # response = post_with_encrypt(url, self.active_payload, encrypt_flag=self.encrypt_flag)
        return response

    # 文件加密
    def file_encrypt(self, date):
        """
        百度文件加密
        :param date: 要加密文件路径的日期
        :return: 加密文件
        """
        file_data = dict()
        # 金山云存放文件路径
        file_data['file'] = 'hj/baidu/file/' + date
        url = self.host + EnumBaiDuPath.BaiDuFileEncryptPath.value
        file_data = json.dumps(file_data)
        response = requests.post(url=url, headers=headers, json=file_data)
        return response


if __name__ == '__main__':
    baidu = BaiDuBizImpl()
