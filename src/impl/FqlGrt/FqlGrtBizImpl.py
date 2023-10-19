# -*- coding: utf-8 -*-
# ------------------------------------------
# 分期乐半增信数据封装类
# ------------------------------------------
import datetime

from engine.MysqlInit import MysqlInit
from src.enums.EnumsCommon import *
from src.impl.common.CommonBizImpl import *
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl
from src.test_data.module_data import FqlGrt
from utils.Apollo import Apollo
from utils.SFTP import SFTP


class FqlGrtBizImpl(MysqlInit):
    def __init__(self, data=None, encrypt_flag=True, person=True):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()
        self.apollo = Apollo()
        self.RepayPublicBizImpl = RepayPublicBizImpl()
        self.SFTP = SFTP()
        # 解析项目特性配置
        self.cfg = FqlGrt.FqlGrt
        self.encrypt_flag = encrypt_flag
        self.strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 当前时间
        self.data = self.get_user_info(data=data, person=person)
        self.partnerCode = 'fql_grt'
        self.merchantId = EnumMerchantId.FQLGRT.value
        self.interestRate = getInterestRate(ProductIdEnum.FQLGRT.value)
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
                base_data = get_base_data(str(self.env) + ' -> ' + str(ProductEnum.FQLGRT.value), 'applyId')
            else:
                base_data = get_base_data_temp('applyId')
        return base_data

    # 授信
    def credit(self, orderType='1', **kwargs):
        self.log.demsg('用户四要素信息: {}'.format(self.data))
        credit_data = dict()
        credit_data['creditApplyId'] = self.data['applyId']
        credit_data['partnerCode'] = self.partnerCode
        credit_data['name'] = self.data['name']
        credit_data['identiNo'] = self.data['cer_no']
        credit_data['mobileNo'] = self.data['telephone']
        credit_data['orderType'] = orderType
        if int(orderType) == 3:
            credit_data['userBankCardNo'] = self.data['bankid']
            credit_data['debitAccountName'] = self.data['name']
            credit_data['debitAccountNo'] = self.data['bankid']
        else:
            sql = "select account_name,branch_name,account,union_bank_id from user_financial_instrument_info " \
                  "where resource_id in (select resource_id from user_role_resource_relation where user_id = '{}') " \
                  "and account_type='1'".format(self.merchantId)
            bank_info = self.MysqlBizImpl.mysql_user.select(sql)
            credit_data['debitAccountName'] = bank_info[0][0]
            credit_data['debitOpenAccountBank'] = bank_info[0][1]
            credit_data['debitAccountNo'] = bank_info[0][2]
            credit_data['debitCnaps'] = bank_info[0][3]

        # 更新 payload 字段值
        credit_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit']['payload'], **credit_data)
        self.active_payload = parser.parser

        self.log.demsg('开始授信申请...')
        url = self.host + self.cfg['credit']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        response = response['bizContent']
        self.log.info("解析后报文：{}".format(response))
        return response

    # 授信查询
    def credit_query(self, **kwargs):
        credit_query_data = dict()
        credit_query_data['applyId'] = self.data['applyId']
        credit_query_data['partnerCode'] = self.partnerCode
        # 更新 payload 字段值
        credit_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit_query']['payload'], **credit_query_data)
        self.active_payload = parser.parser

        self.log.demsg('开始授信查询...')
        url = self.host + self.cfg['credit_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        response = response['bizContent']
        self.log.info("解析后报文：{}".format(response))
        return response

    # 支用申请
    def loan(self, orderType=1, **kwargs):
        self.log.demsg('用户四要素信息: {}'.format(self.data))
        loan_data = dict()
        loan_data['applyId'] = self.data['applyId']
        loan_data['partnerCode'] = self.partnerCode
        loan_data['mobileNo'] = self.data['telephone']
        loan_data['userBankCardNo'] = self.data['bankid']
        loan_data['orderType'] = orderType
        if int(orderType) == 3:
            loan_data['debitAccountName'] = self.data['name']
            loan_data['debitAccountNo'] = self.data['bankid']
        else:
            sql = "select account_name,branch_name,account,union_bank_id from user_financial_instrument_info " \
                  "where resource_id in (select resource_id from user_role_resource_relation where user_id = '{}') " \
                  "and account_type='1'".format(self.merchantId)
            bank_info = self.MysqlBizImpl.mysql_user.select(sql)
            loan_data['debitAccountName'] = bank_info[0][0]
            loan_data['debitOpenAccountBank'] = bank_info[0][1]
            loan_data['debitAccountNo'] = bank_info[0][2]
            loan_data['debitCnaps'] = bank_info[0][3]

        # 更新 payload 字段值
        loan_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan']['payload'], **loan_data)
        self.active_payload = parser.parser

        self.log.demsg('开始支用申请...')
        url = self.host + self.cfg['loan']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        response = response['bizContent']
        self.log.info("解析后报文：{}".format(response))
        return response

    # 支用查询
    def loan_query(self, **kwargs):
        loan_query_data = dict()
        loan_query_data['applyId'] = self.data['applyId']
        loan_query_data['partnerCode'] = self.partnerCode
        # 更新 payload 字段值
        loan_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan_query']['payload'], **loan_query_data)
        self.active_payload = parser.parser

        self.log.demsg('开始支用查询...')
        url = self.host + self.cfg['loan_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        response = response['bizContent']
        self.log.info("解析后报文：{}".format(response))
        return response

    # 还款计划查询
    def repayPlan_query(self, loanInvoiceId=None, **kwargs):
        repayPlan_query_data = dict()
        repayPlan_query_data['applyId'] = self.data['applyId']
        repayPlan_query_data['partnerCode'] = self.partnerCode
        loan_apply_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_apply',
                                                                     thirdpart_apply_id=self.data['applyId'])
        loan_invoice_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                       loan_apply_id=loan_apply_info['loan_apply_id'])
        loanInvoiceId = loanInvoiceId if loanInvoiceId else loan_invoice_info['loan_invoice_id']
        repayPlan_query_data['capitalLoanNo'] = loanInvoiceId
        # 更新 payload 字段值
        repayPlan_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['repayPlan_query']['payload'], **repayPlan_query_data)
        self.active_payload = parser.parser

        self.log.demsg('开始还款计划查询...')
        url = self.host + self.cfg['repayPlan_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        response = response['bizContent']
        self.log.info("解析后报文：{}".format(response))
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
        response = response['bizContent']
        self.log.info("解析后报文：{}".format(response))
        return response

    # 还款通知
    def repay(self, rpyType=10, rpyGuaranteeAmt=3.14, loanInvoiceId=None, term=None, rpyDate=None, **kwargs):
        repay_data = dict()
        repay_data['partnerCode'] = self.partnerCode
        repay_data['assetId'] = self.data['applyId']
        if loanInvoiceId:
            loanInvoiceId = loanInvoiceId
            loan_invoice_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                           loan_invoice_id=loanInvoiceId)
            loan_apply_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_apply',
                                                                         loan_apply_id=loan_invoice_info[
                                                                             'loan_apply_id'])
            repay_data['assetId'] = loan_apply_info['thirdpart_apply_id']
        else:
            repay_data['assetId'] = self.data['applyId']
            loan_apply_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_apply',
                                                                         thirdpart_apply_id=self.data['applyId'])
            loan_invoice_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                           loan_apply_id=loan_apply_info[
                                                                               'loan_apply_id'])
            loanInvoiceId = loan_invoice_info['loan_invoice_id']
        repay_data['capitalLoanNo'] = loanInvoiceId
        repay_data['billId'] = "billId" + self.strings
        rpyDate = rpyDate if rpyDate else time.strftime('%Y-%m-%d', time.localtime())
        repay_data['rpyDate'] = rpyDate
        repay_data['rpyType'] = rpyType
        if term:
            asset_repay_plan = self.MysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                                         loan_invoice_id=loanInvoiceId,
                                                                         current_num=term)
        else:
            key = "loan_invoice_id = '{}' and repay_plan_status in ('1','2','4','5') ORDER BY 'current_num'".format(
                loanInvoiceId)
            asset_repay_plan = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key, record=0)
        min_term = int(asset_repay_plan['current_num'])
        self.log.demsg('当期最早未还期次: {}'.format(min_term))
        rpyDetails = list()
        repay_detail_data = dict()
        totalAmount = 0
        if rpyType == 30:
            days = get_day(asset_repay_plan["start_date"], rpyDate)
            key = "loan_invoice_id = '{}' and current_num >= '{}'".format(loanInvoiceId, min_term)
            asset_repay_plan = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key=key, record=999)
            for i in asset_repay_plan:
                repay_detail_data = dict()
                repay_detail_data['rpyTerm'] = i['current_num']
                repay_detail_data['rpyPrincipal'] = float(i['pre_repay_principal'])
                if i['current_num'] == min_term:
                    if min_term == 1:
                        days = days if days != 0 else 1
                    day_rate = round(self.interestRate / (100 * 360), 6)
                    pre_repay_date = datetime.strptime(str(i['pre_repay_date']), "%Y-%m-%d").date()
                    repay_date = datetime.strptime(rpyDate, "%Y-%m-%d").date()
                    if days > 0:
                        if repay_date < pre_repay_date:
                            repay_detail_data['rpyFeeAmt'] = round(float(i['before_calc_principal']) * days * day_rate,
                                                                   2)
                        else:
                            repay_detail_data['rpyFeeAmt'] = float(i['pre_repay_interest'])
                    else:
                        repay_detail_data['rpyFeeAmt'] = 0
                    repay_detail_data['rpyMuclt'] = float(i['pre_repay_overdue_fee'])
                    repay_detail_data['rpyGuaranteeAmt'] = rpyGuaranteeAmt if days > 0 else 0
                    repay_detail_data['rpyAmt'] = round(
                        float(i['pre_repay_principal']) + repay_detail_data['rpyFeeAmt'] + repay_detail_data[
                            'rpyMuclt'], 2)
                else:
                    repay_detail_data['rpyAmt'] = float(i['pre_repay_principal'])
                    repay_detail_data['rpyFeeAmt'] = 0
                    repay_detail_data['rpyMuclt'] = 0
                    repay_detail_data['rpyGuaranteeAmt'] = 0
                totalAmount += repay_detail_data['rpyAmt'] + repay_detail_data['rpyGuaranteeAmt']
                rpyDetails.append(repay_detail_data)
        else:
            repay_detail_data['rpyTerm'] = min_term
            repay_detail_data['rpyAmt'] = float(asset_repay_plan['pre_repay_amount'])
            repay_detail_data['rpyPrincipal'] = float(asset_repay_plan['pre_repay_principal'])
            repay_detail_data['rpyFeeAmt'] = float(asset_repay_plan['pre_repay_interest'])
            repay_detail_data['rpyMuclt'] = float(asset_repay_plan['pre_repay_overdue_fee'])
            repay_detail_data['rpyGuaranteeAmt'] = rpyGuaranteeAmt
            rpyDetails.append(repay_detail_data)
            totalAmount = repay_detail_data['rpyAmt'] + repay_detail_data['rpyGuaranteeAmt']
        repay_data['rpyDetails'] = rpyDetails
        repay_data['rpyTotalAmt'] = round(totalAmount, 2)

        # 更新 payload 字段值
        repay_data.update(kwargs)
        parser = DataUpdate(self.cfg['repay']['payload'], **repay_data)
        self.active_payload = parser.parser

        self.log.demsg('开始还款通知...')
        url = self.host + self.cfg['repay']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        response = response['bizContent']
        self.log.info("解析后报文：{}".format(response))
        return response

    # 还款通知查询
    def repay_query(self, loanInvoiceId=None, **kwargs):
        repay_query_data = dict()
        repay_query_data['partnerCode'] = self.partnerCode
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
        response = response['bizContent']
        self.log.info("解析后报文：{}".format(response))
        return response

    # 代扣明细组装
    def withhold_detail(self, rpyType=10, rpyGuaranteeAmt=3.14, loanInvoiceId=None, term=None, rpyDate=None):
        """
        组装单笔代扣明细
        :param rpyType: 还款方式
        :param rpyGuaranteeAmt: 担保金额
        :param loanInvoiceId: 借据号
        :param term: 最小未还款期次
        :param rpyDate: 代扣日期
        :return:
        """
        withhold_detail_data = dict()
        withhold_detail_data['rpyType'] = rpyType
        rpyDate = rpyDate if rpyDate else time.strftime('%Y-%m-%d', time.localtime())
        withhold_detail_data['rpyDate'] = rpyDate
        if loanInvoiceId:
            loanInvoiceId = loanInvoiceId
            loan_invoice_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                           loan_invoice_id=loanInvoiceId)
            loan_apply_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_apply',
                                                                         loan_apply_id=loan_invoice_info[
                                                                             'loan_apply_id'])
            withhold_detail_data['assetId'] = loan_apply_info['thirdpart_apply_id']
        else:
            withhold_detail_data['assetId'] = self.data['applyId']
            loan_apply_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_apply',
                                                                         thirdpart_apply_id=self.data['applyId'])
            loan_invoice_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                           loan_apply_id=loan_apply_info[
                                                                               'loan_apply_id'])
            loanInvoiceId = loan_invoice_info['loan_invoice_id']
        withhold_detail_data['capitalLoanNo'] = loanInvoiceId
        if term:
            asset_repay_plan = self.MysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                                         loan_invoice_id=loanInvoiceId,
                                                                         current_num=term)
        else:
            key = "loan_invoice_id = '{}' and repay_plan_status in ('1','2','4', '5') ORDER BY 'current_num'".format(
                loanInvoiceId)
            asset_repay_plan = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key, record=0)
        min_term = int(asset_repay_plan['current_num'])
        self.log.demsg('当期最早未还期次: {}'.format(min_term))
        rpyDetails = list()
        repay_detail_data = dict()
        totalAmount = 0
        if rpyType == 30:
            days = get_day(asset_repay_plan["start_date"], rpyDate)
            key = "loan_invoice_id = '{}' and current_num >= '{}'".format(loanInvoiceId, min_term)
            asset_repay_plan = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key=key, record=999)
            for i in asset_repay_plan:
                repay_detail_data = dict()
                repay_detail_data['rpyTerm'] = i['current_num']
                repay_detail_data['rpyPrincipal'] = float(i['pre_repay_principal'])
                if i['current_num'] == min_term:
                    if min_term == 1:
                        days = days if days != 0 else 1
                    day_rate = round(self.interestRate / (100 * 360), 6)
                    pre_repay_date = datetime.strptime(str(i['pre_repay_date']), "%Y-%m-%d").date()
                    repay_date = datetime.strptime(rpyDate, "%Y-%m-%d").date()
                    if days > 0:
                        if repay_date < pre_repay_date:
                            repay_detail_data['rpyFeeAmt'] = round(float(i['before_calc_principal']) * days * day_rate,
                                                                   2)
                        else:
                            repay_detail_data['rpyFeeAmt'] = float(i['pre_repay_interest'])
                    else:
                        repay_detail_data['rpyFeeAmt'] = 0
                    repay_detail_data['rpyMuclt'] = float(i['pre_repay_overdue_fee'])
                    repay_detail_data['rpyGuaranteeAmt'] = rpyGuaranteeAmt if days > 0 else 0
                    repay_detail_data['rpyAmt'] = round(
                        float(i['pre_repay_principal']) + repay_detail_data['rpyFeeAmt'] + repay_detail_data[
                            'rpyMuclt'], 2)
                else:
                    repay_detail_data['rpyAmt'] = float(i['pre_repay_principal'])
                    repay_detail_data['rpyFeeAmt'] = 0
                    repay_detail_data['rpyMuclt'] = 0
                    repay_detail_data['rpyGuaranteeAmt'] = 0
                totalAmount += repay_detail_data['rpyAmt'] + repay_detail_data['rpyGuaranteeAmt']
                rpyDetails.append(repay_detail_data)
        else:
            repay_detail_data['rpyTerm'] = min_term
            repay_detail_data['rpyAmt'] = float(asset_repay_plan['pre_repay_amount'])
            repay_detail_data['rpyPrincipal'] = float(asset_repay_plan['pre_repay_principal'])
            repay_detail_data['rpyFeeAmt'] = float(asset_repay_plan['pre_repay_interest'])
            repay_detail_data['rpyMuclt'] = float(asset_repay_plan['pre_repay_overdue_fee'])
            repay_detail_data['rpyGuaranteeAmt'] = rpyGuaranteeAmt
            rpyDetails.append(repay_detail_data)
            totalAmount = repay_detail_data['rpyAmt'] + repay_detail_data['rpyGuaranteeAmt']
        withhold_detail_data['billDetails'] = rpyDetails
        withhold_detail_data['rpyTotalAmt'] = round(totalAmount, 2)
        # 更新代扣明细字段值
        withhold_detail = self.cfg['withhold']['payload']['withholdDetail'][0]
        parser = DataUpdate(withhold_detail, **withhold_detail_data)
        detail_data = parser.parser
        self.log.info('代扣明细: {}'.format(detail_data))
        return dict(detail_data)

    # 多个代扣明细组装list
    def withhold_detail_list(self, *detail_data):
        """
        将多笔借据代扣明细组装到list
        :param detail_data: 多个代扣明细
        :return: 代扣明细list
        """
        detail_list = list(detail_data)
        self.log.info('代扣明细list: {}'.format(detail_list))
        return detail_list

    # 代扣申请
    def withhold(self, detail_list, rpyGuaranteeAmt=3.14, **kwargs):
        """
        组装代扣申请
        :param detail_list: 代扣明细组合
        :param kwargs:
        :return:
        """
        withhold_data = dict()
        withhold_data['withholdSerialNo'] = 'withholdSerialNo' + self.strings
        withhold_data['partnerCode'] = self.partnerCode
        withhold_data['userName'] = self.data['name']
        withhold_data['cardNo'] = self.data['bankid']
        withhold_data['idNo'] = self.data['cer_no']
        withhold_data['phoneNo'] = self.data['telephone']
        withholdAmt = sum([detail['rpyTotalAmt'] for detail in detail_list])
        withhold_data['withholdAmt'] = round(withholdAmt, 2)

        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['withhold']['payload'], **withhold_data)
        withhold_payload = parser.parser
        # 更新代扣明细
        withhold_payload['withholdDetail'] = detail_list
        # 更新出账信息
        withhold_payload['sepOutInfo'][0]['amt'] = round(withholdAmt, 2)
        withhold_payload['sepOutInfo'][0]['account'] = self.data['bankid']
        # 更新分账信息
        withhold_payload['sepInInfo'][0]['amt'] = round(withholdAmt - rpyGuaranteeAmt, 2)
        withhold_payload['sepInInfo'][0]['detail'][0]['amt'] = round(withholdAmt - rpyGuaranteeAmt, 2)
        withhold_payload['sepInInfo'][1]['amt'] = rpyGuaranteeAmt
        withhold_payload['sepInInfo'][1]['detail'][0]['amt'] = rpyGuaranteeAmt

        withhold_data1 = dict()
        withhold_data1.update(kwargs)
        parser1 = DataUpdate(withhold_payload, **withhold_data1)
        self.active_payload = parser1.parser

        self.log.demsg('开始代扣申请...')
        url = self.host + self.cfg['withhold']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        response = response['bizContent']
        self.log.info("解析后报文：{}".format(response))
        return response

    # 代扣查询
    def withhold_query(self, **kwargs):
        withhold_query_data = dict()
        withhold_query_data['partnerCode'] = self.partnerCode

        # 更新 payload 字段值
        withhold_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['withhold_query']['payload'], **withhold_query_data)
        self.active_payload = parser.parser

        self.log.demsg('开始代扣结果查询...')
        url = self.host + self.cfg['withhold_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        response = response['bizContent']
        self.log.info("解析后报文：{}".format(response))
        return response

    # 代偿文件
    def compensation(self, loan_invoice_id=None, repay_date=None):
        repay_date = repay_date if repay_date else time.strftime('%Y-%m-%d', time.localtime())
        if loan_invoice_id:
            key = "loan_invoice_id = '{}' and repay_plan_status in ('1','4') ORDER BY 'current_num' limit 1".format(
                loan_invoice_id)
            asset_repay_plan = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key=key, record=999)
        else:
            key = "merchant_id = '{}' and repay_plan_status = '4' and overdue_days >= 15 ORDER BY 'current_num'".format(
                self.merchantId)
            asset_repay_plan = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key=key, record=999)
        compensation_list = list()
        for i in asset_repay_plan:
            compensation_data = dict()
            credit_loan_invoice_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                                  loan_invoice_id=i['loan_invoice_id'])
            loan_apply_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_apply',
                                                                         loan_apply_id=credit_loan_invoice_info[
                                                                             'loan_apply_id'])
            compensation_data['applyId'] = loan_apply_info['third_loan_invoice_id']
            compensation_data['capitalLoanNo'] = i['loan_invoice_id']
            compensation_data['term'] = i['current_num']
            compensation_data['repay_type'] = "50"
            compensation_data['principal'] = float(i['pre_repay_principal'])
            compensation_data['interest'] = float(i['pre_repay_interest'])
            compensation_data['overdue_fee'] = float(i['pre_repay_overdue_fee'])
            compensation_data['repay_date'] = repay_date.replace('-', '')
            compensation_data['backup'] = ""
            compensation_list.append(compensation_data)

        # 初始化本地目录
        _ProjectPath = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # 项目根目录
        _FilePath = os.path.join(_ProjectPath, 'FilePath', ProductEnum.FQLGRT.value, TEST_ENV_INFO)  # 文件存放目录
        if not os.path.exists(_FilePath):
            os.makedirs(_FilePath)
        data_save_path = os.path.join(_FilePath, 'compensation', repay_date.replace('-', ''))
        if not os.path.exists(data_save_path):
            os.makedirs(data_save_path)
        # 初始化代偿文件名
        compensation_file = os.path.join(data_save_path, 'compensation_%s.txt' % (repay_date.replace('-', '')))
        compensation_ok = os.path.join(data_save_path, 'compensation_%s.ok' % (repay_date.replace('-', '')))
        # 生成空文件
        os.open(compensation_ok, os.O_CREAT)
        # 写入代偿文件
        with open(compensation_file, 'w+', encoding='utf-8') as f:
            for item in compensation_list:
                val_list = map(str, [item[key] for key in item])
                strs = '|'.join(val_list)
                f.write(strs + '\n')
        # 上传文件
        self.SFTP.sftp_upload(data_save_path,
                              'hj/xdgl/fqlgrt/upload/fql_grt/{}'.format(repay_date.replace('-', '')))
