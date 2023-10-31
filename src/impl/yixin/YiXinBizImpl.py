# -*- coding: utf-8 -*-
# ------------------------------------------
# 宜信接口数据封装类
# ------------------------------------------
import math

from engine.MysqlInit import MysqlInit
from src.enums.EnumYinLiu import EnumRepayType
from src.enums.EnumsCommon import *
from src.test_data.module_data import YiXin
from src.impl.common.CommonBizImpl import *
from utils.FileHandle import Files
from utils.Apollo import Apollo


class YiXinBizImpl(MysqlInit):
    def __init__(self, data=None, encrypt_flag=True, person=True):
        """
        @param data: 四要素 为空系统随机获取，若person=True四要输写入person文件
        @param encrypt_flag: 接口加密标识，默认加密
        @param person: 若person=True四要输写入person文件，否则不写入
        """
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()
        self.apollo = Apollo()
        # 解析项目特性配置
        self.cfg = YiXin.YiXin
        self.encrypt_flag = encrypt_flag
        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 当前时间
        self.times = str(int(round(time.time() * 1000)))  # 当前13位时间戳
        self.data = self.get_user_info(data=data, person=person)
        self.interestRate = getInterestRate(ProductIdEnum.YIXIN.value)
        # 初始化产品、商户
        self.productId = ProductIdEnum.YIXIN.value
        self.merchantId = EnumMerchantId.YIXIN.value

        # 初始化payload变量
        self.active_payload = {}

        self.encrypt_url = self.host + self.cfg['encrypt']['interface'].format(self.merchantId)
        self.decrypt_url = self.host + self.cfg['decrypt']['interface']

    def get_user_info(self, data=None, person=True):
        # 获取四要素信息
        if data:
            base_data = data
        else:
            if person:
                base_data = get_base_data(str(self.env) + ' -> ' + str(ProductEnum.YIXIN.value))
            else:
                base_data = get_base_data_temp()
        return base_data

    # 发起代扣协议申请
    def getCardRealNameMessage(self, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        getCardRealNameMessage = dict()
        # head
        getCardRealNameMessage['requestSerialNo'] = 'requestNo' + strings + "_1000"
        getCardRealNameMessage['requestTime'] = self.date
        getCardRealNameMessage['merchantId'] = self.merchantId
        # body
        getCardRealNameMessage['payerIdNum'] = self.data['cer_no']
        getCardRealNameMessage['payer'] = self.data['name']
        getCardRealNameMessage['mobileNo'] = self.data['telephone']
        getCardRealNameMessage['payerBankCardNum'] = self.data['bankid']
        getCardRealNameMessage['payerPhoneNum'] = self.data['telephone']

        # 更新 payload 字段值
        getCardRealNameMessage.update(kwargs)
        parser = DataUpdate(self.cfg['getCardRealNameMessage']['payload'], **getCardRealNameMessage)
        self.active_payload = parser.parser

        self.log.demsg('发起绑卡请求...')
        url = self.host + self.cfg['getCardRealNameMessage']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 确认绑卡申请payload
    def bindCardRealName(self, tradeSerialNo, **kwargs):
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        bindCardRealName_data = dict()
        # head
        bindCardRealName_data['requestSerialNo'] = 'requestNo' + strings + "_1000"
        bindCardRealName_data['requestTime'] = self.date
        bindCardRealName_data['merchantId'] = self.merchantId
        # body
        bindCardRealName_data['tradeSerialNo'] = tradeSerialNo  # 同发起代扣签约返回的交易流水号
        bindCardRealName_data['mobileNo'] = self.data['telephone']
        bindCardRealName_data['payerPhoneNum'] = self.data['telephone']

        # 更新 payload 字段值
        bindCardRealName_data.update(kwargs)
        parser = DataUpdate(self.cfg['bindCardRealName']['payload'], **bindCardRealName_data)
        self.active_payload = parser.parser

        self.log.demsg('确认绑卡请求...')
        url = self.host + self.cfg['bindCardRealName']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 代扣签约查询
    def queryWithholdingAgreement(self, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        queryWithholdingAgreement = dict()
        # head
        queryWithholdingAgreement['requestSerialNo'] = 'requestNo' + strings + "_1000"
        queryWithholdingAgreement['requestTime'] = self.date
        queryWithholdingAgreement['merchantId'] = self.merchantId

        # body
        queryWithholdingAgreement['payerIdNum'] = self.data['cer_no']
        queryWithholdingAgreement['payer'] = self.data['name']
        queryWithholdingAgreement['payerBankCardNum'] = self.data['bankid']
        queryWithholdingAgreement['payerPhoneNum'] = self.data['telephone']
        # 更新 payload 字段值
        queryWithholdingAgreement.update(kwargs)
        parser = DataUpdate(self.cfg['queryWithholdingAgreement']['payload'], **queryWithholdingAgreement)
        self.active_payload = parser.parser

        self.log.demsg('代扣签约查询请求...')
        url = self.host + self.cfg['queryWithholdingAgreement']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 授信申请
    def credit(self, applyAmount=1000, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param applyAmount: 授信金额
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('用户四要素信息: {}'.format(self.data))
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        credit_data = dict()
        # head
        credit_data['requestSerialNo'] = 'requestNo' + strings + "_2000"
        credit_data['requestTime'] = self.date
        credit_data['merchantId'] = self.merchantId

        # body
        credit_data['thirdApplyId'] = 'thirdApplyId' + strings
        credit_data['thirdApplyTime'] = self.date
        credit_data['applyAmount'] = applyAmount
        # 临时新增参数
        credit_data['orderType'] = '1'  # EnumOrderType 固定传1-取现

        # 用户信息
        credit_data['idNo'] = self.data['cer_no']
        credit_data['name'] = self.data['name']
        credit_data['reserveMobile'] = self.data['telephone']
        credit_data['mobileNo'] = self.data['telephone']

        # 还款方式
        credit_data['repayType'] = EnumRepayType.EQUAL_AMT_INTEREST.value
        # 银行卡信息
        credit_data['userBankCardNo'] = self.data['bankid']

        # 更新 payload 字段值
        credit_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit_apply']['payload'], **credit_data)
        self.active_payload = parser.parser
        self.active_payload['body']['productId'] = self.productId  # 产品编号

        # 校验用户是否已存在
        self.MysqlBizImpl.check_user_available(self.data)

        self.log.demsg('开始授信申请...')
        url = self.host + self.cfg['credit_apply']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 授信查询
    def queryCreditResult(self, thirdApplyId=None, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param thirdApplyId: 用户授信申请id, 为空时，根据用户身份证取申请号
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        queryCreditResult_data = dict()
        # head
        queryCreditResult_data['requestSerialNo'] = 'requestNo' + strings + "_3000"
        queryCreditResult_data['requestTime'] = self.date
        queryCreditResult_data['merchantId'] = self.merchantId

        if not thirdApplyId:
            credit_apply_info = self.MysqlBizImpl.get_credit_apply_info(certificate_no=self.data['cer_no'])
            queryCreditResult_data['thirdApplyId'] = credit_apply_info['thirdpart_apply_id']
        else:
            queryCreditResult_data['thirdApplyId'] = thirdApplyId

        # 更新 payload 字段值
        queryCreditResult_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit_query']['payload'], **queryCreditResult_data)
        self.active_payload = parser.parser

        self.log.demsg('授信查询请求...')
        url = self.host + self.cfg['credit_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 还款计划试算
    def repayPlanTrial(self, loanDate=None, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param loanDate: 放款时间
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        repayPlanTrial_data = dict()
        # head
        repayPlanTrial_data['requestSerialNo'] = 'requestNo' + strings + "_3000"
        repayPlanTrial_data['requestTime'] = self.date
        repayPlanTrial_data['merchantId'] = self.merchantId

        # body
        repayPlanTrial_data['productId'] = self.productId
        repayPlanTrial_data['loanDate'] = loanDate if loanDate else time.strftime('%Y-%m-%d', time.localtime())

        # 更新 payload 字段值
        repayPlanTrial_data.update(kwargs)
        parser = DataUpdate(self.cfg['repayPlanTrial']['payload'], **repayPlanTrial_data)
        self.active_payload = parser.parser

        self.log.demsg('还款计划试算请求...')
        url = self.host + self.cfg['repayPlanTrial']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 支用申请
    def applyLoan(self, loanTerm=12, loanAmt=1000, thirdApplyId=None, loan_date=None, **kwargs):
        """ # 支用申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        @param loan_date: 放款时间，默认当前时间 eg:2022-01-01
        @param thirdApplyId: 三方申请号，与授信申请号一致
        @param loanAmt: 支用申请金额, 默认1000 单位元
        @param loanTerm: 借款期数：默认12期
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json response 接口响应参数 数据类型：json
        """
        self.log.info('用户四要素信息: {}'.format(self.data))
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        applyLoan_data = dict()
        # head
        applyLoan_data['requestSerialNo'] = 'requestNo' + strings + "_4000"
        applyLoan_data['requestTime'] = self.date
        applyLoan_data['merchantId'] = self.merchantId
        # body
        if not thirdApplyId:
            credit_apply_info = self.MysqlBizImpl.get_credit_apply_info(certificate_no=self.data['cer_no'], status='03')
            applyLoan_data['thirdApplyId'] = credit_apply_info['thirdpart_apply_id']
        else:
            applyLoan_data['thirdApplyId'] = thirdApplyId

        applyLoan_data['loanApplyNo'] = 'loanApplyNo' + strings

        # 设置apollo放款mock时间 默认当前时间
        loan_date = loan_date if loan_date else time.strftime('%Y-%m-%d', time.localtime())
        apollo_data = dict()
        apollo_data['credit.loan.trade.date.mock'] = True
        apollo_data['credit.loan.date.mock'] = loan_date
        self.apollo.update_config(appId='loan2.1-public', namespace='JCXF.system', **apollo_data)

        applyLoan_data['loanAmt'] = loanAmt
        applyLoan_data['loanTerm'] = loanTerm
        applyLoan_data['orderType'] = '1'  # EnumOrderType 固定传1-取现

        # 用户信息
        applyLoan_data['idNo'] = self.data['cer_no']
        applyLoan_data['mobileNo'] = self.data['telephone']
        applyLoan_data['reserveMobile'] = self.data['telephone']
        applyLoan_data['name'] = self.data['name']
        applyLoan_data['accountNo'] = self.data['bankid']

        # 还款方式
        applyLoan_data['repayType'] = EnumRepayType.EQUAL_AMT_INTEREST.value
        # 担保合同号
        applyLoan_data['guaranteeContractNo'] = 'ContractNo' + strings + "_5000"

        # 首期账单日
        firstRepayDate = get_bill_day(loan_date)
        # 获取还款计划试算中的保费
        preRepayInsuranceFee = self.repayPlanTrial(loanDate=loan_date, applyAmount=loanAmt, term=loanTerm)['body'][
            'repayPlanList']

        # 还款计划
        applyLoan_data['repaymentPlans'] = yinLiuRepayPlanByAvgAmt(billDate=firstRepayDate, loanAmt=loanAmt,
                                                                   yearRate=self.interestRate, term=loanTerm)
        # 取资产还款计划中红线保费值，替换还款计划中保费值
        for key1 in preRepayInsuranceFee:
            for key2 in applyLoan_data['repaymentPlans']:
                if key2.get('period') == key1["currentNum"]:
                    key2['guaranteeAmt'] = key1['preRepayInsuranceFee']
                    break

        # 更新 payload 字段值
        applyLoan_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan_apply']['payload'], **applyLoan_data)
        self.active_payload = parser.parser

        self.log.demsg('发起支用请求...')
        url = self.host + self.cfg['loan_apply']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 借款查询
    def queryLoanResult(self, thirdApplyId=None, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param thirdApplyId: 用户授信申请id, 为空时，根据用户身份证取申请号
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        queryLoanResult_data = dict()
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        # head
        queryLoanResult_data['requestSerialNo'] = 'requestNo' + strings + "_6000"
        queryLoanResult_data['requestTime'] = self.date
        queryLoanResult_data['merchantId'] = self.merchantId

        if not thirdApplyId:
            credit_apply_info = self.MysqlBizImpl.get_credit_apply_info(certificate_no=self.data['cer_no'])
            queryLoanResult_data['thirdApplyId'] = credit_apply_info['thirdpart_apply_id']
        else:
            queryLoanResult_data['thirdApplyId'] = thirdApplyId

        # 更新 payload 字段值
        queryLoanResult_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan_query']['payload'], **queryLoanResult_data)
        self.active_payload = parser.parser

        self.log.demsg('借款查询请求...')
        url = self.host + self.cfg['loan_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 借款&还款计划查询
    def repayPlan_query(self, loanInvoiceId, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param loanInvoiceId: 锦程借据号
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        repayPlan_query_data = dict()
        # head
        repayPlan_query_data['requestSerialNo'] = 'requestNo' + strings + "_7000"
        repayPlan_query_data['requestTime'] = self.date
        repayPlan_query_data['merchantId'] = self.merchantId

        # body
        repayPlan_query_data['loanInvoiceId'] = loanInvoiceId

        # 更新 payload 字段值
        repayPlan_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['repayPlan_query']['payload'], **repayPlan_query_data)
        self.active_payload = parser.parser

        self.log.demsg('借款&还款计划查询请求...')
        url = self.host + self.cfg['repayPlan_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 借款合同查询
    def loanContract_query(self, loanInvoiceId, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param loanInvoiceId: 锦程借据号
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        loanContract_query_data = dict()
        files = Files()
        # head
        loanContract_query_data['requestSerialNo'] = 'requestNo' + strings + "_8000"
        loanContract_query_data['requestTime'] = self.date
        loanContract_query_data['merchantId'] = self.merchantId

        # body
        loanContract_query_data['loanInvoiceId'] = loanInvoiceId

        # 更新 payload 字段值
        loanContract_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['loanContract_query']['payload'], **loanContract_query_data)
        self.active_payload = parser.parser

        self.log.demsg('借款合同查询请求...')
        url = self.host + self.cfg['loanContract_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        files.base64_to_file(response['body']['fileBase64'], 'D:\\testdata\\testdata\\' + response['body']['fileName'])
        return response

    # 还款试算
    def repayTrial(self, loanInvoiceId, repayTerm, repayType, repayDate=None, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param repayType: 还款类型
        @param repayDate: 还款时间
        @param repayTerm: 提前结清传起始期次
        @param loanInvoiceId: 锦程借据号
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        repayTrial_data = dict()
        # head
        repayTrial_data['requestSerialNo'] = 'requestNo' + strings + "_3000"
        repayTrial_data['requestTime'] = self.date
        repayTrial_data['merchantId'] = self.merchantId

        # body
        repayTrial_data['loanInvoiceId'] = loanInvoiceId
        repayTrial_data['repayTerm'] = repayTerm
        repayTrial_data['repayType'] = repayType
        repayTrial_data['repayDate'] = repayDate if repayDate else time.strftime('%Y-%m-%d', time.localtime())

        # 更新 payload 字段值
        repayTrial_data.update(kwargs)
        parser = DataUpdate(self.cfg['repayTrial']['payload'], **repayTrial_data)
        self.active_payload = parser.parser

        self.log.demsg('还款试算请求...')
        url = self.host + self.cfg['repayTrial']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 还款申请
    def repay_apply(self, loanInvoiceId, repay_scene='01', repay_type='1', repayTerm=None, repayGuaranteeFee=1.11,
                    repayDate=None, paymentOrder=None, **kwargs):
        """ # 还款申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        @param loanInvoiceId: 借据号 必填
        @param repay_scene: 还款场景 EnumRepayScene ("01", "线上还款"),("02", "线下还款"),（"04","支付宝还款通知"）（"05","逾期（代偿、回购后）还款通知"）
        @param repay_type： 还款类型 1 按期还款； 2 提前结清； 7 提前还当期； 9 宽限期提前结清； 10 逾期提前结清
        @param repayTerm: 还款期次，默认取当前借据最早未还期次
        @param repayGuaranteeFee: 担保费， 0<担保费<24红线-利息
        @param repayDate: 还款时间，默认当天 eg:'2022-08-01'
        @param paymentOrder: 支付宝订单号，支付宝还款需手动输入（查询支付系统payment_channel_order.PAY_TRANSACTION_ID）
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        self.log.demsg('用户四要素信息: {}'.format(self.data))
        repayDate = repayDate if repayDate else time.strftime('%Y-%m-%d', time.localtime())
        # 如果是贴息产品，担保费为0
        repayGuaranteeFee = repayGuaranteeFee
        # 构造还款参数
        repay_apply_data = dict()
        # head
        repay_apply_data['requestSerialNo'] = 'requestNo' + strings
        repay_apply_data['requestTime'] = self.date
        repay_apply_data['merchantId'] = self.merchantId
        # body
        repay_apply_data['repayScene'] = repay_scene
        repay_apply_data['repayApplySerialNo'] = 'repayNo' + strings
        repay_apply_data['loanInvoiceId'] = loanInvoiceId
        repay_apply_data['thirdRepayTime'] = self.date  # 客户实际还款时间
        repay_apply_data['repayType'] = repay_type
        if repayTerm:
            asset_repay_plan = self.MysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                                         loan_invoice_id=loanInvoiceId,
                                                                         current_num=repayTerm)
        else:
            key = "loan_invoice_id = '{}' and repay_plan_status in ('1','2','4', '5') ORDER BY 'current_num'".format(
                loanInvoiceId)
            asset_repay_plan = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key, record=0)

        self.log.demsg('当期最早未还期次{}'.format(asset_repay_plan['current_num']))
        repayTerm = asset_repay_plan['current_num']
        repay_apply_data['repayNum'] = int(asset_repay_plan['current_num'])
        repay_apply_data["repayAmount"] = float(asset_repay_plan['pre_repay_amount'])  # 总金额
        repay_apply_data["repayInterest"] = float(asset_repay_plan['pre_repay_interest'])  # 利息
        repay_apply_data["repayFee"] = float(asset_repay_plan['pre_repay_fee'])  # 费用
        repay_apply_data["repayOverdueFee"] = float(asset_repay_plan['pre_repay_overdue_fee'])  # 逾期罚息
        repay_apply_data["repayCompoundInterest"] = float(asset_repay_plan['pre_repay_compound_interest'])  # 手续费

        # 线下还款，担保费必须为0
        if repay_scene == '02':  # 线下还款
            repayGuaranteeFee = 0
        repay_apply_data["repayGuaranteeFee"] = repayGuaranteeFee  # 0<担保费<24红线-利息

        # 按期还款、提前当期
        if repay_type == "1" or "7":
            repay_apply_data["repayAmount"] = round(repay_apply_data["repayAmount"] + repayGuaranteeFee, 2)  # 总金额
            repay_apply_data["repayPrincipal"] = round(float(asset_repay_plan['pre_repay_principal']), 2)  # 本金
            repay_apply_data["repayGuaranteeFee"] = repayGuaranteeFee  # 0<担保费<24红线-利息

        # 提前结清
        days = get_day(asset_repay_plan["start_date"], repayDate)
        if repay_type == "2":
            repay_apply_data["repayPrincipal"] = float(asset_repay_plan['before_calc_principal'])  # 本金
            if days == 0:
                repay_apply_data["repayInterest"] = 0  # 上期账单日提前结清，利息应收0
            if days >= 30:
                repay_apply_data["repayInterest"] = repay_apply_data["repayInterest"]  # 计提超过30天，按照30天收整期利息
            else:
                repay_apply_data["repayInterest"] = getDailyAccrueInterest(self.productId, days,
                                                                           asset_repay_plan['before_calc_principal'])  # 提前结清按日计息
            # 提前结清 实还保费<=红线保费（放款保费/30*计提天数）
            channel_agency_repay_plan_detail_sync = self.MysqlBizImpl.get_op_channel_database_info(
                'channel_agency_repay_plan_detail_sync', loan_invoice_id=loanInvoiceId, repay_term=repayTerm)
            repayGuaranteeFee = math.floor(
                channel_agency_repay_plan_detail_sync['pre_guarantee_fee'] / 30 * days * 100) / 100
            repay_apply_data["repayAmount"] = round(
                repay_apply_data["repayPrincipal"] + repay_apply_data["repayInterest"] + repayGuaranteeFee,
                2)  # 总金额
            repay_apply_data["repayGuaranteeFee"] = repayGuaranteeFee  # 0<担保费<24红线-利息

        # 宽限期提前结清
        if repay_type == "9":
            repay_apply_data['repayType'] = "2"
            # 应收当期利息+宽限期期次利息
            key = "loan_invoice_id = '{}' and repay_plan_status = '1' and overdue_days = '0' ORDER BY 'current_num'".format(
                loanInvoiceId)
            currentTerm = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key, record=0)
            # 宽限期期次利息--按日计提
            if currentTerm and currentTerm['current_num'] != repayTerm:
                days = get_day(currentTerm["start_date"], repayDate)
                currentTermInterest = getDailyAccrueInterest(self.productId, days, currentTerm['before_calc_principal'])
            else:
                currentTermInterest = 0
            repay_apply_data["repayInterest"] = round(repay_apply_data["repayInterest"] + currentTermInterest, 2)  # 总利息
            self.log.demsg("宽限期利息：{}".format(repay_apply_data["repayInterest"]))
            repay_apply_data["repayPrincipal"] = float(asset_repay_plan['before_calc_principal'])  # 本金
            repay_apply_data["repayGuaranteeFee"] = repayGuaranteeFee  # 0<担保费<24红线-利息
            repay_apply_data["repayAmount"] = round(
                repay_apply_data["repayPrincipal"] + repay_apply_data["repayInterest"] + repay_apply_data[
                    'repayOverdueFee'] + repay_apply_data["repayFee"] + repayGuaranteeFee, 2)  # 总金额

        # 逾期提前结清
        if repay_type == "10":
            repay_apply_data['repayType'] = "2"
            oveRepayAmt = self.MysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                                    'sum(left_repay_fee)',
                                                                    'sum(pre_repay_interest)',
                                                                    'sum(pre_repay_overdue_fee)',
                                                                    loan_invoice_id=loanInvoiceId,
                                                                    repay_plan_status='4')
            if oveRepayAmt['sum(pre_repay_interest)']:
                left_repay_fee = float("{:.2f}".format(oveRepayAmt['sum(left_repay_fee)']))  # 未还期次费用
                overdue_interest = float("{:.2f}".format(oveRepayAmt['sum(pre_repay_interest)']))  # 未还期次利息
                pre_repay_overdue_fee = float("{:.2f}".format(oveRepayAmt['sum(pre_repay_overdue_fee)']))  # 未还期次罚息
            else:
                left_repay_fee = 0
                overdue_interest = 0
                pre_repay_overdue_fee = 0
            repay_apply_data["repayInterest"] = overdue_interest  # 总利息
            repay_apply_data["repayPrincipal"] = float(asset_repay_plan['before_calc_principal'])  # 本金
            repay_apply_data["repayGuaranteeFee"] = repayGuaranteeFee  # 0<担保费<24红线-利息
            repay_apply_data['repayOverdueFee'] = pre_repay_overdue_fee  # 罚息
            repay_apply_data["repayCompoundInterest"] = left_repay_fee  # 费用
            repay_apply_data["repayAmount"] = round(
                repay_apply_data["repayPrincipal"] + repay_apply_data["repayInterest"] + repay_apply_data[
                    'repayOverdueFee'] + repay_apply_data["repayFee"] + repayGuaranteeFee, 2)  # 总金额

        # 线上还款
        if repay_scene == '01':
            repay_apply_data['repaymentAccountNo'] = self.data['bankid']
            repay_apply_data['repaymentAccountName'] = self.data['name']
            repay_apply_data['repaymentAccountPhone'] = self.data['telephone']
        # 线下还款、逾期还款
        if repay_scene == '02' or '05':
            repay_apply_data['thirdWithholdId'] = 'thirdWithholdId' + strings
        # 支付宝还款
        if repay_scene == '04':
            if not paymentOrder:
                raise Exception("支付宝还款需手动输入（查询支付系统payment_channel_order.PAY_TRANSACTION_ID）")
            repay_apply_data['thirdWithholdId'] = paymentOrder  # 支付宝存量订单
            repay_apply_data['thirdRepayAccountType'] = "支付宝"
            repay_apply_data['appAuthToken'] = 'appAuthToken' + strings
            apollo_data = dict()
            apollo_data['hj.payment.alipay.order.query.switch'] = "1"
            apollo_data['hj.payment.alipay.order.query.tradeAmount'] = round(repay_apply_data["repayAmount"] * 100,
                                                                             2)  # 总金额
            self.apollo.update_config(appId='loan2.1-jcxf-convert', namespace='000', **apollo_data)

        # 更新 payload 字段值
        repay_apply_data.update(kwargs)
        parser = DataUpdate(self.cfg['repay_apply']['payload'], **repay_apply_data)
        self.active_payload = parser.parser

        self.log.demsg('发起还款请求...')
        url = self.host + self.cfg['repay_apply']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 还款查询payload
    def repay_query(self, repayApplySerialNo, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param repayApplySerialNo: 还款申请流水号
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        repay_query_data = dict()
        # head
        repay_query_data['requestSerialNo'] = 'requestNo' + strings + "_1100"
        repay_query_data['requestTime'] = self.date
        repay_query_data['merchantId'] = self.merchantId
        # body
        repay_query_data['repayApplySerialNo'] = repayApplySerialNo

        # 更新 payload 字段值
        repay_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['repay_query']['payload'], **repay_query_data)
        self.active_payload = parser.parser

        self.log.demsg('还款查询请求...')
        url = self.host + self.cfg['repay_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 附件补录
    def supplementAttachment(self, thirdApplyId, fileType=1, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param fileType: 附件类型
        @param thirdApplyId: 渠道申请编号
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        file_data = dict()
        # head
        file_data['requestSerialNo'] = 'requestNo' + strings + "_1300"
        file_data['requestTime'] = self.date
        file_data['merchantId'] = self.merchantId
        # body
        file_data['thirdApplyId'] = thirdApplyId

        # 附件信息
        fileInfos = []
        fileInfo = {'fileType': fileType, 'fileName': "action1.jpg"}
        positive = get_base64_from_img(os.path.join(project_dir(), r'src/test_data/testFile/idCardFile/action1.jpg'))
        # positive = get_base64_from_img(os.path.join(project_dir(), r'src/test_data/testFile/temp/userInfo.txt'))
        fileInfo['file'] = positive  # 身份证正面base64字符串
        fileInfos.append(fileInfo)
        file_data['fileInfos'] = fileInfos

        # 更新 payload 字段值
        file_data.update(kwargs)
        parser = DataUpdate(self.cfg['supplementAttachment']['payload'], **file_data)
        self.active_payload = parser.parser

        self.log.demsg('附件补录...')
        url = self.host + self.cfg['supplementAttachment']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 省市区地址获取
    def getAllAreaInfo(self, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        getAllAreaInfo_data = dict()
        # head
        getAllAreaInfo_data['requestSerialNo'] = 'requestNo' + strings + "_1400"
        getAllAreaInfo_data['requestTime'] = self.date
        getAllAreaInfo_data['merchantId'] = self.merchantId
        # body

        # 更新 payload 字段值
        getAllAreaInfo_data.update(kwargs)
        parser = DataUpdate(self.cfg['getAllAreaInfo']['payload'], **getAllAreaInfo_data)
        self.active_payload = parser.parser

        self.log.demsg('省市区地址获取...')
        url = self.host + self.cfg['getAllAreaInfo']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # LPR查询
    def queryLprInfo(self, thirdApplyId=None, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param thirdApplyId: 三方申请号
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        queryLprInfo_data = dict()
        # head
        queryLprInfo_data['requestSerialNo'] = 'requestNo' + strings + "_1500"
        queryLprInfo_data['requestTime'] = self.date
        queryLprInfo_data['merchantId'] = self.merchantId
        # body
        if not thirdApplyId:
            credit_apply_info = self.MysqlBizImpl.get_credit_apply_info(certificate_no=self.data['cer_no'], status='03')
            queryLprInfo_data['thirdApplyId'] = credit_apply_info['thirdpart_apply_id']
        else:
            queryLprInfo_data['thirdApplyId'] = thirdApplyId
        # 更新 payload 字段值
        queryLprInfo_data.update(kwargs)
        parser = DataUpdate(self.cfg['queryLprInfo']['payload'], **queryLprInfo_data)
        self.active_payload = parser.parser

        self.log.demsg('LPR查询...')
        url = self.host + self.cfg['queryLprInfo']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 授信额度取消
    def cancelCreditLine(self, thirdApplyId=None, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param thirdApplyId: 三方申请号
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        cancelCreditLine_data = dict()
        # head
        cancelCreditLine_data['requestSerialNo'] = 'requestNo' + strings + "_1600"
        cancelCreditLine_data['requestTime'] = self.date
        cancelCreditLine_data['merchantId'] = self.merchantId
        # body
        if not thirdApplyId:
            credit_apply_info = self.MysqlBizImpl.get_credit_apply_info(certificate_no=self.data['cer_no'], status='03')
            cancelCreditLine_data['thirdApplyId'] = credit_apply_info['thirdpart_apply_id']
        else:
            cancelCreditLine_data['thirdApplyId'] = thirdApplyId
        # 更新 payload 字段值
        cancelCreditLine_data.update(kwargs)
        parser = DataUpdate(self.cfg['cancelCreditLine']['payload'], **cancelCreditLine_data)
        self.active_payload = parser.parser

        self.log.demsg('授信额度取消...')
        url = self.host + self.cfg['cancelCreditLine']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 代偿结果查询
    def queryAccountResult(self, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        queryAccountResult_data = dict()
        # head
        queryAccountResult_data['requestSerialNo'] = 'requestNo' + strings + "_1600"
        queryAccountResult_data['requestTime'] = self.date
        queryAccountResult_data['merchantId'] = self.merchantId
        # body
        # if not thirdApplyId:
        #     credit_apply_info = self.MysqlBizImpl.get_credit_apply_info(certificate_no=self.data['cer_no'], status='03')
        #     queryAccountResult_data['thirdApplyId'] = credit_apply_info['thirdpart_apply_id']
        # else:
        #     queryAccountResult_data['thirdApplyId'] = thirdApplyId
        # 更新 payload 字段值
        queryAccountResult_data.update(kwargs)
        parser = DataUpdate(self.cfg['queryAccountResult']['payload'], **queryAccountResult_data)
        self.active_payload = parser.parser

        self.log.demsg('代偿结果查询...')
        url = self.host + self.cfg['queryAccountResult']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 支持的银行列表
    def querySupportBank(self, **kwargs):
        """
        渠道方可调用此接口缓存支持的银行卡列表
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        querySupportBank_data = dict()
        # head
        querySupportBank_data['requestSerialNo'] = 'requestNo' + strings + "_1400"
        querySupportBank_data['requestTime'] = self.date
        querySupportBank_data['merchantId'] = self.merchantId
        # body

        # 更新 payload 字段值
        querySupportBank_data.update(kwargs)
        parser = DataUpdate(self.cfg['querySupportBank']['payload'], **querySupportBank_data)
        self.active_payload = parser.parser

        self.log.demsg('支持银行列表获取...')
        url = self.host + self.cfg['querySupportBank']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 结清证明申请
    def applySettlementCer(self, *args, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        applySettlementCer_data = dict()
        # head
        applySettlementCer_data['requestSerialNo'] = 'requestNo' + strings + "_1400"
        applySettlementCer_data['requestTime'] = self.date
        applySettlementCer_data['merchantId'] = self.merchantId
        # body
        applySettlementCer_data['name'] = self.data['name']
        applySettlementCer_data['idNo'] = self.data['cer_no']
        applySettlementCer_data['mobileNo'] = self.data['telephone']
        applySettlementCer_data['loanApplyIdList'] = list(args)
        # 更新 payload 字段值
        applySettlementCer_data.update(kwargs)
        parser = DataUpdate(self.cfg['applySettlementCer']['payload'], **applySettlementCer_data)
        self.active_payload = parser.parser

        self.log.demsg('结清证明申请...')
        url = self.host + self.cfg['applySettlementCer']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 结清证明下载
    def settlementCerDownload(self, applyId, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param applyId: 结清证明编号
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        settlementCerDownload_data = dict()
        # head
        settlementCerDownload_data['requestSerialNo'] = 'requestNo' + strings + "_1400"
        settlementCerDownload_data['requestTime'] = self.date
        settlementCerDownload_data['merchantId'] = self.merchantId
        # body
        settlementCerDownload_data['name'] = self.data['name']
        settlementCerDownload_data['idNo'] = self.data['cer_no']
        settlementCerDownload_data['applyId'] = applyId
        # 更新 payload 字段值
        settlementCerDownload_data.update(kwargs)
        parser = DataUpdate(self.cfg['settlementCerDownload']['payload'], **settlementCerDownload_data)
        self.active_payload = parser.parser

        self.log.demsg('结清证明下载...')
        url = self.host + self.cfg['settlementCerDownload']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response


if __name__ == '__main__':
    pass
