# -*- coding: utf-8 -*-
# ------------------------------------------
# 哈喽接口数据封装类
# ------------------------------------------
from dateutil.parser import parse

from engine.MysqlInit import MysqlInit
from src.enums.EnumsCommon import *
from src.impl.common.CommonBizImpl import *
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from src.impl.public.YinLiuBizImpl import YinLiuBizImpl
from src.test_data.module_data import HaLo
from utils.Apollo import Apollo
from utils.FileHandle import Files


def computeMD5(message):
    m = hashlib.md5()
    m.update(message.encode(encoding='utf-8'))
    return m.hexdigest()


def get_bill_day(loan_date=None):
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


class HaLoBizImpl(MysqlInit):
    def __init__(self, merchantId=None, data=None, encrypt_flag=True, person=True):
        """
        @param merchantId: 商户ID 默认值：G23E03HALO
        @param data: 四要素 为空系统随机获取，若person=True四要输写入person文件
        @param encrypt_flag: 接口加密标识，默认加密
        @param person: 若person=True四要输写入person文件，否则不写入
        """
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()
        self.apollo = Apollo()
        # 解析项目特性配置
        self.cfg = HaLo.HaLo
        self.encrypt_flag = encrypt_flag
        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 当前时间
        self.times = str(int(round(time.time() * 1000)))  # 当前13位时间戳
        self.data = self.get_user_info(data=data, person=person)
        self.interestRate = getInterestRate(ProductIdEnum.HALO.value)

        # 初始化商户
        self.merchantId = merchantId if merchantId else EnumMerchantId.HALO.value
        # 初始化产品
        self.productId = ProductIdEnum.HALO.value
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
                base_data = get_base_data(str(self.env) + ' -> ' + str(ProductEnum.HaLo.value))
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
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        sharedWithholdingAgreement = dict()
        # head
        sharedWithholdingAgreement['requestSerialNo'] = 'requestNo' + strings + "_1000"
        sharedWithholdingAgreement['requestTime'] = self.date
        sharedWithholdingAgreement['merchantId'] = self.merchantId
        # body
        sharedWithholdingAgreement['aggrementNum'] = 'aggrementNum' + strings
        sharedWithholdingAgreement['payerIdNum'] = self.data['cer_no']
        sharedWithholdingAgreement['payer'] = self.data['name']
        sharedWithholdingAgreement['mobileNo'] = self.data['telephone']
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
        credit_data['interestRate'] = self.interestRate
        credit_data['applyAmount'] = applyAmount
        # 临时新增参数
        credit_data['orderType'] = '1'  # 固定传1-取现

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

    # 支用申请
    def applyLoan(self, loanTerm=6, loanAmt=1000, thirdApplyId=None, loan_date=None, **kwargs):
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

        # 首期还款日
        firstRepayDate = get_bill_day(loan_date)
        applyLoan_data['firstRepayDate'] = firstRepayDate
        applyLoan_data['fixedRepayDay'] = firstRepayDate.split('-')[2]

        applyLoan_data['loanAmt'] = loanAmt
        applyLoan_data['loanTerm'] = loanTerm
        applyLoan_data['interestRate'] = self.interestRate

        # 用户信息
        applyLoan_data['idNo'] = self.data['cer_no']
        applyLoan_data['mobileNo'] = self.data['telephone']
        applyLoan_data['reserveMobile'] = self.data['telephone']
        applyLoan_data['name'] = self.data['name']
        applyLoan_data['accountNo'] = self.data['bankid']

        # 担保合同号
        applyLoan_data['guaranteeContractNo'] = 'ContractNo' + strings + "_5000"

        # 还款计划
        applyLoan_data['repaymentPlans'] = yinLiuRepayPlanByAvgAmt(billDate=firstRepayDate, loanAmt=loanAmt,
                                                                   yearRate=self.interestRate, term=loanTerm)
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

    # 还款申请
    def repay_apply(self, loanInvoiceId, repay_scene='01', repay_type='1', repayTerm=None, repayGuaranteeFee=1,
                    repayDate=None, paymentOrder=None, **kwargs):
        """ # 还款申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        @param repayTerm: 还款期次，默认取当前借据最早未还期次
        @param repayDate: 还款时间，默认当天 eg:'2022-08-01'
        @param repayGuaranteeFee: 担保费， 0<担保费<24红线-利息
        @param repay_scene: 还款场景 EnumRepayScene ("01", "线上还款"),("02", "线下还款"),（"04","支付宝还款通知"）（"05","逾期（代偿、回购后）还款通知"）
        @param loanInvoiceId: 借据号 必填
        @param repay_type： 还款类型 1 按期还款； 2 提前结清； 7 提前还当期
        @param paymentOrder: 支付宝订单号，支付宝还款需手动输入（查询支付系统payment_channel_order.PAY_TRANSACTION_ID）
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        self.log.demsg('用户四要素信息: {}'.format(self.data))
        repayDate = repayDate if repayDate else time.strftime('%Y-%m-%d', time.localtime())
        repay_apply_data = dict()
        # head
        repay_apply_data['requestSerialNo'] = 'requestNo' + strings
        repay_apply_data['requestTime'] = self.date
        repay_apply_data['merchantId'] = self.merchantId
        # body
        bodyData = YinLiuBizImpl().repayApiBodyData(self.data, self.productId, loanInvoiceId, repay_scene,
                                                    repay_type, repayTerm, repayGuaranteeFee, repayDate,
                                                    paymentOrder)

        repay_apply_data.update(bodyData)
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

    # 退货申请
    def returnGoods_apply(self, loanInvoiceId, term, repayDate, **kwargs):
        """
        注意：键名必须与接口原始数据的键名一致
        @param term: 当前待还期次
        @param repayDate: 退货时间
        @param loanInvoiceId: 借据号 必填
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        returnGoods_apply_data = dict()
        # head
        returnGoods_apply_data['requestSerialNo'] = 'requestNo' + strings + "_1200"
        returnGoods_apply_data['requestTime'] = self.date
        returnGoods_apply_data['merchantId'] = self.merchantId
        # body
        returnGoods_apply_data['loanInvoiceId'] = loanInvoiceId
        returnGoods_apply_data['returnGoodsSerialNo'] = 'GoodsSerialNo' + strings

        # 计算剩余应还本金(最早未还期次:期初计息余额before_calc_principal)
        key = "loan_invoice_id = '{}' and repay_plan_status in('1','4') ORDER BY 'current_num'".format(
            loanInvoiceId)
        asset_repay_plan = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key)
        returnGoods_apply_data["returnGoodsPrincipal"] = float(asset_repay_plan['before_calc_principal'])  # 本金

        # 当期已还款，利息0
        days = get_day(asset_repay_plan["start_date"], repayDate)
        # 如果当期已还款，提前还款利息应收0
        if days <= 0:
            returnGoods_apply_data["returnGoodsInterest"] = 0

        # 计算退货应收利息， 放款7日内退货不收罚息
        credit_loan_invoice = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                         loan_invoice_id=loanInvoiceId)
        loanDate = str(credit_loan_invoice['loan_pay_time']).split()[0]
        # loanDate = datetime.strptime(loanDate, '%Y-%m-%d').date()
        # date = datetime.strptime(date, '%Y-%m-%d').date()
        loanDate = parse(loanDate)
        repayDateFormat = parse(repayDate)
        if 7 > int((repayDateFormat - loanDate).days):
            returnGoods_apply_data['returnGoodsInterest'] = 0
            returnGoods_apply_data['returnGoodsOverdueFee'] = 0
        else:
            asset_repay_plan = self.MysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                                         loan_invoice_id=loanInvoiceId,
                                                                         repay_plan_status='1',
                                                                         current_num=term)
            dangqi_interest = float(asset_repay_plan['pre_repay_interest'])  # 当期利息
            # 宽限期借据=应收当期利息+宽限期期次利息，账单日前只收当期利息
            key = "loan_invoice_id = '{}' and repay_plan_status = '1' and overdue_days in (1,2,3) ORDER BY 'current_num'".format(
                loanInvoiceId)
            KXQRepayAmt = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key)
            kuanxianqi_interest = float(KXQRepayAmt['pre_repay_interest']) if KXQRepayAmt else 0  # 宽限期利息
            # 逾期借据=逾期期次利息+当期利息
            oveRepayAmt = self.MysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                                    'sum(pre_repay_interest)',
                                                                    'sum(pre_repay_overdue_fee)',
                                                                    loan_invoice_id=loanInvoiceId,
                                                                    repay_plan_status='4')
            if oveRepayAmt['sum(pre_repay_interest)']:
                weihuan_interest = float("{:.2f}".format(oveRepayAmt['sum(pre_repay_interest)']))  # 未还期次利息
                pre_repay_overdue_fee = float("{:.2f}".format(oveRepayAmt['sum(pre_repay_overdue_fee)']))  # 未还期次罚息
            else:
                weihuan_interest = 0
                pre_repay_overdue_fee = 0
            returnGoods_apply_data['returnGoodsInterest'] = float("{:.2f}".format(dangqi_interest + weihuan_interest +
                                                                                  kuanxianqi_interest))

            # 罚息
            returnGoods_apply_data['returnGoodsOverdueFee'] = pre_repay_overdue_fee

        # 更新退货mock时间
        apollo_data = dict()
        apollo_data['yinliu.return.goods.trade.date.mock'] = "true"
        apollo_data['yinliu.return.goods.date.mock'] = str(repayDate).replace('-', '')
        self.apollo.update_config(appId='jccfc-op-channel', namespace='000', **apollo_data)
        time.sleep(3)
        # 配置还款mock时间
        apollo_data = dict()
        apollo_data['credit.mock.repay.trade.date'] = "true"  # credit.mock.repay.trade.date
        apollo_data['credit.mock.repay.date'] = "{} 00:00:00".format(repayDate)
        self.apollo.update_config(appId='loan2.1-public', namespace='JCXF.system', **apollo_data)

        # 更新 payload 字段值
        returnGoods_apply_data.update(kwargs)
        parser = DataUpdate(self.cfg['returnGoods_apply']['payload'], **returnGoods_apply_data)
        self.active_payload = parser.parser

        self.log.demsg('退货请求...')
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
        fileInfo = {'fileType': "13", 'fileName': "userInfo.txt"}
        positive = get_base64_from_img(os.path.join(project_dir(), r'src/test_data/testFile/temp/userInfo.txt'))
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

    # H5还款申请payload
    def payment(self, loan_invoice_id=None, repay_type='0', payment_type="5", repayTerm=None, **kwargs):
        """
        还款申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        @param repayTerm: 还款期次
        @param loan_invoice_id: 借据号 默认不传根据身份证号获取
        @param repay_type: 还款类型 0：按期还款； 1：提前结清
        @param payment_type： 1 支付宝主动还款 5 银行卡主动还款 6 银行卡代扣
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json response 接口响应参数 数据类型：json
        """
        self.log.demsg('准备锦程H5还款申请报文...')
        data = dict()
        # head
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        requestSerialNo = 'SerialNo' + strings + "2"
        data['requestSerialNo'] = requestSerialNo

        # body
        data['repayType'] = repay_type
        if not loan_invoice_id:
            # 根据用户名称查询借据信息
            key1 = "user_name = '{}'".format(self.data['name'])
            credit_loan_invoice = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key1)
            loan_invoice_id = credit_loan_invoice["loan_invoice_id"]
        data['loanInvoiceId'] = loan_invoice_id

        data['paymentType'] = payment_type
        data['appOrderNo'] = 'appOrderNo' + strings
        data['userName'] = self.data['name']
        if payment_type == "5" or payment_type == "6":
            data['idNo'] = self.data['cer_no']
            data['bankAcctNo'] = self.data['bankid']
            # data['bankAcctName'] = '{}_{}_1022'.format(self.data['name'], "SUCCESS")
            data['bankAcctName'] = self.data['name']
            data['phoneNum'] = self.data['telephone']

        credit_offline_payment_apply = self.MysqlBizImpl.get_credit_database_info('credit_offline_payment_apply',
                                                                                  invoice_id=loan_invoice_id,
                                                                                  periods=repayTerm)
        data['repayAmt'] = round(
            float(credit_offline_payment_apply['repay_total']) + float(credit_offline_payment_apply['other_cost']), 2)
        data['paymentOrderNo'] = credit_offline_payment_apply['payment_order_no']
        # 更新 payload 字段值
        data.update(kwargs)
        parser = DataUpdate(self.cfg['payment']['payload'], **data)
        self.active_payload = parser.parser
        self.active_payload["head"]["jcSystemEncry"] = computeMD5(
            requestSerialNo + self.active_payload["head"]["jcSystemCode"])

        self.log.demsg('发起锦程H5还款申请...')
        url = API['request_host_corp_api'].format(self.env) + self.cfg['payment']['interface']
        response = post_with_encrypt(url, self.active_payload, encrypt_flag=False)
        return response

    # H5还款订单查询申请
    def queryRepaymentApply(self, paymentOrderNo, **kwargs):
        """
        H5还款订单查询申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        @param paymentOrderNo： 订单号
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json response 接口响应参数 数据类型：json
        """
        self.log.demsg('准备锦程H5还款申请报文...')
        data = dict()
        # head
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        requestSerialNo = 'SerialNo' + strings + "2"
        data['requestSerialNo'] = requestSerialNo

        # 更新 payload 字段值
        data['paymentOrderNo'] = paymentOrderNo
        data.update(kwargs)
        parser = DataUpdate(self.cfg['payment']['payload'], **data)
        self.active_payload = parser.parser

        self.log.demsg('发起锦程H5还款申请...')
        url = API['request_host_corp_api'].format(self.env) + self.cfg['payment']['interface']
        response = post_with_encrypt(url, self.active_payload, encrypt_flag=False)
        return response

    # 渠道线下还款申请
    def offlineRepayApply(self, loanInvoiceId, repayType='1', repayTerm=1, repayGuaranteeFee=1, **kwargs):
        """ # 还款申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        @param repayTerm: 还款期次，默认取当前借据最早未还期次
        @param repayGuaranteeFee: 担保费， 0<担保费<24红线-利息
        @param loanInvoiceId: 借据号 必填
        @param repayType： 还款类型 1 按期还款； 2 提前结清； 7 提前还当期
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        self.log.demsg('用户四要素信息: {}'.format(self.data))
        repay_apply_data = dict()
        # head
        repay_apply_data['requestSerialNo'] = 'requestNo' + strings
        repay_apply_data['requestTime'] = self.date
        repay_apply_data['merchantId'] = self.merchantId
        # body
        repay_apply_data['receiveTelephone'] = self.data['telephone']
        repay_apply_data['invoiceId'] = loanInvoiceId
        repay_apply_data['repayType'] = repayType
        repay_apply_data['periods'] = repayTerm
        repay_apply_data['otherCost'] = repayGuaranteeFee

        # 更新 payload 字段值
        repay_apply_data.update(kwargs)
        parser = DataUpdate(self.cfg['repaymentApply']['payload'], **repay_apply_data)
        self.active_payload = parser.parser

        self.log.demsg('发起线下还款请求...')
        url = self.host + self.cfg['repaymentApply']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 还款实权
    def repayTrial(self, loanInvoiceId, repayDate, repayType='1', repayTerm=1, **kwargs):
        """ # 还款申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        @param repayTerm: 还款期次，默认取当前借据最早未还期次
        @param loanInvoiceId: 借据号 必填
        @param repayType： 还款类型 1 按期还款； 2 提前结清； 7 提前还当期
        @param repayDate: 还款时间，默认当天 eg:'2022-08-01'
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        self.log.demsg('用户四要素信息: {}'.format(self.data))
        repay_apply_data = dict()
        # head
        repay_apply_data['requestSerialNo'] = 'requestNo' + strings
        repay_apply_data['requestTime'] = self.date
        repay_apply_data['merchantId'] = self.merchantId
        # body
        repay_apply_data['loanInvoiceId'] = loanInvoiceId
        repay_apply_data['repayType'] = repayType
        repay_apply_data['repayTerm'] = repayTerm
        repay_apply_data['repayDate'] = repayDate

        # 更新 payload 字段值
        repay_apply_data.update(kwargs)
        parser = DataUpdate(self.cfg['repayTrial']['payload'], **repay_apply_data)
        self.active_payload = parser.parser

        self.log.demsg('发起还款试算请求...')
        url = self.host + self.cfg['repayTrial']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response


if __name__ == '__main__':
    s = yinLiuRepayPlanByAvgAmt(billDate='2023-03-18', loanAmt=10000, yearRate=9.5, term=12)
    print(json.dumps(s))
