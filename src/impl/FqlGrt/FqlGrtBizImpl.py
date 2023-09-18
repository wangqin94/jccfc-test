# -*- coding: utf-8 -*-
# ------------------------------------------
# 分期乐半增信数据封装类
# ------------------------------------------

from engine.MysqlInit import MysqlInit
from src.enums.EnumsCommon import *
from src.impl.common.CommonBizImpl import *
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from src.test_data.module_data import FqlGrt
from utils.Apollo import Apollo


class FqlGrtBizImpl(MysqlInit):
    def __init__(self, data=None, encrypt_flag=True, person=True):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()
        self.apollo = Apollo()
        # 解析项目特性配置
        self.cfg = FqlGrt.FqlGrt
        self.encrypt_flag = encrypt_flag
        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 当前时间
        self.times = str(int(round(time.time() * 1000)))  # 当前13位时间戳
        self.data = self.get_user_info(data=data, person=person)
        self.merchantId = EnumMerchantId.FQLGRT.value
        self.interestRate = getInterestRate(ProductIdEnum.FQLGRT.value)
        self.strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        # 初始化payload变量
        self.active_payload = {}

        self.encrypt_url = self.host + self.cfg['encrypt']['interface']
        self.decrypt_url = self.host + self.cfg['decrypt']['interface']

    def get_user_info(self, data=None, person=True):
        # 获取四要素信息
        if data:
            data['applyId'] = "applyId" + self.strings
            update_user_info(data)
            base_data = data
        else:
            if person:
                base_data = get_base_data(str(self.env) + ' -> ' + str(ProductEnum.FQLZX.value), 'applyId')
            else:
                base_data = get_base_data_temp('applyId')
        return base_data

    # 授信
    def credit(self, orderType='1', **kwargs):
        self.log.demsg('用户四要素信息: {}'.format(self.data))
        credit_data = dict()
        credit_data['creditApplyId'] = self.data['applyId']
        credit_data['partnerCode'] = self.merchantId
        credit_data['name'] = self.data['name']
        credit_data['identiNo'] = self.data['cer_no']
        credit_data['mobileNo'] = self.data['telephone']
        credit_data['userBankCardNo'] = self.data['bankid']
        if orderType == '3':
            credit_data['debitAccountName'] = self.data['name']
            credit_data['debitAccountNo'] = self.data['bankid']
        else:
            resource = self.MysqlBizImpl.get_user_database_info('user_role_resource_relation', user_id=self.merchantId)
            bank_info = self.MysqlBizImpl.get_user_database_info('user_financial_instrument_info',
                                                                 resource_id=resource['resource_id'])
            credit_data['debitAccountName'] = bank_info['account_name']
            credit_data['debitOpenAccountBank'] = bank_info['branch_name']
            credit_data['debitAccountNo'] = bank_info['account']
            credit_data['debitCnaps'] = bank_info['union_bank_id']

        # 更新 payload 字段值
        credit_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit']['payload'], **credit_data)
        self.active_payload = parser.parser

        self.log.demsg('开始授信申请...')
        url = self.host + self.cfg['credit']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 授信查询
    def credit_query(self, **kwargs):
        credit_query_data = dict()
        credit_query_data['applyId'] = self.data['applyId']
        credit_query_data['partnerCode'] = self.merchantId
        # 更新 payload 字段值
        credit_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit_apply']['payload'], **credit_query_data)
        self.active_payload = parser.parser

        self.log.demsg('开始授信查询...')
        url = self.host + self.cfg['credit_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 支用申请
    def loan(self, orderType=1, loan_date=None, **kwargs):
        self.log.demsg('用户四要素信息: {}'.format(self.data))
        loan_data = dict()
        loan_data['applyId'] = self.data['applyId']
        loan_data['partnerCode'] = self.merchantId
        loan_data['mobileNo'] = self.data['telephone']
        loan_data['userBankCardNo'] = self.data['bankid']
        if orderType == 3:
            loan_data['debitAccountName'] = self.data['name']
            loan_data['debitAccountNo'] = self.data['bankid']
        else:
            resource = self.MysqlBizImpl.get_user_database_info('user_role_resource_relation', userid=self.merchantId)
            bank_info = self.MysqlBizImpl.get_user_database_info('user_financial_instrument_info',
                                                                 resource_id=resource['resource_id'])
            loan_data['debitAccountName'] = bank_info['account_name']
            loan_data['debitOpenAccountBank'] = bank_info['branch_name']
            loan_data['debitAccountNo'] = bank_info['account']
            loan_data['debitCnaps'] = bank_info['union_bank_id']

        # 设置apollo放款mock时间 默认当前时间
        loan_date = loan_date if loan_date else time.strftime('%Y-%m-%d', time.localtime())
        apollo_data = dict()
        apollo_data['credit.loan.trade.date.mock'] = True
        apollo_data['credit.loan.date.mock'] = loan_date
        self.apollo.update_config(appId='loan2.1-public', namespace='JCXF.system', **apollo_data)

        # 更新 payload 字段值
        loan_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan']['payload'], **loan_data)
        self.active_payload = parser.parser

        self.log.demsg('开始支用申请...')
        url = self.host + self.cfg['loan']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 支用查询
    def loan_query(self, **kwargs):
        loan_query_data = dict()
        loan_query_data['applyId'] = self.data['applyId']
        loan_query_data['partnerCode'] = self.merchantId
        # 更新 payload 字段值
        loan_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan_query']['payload'], **loan_query_data)
        self.active_payload = parser.parser

        self.log.demsg('开始支用查询...')
        url = self.host + self.cfg['loan_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 还款计划查询
    def repayPlan_query(self, loanInvoiceId=None, **kwargs):
        repayPlan_query_data = dict()
        repayPlan_query_data['applyId'] = self.data['applyId']
        repayPlan_query_data['partnerCode'] = self.merchantId
        loan_apply_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_apply',
                                                                     thirdpart_apply_id=self.data['applyId'])
        loan_invoice_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                       loan_apply_id=loan_apply_info['loan_apply_id'])
        loanInvoiceId = loanInvoiceId if loanInvoiceId else loan_invoice_info['loan_invoice_id']
        repayPlan_query_data['capitalLoanNo'] = loan_invoice_info['loan_invoice_id']
        # 更新 payload 字段值
        repayPlan_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['repayPlan_query']['payload'], **repayPlan_query_data)
        self.active_payload = parser.parser

        self.log.demsg('开始还款计划查询...')
        url = self.host + self.cfg['repayPlan_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 还款试算
    def repay_trial(self, loanInvoiceId=None, **kwargs):
        repay_trial_data = dict()
        loan_apply_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_apply',
                                                                     thirdpart_apply_id=self.data['applyId'])
        loan_invoice_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                       loan_apply_id=loan_apply_info['loan_apply_id'])
        loanInvoiceId = loanInvoiceId if loanInvoiceId else loan_invoice_info['loan_invoice_id']
        repay_trial_data['capitalLoanNo'] = loanInvoiceId

        # 更新 payload 字段值
        repay_trial_data.update(kwargs)
        parser = DataUpdate(self.cfg['repay_trial']['payload'], **repay_trial_data)
        self.active_payload = parser.parser

        self.log.demsg('开始还款试算...')
        url = self.host + self.cfg['repay_trial']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 还款通知
    def repay(self, billId='', rpyType=10, rpyGuaranteeAmt=3.14, loanInvoiceId=None, term=None, rpyDate=None, **kwargs):
        repay_data = dict()
        repay_data['partnerCode'] = self.merchantId
        repay_data['assetId'] = self.data['applyId']
        loan_apply_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_apply',
                                                                     thirdpart_apply_id=self.data['applyId'])
        loan_invoice_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                       loan_apply_id=loan_apply_info['loan_apply_id'])
        loanInvoiceId = loanInvoiceId if loanInvoiceId else loan_invoice_info['loan_invoice_id']
        repay_data['capitalLoanNo'] = loanInvoiceId
        repay_data['billId'] = billId
        rpyDate = rpyDate if rpyDate else time.strftime('%Y-%m-%d', time.localtime())
        repay_data['rpyDate'] = rpyDate
        if term:
            asset_repay_plan = self.MysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                                         loan_invoice_id=loanInvoiceId,
                                                                         current_num=term)
        else:
            key = "loan_invoice_id = '{}' and repay_plan_status in ('1','2','4', '5') ORDER BY 'current_num'".format(
                loanInvoiceId)
            asset_repay_plan = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key, record=0)
        min_term = int(asset_repay_plan['current_num'])
        self.log.demsg('当期最早未还期次{}'.format(min_term))
        rpyDetails = list()
        repay_detail_data = dict()
        totalAmount = 0
        if rpyType == 30:
            days = get_day(asset_repay_plan["start_date"], rpyDate)
            loan_term = int(asset_repay_plan['repay_num'])
            for i in range(min_term, loan_term + 1):
                asset_repay_plan = self.MysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                                             loan_invoice_id=loanInvoiceId,
                                                                             current_num=i)
                repay_detail_data = dict()
                repay_detail_data['rpyTerm'] = i
                repay_detail_data['rpyPrincipal'] = float(asset_repay_plan['pre_repay_interest'])
                if i == min_term:
                    repay_detail_data['rpyAmt'] = float(asset_repay_plan['pre_repay_amount'])
                    day_rate = round(self.interestRate / (100 * 360), 6)
                    repay_detail_data['rpyFeeAmt'] = asset_repay_plan[
                                                         "before_calc_principal"] * days * day_rate if days > 0 else 0
                    repay_detail_data['rpyMuclt'] = float(asset_repay_plan['pre_repay_overdue_fee'])
                    repay_detail_data['rpyGuaranteeAmt'] = rpyGuaranteeAmt
                else:
                    repay_detail_data['rpyAmt'] = float(asset_repay_plan['pre_repay_interest'])
                    repay_detail_data['rpyFeeAmt'] = 0
                    repay_detail_data['rpyMuclt'] = 0
                    repay_detail_data['rpyGuaranteeAmt'] = 0
                totalAmount += repay_detail_data['rpyAmt'] + repay_detail_data['rpyGuaranteeAmt']
                rpyDetails.append(repay_detail_data)
        else:
            repay_detail_data['rpyTerm'] = min_term
            repay_detail_data['rpyAmt'] = float(asset_repay_plan['pre_repay_amount'])
            repay_detail_data['rpyPrincipal'] = float(asset_repay_plan['pre_repay_interest'])
            repay_detail_data['rpyFeeAmt'] = float(asset_repay_plan['pre_repay_interest'])
            repay_detail_data['rpyMuclt'] = float(asset_repay_plan['pre_repay_overdue_fee'])
            repay_detail_data['rpyGuaranteeAmt'] = rpyGuaranteeAmt
            rpyDetails.append(repay_detail_data)
            totalAmount = repay_detail_data['rpyAmt'] + repay_detail_data['rpyGuaranteeAmt']
        repay_data['rpyDetails'] = rpyDetails
        repay_data['rpyTotalAmt'] = totalAmount

        # 更新 payload 字段值
        repay_data.update(kwargs)
        parser = DataUpdate(self.cfg['repay']['payload'], **repay_data)
        self.active_payload = parser.parser

        self.log.demsg('开始还款通知...')
        url = self.host + self.cfg['repay']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 还款通知查询
    def repay_query(self, billId='', loanInvoiceId=None, **kwargs):
        repay_query_data = dict()
        repay_query_data['partnerCode'] = self.merchantId
        repay_query_data['billId'] = billId
        loan_apply_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_apply',
                                                                     thirdpart_apply_id=self.data['applyId'])
        loan_invoice_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                       loan_apply_id=loan_apply_info['loan_apply_id'])
        loanInvoiceId = loanInvoiceId if loanInvoiceId else loan_invoice_info['loan_invoice_id']
        repay_query_data['capitalLoanNo'] = loanInvoiceId

        # 更新 payload 字段值
        repay_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['repay_query']['payload'], **repay_query_data)
        self.active_payload = parser.parser

        self.log.demsg('开始还款通知查询...')
        url = self.host + self.cfg['repay_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 代扣申请
    def withhold(self, rpyType=10, rpyGuaranteeAmt=3.14, loanInvoiceId=None, term=None, rpyDate=None, **kwargs):
        withhold_data = dict()
        withhold_data['withholdSerialNo'] = 'withholdSerialNo' + self.strings
        withhold_data['partnerCode'] = self.merchantId
        withhold_data['userName'] = self.data['name']
        withhold_data['cardNo'] = self.data['bankid']
        withhold_data['idNo'] = self.data['cer_no']
        withhold_data['phoneNo'] = self.data['telephone']

        withhold_data['assetId'] = self.data['applyId']
        loan_apply_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_apply',
                                                                     thirdpart_apply_id=self.data['applyId'])
        loan_invoice_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                       loan_apply_id=loan_apply_info['loan_apply_id'])
        loanInvoiceId = loanInvoiceId if loanInvoiceId else loan_invoice_info['loan_invoice_id']
        withhold_data['capitalLoanNo'] = loanInvoiceId
        rpyDate = rpyDate if rpyDate else time.strftime('%Y-%m-%d', time.localtime())
        withhold_data['rpyDate'] = rpyDate
        if term:
            asset_repay_plan = self.MysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                                         loan_invoice_id=loanInvoiceId,
                                                                         current_num=term)
        else:
            key = "loan_invoice_id = '{}' and repay_plan_status in ('1','2','4', '5') ORDER BY 'current_num'".format(
                loanInvoiceId)
            asset_repay_plan = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key, record=0)
        min_term = int(asset_repay_plan['current_num'])
        self.log.demsg('当期最早未还期次{}'.format(min_term))
        rpyDetails = list()
        repay_detail_data = dict()
        totalAmount = 0
        if rpyType == 30:
            days = get_day(asset_repay_plan["start_date"], rpyDate)
            loan_term = int(asset_repay_plan['repay_num'])
            for i in range(min_term, loan_term + 1):
                asset_repay_plan = self.MysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                                             loan_invoice_id=loanInvoiceId,
                                                                             current_num=i)
                repay_detail_data = dict()
                repay_detail_data['rpyTerm'] = i
                repay_detail_data['rpyPrincipal'] = float(asset_repay_plan['pre_repay_interest'])
                if i == min_term:
                    repay_detail_data['rpyAmt'] = float(asset_repay_plan['pre_repay_amount'])
                    day_rate = round(self.interestRate / (100 * 360), 6)
                    repay_detail_data['rpyFeeAmt'] = asset_repay_plan[
                                                         "before_calc_principal"] * days * day_rate if days > 0 else 0
                    repay_detail_data['rpyMuclt'] = float(asset_repay_plan['pre_repay_overdue_fee'])
                    repay_detail_data['rpyGuaranteeAmt'] = rpyGuaranteeAmt
                else:
                    repay_detail_data['rpyAmt'] = float(asset_repay_plan['pre_repay_interest'])
                    repay_detail_data['rpyFeeAmt'] = 0
                    repay_detail_data['rpyMuclt'] = 0
                    repay_detail_data['rpyGuaranteeAmt'] = 0
                totalAmount += repay_detail_data['rpyAmt'] + repay_detail_data['rpyGuaranteeAmt']
                rpyDetails.append(repay_detail_data)
        else:
            repay_detail_data['rpyTerm'] = min_term
            repay_detail_data['rpyAmt'] = float(asset_repay_plan['pre_repay_amount'])
            repay_detail_data['rpyPrincipal'] = float(asset_repay_plan['pre_repay_interest'])
            repay_detail_data['rpyFeeAmt'] = float(asset_repay_plan['pre_repay_interest'])
            repay_detail_data['rpyMuclt'] = float(asset_repay_plan['pre_repay_overdue_fee'])
            repay_detail_data['rpyGuaranteeAmt'] = rpyGuaranteeAmt
            rpyDetails.append(repay_detail_data)
            totalAmount = repay_detail_data['rpyAmt'] + repay_detail_data['rpyGuaranteeAmt']
        withhold_data['rpyDetails'] = rpyDetails
        withhold_data['rpyTotalAmt'] = totalAmount
        withhold_data['sepOutInfo'] = [{"type": "1", "amt": totalAmount - 3.56, "account": self.data['bankid']},
                                       {"type": "2", "amt": "3.56", "account": "11015898003004"}]
        # 更新 payload 字段值
        withhold_data.update(kwargs)
        parser = DataUpdate(self.cfg['withhold']['payload'], **withhold_data)
        self.active_payload = parser.parser

        self.log.demsg('开始代扣申请...')
        url = self.host + self.cfg['withhold']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 代扣查询
    def withhold_query(self, **kwargs):
        withhold_query_data = dict()
        withhold_query_data['partnerCode'] = self.merchantId

        # 更新 payload 字段值
        withhold_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['withhold_query']['payload'], **withhold_query_data)
        self.active_payload = parser.parser

        self.log.demsg('开始代扣结果查询...')
        url = self.host + self.cfg['withhold_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response