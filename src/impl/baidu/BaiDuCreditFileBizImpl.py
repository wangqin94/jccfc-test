# -*- coding: utf-8 -*-
"""
    Function: 百度借据/费率/息费减免/还款计划/还款文件生成
"""

from engine.EnvInit import EnvInit
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils.Models import *
from utils.Logger import Logs
from datetime import datetime
from config.TestEnvInfo import *
from src.enums.EnumsCommon import ProductEnum

_log = Logs()
_ProjectPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # 项目根目录
_FilePath = os.path.join(_ProjectPath, 'FilePath', ProductEnum.BAIDU.value, TEST_ENV_INFO)  # 文件存放目录
if not os.path.exists(_FilePath):
    os.makedirs(_FilePath)


class BaiduFile(EnvInit):
    def __init__(self, data, cur_date=None, loan_record=0, repay_mode='02'):
        """ # 百度对账文件
        @param data:                用户四要素
        @param cur_date:            账务日期，默认None 为当前日期
        @param loan_record:         用户成功支用笔数，默认为0 为第1笔
        """
        super(BaiduFile, self).__init__()
        self.MysqlBizImpl = MysqlBizImpl()
        self.user_name = data['name']
        self.cer_no = data['cer_no']
        self.loan_record = loan_record
        self.repay_mode = repay_mode
        self.current_date = time.strftime('%Y%m%d', time.localtime())
        self.loan_id = 'LoanId' + str(int(round(time.time() * 1000)))

        # 获取借据及账单日期初始值
        self.cur_date = self.current_date if not cur_date else cur_date.replace('-', '')

        # 获取文件存储名
        data_save_path = '%s_%s_%s' % (self.user_name, self.cer_no, time.strftime('%Y%m%d', time.localtime()))
        self.data_save_path = os.path.join(_FilePath, data_save_path)
        self.loan_file_path = self.get_filename(self.cur_date)

        self.info = self.get_user_data_info()
        self.apply_date = self.info['apply_time'].strftime('%Y%m%d')
        self.period_list, self.bill_day = self.get_bill_day()

        self.open_csv_keys = [
            'cur_date', 'leader', 'parter', 'cust_name', 'cert_type', 'cert_no', 'loan_id',
            'apply_date', 'start_date', 'end_date', 'seq_no', 'encash_amt', 'currency',
            'repay_mode', 'repay_cycle', 'total_terms', 'grace_day', 'fund_status',
            'fail_type', 'partner_loan_id', 'order_id', 'card_no'
        ]
        self.repay_plan_csv_keys = [
            'cur_date',
            'loan_id',
            'term_no',
            'start_date',
            'end_date',
            'clear_date',
            'prin_total',
            'prin_repay',
            'int_total',
            'int_repay',
            'int_bal',
            'pnlt_int_total',
            'pnlt_int_repay',
            'fund_fee_total',
            'fund_fee_repay',
            'int_reduced_amt_coupon',
            'pnlt_reduced_amt_coupon',
            'fund_fee_reduced_amt_coupon',
            'term_status',
            'partner_loan_id',
            'charges_total',
            'charges_repay',
            'overdue_total',
            'overdue_repay',
            'repay_violate_total',
            'repay_violate_repay',
            'refund_violate_total',
            'refund_violate_repay',
            'service_total',
            'service_repay',
            'charges_reduced_amt_coupon',
            'overdue_reduced_amt_coupon',
            'repay_violate_reduced_amt_coupon',
            'refund_violate_reduced_amt_coupon',
            'service_reduced_amt_coupon',
            'prin_reduced_amt_manual',
            'int_reduced_amt_manual',
            'pnlt_reduced_amt_manual',
            'fund_fee_reduced_amt_manual',
            'charges_reduced_amt_manual',
            'overdue_reduced_amt_manual',
            'repay_violate_reduced_amt_manual',
            'refund_violate_reduced_amt_manual',
            'service_reduced_amt_manual',
        ]
        self.repay_item_csv_keys = [
            'cur_date',
            'loan_id',
            'tran_date',
            'tran_time',
            'seq_no',
            'term_no',
            'event',
            'total_amt',
            'int_reduced_amt_coupon',
            'pnlt_reduced_amt_coupon',
            'fund_fee_reduced_amt_coupon',
            'income_amt',
            'prin_amt',
            'int_amt',
            'pnlt_int_amt',
            'fund_fee_amt',
            'partner_loan_id',
            'charges_reduced_amt_coupon',
            'overdue_reduced_amt_coupon',
            'repay_violate_reduced_amt_coupon',
            'refund_violate_reduced_amt_coupon',
            'service_reduced_amt_coupon',
            'charges_amt',
            'overdue_amt',
            'repay_violate_amt',
            'refund_violate_amt',
            'service_amt',
        ]
        self.reduce_csv_keys = [
            'cur_date',
            'loan_id',
            'tran_date',
            'tran_time',
            'seq_no',
            'term_no',
            'event',
            'total_reduced_amt_manual',
            'prin_reduced_amt_manual',
            'int_reduced_amt_manual',
            'pnlt_reduced_amt_manual',
            'fund_fee_reduced_amt_manual',
            'charges_reduced_amt_manual',
            'overdue_reduced_amt_manual',
            'repay_violate_reduced_amt_manual',
            'refund_violate_reduced_amt_manual',
            'service_reduced_amt_manual',
            'partner_loan_id'
        ]
        self.loan_rate_csv_keys = [
            'cur_date',
            'loan_id',
            'start_term',
            'end_term',
            'int_rate',
            'int_rate_unit',
            'ovd_rate',
            'ovd_rate_unit',
            'fund_fee_ratio',
            'fund_fee_max',
            'fund_fee_min',
            'partner_loan_id',
            'charges_rate',
            'overdue_rate',
            'repay_violate_rate',
            'refund_violate_rate',
            'service_rate',
        ]
        self.open_csv_template = {
            'cur_date': self.cur_date,
            'leader': 'BAIDU',
            'parter': '0254',
            'cust_name': self.user_name,
            'cert_type': '01',
            'cert_no': self.cer_no,
            'loan_id': "",
            'apply_date': self.apply_date,
            'start_date': self.apply_date,
            'end_date': self.period_list[-1],
            'seq_no': str(int(round(time.time() * 1000))),
            'encash_amt': int(self.info['apply_amount']) * 100,
            'currency': '156',
            'repay_mode': '05',
            'repay_cycle': 'M',
            'total_terms': int(self.info['apply_term']),
            'grace_day': 4,
            'fund_status': '2',
            'fail_type': '',
            'partner_loan_id': self.info['loan_apply_id'],
            'order_id': self.info['thirdpart_order_id'],
            'card_no': data['bankid'],
        }
        self.repay_plan_csv_template = {
            'cur_date': self.cur_date,
            'loan_id': "",
            'term_no': "",
            'start_date': "",
            'end_date': "",
            'clear_date': "",
            'prin_total': "",
            'prin_repay': 0,
            'int_total': 0,
            'int_repay': 0,
            'int_bal': 0,
            'pnlt_int_total': 0,
            'pnlt_int_repay': 0,
            'fund_fee_total': 0,
            'fund_fee_repay': 0,
            'int_reduced_amt_coupon': 0,
            'pnlt_reduced_amt_coupon': 0,
            'fund_fee_reduced_amt_coupon': 0,
            'term_status': "5",
            'partner_loan_id': "",
            'charges_total': 0,
            'charges_repay': 0,
            'overdue_total': 0,
            'overdue_repay': 0,
            'repay_violate_total': 0,
            'repay_violate_repay': 0,
            'refund_violate_total': 0,
            'refund_violate_repay': 0,
            'service_total': 0,
            'service_repay': 0,
            'charges_reduced_amt_coupon': 0,
            'overdue_reduced_amt_coupon': 0,
            'repay_violate_reduced_amt_coupon': 0,
            'refund_violate_reduced_amt_coupon': 0,
            'service_reduced_amt_coupon': 0,
            'prin_reduced_amt_manual': 0,
            'int_reduced_amt_manual': 0,
            'pnlt_reduced_amt_manual': 0,
            'fund_fee_reduced_amt_manual': 0,
            'charges_reduced_amt_manual': 0,
            'overdue_reduced_amt_manual': 0,
            'repay_violate_reduced_amt_manual': 0,
            'refund_violate_reduced_amt_manual': 0,
            'service_reduced_amt_manual': 0
        }
        self.repay_item_csv_template = {
            'cur_date': "",
            'loan_id': "",
            'tran_date': "",
            'tran_time': "180910",
            'seq_no': "",
            'term_no': 1,
            'event': "12",
            'total_amt': 0,
            'int_reduced_amt_coupon': 0,
            'pnlt_reduced_amt_coupon': 0,
            'fund_fee_reduced_amt_coupon': 0,
            'income_amt': 0,
            'prin_amt': 0,
            'int_amt': 0,
            'pnlt_int_amt': 0,
            'fund_fee_amt': 0,
            'partner_loan_id': "",
            'charges_reduced_amt_coupon': 0,
            'overdue_reduced_amt_coupon': 0,
            'repay_violate_reduced_amt_coupon': 0,
            'refund_violate_reduced_amt_coupon': 0,
            'service_reduced_amt_coupon': 0,
            'charges_amt': 0,
            'overdue_amt': 0,
            'repay_violate_amt': 0,
            'refund_violate_amt': 0,
            'service_amt': 0
        }
        self.reduce_csv_template = {
            'cur_date': "",
            'loan_id': "",
            'tran_date': "",
            'tran_time': "180910",
            'seq_no': "",
            'term_no': 0,
            'event': "01",
            'total_reduced_amt_manual': 0,
            'prin_reduced_amt_manual': 0,
            'int_reduced_amt_manual': 0,
            'pnlt_reduced_amt_manual': 0,
            'fund_fee_reduced_amt_manual': 0,
            'charges_reduced_amt_manual': 0,
            'overdue_reduced_amt_manual': 0,
            'repay_violate_reduced_amt_manual': 0,
            'refund_violate_reduced_amt_manual': 0,
            'service_reduced_amt_manual': 0,
            'partner_loan_id': "",
        }
        self.loan_rate_csv_template = {
            'cur_date': "",
            'loan_id': "",
            'start_term': 1,
            'end_term': 3,
            'int_rate': 6.5,
            'int_rate_unit': "D",
            'ovd_rate': 9.8,
            'ovd_rate_unit': "D",
            'fund_fee_ratio': 0,
            'fund_fee_max': 0,
            'fund_fee_min': 0,
            'partner_loan_id': "",
            'charges_rate': 0,
            'overdue_rate': 0,
            'repay_violate_rate': 0,
            'refund_violate_rate': 0,
            'service_rate': 0,
        }

        # 获取每期应还本金和利息
        self.amount = loanByAvgAmt(self.info['apply_amount'], self.info['apply_term'], self.info['apply_rate'])

        # 根据生息日获取对应的账单日和还款日列表
        self.period_date_list, self.bill_day = self.get_bill_day()

        # 获取数据库表用户信息
        self.data_info = self.get_user_data_info()

    # 文件生成入口
    def start(self):
        # 开始写入借据文件
        self.get_open_csv(self.open_csv_template)
        self.get_loan_rate_csv(self.loan_rate_csv_template)
        # 开始写入还款计划/还款 文件
        for amt in self.amount:
            # period_id = strings + "%03d" % syb
            self.get_repay_plan_csv(self.repay_plan_csv_template, amt)

        self.log.demsg("借据文件生成路径：{}".format(_FilePath))

    def get_bill_day(self):
        """
        :return: 返回还款日期，账单日
        """
        date_list = str(self.info['apply_time']).split()[0].split('-')
        bill_year, bill_month, bill_day = map(int, date_list)
        period_date_list = []
        bill_day = 23 if bill_day > 28 else bill_day
        for _ in range(int(self.info['apply_term'])):
            bill_month += 1
            if bill_month > 12:
                bill_year += 1
                bill_month -= 12
            period_date_list.append("%d%02d%02d" % (bill_year, bill_month, bill_day))
        return period_date_list, "%02d" % bill_day

    # 获取文件存放路径，借据文件名，还款计划文件名
    def get_filename(self, repay_date):
        data_save_path = os.path.join(_FilePath, self.data_save_path, str(repay_date))
        if not os.path.exists(data_save_path):
            os.makedirs(data_save_path)
        return data_save_path

    def get_user_data_info(self):
        """
        :function: 获取用户数据库表中信息
        """
        # 查询的数据库表
        table = 'credit_loan_apply'
        # 查询sql语句
        sql = "select * from {}.credit_loan_apply where certificate_no='{}';".format(
            self.MysqlBizImpl.credit_database_name, self.cer_no)
        # 获取表属性字段名
        keys = self.MysqlBizImpl.mysql_credit.select_table_column(table_name=table, database=self.MysqlBizImpl.credit_database_name)
        # 获取查询内容
        values = self.MysqlBizImpl.mysql_credit.select(sql)
        try:
            info = [dict(zip(keys, item)) for item in values][self.loan_record]
        except IndexError as err:
            info = []
            _log.error(err)
        return info

    def get_open_csv(self, temple):
        temple['loan_id'] = self.loan_id
        temple['cur_date'] = self.cur_date
        temple['repay_mode'] = self.repay_mode
        open_csv = os.path.join(self.loan_file_path, 'open.csv')
        table_head = ','.join(self.open_csv_keys)
        val_list = map(str, [self.open_csv_template[key] for key in self.open_csv_keys])
        strings = ','.join(val_list)
        with open(open_csv, 'w', encoding='utf-8') as f:
            s = '\n'.join([table_head, strings])
            f.write(s)

    # 还款计划文件生成
    def get_repay_plan_csv(self, temple, amount_tuple):
        term = self.amount.index(amount_tuple) + 1
        temple['loan_id'] = self.loan_id
        temple['prin_total'] = str(amount_tuple[0])
        temple['int_total'] = str(amount_tuple[1])
        temple['cur_date'] = self.cur_date
        temple['term_no'] = str(term)
        temple['end_date'] = self.period_date_list[term - 1]
        repay_plan = os.path.join(self.loan_file_path, 'repay_plan.csv')
        if term == 1:
            temple['start_date'] = self.apply_date
            table_head = ','.join(self.repay_plan_csv_keys)
            with open(repay_plan, 'w', encoding='utf-8') as f:
                f.write(table_head)
                f.write('\n')
        else:
            temple['start_date'] = self.period_date_list[term - 2]
        val_list = map(str, [self.repay_plan_csv_template[key] for key in self.repay_plan_csv_keys])
        strings = ','.join(val_list)
        with open(repay_plan, 'a+', encoding='utf-8') as f:
            f.write(strings)
            f.write('\n')

    # 费率文件
    def get_loan_rate_csv(self, temple):
        temple['loan_id'] = self.loan_id
        temple['cur_date'] = self.cur_date
        temple['end_term'] = int(self.info["apply_term"])
        # 借据申请表提取年华利率转化为日利率
        temple['int_rate'] = float(self.info['apply_rate'])/360*100
        loan_rate = os.path.join(self.loan_file_path, 'loan_rate.csv')
        if self.repay_mode == "05":
            temple['repay_violate_rate'] = "4"
        table_head = ','.join(self.loan_rate_csv_keys)
        val_list = map(str, [self.loan_rate_csv_template[key] for key in self.loan_rate_csv_keys])
        strings = ','.join(val_list)
        with open(loan_rate, 'w', encoding='utf-8') as f:
            s = '\n'.join([table_head, strings])
            f.write(s)


class BaiduRepayFile(BaiduFile):
    def __init__(self, data, repay_mode='02', repay_date="2021-08-06", repay_term_no=1, repay_type='01',
                 loan_invoice_id=None, prin_amt=100, int_amt=0, pnlt_int_amt=0):
        """ # 百度还款对账文件
        @param data:                四要素
        @param repay_mode:          还款方式，02：随借随还；05：等额本息
        @param repay_date:          账务日期"2021-08-06"，提前结清必填
        @param repay_term_no:       还款期次
        @param repay_type:          还款类型，01：按期还款；02：提前结清；03：逾期还款
        @param loan_invoice_id:     借据号为None取用户第一笔借据，否则取自定义值
        @param prin_amt:            还款本金，随借随还部分还款必填
        @param int_amt:             还款利息，随借随还部分还款必填
        @param pnlt_int_amt:        还款罚息，随借随还部分还款必填
        """

        super(BaiduRepayFile, self).__init__(data)
        self.repay_mode = repay_mode
        self.repay_date = repay_date
        self.repay_term_no = repay_term_no
        self.repay_type = repay_type
        self.repay_file_path = ''
        self.loan_invoice_id = loan_invoice_id
        self.loan_no = self.get_loan_id()
        self.prin_amt = prin_amt
        self.int_amt = int_amt
        self.pnlt_int_amt = pnlt_int_amt

        # 文件生成入口
        self.start_repay_file()

    # 文件生成入口
    def start_repay_file(self):
        # 开始写入还款计划/还款 文件
        self.get_repay_item(self.repay_item_csv_template)
        self.get_new_repay_plan_csv(self.repay_plan_csv_template)
        self.get_reduce_csv(self.reduce_csv_template)
        self.log.demsg("还款文件生成路径：{}".format(_FilePath))

    def get_invoice_info(self):
        """
        return: 期次 total_term, 借据 loan_invoice_id
        """
        # self.loan_invoice_id 为none 按照用户名取第一条借据信息，否则取当条借据信息
        if self.loan_invoice_id:
            loan_invoice_id = self.loan_invoice_id
            key1 = "loan_invoice_id = '{}'".format(loan_invoice_id)
            credit_loan_invoice = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key1)
            total_term = int(credit_loan_invoice["installment_num"])
        else:
            key2 = "user_name = '{}'".format(self.user_name)
            credit_loan_invoice = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key2)
            total_term = int(credit_loan_invoice["installment_num"])
            loan_invoice_id = credit_loan_invoice["loan_invoice_id"]

        return total_term, loan_invoice_id

    def get_loan_id(self):
        """
        return: 三方借据号 loan_no
        """
        if self.loan_invoice_id:
            loan_invoice_id = self.loan_invoice_id
            key1 = "loan_invoice_id = '{}'".format(loan_invoice_id)
            mysql = self.MysqlBizImpl.get_credit_data_info(table="credit_third_wait_loan_deal_info", key=key1)
            loan_no = str(mysql["third_loan_no"])
        else:
            key2 = "user_name = '{}'".format(self.user_name)
            mysql = self.MysqlBizImpl.get_credit_data_info(table="credit_third_wait_loan_deal_info", key=key2)
            loan_no = str(mysql["third_loan_no"])

        return loan_no

    # 还款计划文件生成
    def get_new_repay_plan_csv(self, temple):
        # 写入头信息
        repay_plan = os.path.join(self.loan_file_path, 'repay_plan.csv')
        table_head = ','.join(self.repay_plan_csv_keys)
        with open(repay_plan, 'w', encoding='utf-8') as f:
            f.write(table_head)
            f.write('\n')

        # 根据借据Id和期次获取还款计划并写入
        total_term, loan_invoice_id = self.get_invoice_info()
        for term in range(total_term):
            key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loan_invoice_id, str(term + 1))
            asset_repay_plan = self.MysqlBizImpl.get_asset_data_info(table="asset_repay_plan", key=key3)

            temple['start_date'] = str(asset_repay_plan["start_date"]).replace("-", "")  # 开始时间
            temple['end_date'] = str(asset_repay_plan["pre_repay_date"]).replace("-", "")  # 结束时间
            temple['prin_total'] = int(float(asset_repay_plan["pre_repay_principal"])*100)  # 应还本金
            left_repay_principal = int(float(asset_repay_plan["left_repay_principal"])*100)  # 剩余应还本金
            temple['prin_repay'] = temple['prin_total'] - left_repay_principal  # 已还本金
            temple['int_total'] = int(float(asset_repay_plan["pre_repay_interest"])*100)  # 应还利息
            temple['int_bal'] = int(float(asset_repay_plan["left_repay_interest"])*100)  # 剩余应还利息
            temple['int_repay'] = temple['int_total'] - temple['int_bal']  # 已还利息
            temple['pnlt_int_total'] = int(float(asset_repay_plan["pre_repay_fee"])*100)  # 应还罚息
            left_repay_fee = int(float(asset_repay_plan["left_repay_fee"])*100)  # 剩余应还罚息
            temple['pnlt_int_repay'] = temple['pnlt_int_total'] - left_repay_fee  # 已还罚息

            temple['cur_date'] = self.repay_date.replace("-", "")
            temple['loan_id'] = self.loan_no
            temple['term_no'] = term + 1
            # 获取当前期次还款计划数据并写入
            val_list = map(str, [self.repay_plan_csv_template[key] for key in self.repay_plan_csv_keys])
            strings = ','.join(val_list)
            with open(repay_plan, 'a+', encoding='utf-8') as f:
                f.write(strings)
                f.write('\n')

    def get_repay_item(self, temple):
        temple['term_no'] = int(self.repay_term_no)
        temple['loan_id'] = self.loan_no
        temple['seq_no'] = 'seq_no' + str(int(round(time.time() * 1000)))

        # 获取用户借据信息
        total_term, loan_invoice_id = self.get_invoice_info()
        # 根据借据ID获取用户的申请费率
        key2 = "loan_invoice_id = '{}'".format(loan_invoice_id)
        credit_third_wait_loan_deal_info = self.MysqlBizImpl.get_credit_data_info(table="credit_third_wait_loan_deal_info", key=key2)
        interest_rate = credit_third_wait_loan_deal_info["interest_rate"]  # 年化利率

        # 根据借据Id和期次获取资产侧还款计划
        key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loan_invoice_id, self.repay_term_no)
        asset_repay_plan = self.MysqlBizImpl.get_asset_data_info(table="asset_repay_plan", key=key3)
        temple['total_amt'] = int(float(asset_repay_plan["pre_repay_amount"])*100)  # 总金额
        temple['income_amt'] = int(float(asset_repay_plan["pre_repay_amount"])*100)  # 不含优惠券总金额
        temple['prin_amt'] = int(float(asset_repay_plan["pre_repay_principal"])*100)  # 本金
        temple['int_amt'] = int(float(asset_repay_plan["pre_repay_interest"])*100)  # 利息
        temple['pnlt_int_amt'] = int(float(asset_repay_plan["left_repay_overdue_fee"])*100)  # 费用

        # 按期还款
        if self.repay_type == "01":
            temple['tran_date'] = str(asset_repay_plan["pre_repay_date"]).replace("-", "")
            temple['cur_date'] = str(asset_repay_plan["pre_repay_date"]).replace("-", "")

        # 逾期还款
        elif self.repay_type == "03":
            temple['tran_date'] = str(asset_repay_plan["calc_overdue_fee_date"]).replace("-", "")
            temple['cur_date'] = str(asset_repay_plan["calc_overdue_fee_date"]).replace("-", "")

        # 提前结清（按日收息）
        elif self.repay_type == "02":
            temple['tran_date'] = self.repay_date.replace("-", "")
            temple['cur_date'] = self.repay_date.replace("-", "")
            temple['prin_amt'] = int(float(asset_repay_plan["before_calc_principal"])*100)  # 剩余应还本金
            # 计算提前结清利息:剩余还款本金*（实际还款时间-本期开始时间）*日利率
            days = get_day(asset_repay_plan["start_date"], self.repay_date)

            # 字符串转为日期格式
            start_date = str(asset_repay_plan["start_date"])
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            repay_date = datetime.strptime(self.repay_date, "%Y-%m-%d").date()

            # 当期还款状态
            # repay_plan_status = str(asset_repay_plan["repay_plan_status"])

            if self.repay_mode == '02':
                # 利息\罚息,随借随还按日计息
                if repay_date <= start_date:
                    temple['int_amt'] = 0  # 如果当前期次已还款，利息应该为0
                else:
                    temple['int_amt'] = int(temple['prin_amt'] * days * interest_rate / (100 * 360))
                temple['pnlt_int_amt'] = 0
                temple['income_amt'] = temple['prin_amt'] + temple['int_amt']  # 不含优惠卷总金额
                temple['total_amt'] = temple['income_amt']  # 总金额
            else:
                # 利息\罚息，等额本息按期收息包含4%违约金
                if repay_date <= start_date:
                    temple['int_amt'] = 0  # 如果当前期次已还款，利息应该为0
                else:
                    temple['int_amt'] = int(float(asset_repay_plan["pre_repay_interest"])*100)
                temple['pnlt_int_amt'] = 0
                temple['repay_violate_amt'] = int(temple['prin_amt'] * 0.04)
                temple['income_amt'] = temple['prin_amt'] + temple['repay_violate_amt'] + temple['int_amt']  # 不含优惠卷总金额
                temple['total_amt'] = temple['income_amt']  # 总金额

        # 提前还当期
        elif self.repay_type == "04":
            temple['tran_date'] = self.repay_date.replace("-", "")
            temple['cur_date'] = self.repay_date.replace("-", "")

        # 提前部分还款
        elif self.repay_type == "05":
            temple['tran_date'] = self.repay_date.replace("-", "")
            temple['cur_date'] = self.repay_date.replace("-", "")
            temple['prin_amt'] = int(self.prin_amt) * 100  # 本金
            temple['int_amt'] = int(self.int_amt) * 100  # 利息
            temple['pnlt_int_amt'] = int(self.pnlt_int_amt) * 100  # 费用
            temple['income_amt'] = temple['prin_amt'] + temple['pnlt_int_amt'] + temple['int_amt']  # 不含优惠卷总金额
            temple['total_amt'] = temple['income_amt']  # 总金额

        # 写入头信息
        repay_item = os.path.join(self.loan_file_path, 'repay_item.csv')
        table_head = ','.join(self.repay_item_csv_keys)
        with open(repay_item, 'w', encoding='utf-8') as f:
            f.write(table_head)
            f.write('\n')
        val_list = map(str, [self.repay_item_csv_template[key] for key in self.repay_item_csv_keys])
        strings = ','.join(val_list)
        with open(repay_item, 'a+', encoding='utf-8') as f:
            f.write(strings)
            f.write('\n')

    # 手工减免息费明细文件
    def get_reduce_csv(self, temple):
        # 写入头信息
        reduce_csv = os.path.join(self.loan_file_path, 'reduce.csv')
        table_head = ','.join(self.reduce_csv_keys)
        with open(reduce_csv, 'w', encoding='utf-8') as f:
            f.write(table_head)
            f.write('\n')
        # 获取借据以及对应期次
        total_term, loan_invoice_id = self.get_invoice_info()

        # 根据借据Id和期次获取还款计划并写入
        for term in range(total_term):
            temple['loan_id'] = self.loan_no
            temple['tran_date'] = str(self.repay_date).replace("-", "")
            temple['cur_date'] = str(self.repay_date).replace("-", "")
            temple['seq_no'] = 'seqNo' + str(int(round(time.time() * 1000))) + str(term)
            temple['term_no'] = int(term) + 1
            # 获取当前期次还款计划数据并写入
            val_list = map(str, [self.reduce_csv_template[key] for key in self.reduce_csv_keys])
            strings = ','.join(val_list)
            with open(reduce_csv, 'a+', encoding='utf-8') as f:
                f.write(strings)
                f.write('\n')


if __name__ == '__main__':
    pass
    # 等额本息按期还款、提前结清收取违约金（4%）、提前结清按期收息；随借随还按期还款、部分还款（重算还款计划）、提前结清按日计息
    # repay_mode='02'随借随还，repay_mode='05'等额本息
    # t = BaiduFile(data, cur_date='20210812', loan_record=0, repay_mode='05')
