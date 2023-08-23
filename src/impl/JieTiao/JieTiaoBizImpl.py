# -*- coding: utf-8 -*-
# ------------------------------------------
# 借条接口数据封装类
# ------------------------------------------

from engine.EnvInit import EnvInit
from src.enums.EnumJieTiao import JieTiaoEnum
from src.impl.common.CommonBizImpl import post_with_encrypt
from src.impl.public.RepayPublicBizImpl import *
from src.test_data.module_data import JieTiao
from utils.Apollo import Apollo
from utils.Models import *


class JieTiaoBizImpl(EnvInit):
    def __init__(self, *, data=None, encrypt_flag=True, loan_invoice_id=None, person=True):
        """
        :param data:
        :param encrypt_flag: 加密
        :param loan_invoice_id: 借据号为None取用户第一笔借据，否则取自定义值
        :param person: 若person=True四要输写入person文件，否则不写入
        """
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()
        # 解析项目特性配置
        self.cfg = JieTiao.JieTiao
        self.data = self.get_user_info(data=data, person=person)

        self.encrypt_flag = encrypt_flag
        self.strings = str(int(round(time.time() * 1000)))
        self.loan_invoice_id = loan_invoice_id

        self.encrypt_url = self.host + JieTiaoEnum.JieTiaoEncryptPath.value
        self.decrypt_url = self.host + JieTiaoEnum.JieTiaoDecryptPath.value

        # 初始化payload变量
        self.active_payload = {}
        self.repayPublicBizImpl = RepayPublicBizImpl()
        self.apollo = Apollo()

    def get_user_info(self, data=None, person=True):
        # 获取四要素信息
        if data:
            data['loanReqNo'] = "loanReqNo" + str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
            update_user_info(data)
            base_data = data
        else:
            if person:
                base_data = get_base_data(str(self.env) + ' -> ' + str(ProductEnum.JieTiao.value), "loanReqNo")
            else:
                base_data = get_base_data_temp()
        return base_data

    def loan(self, loan_date=None, **kwargs):
        loan_data = dict()
        date = str(get_before_day(1)).replace('-', '')
        self.MysqlBizImpl.update_channel_database_info('channel_loan_amount', attr="product_id='F22E011'",
                                                       business_date=date)
        loan_data['loanReqNo'] = self.data['loanReqNo']
        loan_data['custName'], loan_data['dbAcctName'] = self.data['name'], self.data['name']
        loan_data['id'] = self.data['cer_no']
        loan_data['dbAcct'] = self.data['bankid']
        loan_data['mobileNo'] = self.data['telephone']
        loan_data['loanDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 更新 payload 字段值
        loan_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan']['payload'], **loan_data)
        self.active_payload = parser.parser
        # 设置apollo放款mock时间 默认当前时间
        loan_date = loan_date if loan_date else time.strftime('%Y-%m-%d', time.localtime())
        apollo_data = dict()
        apollo_data['credit.loan.trade.date.mock'] = True
        apollo_data['credit.loan.date.mock'] = loan_date
        self.apollo.update_config(appId='loan2.1-public', namespace='JCXF.system', **apollo_data)

        self.log.demsg('放款请求接口...')
        url = self.host + self.cfg['loan']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def loan_query(self, **kwargs):
        loan_query_data = dict()

        loan_query_data['loanReqNo'] = self.data['loanReqNo']
        # 更新 payload 字段值
        loan_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan_query']['payload'], **loan_query_data)
        self.active_payload = parser.parser

        self.log.demsg('放款结果查询接口...')
        url = self.host + self.cfg['loan_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def payment(self, **kwargs):
        payment_data = dict()

        payment_data['tranNo'] = 'repayReqNo' + self.strings + "1"
        payment_data['repayCstname'] = self.data['name']
        payment_data['repayRelcard'] = self.data['cer_no']
        payment_data['repayBankAcct'] = self.data['bankid']
        payment_data['repayRelphone'] = self.data['telephone']

        # 更新 payload 字段值
        payment_data.update(kwargs)
        parser = DataUpdate(self.cfg['payment']['payload'], **payment_data)
        self.active_payload = parser.parser

        self.log.demsg('代扣接口...')
        url = self.host + self.cfg['payment']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def payment_query(self, **kwargs):
        payment_query_data = dict()

        # 更新 payload 字段值
        payment_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['payment_query']['payload'], **payment_query_data)
        self.active_payload = parser.parser

        self.log.demsg('代扣结果查询接口...')
        url = self.host + self.cfg['payment_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def repay_notice(self, rpyTerm="1", rpyType="02", rpyDate="2022-07-01", **kwargs):
        """
        还款通知
        :param rpyTerm: 还款期数
        :param rpyType: 还款类型：提前还款:01 期供还款:02 逾期还款：03
        :param rpyDate: 还款日期
        :param kwargs:
        :return:
        """
        # 还款前置任务
        self.repayPublicBizImpl.pre_repay_config(repayDate=rpyDate)
        repay_notice_data = dict()

        repay_notice_data['rpyReqNo'] = 'rpyNoticeNo' + self.strings + "4"
        repay_notice_data['loanReqNo'] = self.data['loanReqNo']
        repay_notice_data['tranNo'] = 'tranNo' + self.strings + "5"
        repay_notice_data['rpyTerm'] = rpyTerm
        repay_notice_data['rpyType'] = rpyType

        # 根据idNo查询支用信息
        key1 = "certificate_no = '{}'".format(self.data['cer_no'])
        credit_loan_apply = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_apply", key=key1)
        # 根据支用申请单号查询借据信息
        if self.loan_invoice_id:
            loan_invoice_id = self.loan_invoice_id
            # key2 = "loan_invoice_id = '{}'".format(loan_invoice_id)
            # credit_loan_invoice = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key2)
            # loan_apply_id = credit_loan_invoice["loan_apply_id"]
            # key21 = "loan_apply_id = '{}'".format(loan_apply_id)
            # credit_loan_apply = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_apply", key=key21)
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
        key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loan_invoice_id, rpyTerm)
        asset_repay_plan = self.MysqlBizImpl.get_asset_data_info(table="asset_repay_plan", key=key3)

        repay_notice_data["rpyPrinAmt"] = float(asset_repay_plan['left_repay_principal'])  # 本金
        repay_notice_data["rpyIntAmt"] = float(asset_repay_plan['left_repay_interest'])  # 利息
        repay_notice_data["rpyOintAmt"] = float(asset_repay_plan['left_repay_overdue_fee'])  # 逾期罚息

        if rpyType == '02':
            repay_notice_data['rpyDate'] = str(asset_repay_plan["pre_repay_date"])
        if rpyType == '03':
            finish_time = asset_repay_plan["calc_overdue_fee_date"] - relativedelta(days=-int(1))
            repay_notice_data['rpyDate'] = str(finish_time)
        if rpyType == '01':
            repay_notice_data['rpyDate'] = rpyDate
            repay_notice_data["rpyPrinAmt"] = float('{:.2f}'.format(asset_repay_plan['before_calc_principal']))  # 本金

            pre_repay_date = str(asset_repay_plan["start_date"])
            pre_repay_date = datetime.strptime(pre_repay_date, "%Y-%m-%d").date()
            repay_date = datetime.strptime(rpyDate, "%Y-%m-%d").date()
            if pre_repay_date > repay_date:
                repay_notice_data["rpyIntAmt"] = 0  # 如果还款时间小于账单日，利息应该为0
            else:
                # 计算提前结清利息:剩余还款本金*（实际还款时间-本期开始时间）*日利率
                days = get_day(asset_repay_plan["start_date"], repay_date)
                paid_prin_amt = asset_repay_plan["before_calc_principal"] * days * execute_rate / (100 * 365)
                repay_notice_data["rpyIntAmt"] = float('{:.2f}'.format(paid_prin_amt))  # 利息

        # 更新 payload 字段值
        repay_notice_data.update(kwargs)
        parser = DataUpdate(self.cfg['repay_notice']['payload'], **repay_notice_data)
        self.active_payload = parser.parser

        self.log.demsg('还款通知接口...')
        url = self.host + self.cfg['repay_notice']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def repay_query(self, **kwargs):
        repay_query_data = dict()

        # 更新 payload 字段值
        repay_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['repay_query']['payload'], **repay_query_data)
        self.active_payload = parser.parser

        self.log.demsg('还款查询接口...')
        url = self.host + self.cfg['repay_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response
