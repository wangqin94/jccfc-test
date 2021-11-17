# -*- coding: utf-8 -*-
# ------------------------------------------
# 百度接口数据封装类
# ------------------------------------------
import hashlib

from config.TestEnvInfo import TEST_ENV_INFO
from src.enums.EnumsCommon import *
from src.test_data.module_data import zhixin
from src.impl.common.CommonUtils import *


def computeMD5(message):
    m = hashlib.md5()
    m.update(message.encode(encoding='utf-8'))
    return m.hexdigest()


class ZhiXinBizImpl(INIT):
    def __init__(self, data=None, encrypt_flag=True):
        super().__init__()
        self.log.demsg('当前测试环境 {}'.format(TEST_ENV_INFO))

        # 解析项目特性配置
        self.cfg = zhixin.zhixin

        self.data = data if data else get_base_data(str(self.env) + ' -> ' + str(ProductEnum.ZHIXIN.value), 'userId')
        self.log.info('用户四要素信息 {}'.format(self.data))

        self.loanAmt = 1000  # 支用申请金额, 默认1000 单位元
        self.term = 3  # 借款期数, 默认3期
        self.encrypt_flag = encrypt_flag
        self.strings = str(int(round(time.time() * 1000)))
        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 当前时间
        self.times = str(int(round(time.time() * 1000)))  # 当前13位时间戳

        # 初始化payload变量
        self.active_payload = {}

        self.encrypt_url = self.host + self.cfg['encrypt']['interface']
        self.decrypt_url = self.host + self.cfg['decrypt']['interface']

        self.getSqlData = GetSqlData()

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
        credit_data['userId'] = self.data['userId']
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
        """
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return:
        """
        queryCreditResult_data = dict()
        # body
        queryCreditResult_data['requestNo'] = 'requestNo' + self.strings + "_4000"
        queryCreditResult_data['requestTime'] = self.times
        queryCreditResult_data['ct'] = self.times

        credit_apply_info = self.getSqlData.get_credit_apply_info(thirdpart_user_id=self.data['userId'])
        queryCreditResult_data['userId'] = self.data['userId']
        queryCreditResult_data['creditApplyNo'] = credit_apply_info['credit_apply_id']

        # 更新 payload 字段值
        queryCreditResult_data.update(kwargs)
        parser = DataUpdate(self.cfg['queryCreditResult']['payload'], **queryCreditResult_data)
        self.active_payload = parser.parser

        self.log.demsg('授信查询请求...')
        url = self.host + self.cfg['queryCreditResult']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 借款还算
    def loanTrial(self, **kwargs):
        """ # 借款试算payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        loanTrial_data = dict()
        # body
        loanTrial_data['requestNo'] = 'requestNo' + self.strings + "_5000"
        loanTrial_data['requestTime'] = self.times
        loanTrial_data['ct'] = self.times

        loanTrial_data['loanApplyNo'] = 'loanApplyNo' + self.strings
        loanTrial_data['userId'] = self.data['userId']
        loanTrial_data['loanTime'] = self.date
        credit_apply_info = self.getSqlData.get_credit_apply_info(thirdpart_user_id=self.data['userId'])
        loanTrial_data['partnerCreditNo'] = credit_apply_info['credit_apply_id']
        loanTrial_data['loanAmt'] = self.loanAmt
        loanTrial_data['term'] = self.term

        # 银行卡信息
        loanTrial_data['idCardNo'] = self.data['cer_no']
        loanTrial_data['userMobile'] = self.data['telephone']
        loanTrial_data['userName'] = self.data['name']
        loanTrial_data['bankCardNo'] = self.data['bankid']

        # 更新 payload 字段值
        loanTrial_data.update(kwargs)
        parser = DataUpdate(self.cfg['loanTrial']['payload'], **loanTrial_data)
        self.active_payload = parser.parser

        self.log.demsg('发起借款试算请求...')
        url = self.host + self.cfg['loanTrial']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 支用申请
    def applyLoan(self, **kwargs):
        """ # 支用申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        applyLoan_data = dict()
        # body
        applyLoan_data['requestNo'] = 'requestNo' + self.strings + "_6000"
        applyLoan_data['requestTime'] = self.times
        applyLoan_data['ct'] = self.times

        applyLoan_data['loanApplyNo'] = 'loanApplyNo' + self.strings
        applyLoan_data['userId'] = self.data['userId']
        applyLoan_data['loanTime'] = self.date
        credit_apply_info = self.getSqlData.get_credit_apply_info(thirdpart_user_id=self.data['userId'])
        applyLoan_data['partnerCreditNo'] = credit_apply_info['credit_apply_id']
        applyLoan_data['loanAmt'] = self.loanAmt
        applyLoan_data['term'] = self.term

        # ocr信息
        applyLoan_data['nameOCR'] = self.data['name']
        applyLoan_data['idCardNoOCR'] = self.data['cer_no']
        positive = get_base64_from_img(os.path.join(project_dir(), r'src\\test_data\\testFile\\idCardFile\\cqid1.png'))
        applyLoan_data['positive'] = positive  # 身份证正面base64字符串
        negative = get_base64_from_img(os.path.join(project_dir(), r'src\\test_data\\testFile\\idCardFile\\cqid2.png'))
        applyLoan_data['negative'] = negative  # 身份证反面base64字符串

        # 银行卡信息
        applyLoan_data['idCardNo'] = self.data['cer_no']
        applyLoan_data['userMobile'] = self.data['telephone']
        applyLoan_data['userName'] = self.data['name']
        applyLoan_data['bankCardNo'] = self.data['bankid']

        applyLoan_data['agreementTime'] = self.date

        # 更新 payload 字段值
        applyLoan_data.update(kwargs)
        parser = DataUpdate(self.cfg['applyLoan']['payload'], **applyLoan_data)
        self.active_payload = parser.parser

        self.log.demsg('发起支用请求...')
        url = self.host + self.cfg['applyLoan']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 借款查询payload
    def queryLoanResult(self, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return:
        """
        queryLoanResult_data = dict()
        # body
        queryLoanResult_data['requestNo'] = 'requestNo' + self.strings + "_7000"
        queryLoanResult_data['requestTime'] = self.times
        queryLoanResult_data['ct'] = self.times

        loan_apply_info = self.getSqlData.get_loan_apply_info(thirdpart_user_id=self.data['userId'])
        queryLoanResult_data['userId'] = self.data['userId']
        queryLoanResult_data['loanApplyNo'] = loan_apply_info['loan_apply_id']

        # 更新 payload 字段值
        queryLoanResult_data.update(kwargs)
        parser = DataUpdate(self.cfg['queryLoanResult']['payload'], **queryLoanResult_data)
        self.active_payload = parser.parser

        self.log.demsg('借款查询请求...')
        url = self.host + self.cfg['queryLoanResult']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 借款&还款计划查询payload
    def queryLoanPlan(self, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return:
        """
        queryLoanPlan_data = dict()
        # body
        queryLoanPlan_data['requestNo'] = 'requestNo' + self.strings + "_8000"
        queryLoanPlan_data['requestTime'] = self.times
        queryLoanPlan_data['ct'] = self.times

        loan_apply_info = self.getSqlData.get_loan_apply_info(thirdpart_user_id=self.data['userId'])
        queryLoanPlan_data['userId'] = self.data['userId']
        queryLoanPlan_data['loanApplyNo'] = loan_apply_info['loan_apply_id']
        credit_loan_invoice = self.getSqlData.get_credit_database_info('credit_loan_invoice',
                                                                       loan_apply_id=queryLoanPlan_data['loanApplyNo'])
        queryLoanPlan_data['partnerLoanNo'] = credit_loan_invoice['loan_invoice_id']

        # 更新 payload 字段值
        queryLoanPlan_data.update(kwargs)
        parser = DataUpdate(self.cfg['queryLoanPlan']['payload'], **queryLoanPlan_data)
        self.active_payload = parser.parser

        self.log.demsg('借款&还款计划查询请求...')
        url = self.host + self.cfg['queryLoanPlan']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 还款试算申请
    def repayTrial(self, **kwargs):
        """ # 还款试算payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        repayTrial_data = dict()
        # body
        repayTrial_data['requestNo'] = 'requestNo' + self.strings + "_9000"
        repayTrial_data['requestTime'] = self.times
        repayTrial_data['ct'] = self.times

        # 还款时间默认当前系统时间
        repayTrial_data['repayTime'] = self.date

        # 更新 payload 字段值
        repayTrial_data.update(kwargs)
        parser = DataUpdate(self.cfg['repayTrial']['payload'], **repayTrial_data)
        self.active_payload = parser.parser

        self.log.demsg('发起还款试算请求...')
        url = self.host + self.cfg['repayTrial']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 还款申请
    def applyRepayment(self, **kwargs):
        """ # 还款申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        applyRepayment_data = dict()
        # body
        applyRepayment_data['requestNo'] = 'requestNo' + self.strings + "_1100"
        applyRepayment_data['requestTime'] = self.times
        applyRepayment_data['ct'] = self.times

        # 还款时间默认当前系统时间
        applyRepayment_data['repayTime'] = self.date

        # 银行卡信息
        applyRepayment_data['idCardNo'] = self.data['cer_no']
        applyRepayment_data['userMobile'] = self.data['telephone']
        applyRepayment_data['userName'] = self.data['name']
        applyRepayment_data['bankCardNo'] = self.data['bankid']

        # 更新 payload 字段值
        applyRepayment_data.update(kwargs)
        parser = DataUpdate(self.cfg['applyRepayment']['payload'], **applyRepayment_data)
        self.active_payload = parser.parser

        self.log.demsg('发起还款请求...')
        url = self.host + self.cfg['applyRepayment']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 还款查询payload
    def queryRepayResult(self, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return:
        """
        queryRepayResult_data = dict()
        # body
        queryRepayResult_data['requestNo'] = 'requestNo' + self.strings + "_1200"
        queryRepayResult_data['requestTime'] = self.times
        queryRepayResult_data['ct'] = self.times

        # 更新 payload 字段值
        queryRepayResult_data.update(kwargs)
        parser = DataUpdate(self.cfg['queryRepayResult']['payload'], **queryRepayResult_data)
        self.active_payload = parser.parser

        self.log.demsg('还款查询请求...')
        url = self.host + self.cfg['queryRepayResult']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response