# -*- coding: utf-8 -*-
# ------------------------------------------
# 百度接口数据封装类
# ------------------------------------------
import hashlib

from config.TestEnvInfo import TEST_ENV_INFO
from src.impl.common.CommonUtils import post_with_encrypt
from utils.Models import *
from engine.Base import INIT
from src.enums.EnumsCommon import *
from src.test_data.module_data import zhixin


def computeMD5(message):
    m = hashlib.md5()
    m.update(message.encode(encoding='utf-8'))
    return m.hexdigest()


class ZhiXinBizImpl(INIT):
    def __init__(self, data=None, encrypt_flag=True):
        super().__init__()
        self.log.demsg('当前测试环境 %s', TEST_ENV_INFO)

        # 解析项目特性配置
        self.cfg = zhixin.zhixin

        self.data = data if data else get_base_data(str(self.env) + ' -> ' + str(ProductEnum.ZHIXIN.value))
        self.log.info('用户四要素信息 \n%s', self.data)

        self.loan_amount = 1000000  # 支用申请金额, 默认1000000  单位分
        self.period = 3  # 借款期数, 默认3期
        self.encrypt_flag = encrypt_flag
        self.strings = str(int(round(time.time() * 1000)))
        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 当前时间
        self.times = str(int(round(time.time() * 1000)))  # 当前13位时间戳

        # 初始化payload变量
        self.active_payload = {}

        self.encrypt_url = self.host + self.cfg['encrypt']['interface']
        self.decrypt_url = self.host + self.cfg['decrypt']['interface']

    # 客户撞库校验
    def checkUser(self, iphone, **kwargs):
        checkUser_data = dict()
        # body
        checkUser_data['requestNo'] = 'requestNo' + self.strings + "_1541"
        checkUser_data['requestTime'] = self.times
        checkUser_data['md5'] = computeMD5(iphone)
        checkUser_data['ct'] = self.times

        # 更新 payload 字段值
        checkUser_data.update(kwargs)
        parser = DataUpdate(self.cfg['checkUser']['payload'], **checkUser_data)
        self.active_payload = parser.parser

        self.log.demsg('发起客户撞库校验...')
        url = self.host + self.cfg['checkUser']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 发起绑卡申请payload
    def applyCertification(self, **kwargs):
        applyCertification_data = dict()
        # body
        applyCertification_data['requestNo'] = 'requestNo' + self.strings + "_1000"
        applyCertification_data['requestTime'] = self.times

        applyCertification_data['userId'] = 'userId' + self.strings
        applyCertification_data['certificationApplyNo'] = 'ZHIXIN' + self.strings
        applyCertification_data['idCardNo'] = self.data['cer_no']
        applyCertification_data['userName'] = self.data['name']
        applyCertification_data['bankCardNo'] = self.data['bankid']
        applyCertification_data['userMobile'] = self.data['telephone']
        applyCertification_data['agreementTime'] = self.date
        applyCertification_data['ct'] = self.times

        # 更新 payload 字段值
        applyCertification_data.update(kwargs)
        parser = DataUpdate(self.cfg['applyCertification']['payload'], **applyCertification_data)
        self.active_payload = parser.parser

        self.log.demsg('发起绑卡请求...')
        url = self.host + self.cfg['applyCertification']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 确认绑卡申请payload
    def verifyCode(self, **kwargs):
        verifyCode_data = dict()
        # body
        verifyCode_data['requestNo'] = 'requestNo' + self.strings + "_2000"
        verifyCode_data['requestTime'] = self.times
        verifyCode_data['ct'] = self.times

        # 更新 payload 字段值
        verifyCode_data.update(kwargs)
        parser = DataUpdate(self.cfg['verifyCode']['payload'], **verifyCode_data)
        self.active_payload = parser.parser

        self.log.demsg('确认绑卡请求...')
        url = self.host + self.cfg['verifyCode']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 授信申请
    def credit(self, **kwargs):
        credit_data = dict()
        # body
        credit_data['requestNo'] = 'requestNo' + self.strings + "_3000"
        credit_data['requestTime'] = self.times
        credit_data['userId'] = 'userId' + self.strings
        credit_data['creditApplyNo'] = 'creditApplyNo' + self.strings
        credit_data['applyTime'] = self.date
        credit_data['agreementTime'] = self.date

        # 设备信息
        credit_data['factoryTime'] = self.times

        # 用户信息
        credit_data['idCardNo'] = self.data['cer_no']
        credit_data['name'] = self.data['name']
        credit_data['mobile'] = self.data['telephone']

        # ocr信息
        credit_data['nameOCR'] = self.data['name']
        credit_data['idCardNoOCR'] = self.data['cer_no']
        positive = get_base64_from_img(os.path.join(project_dir(), r'src\\test_data\\testFile\\idCardFile\\cqid1.png'))
        credit_data['positive'] = positive  # 身份证正面base64字符串
        negative = get_base64_from_img(os.path.join(project_dir(), r'src\\test_data\\testFile\\idCardFile\\cqid2.png'))
        credit_data['negative'] = negative  # 身份证反面base64字符串

        # 活体图信息
        credit_data['assayTime'] = self.date
        best = get_base64_from_img(os.path.join(project_dir(), r'src\\test_data\\testFile\\idCardFile\\cqface.png'))
        credit_data['best'] = best  # 人脸base64字符串
        action1 = get_base64_from_img(os.path.join(project_dir(), r'src\\test_data\\testFile\\idCardFile\\action1.jpg'))
        # credit_data['action1'] = action1  # 身份证反面base64字符串
        action2 = get_base64_from_img(os.path.join(project_dir(), r'src\\test_data\\testFile\\idCardFile\\action2.jpg'))
        # credit_data['action2'] = action2  # 身份证反面base64字符串
        action3 = get_base64_from_img(os.path.join(project_dir(), r'src\\test_data\\testFile\\idCardFile\\action3.jpg'))
        # credit_data['action3'] = action3  # 身份证反面base64字符串

        # 银行卡信息
        credit_data['idCardNo'] = self.data['cer_no']
        credit_data['userMobile'] = self.data['telephone']
        credit_data['userName'] = self.data['name']
        credit_data['bankCardNo'] = self.data['bankid']

        credit_data['ct'] = self.times

        # 更新 payload 字段值
        credit_data.update(kwargs)
        parser = DataUpdate(self.cfg['applyCredit']['payload'], **credit_data)
        self.active_payload = parser.parser

        # 校验用户是否已存在
        self.check_user_available(self.data)

        self.log.demsg('开始授信申请...')
        url = self.host + self.cfg['applyCredit']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 授信查询payload
    def queryCreditResult(self, **kwargs):
        queryCreditResult_data = dict()
        # body
        queryCreditResult_data['requestNo'] = 'requestNo' + self.strings + "_4000"
        queryCreditResult_data['requestTime'] = self.times
        queryCreditResult_data['ct'] = self.times

        # 更新 payload 字段值
        queryCreditResult_data.update(kwargs)
        parser = DataUpdate(self.cfg['queryCreditResult']['payload'], **queryCreditResult_data)
        self.active_payload = parser.parser

        self.log.demsg('确认绑卡请求...')
        url = self.host + self.cfg['queryCreditResult']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
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
        # notice_data['order_id'] = "order_id" + strings
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
        notice_data['order_id'] = loan_no
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
