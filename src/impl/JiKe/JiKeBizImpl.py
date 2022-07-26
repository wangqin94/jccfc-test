# -*- coding: utf-8 -*-
# ------------------------------------------
# 百度接口数据封装类
# ------------------------------------------
import hashlib
from engine.MysqlInit import MysqlInit
from src.enums.EnumsCommon import *
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from src.test_data.module_data import JiKe
from src.impl.common.CommonBizImpl import *
from utils.Apollo import Apollo


def computeMD5(message):
    m = hashlib.md5()
    m.update(message.encode(encoding='utf-8'))
    return m.hexdigest()


def get_jike_bill_day(loan_date=None):
    """
    @param loan_date: 放款时间，如果放款时间空，则默认当前时间 eg:2022-01-01
    @return: 返回首期账单日
    """
    if not loan_date:
        loan_date = time.strftime('%Y-%m-%d', time.localtime())  # 当前时间
    date_list = str(loan_date).split('-')
    bill_year, bill_month, bill_day = map(int, date_list)
    bill_month += 1
    if bill_month > 12:
        bill_year += 1
        bill_month -= 12
    bill_day = 28 if bill_day > 27 else bill_day
    bill_data = '{}-{}-{}'.format(str(bill_year), str("%02d" % bill_month), str("%02d" % bill_day))
    return bill_data

# # -----------------------------------------------------------
# # - 等额本息计算2
# # -----------------------------------------------------------
def jike_loanByAvgAmt2(bill_date, loanAmt, repaymentRate, loanNumber):
    """
    @param loanAmtDate: 首期账单日期
    @param loanAmt: 放款总金额
    @param repaymentRate: 年利率,如9.7%传9.7
    @param loanNumber: 放款期数
    @return: 还款计划列表
    """
    repayment_plan = []

    # 月利率
    monthRate = round(repaymentRate/100/12,20)
    perPeriodAmountMultiply = loanAmt
    perPeriodAmountMultiplicand = monthRate*(monthRate+1)**loanNumber
    perPeriodAmountDivisor = (monthRate+1)**loanNumber-1
    perPeriodAmountSum = round(perPeriodAmountMultiply*perPeriodAmountMultiplicand/perPeriodAmountDivisor,64)
    # 剩余本金
    residualPrincipalTotal = loanAmt
    # 剩余利息
    residualInterestTotal = perPeriodAmountSum*loanNumber-loanAmt

    for i in range(1, loanNumber + 1):
        isLastPeriod = i==loanNumber

        interestMultiply = loanAmt*monthRate
        interestMultiplicand = (monthRate+1)**loanNumber-(monthRate+1)**(i-1)
        interestdDivisor = (monthRate+1)**loanNumber-1
        interest = residualInterestTotal if isLastPeriod else round(interestMultiply*interestMultiplicand/interestdDivisor,64)
        principal = residualPrincipalTotal if isLastPeriod else perPeriodAmountSum-interest
        interest = round(interest,2)
        principal = round(principal,2)
        # 计算本金利息
        residualPrincipalTotal = residualPrincipalTotal-principal
        residualInterestTotal = residualInterestTotal-interest
        repaymentPlans = {}
        # 期次
        repaymentPlans['period'] = i
        # 账单日
        repaymentPlans['billDate'] = get_custom_month(i - 1, bill_date)
        # 本金
        repaymentPlans['principalAmt'] = int(principal*100)
        # 利息
        repaymentPlans['interestAmt'] = int(interest*100)
        # 服务费
        repaymentPlans['guaranteeAmt'] = 111
        repayment_plan.append(repaymentPlans)
    return repayment_plan

# # -----------------------------------------------------------
# # - 等额本息计算
# # -----------------------------------------------------------
def jike_loanByAvgAmt(loanamt, term, year_rate_jc, year_rate_jk, bill_date):
    """

    @param loanamt:         借款金额
    @param term:            期数
    @param year_rate_jc:    锦程实收利率
    @param year_rate_jk:    即科对客放款利率
    @param bill_date:       用户首期账单日
    @return:还款计划表
    """
    repayment_plan = []
    repaymentPlans = {}
    # 月利率
    month_rate_jc = year_rate_jc / 1200
    month_rate_jk = year_rate_jk / 1200
    # 每月还款总额
    amtpermonth_jc = loanamt * month_rate_jc * pow((1 + month_rate_jc), term) / (pow((1 + month_rate_jc), term) - 1)
    amtpermonth_jk = loanamt * month_rate_jk * pow((1 + month_rate_jk), term) / (pow((1 + month_rate_jk), term) - 1)
    for i in range(1, term + 1):
        if i == 1:
            # 第一个月还款利息
            month_interest_jc = loanamt * month_rate_jc
            month_interest_jk = loanamt * month_rate_jk
        else:
            # 第2-n个月还款利息
            month_interest_jc = (loanamt * month_rate_jc - amtpermonth_jc) * pow((1 + month_rate_jc),
                                                                                 (i - 1)) + amtpermonth_jc
            month_interest_jk = (loanamt * month_rate_jk - amtpermonth_jk) * pow((1 + month_rate_jc),
                                                                                 (i - 1)) + amtpermonth_jk
        # 应还本金
        month_principal = amtpermonth_jc - month_interest_jc
        month_principal = round(month_principal, 2)
        month_interest = round(month_interest_jc, 2)
        repaymentPlans['period'] = i
        repaymentPlans['billDate'] = get_custom_month(i - 1, bill_date)
        repaymentPlans['principalAmt'] = int(month_principal * 100)
        repaymentPlans['interestAmt'] = int(month_interest * 100)
        repaymentPlans['guaranteeAmt'] = int(round((month_interest_jk - month_interest_jc), 2) * 100)
        repayment_plan.append(repaymentPlans)
    return repayment_plan


class JiKeBizImpl(MysqlInit):
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
        self.cfg = JiKe.JiKe
        self.encrypt_flag = encrypt_flag
        self.strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 当前时间
        self.times = str(int(round(time.time() * 1000)))  # 当前13位时间戳
        self.data = self.get_user_info(data=data, person=person)

        # 初始化payload变量
        self.active_payload = {}

        self.encrypt_url = self.host + self.cfg['encrypt']['interface']
        self.decrypt_url = self.host + self.cfg['decrypt']['interface']

    def get_user_info(self, data=None, person=True):
        # 获取四要素信息
        if data:
            base_data = data
        else:
            if person:
                base_data = get_base_data(str(self.env) + ' -> ' + str(ProductEnum.JIKE.value))
            else:
                base_data = get_base_data_temp()
        return base_data

    # 发起代扣协议申请
    def sharedWithholdingAgreement(self, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        sharedWithholdingAgreement = dict()
        # head
        sharedWithholdingAgreement['requestSerialNo'] = 'requestNo' + self.strings + "_1000"
        sharedWithholdingAgreement['requestTime'] = self.date
        # body
        sharedWithholdingAgreement['aggrementNum'] = 'aggrementNum' + self.strings
        sharedWithholdingAgreement['payerIdNum'] = self.data['cer_no']
        sharedWithholdingAgreement['payer'] = self.data['name']
        sharedWithholdingAgreement['payerBankCardNum'] = self.data['bankid']
        sharedWithholdingAgreement['payerPhoneNum'] = self.data['telephone']
        sharedWithholdingAgreement['agreementTime'] = self.date

        # 更新 payload 字段值
        sharedWithholdingAgreement.update(kwargs)
        parser = DataUpdate(self.cfg['sharedWithholdingAgreement']['payload'], **sharedWithholdingAgreement)
        self.active_payload = parser.parser

        self.log.demsg('发起绑卡请求...')
        url = self.host + self.cfg['sharedWithholdingAgreement']['interface']
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
        queryWithholdingAgreement = dict()
        # head
        queryWithholdingAgreement['requestSerialNo'] = 'requestNo' + self.strings + "_1000"
        queryWithholdingAgreement['requestTime'] = self.date
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

    # 换卡通知接口
    def updateWithholdCard(self, loanInvoiceId, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param loanInvoiceId: 锦程借据号
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return:
        """
        updateWithholdCard = dict()
        # head
        updateWithholdCard['requestSerialNo'] = 'requestNo' + self.strings + "_1000"
        updateWithholdCard['requestTime'] = self.date

        # body
        updateWithholdCard['idNo'] = self.data['cer_no']
        updateWithholdCard['loanInvoiceId'] = loanInvoiceId
        # 新银行卡号
        updateWithholdCard['repaymentAccountNo'] = BankNo().get_bank_card()

        # 更新 payload 字段值
        updateWithholdCard.update(kwargs)
        parser = DataUpdate(self.cfg['updateWithholdCard']['payload'], **updateWithholdCard)
        self.active_payload = parser.parser

        self.log.demsg('换卡通知请求...')
        url = self.host + self.cfg['updateWithholdCard']['interface']
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
        self.log.info('用户四要素信息: {}'.format(self.data))
        credit_data = dict()
        # head
        credit_data['requestSerialNo'] = 'requestNo' + self.strings + "_2000"
        credit_data['requestTime'] = self.date
        # body

        credit_data['thirdApplyId'] = 'thirdApplyId' + self.strings
        credit_data['interestRate'] = 23.4
        credit_data['applyAmount'] = applyAmount
        # 临时新增参数
        credit_data['orderType'] = '1' #应传2
        credit_data['storeCode'] = 'store20220725'

        # 用户信息
        credit_data['idNo'] = self.data['cer_no']
        credit_data['name'] = self.data['name']
        credit_data['reserveMobile'] = self.data['telephone']
        credit_data['mobileNo'] = self.data['telephone']

        # 银行卡信息
        credit_data['userBankCardNo'] = self.data['bankid']

        # 更新 payload 字段值
        credit_data.update(kwargs)

        parser = DataUpdate(self.cfg['credit_apply']['payload'], **credit_data)
        self.active_payload = parser.parser

        # 校验用户是否已存在
        self.MysqlBizImpl.check_user_available(self.data)

        # 配置风控mock返回建议额度与授信额度一致
        apollo_data = dict()
        apollo_data['hj.channel.risk.credit.line.amt.mock'] = self.active_payload['body']['applyAmount']
        self.apollo.update_config(appId='loan2.1-jcxf-credit', **apollo_data)

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
        queryCreditResult_data = dict()
        # head
        queryCreditResult_data['requestSerialNo'] = 'requestNo' + self.strings + "_3000"
        queryCreditResult_data['requestTime'] = self.date

        if not thirdApplyId:
            credit_apply_info = self.MysqlBizImpl.get_credit_apply_info(certificate_no=self.data['cer_no'])
            queryCreditResult_data['thirdApplyId'] = credit_apply_info['thirdpart_apply_id']

        # 更新 payload 字段值
        queryCreditResult_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit_query']['payload'], **queryCreditResult_data)
        self.active_payload = parser.parser

        self.log.demsg('授信查询请求...')
        url = self.host + self.cfg['credit_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 支用申请
    def applyLoan(self, loan_date=None, loanTerm=12, loanAmt=1000, thirdApplyId=None, rate=23.4, **kwargs):
        """ # 支用申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        @param rate: 支用利率
        @param loan_date: 放款时间，默认当前时间 eg:2022-01-01
        @param thirdApplyId: 三方申请号，与授信申请号一致
        @param loanAmt: 支用申请金额, 默认1000 单位元
        @param loanTerm: 借款期数：默认12期
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json response 接口响应参数 数据类型：json
        """
        self.log.info('用户四要素信息: {}'.format(self.data))
        applyLoan_data = dict()
        # head
        applyLoan_data['requestSerialNo'] = 'requestNo' + self.strings + "_4000"
        applyLoan_data['requestTime'] = self.date
        # body
        if not thirdApplyId:
            credit_apply_info = self.MysqlBizImpl.get_credit_apply_info(certificate_no=self.data['cer_no'], status='03')
            applyLoan_data['thirdApplyId'] = credit_apply_info['thirdpart_apply_id']

        applyLoan_data['loanApplyNo'] = 'loanApplyNo' + self.strings

        # 设置apollo放款mock时间 默认当前时间
        if loan_date:
            apollo_data = dict()
            apollo_data['credit.loan.trade.date.mock'] = "true"
            apollo_data['credit.loan.date.mock'] = loan_date
            self.apollo.update_config(appId='loan2.1-public', namespace='JCXF.system', **apollo_data)
        else:
            loan_date = time.strftime('%Y-%m-%d', time.localtime())  # 当前时间

        # 首期还款日
        firstRepayDate = get_jike_bill_day(loan_date)
        applyLoan_data['firstRepayDate'] = firstRepayDate
        applyLoan_data['fixedRepayDay'] = firstRepayDate.split('-')[2]

        applyLoan_data['loanAmt'] = loanAmt
        applyLoan_data['loanTerm'] = loanTerm
        applyLoan_data['interestRate'] = rate

        # 用户信息
        applyLoan_data['idNo'] = self.data['cer_no']
        applyLoan_data['mobileNo'] = self.data['telephone']
        applyLoan_data['reserveMobile'] = self.data['telephone']
        applyLoan_data['name'] = self.data['name']
        applyLoan_data['accountNo'] = self.data['bankid']

        # 担保合同号
        applyLoan_data['guaranteeContractNo'] = 'ContractNo' + self.strings + "_5000"

        # 还款计划
        # applyLoan_data['repaymentPlans'] = jike_loanByAvgAmt(loanAmt, loanTerm, year_rate_jc=9.7, year_rate_jk=rate, bill_date=firstRepayDate)
        applyLoan_data['repaymentPlans'] = jike_loanByAvgAmt2(bill_date=firstRepayDate,loanAmt=loanAmt,repaymentRate=9.7,loanNumber=loanTerm)
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
        # head
        queryLoanResult_data['requestSerialNo'] = 'requestNo' + self.strings + "_6000"
        queryLoanResult_data['requestTime'] = self.date

        if not thirdApplyId:
            credit_apply_info = self.MysqlBizImpl.get_credit_apply_info(certificate_no=self.data['cer_no'])
            queryLoanResult_data['thirdApplyId'] = credit_apply_info['thirdpart_apply_id']

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
        repayPlan_query_data = dict()
        # head
        repayPlan_query_data['requestSerialNo'] = 'requestNo' + self.strings + "_7000"
        repayPlan_query_data['requestTime'] = self.date

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
        loanContract_query_data = dict()
        # head
        loanContract_query_data['requestSerialNo'] = 'requestNo' + self.strings + "_8000"
        loanContract_query_data['requestTime'] = self.date

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
        return response

    # 还款申请
    def repay_apply(self, loanInvoiceId, repay_scene='01', repay_type='1', repayGuaranteeFee=1, **kwargs):
        """ # 还款申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        @param repayGuaranteeFee: 担保费， 0<担保费<24红线-利息
        @param repay_scene: 还款场景 EnumRepayScene ("01", "线上还款"),("02", "线下还款"),（"04","支付宝还款通知"）（"05","逾期（代偿、回购后）还款通知"）
        @param loanInvoiceId: 借据号 必填
        @param repay_type： 还款类型 1 按期还款； 2 提前结清； 7 提前还当期
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        self.log.info('用户四要素信息: {}'.format(self.data))
        repay_apply_data = dict()
        # head
        repay_apply_data['requestSerialNo'] = 'requestNo' + self.strings + "_9000"
        repay_apply_data['requestTime'] = self.date
        # body
        repay_apply_data['repayApplySerialNo'] = 'repayApplySerialNo' + self.strings
        repay_apply_data['loanInvoiceId'] = loanInvoiceId
        repay_apply_data['repayScene'] = repay_scene

        if repay_scene == '01':  # 线上还款
            repay_apply_data['repaymentAccountNo'] = self.data['bankid']
        if repay_scene == '02' or '05':  # 线下还款、逾期还款
            repay_apply_data['thirdWithholdId'] = 'thirdWithholdId' + self.strings
        if repay_scene == '04':  # 支付宝还款
            repay_apply_data['thirdWithholdId'] = repay_apply_data['repayApplySerialNo']
            repay_apply_data['appAuthToken'] = 'appAuthToken' + self.strings

        repay_apply_data['repayType'] = repay_type
        key = "loan_invoice_id = '{}' and repay_plan_status = '1' ORDER BY 'current_num'".format(
            loanInvoiceId)
        asset_repay_plan = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key)
        self.log.demsg('当期最早未还期次{}'.format(asset_repay_plan['current_num']))
        repay_apply_data['repayNum'] = int(asset_repay_plan['current_num'])
        repay_apply_data["repayInterest"] = float(asset_repay_plan['pre_repay_interest'])  # 利息
        repay_apply_data["repayGuaranteeFee"] = repayGuaranteeFee  # 0<担保费<24红线-利息
        repay_apply_data["repayFee"] = float(asset_repay_plan['pre_repay_fee'])  # 费用
        repay_apply_data["repayOverdueFee"] = float(asset_repay_plan['pre_repay_overdue_fee'])  # 逾期罚息
        repay_apply_data["repayCompoundInterest"] = float(asset_repay_plan['pre_repay_compound_interest'])  # 手续费

        # 按期还款、提前当期
        if repay_type == "1" or "7":
            repay_apply_data["repayAmount"] = float(asset_repay_plan['pre_repay_amount']) + repayGuaranteeFee  # 总金额
            repay_apply_data["repayPrincipal"] = float(asset_repay_plan['pre_repay_principal'])  # 本金

        # 提前结清
        if repay_type == "2":
            repay_apply_data["repayPrincipal"] = float(asset_repay_plan['before_calc_principal'])  # 本金
            repay_apply_data["repayAmount"] = repay_apply_data["repayPrincipal"] + repay_apply_data[
                "repayInterest"] + repayGuaranteeFee  # 总金额

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
        repay_query_data = dict()
        # head
        repay_query_data['requestSerialNo'] = 'requestNo' + self.strings + "_1100"
        repay_query_data['requestTime'] = self.date
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

    # 退货申请
    def returnGoods_apply(self, loanInvoiceId, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param loanInvoiceId: 借据号 必填
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        returnGoods_apply_data = dict()
        # head
        returnGoods_apply_data['requestSerialNo'] = 'requestNo' + self.strings + "_1200"
        returnGoods_apply_data['requestTime'] = self.date
        # body
        returnGoods_apply_data['loanInvoiceId'] = loanInvoiceId
        returnGoods_apply_data['returnGoodsSerialNo'] = 'GoodsSerialNo' + self.strings

        # 计算剩余应还本金(最早未还期次:期初计息余额before_calc_principal)
        key = "loan_invoice_id = '{}' and (repay_plan_status = '1' or repay_plan_status = '4') ORDER BY 'current_num'".format(
            loanInvoiceId)
        asset_repay_plan = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key)
        returnGoods_apply_data["returnGoodsPrincipal"] = float(asset_repay_plan['before_calc_principal'])  # 本金

        # 计算退货应收利息=当期利息+未还期次利息
        key = "loan_invoice_id = '{}' and repay_plan_status = '1' ORDER BY 'current_num'".format(
            loanInvoiceId)
        asset_repay_plan = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key)
        dangqi_interest = float(asset_repay_plan['pre_repay_interest'])  # 当期利息
        repayAmt = self.MysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                             'sum(pre_repay_interest)',
                                                             'sum(pre_repay_overdue_fee)',
                                                             loan_invoice_id=loanInvoiceId,
                                                             repay_plan_status='4')
        if repayAmt['sum(pre_repay_interest)']:
            weihuan_interest = float("{:.2f}".format(repayAmt['sum(pre_repay_interest)']))  # 未还期次利息
            pre_repay_overdue_fee = float("{:.2f}".format(repayAmt['sum(pre_repay_overdue_fee)']))  # 未还期次罚息
        else:
            weihuan_interest = 0
            pre_repay_overdue_fee = 0
        returnGoods_apply_data['returnGoodsInterest'] = dangqi_interest + weihuan_interest

        # 罚息
        returnGoods_apply_data['returnGoodsOverdueFee'] = pre_repay_overdue_fee

        # 更新 payload 字段值
        returnGoods_apply_data.update(kwargs)
        parser = DataUpdate(self.cfg['returnGoods_apply']['payload'], **returnGoods_apply_data)
        self.active_payload = parser.parser

        self.log.demsg('还款查询请求...')
        url = self.host + self.cfg['returnGoods_apply']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 附件补录
    def supplementAttachment(self, thirdApplyId, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param thirdApplyId: 渠道申请编号
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        file_data = dict()
        # head
        file_data['requestSerialNo'] = 'requestNo' + self.strings + "_1300"
        file_data['requestTime'] = self.date
        # body
        file_data['thirdApplyId'] = thirdApplyId

        # 附件信息
        fileInfos = []
        fileInfo = {'fileType': "1", 'fileName': "cqid1.png"}
        positive = get_base64_from_img(os.path.join(project_dir(), r'src/test_data/testFile/idCardFile/cqid1.png'))
        fileInfo['file'] = positive  # 身份证正面base64字符串
        file_data['fileInfos'] = fileInfos.append(fileInfo)

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
        getAllAreaInfo_data = dict()
        # head
        getAllAreaInfo_data['requestSerialNo'] = 'requestNo' + self.strings + "_1400"
        getAllAreaInfo_data['requestTime'] = self.date
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
    def queryLprInfo(self, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        queryLprInfo_data = dict()
        # head
        queryLprInfo_data['requestSerialNo'] = 'requestNo' + self.strings + "_1500"
        queryLprInfo_data['requestTime'] = self.date
        # body

        # 更新 payload 字段值
        queryLprInfo_data.update(kwargs)
        parser = DataUpdate(self.cfg['queryLprInfo']['payload'], **queryLprInfo_data)
        self.active_payload = parser.parser

        self.log.demsg('LPR查询...')
        url = self.host + self.cfg['queryLprInfo']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response
