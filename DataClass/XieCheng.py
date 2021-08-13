# -*- coding: utf-8 -*-
# ------------------------------------------
# 携程接口数据封装类
# ------------------------------------------

import time
from datetime import datetime

from Engine.Base import INIT
from Config.TestEnvInfo import *
from ComLib.Models import *


class PayloadGenerator(INIT):
    def __init__(self, *, data=None, repay_term_no="1", repay_mode="1", loan_invoice_id=None, repay_date='2021-08-09'):
        """
        :param data:  四要素
        :param repay_term_no:   还款期次
        :param repay_mode:      还款类型:1 按期还款；2 提前结清；3逾期还款
        :param loan_invoice_id: 借据号为None取用户第一笔借据，否则取自定义值
        :param repay_date:      实际还款时间'2021-08-09'
        """
        super().__init__()
        self.data = data if data else get_base_data(str(self.env) + ' -> ' + str(self.project), 'open_id')
        self.log.info('用户四要素信息 \n%s', self.data)

        self.strings = str(int(round(time.time() * 1000)))

        self.credit_amount = 3000000  # 授信申请金额, 默认3000000  单位分
        self.loan_amount = 60000  # 支用申请金额, 默认1000000  单位分
        self.period = 3  # 借款期数, 默认3期
        self.repay_term_no = repay_term_no
        self.repay_mode = repay_mode
        self.loan_invoice_id = loan_invoice_id
        self.repay_date = repay_date

        # 初始化payload变量
        self.pre_credit_payload = {}
        self.credit_payload = {}
        self.loan_payload = {}
        self.repay_notice_payload = {}
        self.active_payload = {}

        # 初始数据库变量
        self.credit_database_name = '%s_credit' % TEST_ENV_INFO.lower()
        self.asset_database_name = '%s_asset' % TEST_ENV_INFO.lower()

    def set_active_payload(self, payload):
        self.active_payload = payload
        self.log.info(self.active_payload)

    # 预授信申请payload
    def pre_credit_msg(self, **kwargs):
        pre_credit_data = dict()

        # 四要素
        pre_credit_data['id_no'] = self.data['cer_no']
        pre_credit_data['card_no'] = self.data['bankid']
        pre_credit_data['user_name'] = self.data['name']
        pre_credit_data['bank_bind_mobile'] = self.data['telephone']

        pre_credit_data['open_id'] = self.data["open_id"]
        pre_credit_data['request_no'] = 'request_no' + self.strings + "1"
        pre_credit_data['advice_amount'] = self.credit_amount

        pre_credit_data['id_no'] = self.data['cer_no']
        pre_credit_data['user_name'] = self.data['name']
        pre_credit_data['mobile'] = self.data['telephone']
        pre_credit_data['advice_rate_type'] = "Y"

        pre_credit_data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['pre_credit']['payload'], **pre_credit_data)
        self.pre_credit_payload = parser.parser
        self.log.info("payload数据: %s", self.pre_credit_payload)
        self.set_active_payload(self.pre_credit_payload)

    # 授信payload
    def credit_msg(self, **kwargs):
        credit_data = dict()
        # 四要素
        credit_data['id_no'] = self.data['cer_no']
        credit_data['card_no'] = self.data['bankid']
        credit_data['user_name'] = self.data['name']
        credit_data['bank_bind_mobile'] = self.data['telephone']

        credit_data['open_id'] = self.data["open_id"]
        credit_data['request_no'] = 'request_no' + self.strings + "2"
        credit_data['advice_amount'] = self.credit_amount
        credit_data['id_no'] = self.data['cer_no']
        credit_data['user_name'] = self.data['name']
        credit_data['mobile'] = self.data['telephone']
        credit_data['advice_rate_type'] = "Y"

        credit_data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['credit']['payload'], **credit_data)
        self.credit_payload = parser.parser
        self.log.info("payload数据: %s", self.credit_payload)
        self.set_active_payload(self.credit_payload)

    # 支用申请payload
    def loan_msg(self, **kwargs):
        """ # 支用申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        loan_data = dict()
        # 四要素
        loan_data['id_no'] = self.data['cer_no']
        loan_data['card_no'] = self.data['bankid']
        loan_data['user_name'] = self.data['name']
        loan_data['bank_bind_mobile'] = self.data['telephone']

        loan_data['open_id'] = self.data["open_id"]
        loan_data['loan_no'] = 'loan_no' + self.strings
        loan_data['loan_amount'] = self.loan_amount
        loan_data['request_no'] = 'request_no' + self.strings + "3"
        loan_data['first_repay_date'] = datetime.now().strftime('%Y%m%d%H%M%S')

        loan_data.update(kwargs)

        parser = DataUpdate(self.cfg['loan']['payload'], **loan_data)
        self.loan_payload = parser.parser
        self.log.info("payload数据: %s", self.loan_payload)
        self.set_active_payload(self.loan_payload)

    # 还款通知payload
    def repay_notice_msg(self, **kwargs):
        """ # 还款通知payload字段装填
        注意：键名必须与接口原始数据的键名一致
        :param kwargs: 需要临时装填的字段以及值 eg: key=value
        :return: None
        """
        repay_notice = dict()
        # 根据openId查询支用信息
        key1 = "thirdpart_user_id = '{}'".format(self.data['open_id'])
        credit_loan_apply = self.get_credit_data_info(table="credit_loan_apply", key=key1)
        apply_rate = credit_loan_apply["apply_rate"]

        # 根据支用申请单号查询借据信息
        if self.loan_invoice_id:
            loan_invoice_id = self.loan_invoice_id
            key2 = "loan_invoice_id = '{}'".format(loan_invoice_id)
            credit_loan_invoice = self.get_credit_data_info(table="credit_loan_invoice", key=key2)
            loan_apply_id = credit_loan_invoice["loan_apply_id"]
            key21 = "loan_apply_id = '{}'".format(loan_apply_id)
            credit_loan_apply = self.get_credit_data_info(table="credit_loan_apply", key=key21)
        else:
            loan_apply_id = credit_loan_apply["loan_apply_id"]
            key2 = "loan_apply_id = '{}'".format(loan_apply_id)
            credit_loan_invoice = self.get_credit_data_info(table="credit_loan_invoice", key=key2)
            loan_invoice_id = credit_loan_invoice["loan_invoice_id"]

        # 根据借据Id和期次获取还款计划
        key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loan_invoice_id, self.repay_term_no)
        asset_repay_plan = self.get_asset_data_info(table="asset_repay_plan", key=key3)

        # 通知payload
        repay_notice['open_id'] = self.data['open_id']
        repay_notice['loan_no'] = credit_loan_apply['third_loan_invoice_id']
        repay_notice['repay_no'] = 'repay_no' + self.strings + "1"
        repay_notice['repay_type'] = "1"
        repay_notice['repay_term_no'] = self.repay_term_no
        repay_notice['repay_term_no'] = "1"
        repay_notice['finish_time'] = time.strftime('%Y%m%d%H%M%S', time.localtime())

        repay_notice["actual_repay_amount"] = float(asset_repay_plan['pre_repay_amount'])  # 总金额
        repay_notice["repay_principal"] = float(asset_repay_plan['pre_repay_principal'])  # 本金
        repay_notice["repay_interest"] = float(asset_repay_plan['pre_repay_interest'])  # 利息
        repay_notice["repay_penalty_amount"] = float(asset_repay_plan['pre_repay_overdue_fee'])  # 逾期罚息
        repay_notice["repay_fee"] = float(asset_repay_plan['pre_repay_fee'])  # 手续费

        # 按期还款
        if self.repay_mode == "1":
            repay_notice['repay_type'] = self.repay_mode
            repay_notice['finish_time'] = str(asset_repay_plan["pre_repay_date"]).replace("-", "") + "112233"

        # 逾期还款
        elif self.repay_mode == "3":
            repay_notice['repay_type'] = "1"
            repay_notice['finish_time'] = str(asset_repay_plan["calc_overdue_fee_date"]).replace("-", "") + "112233"

        # 提前结清
        elif self.repay_mode == "2":
            repay_notice['repay_type'] = self.repay_mode
            repay_notice['finish_time'] = str(self.repay_date.replace("-", "")) + "112233"
            repay_notice["repay_principal"] = float(asset_repay_plan['before_calc_principal'])  # 本金

            pre_repay_date = str(asset_repay_plan["pre_repay_date"])
            pre_repay_date = datetime.strptime(pre_repay_date, "%Y-%m-%d").date()
            repay_date = datetime.strptime(self.repay_date, "%Y-%m-%d").date()
            if pre_repay_date > repay_date:
                repay_notice["repay_interest"] = 0  # 如果还款时间小于账单日，利息应该为0
            else:
                # 计算提前结清利息:剩余还款本金*（实际还款时间-本期开始时间）*日利率
                days = get_day(asset_repay_plan["start_date"], self.repay_date)
                paid_prin_amt = asset_repay_plan["before_calc_principal"] * days * apply_rate / (100 * 360)
                repay_notice["repay_interest"] = float('{:.2f}'.format(paid_prin_amt))  # 利息

            repay_notice["repay_penalty_amount"] = 0
            repay_notice["repay_fee"] = 0
            repay_notice["actual_repay_amount"] = repay_notice["repay_principal"] + repay_notice[
                "repay_interest"]  # 总金额
            print("总金额：{}，本金：{}，利息{}".format(repay_notice["actual_repay_amount"], repay_notice["repay_principal"],
                                             repay_notice["repay_interest"]))

        repay_notice.update(kwargs)

        parser = DataUpdate(self.cfg['loan_repay_notice']['payload'], **repay_notice)
        self.repay_notice_payload = parser.parser
        self.log.info("payload数据: %s", self.repay_notice_payload)
        self.set_active_payload(self.repay_notice_payload)


if __name__ == '__main__':
    info = PayloadGenerator()
