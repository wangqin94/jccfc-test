# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：YinLiuBizImpl.py
@Author  ：jccfc
@Date    ：2024/1/16 14:51 
"""
from engine.EnvInit import *
from src.impl.common.CommonBizImpl import getDailyAccrueInterest
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils.Apollo import Apollo
from utils.JobCenter import JOB
from utils.Models import *
from utils.Redis import Redis


class YinLiuBizImpl(EnvInit):
    def __init__(self):
        """"""
        super().__init__()
        self.redis = Redis()
        self.job = JOB()
        self.apollo = Apollo()
        self.MysqlBizImpl = MysqlBizImpl()

    def repayApiBodyData(self, data, productId, loanInvoiceId, repayScene='01', repayType='1', repayTerm=None,
                         repayGuaranteeFee=1.11,
                         repayDate=None, paymentOrder=None):
        """
        封装统一还款请求body
        @param productId: 产品id
        @param data: 用户四要素
        @param loanInvoiceId: 借据号 必填
        @param repayScene: 还款场景 EnumRepayScene ("01", "线上还款"),("02", "线下还款"),（"04","支付宝还款通知"）（"05","逾期（代偿、回购后）还款通知"）
        @param repayType： 还款类型 1 按期还款； 2 提前结清； 7 提前还当期； 9 宽限期提前结清； 10 逾期提前结清
        @param repayTerm: 还款期次，默认取当前借据最早未还期次
        @param repayGuaranteeFee: 担保费， 0<担保费<24红线-利息
        @param repayDate: 还款时间，默认当天 eg:'2022-08-01'
        @param paymentOrder: 支付宝订单号，支付宝还款需手动输入（查询支付系统payment_channel_order.PAY_TRANSACTION_ID）
        @return: response 接口响应参数 数据类型：json
        @return:
        """
        strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        # 构造还款参数
        repay_apply_data = dict()
        repay_apply_data['repayScene'] = repayScene
        repay_apply_data['repayApplySerialNo'] = 'repayNo' + strings
        repay_apply_data['loanInvoiceId'] = loanInvoiceId
        repay_apply_data['thirdRepayTime'] = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 客户实际还款时间
        repay_apply_data['repayType'] = repayType
        if repayTerm:
            asset_repay_plan = self.MysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                                         loan_invoice_id=loanInvoiceId,
                                                                         current_num=repayTerm)
        else:
            key = "loan_invoice_id = '{}' and repay_plan_status in ('1','2','4', '5') ORDER BY 'current_num'".format(
                loanInvoiceId)
            asset_repay_plan = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key, record=0)
            repayTerm = asset_repay_plan['current_num']
        self.log.demsg('当期最早未还期次{}'.format(asset_repay_plan['current_num']))
        # 当月计息天数
        days = get_day(asset_repay_plan["start_date"], repayDate)
        repay_apply_data['repayNum'] = int(asset_repay_plan['current_num'])
        repay_apply_data["repayPrincipal"] = float(asset_repay_plan['pre_repay_principal'])  # 本金
        repay_apply_data["repayInterest"] = float(asset_repay_plan['pre_repay_interest'])  # 利息
        repay_apply_data["repayFee"] = float(asset_repay_plan['pre_repay_fee'])  # 费用
        repay_apply_data["repayOverdueFee"] = float(asset_repay_plan['pre_repay_overdue_fee'])  # 逾期罚息
        repay_apply_data["repayCompoundInterest"] = float(asset_repay_plan['pre_repay_compound_interest'])  # 手续费
        repay_apply_data["repayGuaranteeFee"] = repayGuaranteeFee  # 0<担保费<24红线-利息
        repay_apply_data["repayAmount"] = round(float(asset_repay_plan['pre_repay_amount']) + repayGuaranteeFee,
                                                2)  # 总金额

        # 提前还款开关,如果开关打开按日计息，关闭状态需要查提前还款后记息方式（1：按天，2：按期）
        hj_advance_repay_rule_switch = MysqlBizImpl().get_base_database_info('product_product_param',
                                                                             product_id=productId,
                                                                             param_key='hj_advance_repay_rule_switch')
        advance_repay_switch = hj_advance_repay_rule_switch['param_value']
        # 提前还款开关
        advance_repay_profit_type = MysqlBizImpl().get_base_database_info('product_product_param',
                                                                          product_id=productId,
                                                                          param_key='advance_repay_profit_type')
        advance_repay_profit_type = advance_repay_profit_type['param_value']
        # 提前还当期、提前结清、宽限期提前结清按日计息
        if repayType in ("2", "7", "9"):
            if advance_repay_switch == '1' or (advance_repay_switch == '0' and advance_repay_profit_type == '1'):
                repay_apply_data['repayInterest'] = getDailyAccrueInterest(productId, days, asset_repay_plan[
                    'before_calc_principal'])  # 提前还当期、提前结清按日计息
                self.log.info("当前月计息天数：{}天, 按日计提利息：{}".format(days, repay_apply_data['repayInterest']))
                # 如果按日计提利息>大于资产还款计划整期应还利息 利息取整期应还利息
                if repay_apply_data['repayInterest'] > float(asset_repay_plan['left_repay_interest']):
                    repay_apply_data['repayInterest'] = float(asset_repay_plan['left_repay_interest'])
                # 根据最新计提信息重算还款总额
                repay_apply_data["repayAmount"] = round(
                    repay_apply_data["repayPrincipal"] + repay_apply_data["repayInterest"] + repayGuaranteeFee,
                    2)  # 总金额

        # 提前结清
        if repayType == "2":
            repay_apply_data["repayPrincipal"] = float(asset_repay_plan['before_calc_principal'])  # 本金
            # 如果当期已还款，提前还款利息应收0
            repay_apply_data["repayInterest"] = repay_apply_data["repayInterest"] if days > 0 else 0
            # 根据最新本金、利息重算还款总额
            repay_apply_data["repayAmount"] = round(
                repay_apply_data["repayPrincipal"] + repay_apply_data["repayInterest"] + repayGuaranteeFee,
                2)  # 总金额

        # 宽限期提前结清
        if repayType == "9":
            repay_apply_data['repayType'] = "2"
            # 应收当期利息+宽限期期次利息
            key = "loan_invoice_id = '{}' and repay_plan_status = '1' and overdue_days = '0' ORDER BY 'current_num'".format(
                loanInvoiceId)
            currentTerm = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key, record=0)
            currentTermInterest = float(currentTerm['pre_repay_interest']) if currentTerm and currentTerm[
                'current_num'] != repayTerm else 0  # 宽限期利息
            repay_apply_data["repayInterest"] = round(repay_apply_data["repayInterest"] + currentTermInterest, 2)  # 总利息
            self.log.demsg("宽限期利息：{}".format(repay_apply_data["repayInterest"]))
            repay_apply_data["repayPrincipal"] = float(asset_repay_plan['before_calc_principal'])  # 本金
            repay_apply_data["repayAmount"] = round(
                repay_apply_data["repayPrincipal"] + repay_apply_data["repayInterest"] + repay_apply_data[
                    'repayOverdueFee'] + repay_apply_data["repayFee"] + repayGuaranteeFee, 2)  # 总金额

        # 逾期提前结清
        if repayType == "10":
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
            repay_apply_data['repayOverdueFee'] = pre_repay_overdue_fee  # 罚息
            repay_apply_data["repayCompoundInterest"] = left_repay_fee  # 费用
            repay_apply_data["repayAmount"] = round(
                repay_apply_data["repayPrincipal"] + repay_apply_data["repayInterest"] + repay_apply_data[
                    'repayOverdueFee'] + repay_apply_data["repayFee"] + repayGuaranteeFee, 2)  # 总金额

        # 线上还款
        if repayScene == '01':
            repay_apply_data['repaymentAccountNo'] = data['bankid']
            repay_apply_data['repaymentAccountName'] = data['name']
            repay_apply_data['repaymentAccountPhone'] = data['telephone']
        # 线下还款、逾期还款
        if repayScene == '02' or '05':
            repay_apply_data['thirdWithholdId'] = 'thirdWithholdId' + strings
        # 支付宝还款
        if repayScene == '04':
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

        return repay_apply_data


if __name__ == '__main__':
    pass
