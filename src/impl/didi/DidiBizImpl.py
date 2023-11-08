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
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl
from src.test_data.module_data import Didi
from utils.Apollo import Apollo
from utils.FileCreator import create_attachment_pdf, create_attachment_image
from utils.Models import get_base_data, get_base_data_temp, DataUpdate
from utils.SFTP import SFTP


class DidiBizImpl(MysqlInit):

    def __init__(self, merchantId=None, data=None, encrypt_flag=True, person=True, loan_invoice_id=None):
        super().__init__()
        self.repayPublicBizImpl = RepayPublicBizImpl()
        self.loan_invoice_id = loan_invoice_id
        self.MysqlBizImpl = MysqlBizImpl()
        self.apollo = Apollo()
        self.sftp = SFTP('didi')
        # 解析项目特性配置
        self.cfg = Didi.Didi
        self.encrypt_flag = encrypt_flag
        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 当前时间
        self.day = time.strftime('%d', time.localtime())  # 当前日
        self.times = str(int(round(time.time())))  # 当前13位时间戳
        self.data = self.get_user_info(data=data, person=person)
        # self.MysqlBizImpl.check_user_available(self.data)

        # 初始化产品
        self.merchantId = merchantId if merchantId else EnumMerchantId.DIDI.value

        # 初始化payload变量
        self.active_payload = {}
        self.applicationId = f'DC00003080{self.date}{self.times}'
        # self.applicationId = 'DC00003080202311071626401699345600'
        self.loanOrderId = self.date
        # self.loanOrderId = '20231107092001258889911122'
        self.encrypt_url = self.host + self.cfg['encrypt']['interface']
        self.decrypt_url = self.host + self.cfg['decrypt']['interface']
        self.sftpDir = '/data/P0057/20231107'
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
        self.upload_credit_file(self.applicationId)

        # self.log.demsg('用户四要素信息: {}'.format(self.data))
        # strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        credit_data = dict()

        # 用户信息
        credit_data['sftpDir'] = self.sftpDir + "/10/"
        credit_data['idNo'] = self.data['cer_no']
        credit_data['name'] = self.data['name']
        credit_data['phone'] = self.data['telephone']
        credit_data['bankCardNo'] = self.data['bankid']

        credit_data['gender'] = '⼥'
        credit_data['scoreOne'] = applyAmount * 100 + 260000  # 单位 分
        credit_data['scoreTwo'] = 300 * 40 + 350000  # *百万分之一 互金存的年化利率 * 360
        credit_data['scoreThree'] = 415 * 20 + 360000  # *百万分之一 互金存的罚息利率 * 360
        credit_data['applicationId'] = self.applicationId
        # # 银行卡信息

        parser = DataUpdate(self.cfg['credit_apply']['payload'], unique=False, **credit_data)
        parser = DataUpdate(parser.parser, unique=False, **kwargs)
        self.active_payload = parser.parser

        # 校验用户是否已存在
        # self.MysqlBizImpl.check_user_available(self.data)
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

    def loanRiskCheck(self, loanAmount=20000, applyTerm=12, **kwargs):
        """
        支用风控审核
        :param applyTerm:
        :param loanAmount:
        :param userInfo:
        :param kwargs:
        :return:
        """

        self.upload_loan_file(self.loanOrderId)

        loan_risk_check_data = dict()

        loan_risk_check_data['name'] = self.data['name']
        loan_risk_check_data['idNo'] = self.data['cer_no']
        loan_risk_check_data['bankCardNo'] = self.data['bankid']
        loan_risk_check_data['phone'] = self.data['telephone']
        loan_risk_check_data['applicationId'] = self.applicationId
        loan_risk_check_data['loanOrderId'] = self.loanOrderId
        loan_risk_check_data['loanAmount'] = loanAmount * 100
        loan_risk_check_data['interestType'] = 2
        loan_risk_check_data['totalInstallment'] = applyTerm
        loan_risk_check_data['loanRating'] = 500  # *百万分之一 互金存的年化利率
        loan_risk_check_data['penaltyInterestRate'] = 415  # *百万分之一 互金存的罚息利率
        loan_risk_check_data['sftpDir'] = self.sftpDir + "/12/"
        loan_risk_check_data['callbackUrl'] = "www.baidu.com"
        loan_risk_check_data['finProductType'] = 2  # 产品类型: 1.随借随还， 2.固定期限
        loan_risk_check_data['rateType'] = 0  # 是否涉及营销定价优惠；默认为【0】否  1 是
        loan_risk_check_data['loanUsage'] = '1'
        loan_risk_check_data['preAbsId'] = self.date

        parser = DataUpdate(self.cfg['loan_risk_check']['payload'], unique=False, **loan_risk_check_data)
        parser = DataUpdate(parser.parser, unique=False, **kwargs)
        self.active_payload = parser.parser

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
        queryLoanRiskCheck_data['loanOrderId'] = self.loanOrderId

        parser = DataUpdate(self.cfg['query_loan_risk_check']['payload'], **queryLoanRiskCheck_data)

        self.active_payload = parser.parser
        url = self.host + self.cfg['query_loan_risk_check']['interface']

        self.log.demsg('查询支用结果...')
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def applyLoan(self, thirdApplyId, loanDate=None, loanAmount=20000, userInfo=None, **kwargs):
        """
        支用申请
        :param thirdApplyId:
        :param loanAmount:
        :param userInfo:
        :param kwargs:
        :return:
        """
        apply_loan_data = dict()

        if loanDate is None:
            apollo_data = dict()
            apply_loan_data['repayDay'] = self.day
            apollo_data['credit.loan.trade.date.mock'] = 'false'
            self.apollo.update_config(appId='loan2.1-public', namespace='JCXF.system', **apollo_data)

        else:
            apollo_data = dict()
            apollo_data['credit.loan.trade.date.mock'] = 'true'
            apollo_data['credit.loan.date.mock'] = loanDate
            self.apollo.update_config(appId='loan2.1-public', namespace='JCXF.system', **apollo_data)

        apply_loan_data['name'] = self.data['name']
        apply_loan_data['idNo'] = self.data['cer_no']
        apply_loan_data['bankCardNo'] = self.data['bankid']
        apply_loan_data['phone'] = self.data['telephone']

        apply_loan_data['applicationId'] = thirdApplyId
        apply_loan_data['loanOrderId'] = self.loanOrderId
        apply_loan_data['loanAmount'] = loanAmount * 100
        apply_loan_data['repayDay'] = ''

        parser = DataUpdate(self.cfg['loan_apply']['payload'], unique=False, **apply_loan_data)
        # 更新调用层数据
        parser = DataUpdate(parser.parser, unique=False, **kwargs)
        self.active_payload = parser.parser

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
            queryLoanResult_data['loanOrderId'] = self.loanOrderId
        else:
            queryLoanResult_data['loanOrderId'] = loanOrderId
        parser = DataUpdate(self.cfg['query_loan_result']['payload'], **queryLoanResult_data)

        self.active_payload = parser.parser
        url = self.host + self.cfg['query_loan_result']['interface']
        self.log.demsg('查询放款结果...')
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def upload_credit_file(self, applicationId=None):
        """
        上传附件（模拟滴滴方附件上传到他们的SFTP）
        :return:NONE
        """
        if applicationId is None:
            applicationId = self.applicationId
        p_path = os.path.abspath(os.path.dirname(__file__))
        attachment = p_path[:p_path.index("jccfc-test") + len("jccfc-test")] + '/image/temp/'
        png_path = attachment + "10/"
        pdf_path = attachment + "20/"
        if os.path.exists(png_path):
            os.removedirs(png_path)
        if os.path.exists(pdf_path):
            os.removedirs(pdf_path)
        os.mkdir(attachment)
        os.mkdir(attachment + "/10/")
        os.mkdir(attachment + "/20/")

        sftpDir_credit_png = self.sftpDir + '/10/'
        sftpDir_credit_pdf = self.sftpDir + '/20/' + applicationId + '/'
        front = "/10/" + applicationId + "_01"
        back = "/10/" + applicationId + "_02"
        face = "/10/" + applicationId + "_03"

        front_path = create_attachment_image(self.data, front)
        back_path = create_attachment_image(self.data, back)
        face_path = create_attachment_image(self.data, face)

        # # 身份证正面front
        # self.sftp.upload_file(r"C:\Users\jccfc\PycharmProjects\jccfc-test\image\DD0000308020231023180540f780e7_01.png", sftpDir_credit_pdf,
        #                       clean=False)
        # # 身份证反面back
        # self.sftp.upload_file(r"C:\Users\jccfc\PycharmProjects\jccfc-test\image\DD0000308020231023180540f780e7_02.png", sftpDir_credit_pdf,
        #                       clean=False)
        # # 人脸照face
        # self.sftp.upload_file(r"C:\Users\jccfc\PycharmProjects\jccfc-test\image\DD0000308020231023180540f780e7_03.png", sftpDir_credit_pdf,
        #                       clean=False)
        # 征信查询授权书INVESTIGATION
        # INVESTIGATION = "/20" + "/INVESTIGATION"
        # INVESTIGATION_path = create_attachment_pdf(INVESTIGATION, contentText='征信查询授权书', person=self.data)
        self.sftp.upload_file(r"C:\Users\jccfc\PycharmProjects\jccfc-test\image\INVESTIGATION.pdf", sftpDir_credit_pdf,
                              clean=False)
        # 个⼈信息查询授权协议
        # PINFOQUERY = "/20" + "/PINFOQUERY"
        # # PINFOQUERY_path = create_attachment_pdf(PINFOQUERY, contentText='三方数据查询授权书', person=self.data)
        self.sftp.upload_file(r"C:\Users\jccfc\PycharmProjects\jccfc-test\image\PINFOQUERY.pdf", sftpDir_credit_pdf,
                              clean=False)
        # 人脸识别授权书PINFOUSE
        # PINFOUSE = "/20" + "/PINFOUSE"
        # PINFOUSE_path = create_attachment_pdf(PINFOUSE, contentText='人脸识别授权书', person=self.data)
        self.sftp.upload_file(r"C:\Users\jccfc\PycharmProjects\jccfc-test\image\PINFOUSE.pdf", sftpDir_credit_pdf,
                              clean=False)



        # 授信合同
        # LOANCREDIT = "/20/" + applicationId + "/LOANCREDIT"
        # LOANCREDIT_path = create_attachment_pdf(LOANCREDIT, contentText='授信合同', person=self.data)

        # 授信合同LOANCREDIT
        # self.sftp = SFTP('didi')
        self.sftp.upload_file(r"C:\Users\jccfc\PycharmProjects\jccfc-test\image\LOANCREDIT.pdf", sftpDir_credit_pdf,
                              clean=False)

        self.sftp.upload_dir(png_path, sftpDir_credit_png)
        # self.sftp.upload_dir(pdf_path, sftpDir_credit_pdf)

        # 身份证正反面
        # 人脸照
        # 征信查询授权书(INVESTIGATION
        #         .pdf)、三方数据查询授权书（PINFOQUERY.pdf
        # ）、授信合同（LOANCREDIT.pdf
        # ）、人脸识别授权书（PINFOUSE.pdf
        # ）、非学生承诺函（COVENANT.pdf）

        # self.sftp.sftp_close()

        # 删除本地文件
        # os.remove(attachment)
        # os.remove(back_path)
        # os.remove(face_path)
        # os.remove(INVESTIGATION_path)
        # os.remove(PINFOQUERY_path)
        # os.remove(COVENANT_path)
        # os.remove(LOANCREDIT_path)
        # os.remove(LOAN_path)

    def upload_loan_file(self, loanOrderId=None):
        """
        上传附件（模拟滴滴方附件上传到他们的SFTP）
        :return:NONE
        """
        if loanOrderId is None:
             loanOrderId = self.loanOrderId
        p_path = os.path.abspath(os.path.dirname(__file__))
        attachment = p_path[:p_path.index("jccfc-test") + len("jccfc-test")] + '/image/temp/'
        png_path = attachment + "12/"
        pdf_path = attachment + "20/"
        if os.path.exists(png_path):
            os.removedirs(png_path)
        if os.path.exists(pdf_path):
            os.removedirs(pdf_path)
        os.mkdir(attachment)
        os.mkdir(attachment + "/12/")
        os.mkdir(attachment + "/20/")

        sftpDir_credit_png = self.sftpDir + '/12/'
        sftpDir_credit_pdf = self.sftpDir + '/20/' + self.loanOrderId + '/'
        front = "/12/" + loanOrderId + "_01"
        back = "/12/" + loanOrderId + "_02"
        face = "/12/" + loanOrderId + "_03"

        front_path = create_attachment_image(self.data, front)
        back_path = create_attachment_image(self.data, back)
        face_path = create_attachment_image(self.data, face)
        # 身份证正面front
        # self.sftp.upload_file(r"C:\Users\jccfc\PycharmProjects\jccfc-test\image\DD0000308020231023180540f780e7_01.png",
        #                       sftpDir_credit_pdf,
        #                       clean=False)
        # # 身份证反面back
        # self.sftp.upload_file(r"C:\Users\jccfc\PycharmProjects\jccfc-test\image\DD0000308020231023180540f780e7_02.png",
        #                       sftpDir_credit_pdf,
        #                       clean=False)
        # # 人脸照face
        # self.sftp.upload_file(r"C:\Users\jccfc\PycharmProjects\jccfc-test\image\DD0000308020231023180540f780e7_03.png",
        #                       sftpDir_credit_pdf,
        #                       clean=False)

        # 支用单LOANCREDIT
        self.sftp.upload_file(r"C:\Users\jccfc\PycharmProjects\jccfc-test\image\LOAN.pdf", sftpDir_credit_pdf,
                              clean=False)

        self.sftp.upload_dir(png_path, sftpDir_credit_png)
        # 身份证正反面
        # 人脸照
        # 借款合同(LOAN)

        # self.sftp.sftp_close()

        # 删除本地文件
        # os.remove(front_path)
        # os.remove(back_path)
        # os.remove(face_path)
        # os.remove(INVESTIGATION_path)
        # os.remove(PINFOQUERY_path)
        # os.remove(COVENANT_path)
        # os.remove(LOANCREDIT_path)

    def repay(self, repay_date, repay_term_no, loanOrderId, repayType=0, **kwargs):
        """
        主动还款--代扣
        :param repay_date:  还款日
        :param repay_term_no: 还款期数
        :param loanOrderId: 三方支用号
        :param repayType: 还款类型： 1.当期还款， 2.结清全部
        :param kwargs:
        :return:
        """

        # 还款前置任务
        self.repayPublicBizImpl.pre_repay_config(repayDate=repay_date)

        # 根据openId查询支用信息
        key1 = "thirdpart_apply_id = '{}'".format(loanOrderId)
        credit_loan_apply = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_apply", key=key1)
        key_1 = "credit_apply_id = '{}'".format(credit_loan_apply['credit_apply_id'])
        credit_apply = self.MysqlBizImpl.get_credit_data_info(table="credit_apply", key=key_1)

        # 根据支用申请单号查询借据信息
        if self.loan_invoice_id:
            loan_invoice_id = self.loan_invoice_id
            key2 = "loan_invoice_id = '{}'".format(loan_invoice_id)
            credit_loan_invoice = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key2)
            loan_apply_id = credit_loan_invoice["loan_apply_id"]
            key21 = "loan_apply_id = '{}'".format(loan_apply_id)
            credit_loan_apply = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_apply", key=key21)
        else:
            loan_apply_id = credit_loan_apply["loan_apply_id"]
            key2 = "loan_apply_id = '{}'".format(loan_apply_id)
            credit_loan_invoice = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key2)
            loan_invoice_id = credit_loan_invoice["loan_invoice_id"]

        # 取资产执行利率
        asset_loan_invoice_info = self.MysqlBizImpl.get_asset_database_info(table="asset_loan_invoice_info",
                                                                            loan_invoice_id=loan_invoice_id)
        execute_rate = asset_loan_invoice_info["execute_rate"]
        # 根据借据Id和期次获取还款计划
        key3 = "loan_invoice_id = '{}' and current_num in ({})".format(loan_invoice_id, repay_term_no)
        key4 = 'sum(pre_repay_amount),sum(pre_repay_principal),sum(pre_repay_interest),sum(pre_repay_overdue_fee),sum(pre_repay_fee)'
        asset_repay_plan = self.MysqlBizImpl.get_asset_repay_plan(table="asset_repay_plan", key=key3, key1=key4)

        initiateRepay_data = dict()
        initiateRepay_data['applicationId'] = credit_apply['thirdpart_apply_id']
        initiateRepay_data['loanOrderId'] = loanOrderId
        initiateRepay_data['payId'] = 'DD00' + time.strftime('%Y%m%d%H%M%S', time.localtime())
        initiateRepay_data['payType'] = 1  # 还款⽀付⽅式： 1 ⽤户主动还款； 2 合作⽅发起代扣还款； 3 滴滴发起代扣还
        initiateRepay_data['repayType'] = repayType  # 还款类型： 1.当期还款， 2.结清全部
        initiateRepay_data['loanNumbers'] = repay_term_no
        initiateRepay_data[
            'callbackUrl'] = 'http://manhattanloantest.xiaojukeji.com/manhattan/loan/openfin/superpartner/standard/activeRepayResult'
        initiateRepay_data['agreementNo'] = '00000000000204572240'
        initiateRepay_data['repayAmountInfo'] = {
            "principal": int(asset_repay_plan['sum(pre_repay_principal)'] * 100),  # 本金
            "interestPenalty": int(asset_repay_plan['sum(pre_repay_overdue_fee)'] * 100),
            "advanceClearFee": 0,
            "totalAmount": int(asset_repay_plan['sum(pre_repay_amount)'] * 100),
            "guaranteeFee": 0,
            "insuranceFee": 0,
            "interest": int(asset_repay_plan['sum(pre_repay_interest)'] * 100),
            "ratedInterest": 0,
            "principalPenalty": 0,
            "guaranteeConsultFee": 0
        }
        if repayType == 2:
            initiateRepay_data['repayAmountInfo']['advanceClearFee'] = int(initiateRepay_data['repayAmountInfo'][
                                                                               'principal'] * 4 / 100)
        initiateRepay_data['repayDate'] = repay_date
        initiateRepay_data['subAccStatus'] = 0
        initiateRepay_data['subAcctList'] = []
        initiateRepay_data['userInfo'] = {
            "name": credit_apply['user_name'],
            "idNo": credit_apply['certificate_no'],
            "phone": credit_apply['user_tel'],
            "bankCardNo": "6217861697102024366",
            "bankName": "中国银行",
            "bankAddr": "BOC",
            "jobType": "1",
            "province": "四川",
            "city": "成都",
            "county": "高新",
            "address": "中航城市广场",
            "nationality": "中国",
            "certificateType": "1"
        }
        # 更新当前方法层数据
        parser = DataUpdate(self.cfg['repay']['payload'], unique=False, **initiateRepay_data)
        # 更新调用层数据
        parser = DataUpdate(parser.parser, **kwargs)
        self.active_payload = parser.parser
        url = self.host + self.cfg['repay']['interface']
        self.log.demsg('查询放款结果...')
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def queryRepayResult(self, loanOrderId=None, payId=None, **kwargs):
        '''
        查询代扣结果
        :param loanOrderId:
        :param payId:
        :param kwargs:
        :return:
        '''
        queryRepayResultData = dict()
        queryRepayResultData['loanOrderId'] = loanOrderId
        queryRepayResultData['payId'] = payId

        parser = DataUpdate(self.cfg['query_repay_result']['payload'], unique=False, **queryRepayResultData)
        parser = DataUpdate(parser.parser, **kwargs)

        parser = DataUpdate(parser.parser, **kwargs)
        self.active_payload = parser.parser
        url = self.host + self.cfg['query_repay_result']['interface']
        self.log.demsg('查询放款结果...')
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def repayNotify(self, loanOrderId, payId, repay_date, repay_term_no='1,2', payChannel=291, repayType=1, **kwargs):
        """
        滴滴通知入账接口
        :param loanOrderId:
        :param payId:
        :param repay_date:
        :param repay_term_no:
        :param kwargs:
        :return:
        """
        repayNotifyData = dict()

        # 还款前置任务
        self.repayPublicBizImpl.pre_repay_config(repayDate=repay_date)

        # 根据openId查询支用信息
        key1 = "thirdpart_apply_id = '{}'".format(loanOrderId)
        credit_loan_apply = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_apply", key=key1)

        # 根据支用申请单号查询借据信息
        if self.loan_invoice_id:
            loan_invoice_id = self.loan_invoice_id
            key2 = "loan_invoice_id = '{}'".format(loan_invoice_id)
            credit_loan_invoice = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key2)
            loan_apply_id = credit_loan_invoice["loan_apply_id"]
            key21 = "loan_apply_id = '{}'".format(loan_apply_id)
            credit_loan_apply = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_apply", key=key21)
        else:
            loan_apply_id = credit_loan_apply["loan_apply_id"]
            key2 = "loan_apply_id = '{}'".format(loan_apply_id)
            credit_loan_invoice = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key2)
            loan_invoice_id = credit_loan_invoice["loan_invoice_id"]

        # 取资产执行利率
        asset_loan_invoice_info = self.MysqlBizImpl.get_asset_database_info(table="asset_loan_invoice_info",
                                                                            loan_invoice_id=loan_invoice_id)
        execute_rate = asset_loan_invoice_info["execute_rate"]
        # 根据借据Id和期次获取还款计划
        key3 = "loan_invoice_id = '{}' and current_num in ({})".format(loan_invoice_id, repay_term_no)
        key4 = 'sum(pre_repay_amount),sum(pre_repay_principal),sum(pre_repay_interest),sum(pre_repay_overdue_fee),sum(pre_repay_fee)'
        asset_repay_plan = self.MysqlBizImpl.get_asset_repay_plan(table="asset_repay_plan", key=key3, key1=key4)

        # 通知payload
        repayNotifyData['loanOrderId'] = loanOrderId
        repayNotifyData['payId'] = payId
        repayNotifyData['loanNumbers'] = repay_term_no

        repayNotifyData['totalRepayAmountInfo'] = {
            'totalAmount': int(asset_repay_plan['sum(pre_repay_amount)'] * 100),  # 总金额
            'principal': int(asset_repay_plan['sum(pre_repay_principal)'] * 100),  # 本金
            'interest': int(asset_repay_plan['sum(pre_repay_interest)'] * 100),  # 利息
            'principalPenalty': int(asset_repay_plan['sum(pre_repay_overdue_fee)'] * 100),  # 逾期罚息
            'advanceClearFee': 0 if repayType == 1 else int(asset_repay_plan['sum(pre_repay_principal)'] * 4)  # 手续费
        }

        repayNotifyData['repayDetails'] = list()
        repay_term_list = repay_term_no.split(',')
        for num in repay_term_list:
            key5 = "loan_invoice_id = '{}' and current_num in ({})".format(loan_invoice_id, num)
            asset_repay_plan_num = self.MysqlBizImpl.get_asset_repay_plan(table="asset_repay_plan", key=key5, key1=key4)
            repayAmountInfo = {
                "repayAmountInfo": {
                    "guaranteeConsultFee": 0,
                    "guaranteeFee": 0,
                    "totalAmount": int(asset_repay_plan_num['sum(pre_repay_amount)'] * 100),
                    "ratedInterest": 0,
                    "advanceClearFee": int(
                        asset_repay_plan_num['sum(pre_repay_principal)'] * 4) if repayType == 2 else 0,
                    "interestPenalty": 0,
                    "principal": int(asset_repay_plan_num['sum(pre_repay_principal)'] * 100),
                    "insuranceFee": 0,
                    "principalPenalty": int(asset_repay_plan_num['sum(pre_repay_overdue_fee)'] * 100),
                    "interest": int(asset_repay_plan_num['sum(pre_repay_interest)'] * 100),
                    "preferentialInterest": 0
                },
                "loanNumber": int(num)
            }
            repayNotifyData['repayDetails'].append(repayAmountInfo)

        repayNotifyData['repayType'] = '1'
        repayNotifyData['payChannel'] = payChannel  # 还款⽀付渠道5: ⽀付宝14: 转账还款(招⾏⼤额)99：线下还款(对公⾏⽅户)291：中⾦协议⽀付
        repayNotifyData['payType'] = '1'  # 1: 主动还款  3：批量扣款 4: 线下还款
        repayNotifyData['payChannelAccountId'] = ''  # 还款⽀付卡号  如果是银⾏卡，则为银⾏卡号；  如果是⽀付宝&微信为对应的账户Id； 如果是线下对公还款则为空；
        repayNotifyData['repayStatus'] = '1'  # 还款状态  1：还款成功  2：还款失败
        repayNotifyData['tranDate'] = time.strftime('%Y-%m-%d',
                                                    time.localtime())  # 交易⽇期（账务⽇期） ,格式为： yyyy-MM-dd，还款成功后必填。
        repayNotifyData['repayTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        parser = DataUpdate(self.cfg['collectActiveRepayResult']['payload'], **repayNotifyData)
        parser = DataUpdate(parser.parser, **kwargs)
        self.active_payload = parser.parser
        url = self.host + self.cfg['collectActiveRepayResult']['interface']
        self.log.demsg('滴滴入账通知...')
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        # 跑入账定时任务

        return response

    def userScoreAdvice(self, applicationId, scoreType, applyAmount=None, scoreTwo=None, scoreThree=None,
                        endDate=None):
        """
         滴滴贷中评分调整
        :param applicationId:
        :param scoreType:
        :param applyAmount:
        :param scoreTwo:
        :param scoreThree:
        :param endDate:
        :return:
        """
        userScoreAdviceData = dict()
        userScoreAdviceData['orderId'] = time.strftime('%Y%m%d%H%M%S', time.localtime())
        userScoreAdviceData['applicationId'] = applicationId
        userScoreAdviceData['scoreType'] = scoreType

        parser = DataUpdate(self.cfg['userScoreAdvice']['payload'], **userScoreAdviceData)
        self.active_payload = parser.parser
        if scoreType == 1:
            self.active_payload['scoreOne'] = applyAmount * 100 + 260000

        if scoreType == 2:
            self.active_payload['scoreTwo'] = scoreTwo * 40 + 350000
            self.active_payload['scoreThree'] = scoreThree * 20 + 360000
        if scoreType == 6:
            self.active_payload['scoreSix'] = 3
        if scoreType == 7:
            self.active_payload['endDate'] = time.strftime('%Y-%m-%d', time.localtime()) if endDate is None else endDate

        url = self.host + self.cfg['userScoreAdvice']['interface']

        self.log.demsg('滴滴贷中评分...')
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def userScoreQuery(self, orderId):
        """
        滴滴贷中评分调整查询
        :param orderId:
        :return:
        """
        self.active_payload = self.cfg['userScoreQuery']['payload']
        self.active_payload['orderId'] = orderId
        self.log.demsg('滴滴贷中评分结果查询...')
        url = self.host + self.cfg['userScoreQuery']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def didiNotifyPartnerUploadFile(self, **kwargs):
        pass

    def queryPartnerUploadFileResult(self, **kwargs):
        pass

    def didiUploadFile(self, **kwargs):
        pass
