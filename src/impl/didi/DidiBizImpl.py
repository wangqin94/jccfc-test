# -*- coding: utf-8 -*-
# ------------------------------------------
# 滴滴-滴水贷接口数据封装类
# ------------------------------------------
import os
import time

from engine.MysqlInit import MysqlInit
from src.enums.EnumsCommon import EnumMerchantId, ProductEnum
from src.impl.common.CommonBizImpl import post_with_encrypt
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from src.test_data.module_data import Didi
from utils.Apollo import Apollo
from utils.FileCreator import create_attachment_pdf, create_attachment_image
from utils.Models import get_base_data, get_base_data_temp, DataUpdate
from utils.SFTP import SFTP


class DidiBizImpl(MysqlInit):

    def __init__(self, merchantId=None, data=None, encrypt_flag=True, person=True):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()
        self.apollo = Apollo()
        self.sftp = SFTP()
        # 解析项目特性配置
        self.cfg = Didi.Didi
        self.encrypt_flag = encrypt_flag
        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 当前时间
        self.times = str(int(round(time.time())))  # 当前13位时间戳
        self.data = self.get_user_info(data=data, person=person)
        # self.MysqlBizImpl.check_user_available(self.data)

        # 初始化产品
        self.merchantId = merchantId if merchantId else EnumMerchantId.DIDI.value

        # 初始化payload变量
        self.active_payload = {}
        self.applicationId = f'DC00003080{self.date}{self.times}'
        self.loanOrderId = self.date
        self.encrypt_url = self.host + self.cfg['encrypt']['interface']
        self.decrypt_url = self.host + self.cfg['decrypt']['interface']

    def get_user_info(self, data=None, person=True):
        # 获取四要素信息
        if data:
            base_data = data
        else:
            if person:
                base_data = get_base_data(str(self.env) + ' -> ' + str(ProductEnum.DIDI.value), bankName='中国银行')
            else:
                base_data = get_base_data_temp()
        return base_data

    def credit(self, applyAmount=20000, **kwargs):
        """
        滴滴授信申请
        :param applyAmount: 申请金额 单位 元
        :param kwargs:
        :return:
        """
        # 上传文件
        self.upload_file()

        # self.log.demsg('用户四要素信息: {}'.format(self.data))
        # strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        credit_data = dict()
        credit_data['userInfo'] = dict()
        credit_data['ocrInfo'] = dict()
        # 用户信息
        credit_data['userInfo']['idNo'] = self.data['cer_no']
        credit_data['userInfo']['name'] = self.data['name']
        credit_data['userInfo']['phone'] = self.data['telephone']
        credit_data['userInfo']['bankCardNo'] = self.data['bankid']

        credit_data['ocrInfo']['name'] = self.data['name']
        credit_data['ocrInfo']['idNo'] = self.data['cer_no']
        credit_data['ocrInfo']['gender'] = '⼥'

        credit_data['userScoreInfo'] = dict()
        credit_data['userScoreInfo']['scoreOne'] = applyAmount * 100 + 260000  # 单位 分
        credit_data['userScoreInfo']['scoreTwo'] = 650 * 40 + 350000  # *百万分之一 互金存的年化利率 * 360
        credit_data['userScoreInfo']['scoreThree'] = 415 * 20 + 360000  # *百万分之一 互金存的年化利率 * 360
        # 银行卡信息

        parser = DataUpdate(self.cfg['credit_apply']['payload'], **credit_data)
        self.active_payload = parser.parser
        self.active_payload['applicationId'] = self.applicationId

        # 更新 payload 字段值
        self.active_payload.update(kwargs)
        # 校验用户是否已存在
        self.MysqlBizImpl.check_user_available(self.data)
        # 配置风控mock返回建议额度与授信额度一致
        apollo_data = dict()
        apollo_data['hj.channel.risk.credit.line.amt.mock'] = applyAmount
        self.apollo.update_config(appId='loan2.1-jcxf-credit', **apollo_data)

        self.log.demsg('开始授信申请...')
        url = self.host + self.cfg['credit_apply']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)

        return response

    def queryCreditResult(self, thirdApplyId=None):
        """
        查询授信结果
        :param thirdApplyId:
        :return:
        """
        queryCreditResult_data = dict()
        if thirdApplyId is None:
            credit_apply_info = self.MysqlBizImpl.get_credit_apply_info(certificate_no=self.data['cer_no'])
            queryCreditResult_data['applicationId'] = credit_apply_info['thirdpart_apply_id']
        else:
            queryCreditResult_data['applicationId'] = thirdApplyId
        parser = DataUpdate(self.cfg['credit_query']['payload'], **queryCreditResult_data)
        self.active_payload = parser.parser

        url = self.host + self.cfg['credit_query']['interface']
        self.log.demsg('开始授信查询...')
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def loanRiskCheck(self, loanAmount=20000, applyTerm=60, userInfo=None, **kwargs):
        """
        支用风控审核
        :param applyTerm:
        :param loanAmount:
        :param userInfo:
        :param kwargs:
        :return:
        """
        loan_risk_check_data = dict()

        loan_risk_check_data['userInfo'] = dict()
        loan_risk_check_data['userInfo']['name'] = self.data['name']
        loan_risk_check_data['userInfo']['idNo'] = self.data['cer_no']
        loan_risk_check_data['userInfo']['bankCardNo'] = self.data['bankid']
        loan_risk_check_data['userInfo']['phone'] = self.data['telephone']

        loan_risk_check_data['ocrInfo'] = dict()
        loan_risk_check_data['ocrInfo']['name'] = self.data['name']
        loan_risk_check_data['ocrInfo']['idNo'] = self.data['cer_no']
        loan_risk_check_data['ocrInfo']['gender'] = self.data['telephone']

        loan_risk_check_data['applicationId'] = self.applicationId
        loan_risk_check_data['loanOrderId'] = self.loanOrderId
        loan_risk_check_data['loanAmount'] = loanAmount * 100
        loan_risk_check_data['interestType'] = 1
        loan_risk_check_data['totalInstallment'] = applyTerm
        loan_risk_check_data['interestRate'] = 650  # *百万分之一 互金存的年化利率
        loan_risk_check_data['interestPenaltyRate'] = 415  # *百万分之一 互金存的年化利率
        loan_risk_check_data['sftpDir'] = "/hj/xdgl/didi/credit"
        loan_risk_check_data['callbackUrl'] = "www.baidu.com"
        loan_risk_check_data['finProductType'] = 1  # 产品类型: 1.随借随还， 2.固定期限
        loan_risk_check_data['rateType'] = 2  # 产品类型: 1.随借随还， 2.固定期限
        loan_risk_check_data['loanUsage'] = '1'
        loan_risk_check_data['preAbsId'] = self.date

        parser = DataUpdate(self.cfg['loan_risk_check']['payload'], **loan_risk_check_data)
        self.active_payload = parser.parser
        self.active_payload.update(kwargs)

        url = self.host + self.cfg['loan_risk_check']['interface']
        self.log.demsg('开始支用申请...')
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def queryLoanRiskCheck(self, thirdApplyId=None):
        queryLoanRiskCheck_data = dict()
        if not thirdApplyId:
            credit_apply_info = self.MysqlBizImpl.get_credit_apply_info(certificate_no=self.data['cer_no'])
            queryLoanRiskCheck_data['applicationId'] = credit_apply_info['thirdpart_apply_id']
        else:
            queryLoanRiskCheck_data['applicationId'] = thirdApplyId
        queryLoanRiskCheck_data['loanOrderId'] = self.loanOrderId  # todo 到时直接查数据库

        parser = DataUpdate(self.cfg['query_loan_risk_check']['payload'], **queryLoanRiskCheck_data)

        self.active_payload = parser.parser
        url = self.host + self.cfg['query_loan_risk_check']['interface']

        self.log.demsg('查询支用结果...')
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def applyLoan(self, thirdApplyId, loanAmount=20000, userInfo=None, **kwargs):
        """
        支用申请
        :param thirdApplyId:
        :param loanAmount:
        :param userInfo:
        :param kwargs:
        :return:
        """

        apply_loan_data = dict()

        apply_loan_data['userInfo'] = dict()
        apply_loan_data['userInfo']['name'] = self.data['name']
        apply_loan_data['userInfo']['idNo'] = self.data['cer_no']
        apply_loan_data['userInfo']['bankCardNo'] = self.data['bankid']
        apply_loan_data['userInfo']['phone'] = self.data['telephone']

        parser = DataUpdate(self.cfg['loan_apply']['payload'], **apply_loan_data['userInfo'])

        self.active_payload = parser.parser
        self.active_payload['applicationId'] = thirdApplyId
        self.active_payload['loanOrderId'] = self.loanOrderId
        self.active_payload['loanAmount'] = loanAmount*100
        self.active_payload['repayDay'] = '5'
        self.active_payload['callbackUrl'] = "www.baidu.com"

        self.active_payload.update(kwargs)
        if userInfo is not None:
            self.active_payload['userInfo'].update(**userInfo)
        url = self.host + self.cfg['loan_apply']['interface']
        self.log.demsg('开始放款申请...')
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def queryLoanResult(self, loanOrderId=None):
        """
        查询放款结果
        :param loanOrderId:
        :return:
        """
        queryLoanResult_data = dict()
        if loanOrderId is None:
            queryLoanResult_data['loanOrderId'] = self.loanOrderId  # todo 查询数据库
        else:
            queryLoanResult_data['loanOrderId'] = loanOrderId
        parser = DataUpdate(self.cfg['query_loan_result']['payload'], **queryLoanResult_data)

        self.active_payload = parser.parser
        url = self.host + self.cfg['query_loan_result']['interface']
        self.log.demsg('查询放款结果...')
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def upload_file(self, applicationId=None):
        """
        上传附件（模拟滴滴方附件上传到他们的SFTP）
        :return:NONE
        """
        if applicationId is None:
            applicationId = self.applicationId
        p_path = os.path.abspath(os.path.dirname(__file__))
        attachment = p_path[:p_path.index("jccfc-test") + len("jccfc-test")] + '/image/temp/'
        png_path = attachment + "/10/"
        pdf_path = attachment + "/20/"
        if os.path.exists(png_path):
            os.removedirs(png_path)
        if os.path.exists(pdf_path):
            os.removedirs(pdf_path)
        os.mkdir(attachment)
        os.mkdir(attachment + "/10/")
        os.mkdir(attachment + "/20/")

        sftpDir_credit_png = '/hj/xdgl/didi/credit/10'
        sftpDir_credit_pdf = '/hj/xdgl/didi/credit/20'
        front = "/10/" + applicationId + "_01"
        back = "/10/" + applicationId + "_02"
        face = "/10/" + applicationId + "_03"

        front_path = create_attachment_image(self.data, front)
        back_path = create_attachment_image(self.data, back)
        face_path = create_attachment_image(self.data, face)

        # 征信查询授权书
        INVESTIGATION = "/20/" + applicationId + "INVESTIGATION"
        INVESTIGATION_path = create_attachment_pdf(INVESTIGATION, person=self.data)
        # 三方数据查询授权书
        PINFOOUERY = "/20/" + applicationId + "PINFOQUERY"
        PINFOOUERY_path = create_attachment_pdf(PINFOOUERY, person=self.data)

        # # 人脸识别授权书(暂时待定)
        # PINFOUSE = "/20/" + applicationId + "PINFOUSE"
        # create_attachment_pdf(PINFOUSE, person=self.data)

        # 授信合同
        LOANCREDIT = "/20/" + applicationId + "LOANCREDIT"
        LOANCREDIT_path = create_attachment_pdf(LOANCREDIT, person=self.data)

        self.sftp.upload_dir(png_path, sftpDir_credit_png)
        self.sftp.upload_dir(pdf_path, sftpDir_credit_pdf)
        # self.sftp.sftp_close()

        # 删除本地文件
        os.remove(front_path)
        os.remove(back_path)
        os.remove(face_path)
        os.remove(INVESTIGATION_path)
        os.remove(PINFOOUERY_path)
        os.remove(LOANCREDIT_path)

    def initiateRepay(self):
        """
        还款接口
        :return:
        """
        url = self.host + self.cfg['initiate_Repay']['interface']

        initiateRepay_data = dict()
        initiateRepay_data['applicationId'] = ''
        initiateRepay_data['loanOrderId'] = ''
        initiateRepay_data['payId'] = ''
        initiateRepay_data['payType'] = ''
        initiateRepay_data['repayType'] = ''
        initiateRepay_data['loanNumbers'] = ''
        initiateRepay_data['callbackUrl'] = ''
        initiateRepay_data['agreementNo'] = ''
        initiateRepay_data['repayAmountInfo'] = ''
        initiateRepay_data['repayDate'] = ''
        initiateRepay_data['subAccStatus'] = ''
        initiateRepay_data['subAcctList'] = ''
        initiateRepay_data['userInfo'] = ''
