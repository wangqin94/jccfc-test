# -*- coding: utf-8 -*-
"""
    Function: 美团借据/还款计划/还款文件生成
"""

import sys
from datetime import date, timedelta

from engine.EnvInit import EnvInit
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils.Logger import Logs
from src.enums.EnumsCommon import *
from src.impl.common.CommonBizImpl import *

_log = Logs()
_ProjectPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # 项目根目录
_FilePath = os.path.join(_ProjectPath, 'FilePath', ProductEnum.MEITUAN.value, TEST_ENV_INFO)  # 文件存放目录
if not os.path.exists(_FilePath):
    os.makedirs(_FilePath)


class MtFile(EnvInit):
    def __init__(self, certificate_no, user_name, apply_date=None, delay=(0, 0), loan_record=0):
        """
        @param certificate_no:  用户身份证号
        @param user_name:       用户姓名
        @param apply_date:      放贷日期'2021-06-30', 为None时，取当前系统时间
        @param delay:           逾期数据, (逾期期数, 逾期天数)
        @param loan_record:     用户第几笔去用申请，0为第一笔，1为第二笔
        """
        super().__init__()
        self.log.demsg('当前测试环境 %s', TEST_ENV_INFO)
        self.MysqlBizImpl = MysqlBizImpl()
        self.user_name = user_name
        self.certificate_no = certificate_no
        self.loan_record = loan_record
        self.current_date = time.strftime('%Y-%m-%d', time.localtime())
        # 获取借据及账单日期初始值
        self.loan_date = self.current_date if not apply_date else apply_date
        self.delay_days = 0  # 逾期天数
        self.delay_term = delay[0]  # 逾期期数，第几期设定为逾期
        if self.delay_term > 0:
            self.delay_days = delay[1]  # 设置用户自定义逾期天数
        self.repay_all_strings = list()  # 提前结清还款字符串列表
        self.loan_id = str(int(round(time.time() * 1000))) + "10086"
        # 获取文件名及存放路径
        self.data_save_path, self.bank_loan_filename, self.bank_period_filename = self.get_filename()
        print(self.data_save_path, self.bank_loan_filename, self.bank_period_filename)

        # 获取用户数据库表 hsit_credit.credit_loan_apply, hsit_user.user_financial_instrument_info信息
        self.data_info = self.MysqlBizImpl.get_credit_database_info('credit_loan_apply', record=self.loan_record,
                                                                    certificate_no=self.certificate_no)
        self.data_info1 = self.MysqlBizImpl.get_user_database_info('user_financial_instrument_info',
                                                                   account_name=self.user_name)

        # 根据生息日获取对应的账单日和还款日列表
        self.period_date_list, self.bill_day = self.loan_and_period_date_parser(self.loan_date,
                                                                                period=self.data_info['apply_term'])
        # 借据/还款计划/还款 字段名列表，(文件生成时字符串拼接使用)
        self.loan_temple = [
            'loan_id',
            'account_id',
            'loan_no',
            'card_no',
            'card_bank_name',
            'fund_seq_no',
            'loan_type',
            'interest_rate',
            'interest_rate_duration_unit',
            'penalty_interest_rate',
            'penalty_interest_rate_duration_unit',
            'loan_total_principal',
            'loan_periods',
            'repay_type',
            'interval_type',
            'total_terms',
            'start_interest_day',
            'open_date',
            'expire_date',
            'status',
            'settle_date',
            'loan_balance',
            'planed_principal',
            'non_planed_principal',
            'principal_balance',
            'interest_balance',
            'interest_penalty_balance',
            'fee_balance',
            'deserved_principal_amount',
            'deserved_interest_amount',
            'deserved_interest_penalty_amount',
            'deserved_fee_amount',
            'paid_principal_amount',
            'paid_interest_amount',
            'paid_interest_penalty_amount',
            'paid_fee_amount',
            'overdue_days',
            'overdue_level',
            'version',
            'add_time',
            'update_time',
            'creditor_proportion',
            'app_no',
            'use_type',
            'channel',
            'bill_day',
            'start_refund_date',
        ]
        self.period_temple = [
            'period_id',
            'loan_id',
            'status',
            'plan_repay_date',
            'settle_date',
            'overdue_level',
            'overdue_days',
            'period_balance',
            'principal_balance',
            'interest_balance',
            'interest_penalty_balance',
            'fee_balance',
            'deserved_principal_amount',
            'deserved_interest_amount',
            'deserved_interest_penalty_amount',
            'deserved_fee_amount',
            'paid_principal_amount',
            'paid_interest_amount',
            'paid_interest_penalty_amount',
            'paid_fee_amount',
            'add_time',
            'update_time',
            'version',
            'current_period',
            'loan_no',
        ]
        self.repay_temple = [
            'business_ref_no',
            'loan_no',
            'loan_id',
            'period_id',
            'repay_type',
            'repay_date',
            'repay_amt',
            'paid_prin_amt',
            'paid_int_amt',
            'paid_ovd_prin_pnlt_amt_00',
            'repay_fee',
            'trade_timestamp',
            'current_period',
            'status',
            'plan_repay_date'
        ]

        # 借据/还款计划/还款 键值对字典数据模板
        self.bank_loan_temple = {
            'loan_id': self.loan_id,
            'account_id': str(int(round(time.time() * 1000))) + "10010",
            'loan_no': self.data_info['third_loan_invoice_id'],
            'card_no': self.data_info1['account'],
            'card_bank_name': self.data_info1['open_brank_name'],
            'fund_seq_no': self.data_info['loan_apply_serial_id'],
            'loan_type': '0',
            'interest_rate': '9.8',
            'interest_rate_duration_unit': '1',
            'penalty_interest_rate': '9.8',
            'penalty_interest_rate_duration_unit': '1',
            'loan_total_principal': self.data_info['apply_amount'] * 100,
            'loan_periods': self.data_info['apply_term'],
            'repay_type': '1',
            'interval_type': '0',
            'total_terms': self.data_info['apply_term'],
            'start_interest_day': self.loan_date,
            'open_date': self.loan_date,
            'expire_date': self.period_date_list[-1],
            'status': '0',
            'settle_date': '',
            'loan_balance': self.data_info['apply_amount'] * 100,
            'planed_principal': self.data_info['apply_amount'] * 100,
            'non_planed_principal': '0',
            'principal_balance': '0',
            'interest_balance': '0',
            'interest_penalty_balance': '0',
            'fee_balance': '0',
            'deserved_principal_amount': self.data_info['apply_amount'] * 100,
            'deserved_interest_amount': '0',
            'deserved_interest_penalty_amount': '0',
            'deserved_fee_amount': '0',
            'paid_principal_amount': '0',
            'paid_interest_amount': '0',
            'paid_interest_penalty_amount': '0',
            'paid_fee_amount': '0',
            'overdue_days': '0',
            'overdue_level': '0',
            'version': '2',
            'add_time': self.data_info['create_time'],
            'update_time': self.data_info['update_time'],
            'creditor_proportion': '0.9',
            'app_no': self.data_info['thirdpart_apply_id'],
            'use_type': '1',
            'channel': '1',
            'bill_day': self.bill_day,
            'start_refund_date': self.period_date_list[0]}
        self.bank_period_temple = {
            'period_id': '',
            'loan_id': self.loan_id,
            'status': '0',
            'plan_repay_date': '2021-02-20',
            'settle_date': '',
            'overdue_level': '0',
            'overdue_days': '0',
            'period_balance': '0',
            'principal_balance': '0',
            'interest_balance': '0',
            'interest_penalty_balance': '0',
            'fee_balance': '0',
            'deserved_principal_amount': '19514',
            'deserved_interest_amount': '1646',
            'deserved_interest_penalty_amount': '0',
            'deserved_fee_amount': '0',
            'paid_principal_amount': '0',
            'paid_interest_amount': '0',
            'paid_interest_penalty_amount': '0',
            'paid_fee_amount': '0',
            'add_time': '',
            'update_time': '',
            'version': '1',
            'current_period': '1',
            'loan_no': self.data_info['third_loan_invoice_id'],
        }
        self.bank_repay_temple = {
            'business_ref_no': '',
            'loan_no': self.data_info['third_loan_invoice_id'],
            'loan_id': self.loan_id,
            'period_id': '',
            'repay_type': '1',
            'repay_date': '',
            'repay_amt': '',
            'paid_prin_amt': '',
            'paid_int_amt': '',
            'paid_ovd_prin_pnlt_amt_00': '',
            'repay_fee': '0',
            'trade_timestamp': '',
            'current_period': '',
            'status': '',
            'plan_repay_date': '',
        }

        # 支持借款金额和期数的本金利息列表， 自定义添加值
        self.amount_dict = {
            '500_3': [(19385, 1823), (20014, 1194), (20601, 606)],
            '600_3': [(19391, 1823), (20020, 1194), (20589, 625)],
            '800_3': [(25847, 2430), (26685, 1592), (27468, 808)],
            '1000_3': [(32308, 3038), (33356, 1990), (34336, 1009)],
            '2000_6': [(32308, 3038), (33356, 1990), (34336, 1009), (32308, 3038), (33356, 1990), (34336, 1009)],
            '2000_3': [(32308, 3038), (33356, 1990), (34336, 1009)],
            '10000_3': [(325231, 27440), (332172, 20499), (342597, 10072)],
            '10000_12': [(325231, 27440), (332172, 20499), (342597, 10072), (325231, 27440), (332172, 20499),
                         (342597, 10072), (325231, 27440), (332172, 20499), (342597, 10072), (325231, 27440),
                         (332172, 20499), (342597, 10072)],
            '20000_3': [(650461, 54880), (664342, 40999), (685197, 20145)],
            '30000_3': [(975692, 82320), (996514, 61498), (1027794, 30217)],
        }

        # 获取每期应还本金和利息
        # self.amount = self.get_repay_period_amount()
        self.amount = loanByAvgAmt(self.data_info['apply_amount'], self.data_info['apply_term'],
                                   self.data_info['apply_rate'])

        # 执行
        self.start()

    # 文件生成入口
    def start(self):
        # 开始写入借据文件
        self.bank_loan_create()
        # 写入还款计划数据头信息
        with open(self.bank_period_filename, 'w', encoding='utf-8') as f:
            f.write("dataRowCount|+|%d" % len(self.period_date_list))
        # 开始写入还款计划/还款 文件
        syb, strings = 1, str(int(round(time.time() * 1000)))
        for amt, dates in zip(self.amount, self.period_date_list):
            period_id = strings + "%03d" % syb
            self.bank_period_create(self.bank_period_temple, amt, dates, period_id)
            self.bank_repay_period(self.bank_repay_temple, amt, dates, period_id)
            syb += 1  # period_id 尾部标记，区分每期的ID
        # 生成提前结清文件
        self.repay_all()
        self.log.demsg("还款文件生成路径：{}".format(_FilePath))

    # 获取文件存放路径，借据文件名，还款计划文件名
    def get_filename(self):
        # 初始化文件存放路径，(用户_身份证号)
        data_save_path = '%s_%s' % (
            self.user_name, self.certificate_no)
        data_save_path = os.path.join(_FilePath, data_save_path, self.loan_date.replace('-', ''))
        if not os.path.exists(data_save_path):
            os.makedirs(data_save_path)
        # 借据文件名
        loan_create = os.path.join(data_save_path, 'bank_loan_create_%s.txt' % self.loan_date.replace('-', ''))
        # 还款计划文件名
        period_create = os.path.join(data_save_path, 'bank_period_create_%s.txt' % (self.loan_date.replace('-', '')))
        return data_save_path, loan_create, period_create

    # 日期计算
    @staticmethod
    def loan_and_period_date_parser(date_str, period, flag=True):
        """
        @param date_str: (str)借款日期  eg: '2020-01-09'
        @param period: (int)分期数  eg: 3
        @param flag:
        :return:
        """
        date_list = date_str.split('-')
        bill_year = int(date_list[0])
        bill_month = int(date_list[1])
        bill_day = int(date_list[-1])
        period_date_list = []
        if bill_day >= 26:
            bill_day -= 25
            bill_month += 1
        for _ in range(int(period)):
            bill_month += 1
            if bill_month > 12:
                bill_year += 1
                bill_month -= 12
            period_date_list.append("%d-%02d-%02d" % (bill_year, bill_month, bill_day))
        return period_date_list, "%02d" % bill_day

    # 获取每期应还本金利息数据
    def get_repay_period_amount(self):
        flag = "%s_%s" % (str(int(self.data_info['apply_amount'])), str(int(self.data_info['apply_term'])))
        print(flag)
        if flag not in self.amount_dict:
            print("################ 放款金额或还款期数不支持, 请联系管理员... ###################")
            sys.exit()
        # 获取每期应还本金和利息
        return self.amount_dict[
            '%s_%s' % (str(int(self.data_info['apply_amount'])), str(int(self.data_info['apply_term'])))]

    # 借据文件生成
    def bank_loan_create(self):
        val_list = map(str, [self.bank_loan_temple[key] for key in self.loan_temple])
        strs = '|+|'.join(val_list)
        with open(self.bank_loan_filename, 'w', encoding='utf-8') as f:
            f.write("dataRowCount|+|1")
            f.write('\n')
            f.write(strs)
        # 创建.ok文件
        with open(os.path.splitext(self.bank_loan_filename)[0] + '.ok', 'w', encoding='utf-8') as f:
            f.write('%s' % os.path.basename(self.bank_loan_filename))

    # 还款计划文件生成
    def bank_period_create(self, temple, amount_tuple, plan_repay_date, period_id):
        term = self.amount.index(amount_tuple) + 1
        times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        temple['period_id'] = period_id
        temple['deserved_principal_amount'] = str(amount_tuple[0])
        temple['deserved_interest_amount'] = str(amount_tuple[1])
        temple['add_time'] = times
        temple['update_time'] = times
        temple['plan_repay_date'] = plan_repay_date
        temple['current_period'] = str(term)
        val_list = map(str, [temple[key] for key in self.period_temple])
        strs = '|+|'.join(val_list)
        with open(self.bank_period_filename, 'a+', encoding='utf-8') as f:
            f.write('\n')
            f.write(strs)
        # 创建.ok文件
        with open(os.path.splitext(self.bank_period_filename)[0] + '.ok', 'w', encoding='utf-8') as f:
            f.write('%s' % os.path.basename(self.bank_period_filename))

    # 还款文件生成
    def bank_repay_period(self, temple, amount_tuple, plan_repay_date, period_id):
        """
        @param temple: 还款字段字典模板
        @param amount_tuple: 当前期应还本金和利息
        @param plan_repay_date: 计划还款日
        @param period_id: 还款期ID与还款计划相对应
        :return:
        """
        times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        term = self.amount.index(amount_tuple) + 1
        repay_date = plan_repay_date
        if term == self.delay_term:
            repay_date = str(date(*map(int, plan_repay_date.split('-'))) + timedelta(days=int(self.delay_days)))
            print('repay_date: ', repay_date)
        # temple['repay_type'] = '1'  # 提前结清
        temple['repay_type'] = '3'  # 按期还款
        if term == self.delay_term and self.delay_days > 0:
            temple['repay_type'] = '8'  # 逾期代扣
        temple['business_ref_no'] = str(round(time.time_ns()))
        temple['period_id'] = period_id
        temple['repay_date'] = repay_date
        temple['repay_amt'] = str(sum(amount_tuple))
        temple['paid_prin_amt'] = str(amount_tuple[0])
        temple['paid_int_amt'] = str(amount_tuple[1])
        temple['paid_ovd_prin_pnlt_amt_00'] = '0'
        if term == self.delay_term:
            temple['paid_ovd_prin_pnlt_amt_00'] = str('{:.2f}'.format(amount_tuple[0] * 0.00098 * self.delay_days))
        temple['trade_timestamp'] = repay_date + ' ' + time.strftime('%H:%M:%S', time.localtime())
        temple['plan_repay_date'] = plan_repay_date
        temple['current_period'] = str(term)
        temple['status'] = '1'
        # 单期还款文件名
        filename = 'bank_repay_period_%s.txt' % (plan_repay_date.replace('-', ''))
        repay_period_filename = os.path.join(self.data_save_path, filename)
        # 写入单期还款文件
        with open(repay_period_filename, 'w', encoding='utf-8') as f:
            f.write("dataRowCount|+|1")
        val_list = map(str, [temple[key] for key in self.repay_temple])
        strs = '|+|'.join(val_list)
        with open(repay_period_filename, 'a+', encoding='utf-8') as f:
            f.write('\n')
            f.write(strs)
        # 创建.ok文件
        with open(os.path.splitext(repay_period_filename)[0] + '.ok', 'w', encoding='utf-8') as f:
            f.write('%s' % os.path.basename(repay_period_filename))
        # 提前还款信息生成
        temple['repay_type'] = '1'
        temple['repay_date'] = self.current_date
        # 首期提前还款利息金额
        if term == 1:
            occupy = (date(*map(int, self.current_date.split('-'))) - date(*map(int, self.loan_date.split('-')))).days
            occupy = 1 if occupy == 0 else occupy  # 头尾只算一个，当天还款算一天
            inrt = str('{:.2f}'.format(amount_tuple[0] * 0.00098 * occupy))  # 提前结清利息
            temple['paid_int_amt'] = inrt
        else:
            temple['paid_int_amt'] = '0'
        val_list = map(str, [temple[key] for key in self.repay_temple])
        strs = '|+|'.join(val_list)
        self.repay_all_strings.append(strs)

    # 提前结清文件
    def repay_all(self):
        repay_all_filename = 'bank_repay_period_%s.txt' % (time.strftime('%Y%m%d', time.localtime()))
        repay_all_filename = os.path.join(self.data_save_path, 'repay_all_' + repay_all_filename)
        strings = '\n'.join(self.repay_all_strings)
        with open(repay_all_filename, 'w', encoding='utf-8') as f:
            f.write("dataRowCount|+|%s" % len(self.amount))
            f.write('\n')
            f.write(strings)
        # 创建.ok文件
        with open(os.path.splitext(repay_all_filename)[0] + '.ok', 'w', encoding='utf-8') as f:
            f.write('%s' % os.path.basename(repay_all_filename))


class MeiTuanLoanFile(EnvInit):
    def __init__(self, data, apply_date=None, loan_record=0):
        """
        @param data:            用户四要素
        @param apply_date:      放贷日期'2021-06-30', 为None时，取当前系统时间
        @param loan_record:     用户第几笔去用申请，0为第一笔，1为第二笔
        """
        super().__init__()
        self.log.demsg('当前测试环境 %s', self.env)
        self.MysqlBizImpl = MysqlBizImpl()
        self.user_name = data['name']
        self.certificate_no = data['cer_no']
        # 获取借据及账单日期初始值
        self.current_date = time.strftime('%Y-%m-%d', time.localtime())
        self.loan_date = self.current_date if not apply_date else apply_date

        self.loan_id = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999)) + "10086"
        # 获取文件名及存放路径
        self.data_save_path, self.bank_loan_create_path, self.bank_period_create_path, self.bank_loan_filename, self.bank_period_filename = self.get_filename()

        # 获取用户数据库表 hsit_credit.credit_loan_apply, hsit_user.user_financial_instrument_info信息
        self.credit_loan_apply = self.MysqlBizImpl.get_credit_database_info('credit_loan_apply', record=loan_record,
                                                                            certificate_no=self.certificate_no)
        self.data_info1 = self.MysqlBizImpl.get_user_database_info('user_financial_instrument_info',
                                                                   account_name=self.user_name)

        # 根据生息日获取对应的账单日和还款日列表
        self.period_date_list, self.bill_day = self.loan_and_period_date_parser(self.loan_date,
                                                                                period=self.credit_loan_apply[
                                                                                    'apply_term'])
        # 借据/还款计划/还款 字段名列表，(文件生成时字符串拼接使用)
        self.loan_temple = [
            'loan_id',
            'account_id',
            'loan_no',
            'card_no',
            'card_bank_name',
            'fund_seq_no',
            'loan_type',
            'interest_rate',
            'interest_rate_duration_unit',
            'penalty_interest_rate',
            'penalty_interest_rate_duration_unit',
            'loan_total_principal',
            'loan_periods',
            'repay_type',
            'interval_type',
            'total_terms',
            'start_interest_day',
            'open_date',
            'expire_date',
            'status',
            'settle_date',
            'loan_balance',
            'planed_principal',
            'non_planed_principal',
            'principal_balance',
            'interest_balance',
            'interest_penalty_balance',
            'fee_balance',
            'deserved_principal_amount',
            'deserved_interest_amount',
            'deserved_interest_penalty_amount',
            'deserved_fee_amount',
            'paid_principal_amount',
            'paid_interest_amount',
            'paid_interest_penalty_amount',
            'paid_fee_amount',
            'overdue_days',
            'overdue_level',
            'version',
            'add_time',
            'update_time',
            'creditor_proportion',
            'app_no',
            'use_type',
            'channel',
            'bill_day',
            'start_refund_date',
        ]
        self.period_temple = [
            'period_id',
            'loan_id',
            'status',
            'plan_repay_date',
            'settle_date',
            'overdue_level',
            'overdue_days',
            'period_balance',
            'principal_balance',
            'interest_balance',
            'interest_penalty_balance',
            'fee_balance',
            'deserved_principal_amount',
            'deserved_interest_amount',
            'deserved_interest_penalty_amount',
            'deserved_fee_amount',
            'paid_principal_amount',
            'paid_interest_amount',
            'paid_interest_penalty_amount',
            'paid_fee_amount',
            'add_time',
            'update_time',
            'version',
            'current_period',
            'loan_no',
        ]
        self.repay_temple = [
            'business_ref_no',
            'loan_no',
            'loan_id',
            'period_id',
            'repay_type',
            'repay_date',
            'repay_amt',
            'paid_prin_amt',
            'paid_int_amt',
            'paid_ovd_prin_pnlt_amt_00',
            'repay_fee',
            'trade_timestamp',
            'current_period',
            'status',
            'plan_repay_date'
        ]

        # 借据/还款计划/还款 键值对字典数据模板
        self.bank_loan_temple = {
            'loan_id': self.loan_id,
            'account_id': str(int(round(time.time() * 1000))) + "10010",
            'loan_no': self.credit_loan_apply['third_loan_invoice_id'],
            'card_no': self.data_info1['account'],
            'card_bank_name': self.data_info1['open_brank_name'],
            'fund_seq_no': self.credit_loan_apply['loan_apply_serial_id'],
            'loan_type': '0',
            'interest_rate': '9.8',
            'interest_rate_duration_unit': '1',
            'penalty_interest_rate': '9.8',
            'penalty_interest_rate_duration_unit': '1',
            'loan_total_principal': self.credit_loan_apply['apply_amount'] * 100,
            'loan_periods': self.credit_loan_apply['apply_term'],
            'repay_type': '1',
            'interval_type': '0',
            'total_terms': self.credit_loan_apply['apply_term'],
            'start_interest_day': self.loan_date,
            'open_date': self.loan_date,
            'expire_date': self.period_date_list[-1],
            'status': '0',
            'settle_date': '',
            'loan_balance': self.credit_loan_apply['apply_amount'] * 100,
            'planed_principal': self.credit_loan_apply['apply_amount'] * 100,
            'non_planed_principal': '0',
            'principal_balance': '0',
            'interest_balance': '0',
            'interest_penalty_balance': '0',
            'fee_balance': '0',
            'deserved_principal_amount': self.credit_loan_apply['apply_amount'] * 100,
            'deserved_interest_amount': '0',
            'deserved_interest_penalty_amount': '0',
            'deserved_fee_amount': '0',
            'paid_principal_amount': '0',
            'paid_interest_amount': '0',
            'paid_interest_penalty_amount': '0',
            'paid_fee_amount': '0',
            'overdue_days': '0',
            'overdue_level': '0',
            'version': '2',
            'add_time': self.credit_loan_apply['create_time'],
            'update_time': self.credit_loan_apply['update_time'],
            'creditor_proportion': '0.9',
            'app_no': self.credit_loan_apply['thirdpart_apply_id'],
            'use_type': '1',
            'channel': '1',
            'bill_day': self.bill_day,
            'start_refund_date': self.period_date_list[0]}
        self.bank_period_temple = {
            'period_id': '',
            'loan_id': self.loan_id,
            'status': '0',
            'plan_repay_date': '2021-02-20',
            'settle_date': '',
            'overdue_level': '0',
            'overdue_days': '0',
            'period_balance': '0',
            'principal_balance': '0',
            'interest_balance': '0',
            'interest_penalty_balance': '0',
            'fee_balance': '0',
            'deserved_principal_amount': '19514',
            'deserved_interest_amount': '1646',
            'deserved_interest_penalty_amount': '0',
            'deserved_fee_amount': '0',
            'paid_principal_amount': '0',
            'paid_interest_amount': '0',
            'paid_interest_penalty_amount': '0',
            'paid_fee_amount': '0',
            'add_time': '',
            'update_time': '',
            'version': '1',
            'current_period': '1',
            'loan_no': self.credit_loan_apply['third_loan_invoice_id'],
        }

        # 获取每期应还本金和利息
        # self.amount = self.get_repay_period_amount()
        self.amount = loanByAvgAmt(self.credit_loan_apply['apply_amount'], self.credit_loan_apply['apply_term'],
                                   self.credit_loan_apply['apply_rate'])

        # 执行
        self.start()

    # 文件生成入口
    def start(self):
        # 开始写入借据文件
        self.bank_loan_create()
        # 写入还款计划数据头信息
        with open(self.bank_period_filename, 'w', encoding='utf-8') as f:
            f.write("dataRowCount|+|%d" % len(self.period_date_list))
        # 开始写入还款计划 文件
        syb, strings = 1, str(int(round(time.time() * 1000)))
        for amt, dates in zip(self.amount, self.period_date_list):
            period_id = strings + "%03d" % syb
            self.bank_period_create(self.bank_period_temple, amt, dates, period_id)
            syb += 1  # period_id 尾部标记，区分每期的ID
        self.log.demsg("放款文件生成路径：{}".format(self.data_save_path))

        # 上传借据文件
        local = self.bank_loan_create_path
        remote = os.path.join(sftp_path['meituan']['bank_loan_create'], self.loan_date.replace('-', ''))
        self.sftp.sftp_upload(local, format_path(remote))

        # 上传期数单还款计划文件
        local = self.bank_period_create_path
        remote = os.path.join(sftp_path['meituan']['bank_period_create'], self.loan_date.replace('-', ''))
        self.sftp.sftp_upload(local, format_path(remote))

    # 获取文件存放路径，借据文件名，还款计划文件名
    def get_filename(self):
        # 初始化文件存放路径，(用户_身份证号)
        data_save_path = '%s_%s' % (
            self.user_name, self.certificate_no)
        data_save_path = os.path.join(_FilePath, data_save_path, self.loan_date.replace('-', ''))
        if not os.path.exists(data_save_path):
            os.makedirs(data_save_path)
        # 借据文件
        bank_loan_create_path = os.path.join(data_save_path, "bank_loan_create")
        if not os.path.exists(bank_loan_create_path):
            os.makedirs(bank_loan_create_path)
        # 还款计划文件
        bank_period_create_path = os.path.join(data_save_path, "bank_period_create")
        if not os.path.exists(bank_period_create_path):
            os.makedirs(bank_period_create_path)
        # 借据文件名
        loan_create = os.path.join(bank_loan_create_path, 'bank_loan_create_%s.txt' % self.loan_date.replace('-', ''))
        # 还款计划文件名
        period_create = os.path.join(bank_period_create_path,
                                     'bank_period_create_%s.txt' % (self.loan_date.replace('-', '')))
        return data_save_path, bank_loan_create_path, bank_period_create_path, loan_create, period_create

    # 日期计算
    @staticmethod
    def loan_and_period_date_parser(date_str, period, flag=True):
        """
        @param date_str: (str)借款日期  eg: '2020-01-09'
        @param period: (int)分期数  eg: 3
        @param flag:
        :return:
        """
        date_list = date_str.split('-')
        bill_year = int(date_list[0])
        bill_month = int(date_list[1])
        bill_day = int(date_list[-1])
        period_date_list = []
        if bill_day >= 26:
            bill_day -= 25
            bill_month += 1
        for _ in range(int(period)):
            bill_month += 1
            if bill_month > 12:
                bill_year += 1
                bill_month -= 12
            period_date_list.append("%d-%02d-%02d" % (bill_year, bill_month, bill_day))
        return period_date_list, "%02d" % bill_day

    # 借据文件生成
    def bank_loan_create(self):
        val_list = map(str, [self.bank_loan_temple[key] for key in self.loan_temple])
        strs = '|+|'.join(val_list)
        with open(self.bank_loan_filename, 'w', encoding='utf-8') as f:
            f.write("dataRowCount|+|1")
            f.write('\n')
            f.write(strs)
        # 创建.ok文件
        with open(os.path.splitext(self.bank_loan_filename)[0] + '.ok', 'w', encoding='utf-8') as f:
            f.write('%s' % os.path.basename(self.bank_loan_filename))

    # 还款计划文件生成
    def bank_period_create(self, temple, amount_tuple, plan_repay_date, period_id):
        term = self.amount.index(amount_tuple) + 1
        times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        temple['period_id'] = period_id
        temple['deserved_principal_amount'] = str(amount_tuple[0])
        temple['deserved_interest_amount'] = str(amount_tuple[1])
        temple['add_time'] = times
        temple['update_time'] = times
        temple['plan_repay_date'] = plan_repay_date
        temple['current_period'] = str(term)
        val_list = map(str, [temple[key] for key in self.period_temple])
        strs = '|+|'.join(val_list)
        with open(self.bank_period_filename, 'a+', encoding='utf-8') as f:
            f.write('\n')
            f.write(strs)
        # 创建.ok文件
        with open(os.path.splitext(self.bank_period_filename)[0] + '.ok', 'w', encoding='utf-8') as f:
            f.write('%s' % os.path.basename(self.bank_period_filename))


class MeiTuanRepayFile(EnvInit):
    def __init__(self, user_data, repay_type, loan_invoice_id=None, repay_term_no='1', repay_date="2021-08-06",
                 prin_amt=None, int_amt=None,
                 pnlt_int_amt=None):
        """
        @param user_data:           用户四要素   必填参数
        @param repay_type:          还款类型：   按期还款：01； 提前结清：02； 逾期还款：03
        @param loan_invoice_id:     借据号
        @param repay_term_no:       还款期次    必填参数
        @param repay_date:          账务日期"2021-08-06"，提前结清必填 ps:提前结清和逾期还款必填
        @param prin_amt:            还款本金，逾期部分还款选填
        @param int_amt:             还款利息，逾期部分还款选填
        @param pnlt_int_amt:        还款罚息，逾期部分还款选填
        """
        super().__init__()
        self.log.demsg('当前测试环境 %s', self.env)
        self.MysqlBizImpl = MysqlBizImpl()
        self.loan_invoice_id = loan_invoice_id
        self.user_data = user_data
        self.loan_no = self.get_loan_id()
        self.repay_type = repay_type
        self.repay_term_no = repay_term_no
        self.repay_date = repay_date
        self.prin_amt = prin_amt
        self.int_amt = int_amt
        self.pnlt_int_amt = pnlt_int_amt

        # # 获取借据及账单日期初始值
        # self.current_date = time.strftime('%Y-%m-%d', time.localtime())

        # bank_repay_period(期数单动账) 字段名列表，(文件生成时字符串拼接使用)
        self.repay_period_temple = [
            'business_ref_no',
            'loan_no',
            'loan_id',
            'period_id',
            'repay_type',
            'repay_date',
            'repay_amt',
            'paid_prin_amt',
            'paid_int_amt',
            'paid_ovd_prin_pnlt_amt_00',
            'repay_fee',
            'trade_timestamp',
            'current_period',
            'status',
            'plan_repay_date'
        ]
        # bank_repay_loan_(借据还款动账)
        self.repay_loan_temple = [
            'business_ref_no',
            'loan_no',
            'loan_id',
            'card_no',
            'card_bank_name',
            'fund_seq_no',
            'repay_type',
            'repay_date',
            'repay_amt',
            'paid_prin_amt',
            'paid_int_amt',
            'paid_ovd_prin_pnlt_amt_00',
            'repay_fee',
            'trade_timestamp',
            'accrued_status',
        ]

        # 期数动账单还款 键值对字典数据模板
        self.bank_repay_period_temple = {
            'business_ref_no': str(round(time.time_ns())),  # 业务流水号
            'loan_no': self.loan_no,  # 美团借据号
            'loan_id': str(int(round(time.time() * 1000))) + str(random.randint(0, 9999)),  # 美团借款ID号
            'period_id': str(int(round(time.time() * 1000))) + str(random.randint(0, 9999)),
            'repay_type': '1',  # 美团还款类型
            'repay_date': '',
            'repay_amt': '0',
            'paid_prin_amt': '0',
            'paid_int_amt': '0',
            'paid_ovd_prin_pnlt_amt_00': '0',
            'repay_fee': '0',
            'trade_timestamp': '',
            'current_period': '',  # 当前期次
            'status': '1',  # 结清标识
            'plan_repay_date': '',  # 计划还款时间
        }

        # bank_repay_loan 键值对字典数据模板
        self.bank_repay_loan_temple = {
            'business_ref_no': str(round(time.time_ns())),  # 业务流水号
            'loan_no': self.loan_no,  # 美团借据号
            'loan_id': str(int(round(time.time() * 1000))) + str(random.randint(0, 9999)),  # 美团借款ID号
            'card_no': '',  # 还款银行卡号
            'card_bank_name': '工商银行',  # 还款银行卡银行名称
            'fund_seq_no': str(int(round(time.time() * 1000))) + str(random.randint(0, 9999)),  # 还款业务流水号
            'repay_type': '1',  # 美团还款类型
            'repay_date': '',
            'repay_amt': '0',
            'paid_prin_amt': '0',
            'paid_int_amt': '0',
            'paid_ovd_prin_pnlt_amt_00': '0',
            'repay_fee': '0',
            'trade_timestamp': '',
            'accrued_status': '0',  # 入账状态，应计0，非应计1，核销2
        }

        # 执行文件生成上传SFTP服务器
        self.start()

    def start(self):
        # 生成账单日还款文件
        if self.repay_type == '01':
            self.bill_day_repay_file(repay_term_no=self.repay_term_no)
        # 生成提前结清还款文件
        if self.repay_type == '02':
            self.pre_repay_file(repay_date=self.repay_date, repay_term_no=self.repay_term_no)
        # 生成逾期还款文件
        if self.repay_type == '03':
            self.ovd_repay_file(repay_date=self.repay_date, repay_term_no=self.repay_term_no, prin_amt=self.prin_amt,
                                int_amt=self.int_amt, pnlt_int_amt=self.pnlt_int_amt)

        # 上传借据还款动账文件
        bank_repay_loan_path = self.get_filename(self.repay_date)['bank_repay_loan_path']
        remote = os.path.join(sftp_path['meituan']['bank_repay_loan'], self.repay_date.replace('-', ''))
        self.sftp.sftp_upload(bank_repay_loan_path, format_path(remote))
        # 上传期数单动账文件
        bank_repay_period_path = self.get_filename(self.repay_date)['bank_repay_period_path']
        remote = os.path.join(sftp_path['meituan']['bank_repay_period'], self.repay_date.replace('-', ''))
        self.sftp.sftp_upload(bank_repay_period_path, format_path(remote))

    # 获取文件存放路径，借据文件名，还款计划文件名
    def get_filename(self, repay_date):
        # 初始化文件存放路径，(用户_身份证号)
        data_save_path = '%s_%s' % (
            self.user_data['name'], self.user_data['cer_no'])
        data_save_path = os.path.join(_FilePath, data_save_path, repay_date.replace('-', ''))
        if not os.path.exists(data_save_path):
            os.makedirs(data_save_path)
        # 借据还款动账文件
        bank_repay_loan_path = os.path.join(data_save_path, "bank_repay_loan")
        if not os.path.exists(bank_repay_loan_path):
            os.makedirs(bank_repay_loan_path)
        # 期数动账单文件
        bank_repay_period_path = os.path.join(data_save_path, "bank_repay_period")
        if not os.path.exists(bank_repay_period_path):
            os.makedirs(bank_repay_period_path)
        # 借据还款动账文件名
        bank_repay_loan_file_name = os.path.join(bank_repay_loan_path,
                                                 'bank_repay_loan_%s.txt' % repay_date.replace('-', ''))
        # 期数动账单文件名
        bank_repay_period_file_name = os.path.join(bank_repay_period_path,
                                                   'bank_repay_period_%s.txt' % (repay_date.replace('-', '')))
        data = dict()
        data['data_save_path'] = data_save_path
        data['bank_repay_loan_path'] = bank_repay_loan_path
        data['bank_repay_period_path'] = bank_repay_period_path
        data['bank_repay_loan_file_name'] = bank_repay_loan_file_name
        data['bank_repay_period_file_name'] = bank_repay_period_file_name
        return data

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
            key2 = "user_name = '{}'".format(self.user_data['name'])
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
            key2 = "user_name = '{}'".format(self.user_data['name'])
            mysql = self.MysqlBizImpl.get_credit_data_info(table="credit_third_wait_loan_deal_info", key=key2)
            loan_no = str(mysql["third_loan_no"])

        return loan_no

    def write_repay_file(self, temple, repay_temple, filename, data_save_path):
        """
        @param temple: 待更新字段
        @param repay_temple: 更新字段key（定义表字段）
        @param filename: 写入文件名
        @param data_save_path: 写入文件夹地址
        @return:
        """
        # 写入单期还款文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("dataRowCount|+|1")
        val_list = map(str, [temple[key] for key in repay_temple])
        strs = '|+|'.join(val_list)
        with open(filename, 'a+', encoding='utf-8') as f:
            f.write('\n')
            f.write(strs)
        # 创建.ok文件
        with open(os.path.splitext(filename)[0] + '.ok', 'w', encoding='utf-8') as f:
            f.write('%s' % os.path.basename(filename))
        self.log.demsg("还款文件数据写入成功：{}".format(data_save_path))

    def credit_temple_file(self, filename, data_save_path):
        """
        # 创建还款文件
        @param filename: 创建文件名
        @param data_save_path: 文件夹地址
        @return:
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("dataRowCount|+|1")
        # 创建.ok文件
        with open(os.path.splitext(filename)[0] + '.ok', 'w', encoding='utf-8') as f:
            f.write('%s' % os.path.basename(filename))
        self.log.demsg("还款文件生成路径：{}".format(data_save_path))

    @staticmethod
    def write_file(temple, repay_temple, filename):
        """
        # 写入文件
        @param temple: 待更新字段
        @param repay_temple: 更新字段key（定义表字段）
        @param filename: 写入文件名
        @return:
        """
        val_list = map(str, [temple[key] for key in repay_temple])
        strs = '|+|'.join(val_list)
        with open(filename, 'a+', encoding='utf-8') as f:
            f.write('\n')
            f.write(strs)

    # 按期还款文件生成
    def bill_day_repay_file(self, repay_term_no):
        """
        @param repay_term_no: 还款期次
        @return:
        """
        # 获取用户借据信息
        total_term, loan_invoice_id = self.get_invoice_info()

        # 根据借据Id和期次获取资产侧还款计划
        key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loan_invoice_id, repay_term_no)
        asset_repay_plan = self.MysqlBizImpl.get_asset_data_info(table="asset_repay_plan", key=key3)

        temple = {}
        repay_date = str(asset_repay_plan["pre_repay_date"])
        self.repay_date = repay_date
        temple['repay_date'] = repay_date
        temple['repay_type'] = '3'  # 按期还款
        temple['trade_timestamp'] = repay_date + " " + time.strftime('%H:%M:%S', time.localtime())
        temple['repay_amt'] = str(int(asset_repay_plan["pre_repay_amount"] * 100))  # 总金额
        temple['paid_prin_amt'] = str(int(asset_repay_plan["pre_repay_principal"] * 100))  # 本金
        temple['paid_int_amt'] = str(int(asset_repay_plan["pre_repay_interest"] * 100))  # 利息
        temple['paid_ovd_prin_pnlt_amt_00'] = str(int(asset_repay_plan["left_repay_overdue_fee"] * 100))  # 逾期罚息

        # 期数动账文件赋值
        self.bank_repay_period_temple.update(temple)
        self.bank_repay_period_temple['plan_repay_date'] = repay_date
        self.bank_repay_period_temple['current_period'] = str(repay_term_no)
        self.bank_repay_period_temple['period_id'] = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        self.bank_repay_period_temple['status'] = '1'
        # 开始写入文件内容
        bank_repay_period_file_name = self.get_filename(repay_date)['bank_repay_period_file_name']
        bank_repay_period_path = self.get_filename(repay_date)['bank_repay_period_path']
        self.write_repay_file(self.bank_repay_period_temple, self.repay_period_temple, bank_repay_period_file_name,
                              bank_repay_period_path)

        # 借据还款动账文件赋值
        self.bank_repay_loan_temple.update(temple)
        self.bank_repay_loan_temple['card_no'] = self.user_data['bankid']
        # 开始写入文件内容
        bank_repay_loan_file_name = self.get_filename(repay_date)['bank_repay_loan_file_name']
        bank_repay_loan_path = self.get_filename(repay_date)['bank_repay_loan_path']
        self.write_repay_file(self.bank_repay_loan_temple, self.repay_loan_temple, bank_repay_loan_file_name,
                              bank_repay_loan_path)

    # 逾期还款文件生成
    def ovd_repay_file(self, repay_date="2021-08-06", repay_term_no='1', prin_amt=None, int_amt=None,
                       pnlt_int_amt=None):
        """
        @param repay_term_no:       还款期次
        @param repay_date:          账务日期"2021-08-06"，提前结清必填
        @param prin_amt:            还款本金，逾期部分还款选填
        @param int_amt:             还款利息，逾期部分还款选填
        @param pnlt_int_amt:        还款罚息，逾期部分还款选填
        @return:
        """
        # 获取用户借据信息
        total_term, loan_invoice_id = self.get_invoice_info()

        # 根据借据Id和期次获取资产侧还款计划
        key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loan_invoice_id, repay_term_no)
        asset_repay_plan = self.MysqlBizImpl.get_asset_data_info(table="asset_repay_plan", key=key3)

        temple = dict()
        temple['repay_date'] = repay_date
        temple['repay_type'] = '8'  # 按期还款
        temple['trade_timestamp'] = repay_date + " " + time.strftime('%H:%M:%S', time.localtime())
        # 如果本金、利息、罚息输入为空，取还款计划中待还本利罚
        if not prin_amt and not int_amt and not pnlt_int_amt:
            temple['repay_amt'] = str(int(asset_repay_plan["pre_repay_amount"] * 100))  # 总金额
            temple['paid_prin_amt'] = str(int(asset_repay_plan["pre_repay_principal"] * 100))  # 本金
            temple['paid_int_amt'] = str(int(asset_repay_plan["pre_repay_interest"] * 100))  # 利息
            temple['paid_ovd_prin_pnlt_amt_00'] = str(int(asset_repay_plan["left_repay_overdue_fee"] * 100))  # 逾期罚息
        else:
            temple['paid_prin_amt'] = str(prin_amt)  # 本金
            temple['paid_int_amt'] = str(int_amt)  # 利息
            temple['paid_ovd_prin_pnlt_amt_00'] = str(pnlt_int_amt)  # 逾期罚息
            temple['repay_amt'] = str(int(prin_amt) + int(int_amt) + int(pnlt_int_amt))  # 总金额

        # 期数动账文件赋值
        self.bank_repay_period_temple.update(temple)
        self.bank_repay_period_temple['plan_repay_date'] = repay_date
        self.bank_repay_period_temple['current_period'] = str(repay_term_no)
        self.bank_repay_period_temple['period_id'] = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        self.bank_repay_period_temple['status'] = '1'
        # 开始写入文件内容
        bank_repay_period_file_name = self.get_filename(repay_date)['bank_repay_period_file_name']
        bank_repay_period_path = self.get_filename(repay_date)['bank_repay_period_path']
        self.write_repay_file(self.bank_repay_period_temple, self.repay_period_temple, bank_repay_period_file_name,
                              bank_repay_period_path)

        # 借据还款动账文件赋值
        self.bank_repay_loan_temple.update(temple)
        self.bank_repay_loan_temple['card_no'] = self.user_data['bankid']
        # 开始写入文件内容
        bank_repay_loan_file_name = self.get_filename(repay_date)['bank_repay_loan_file_name']
        bank_repay_loan_path = self.get_filename(repay_date)['bank_repay_loan_path']
        self.write_repay_file(self.bank_repay_loan_temple, self.repay_loan_temple, bank_repay_loan_file_name,
                              bank_repay_loan_path)

    # 提前结清还款文件生成
    def pre_repay_file(self, repay_date="2021-08-06", repay_term_no='1'):
        """
        @param repay_term_no:       还款期次
        @param repay_date:          账务日期"2021-08-06"，提前结清必填
        @return:
        """
        data_save_path = self.get_filename(repay_date)['data_save_path']
        # 创建期数动账待写入文件
        bank_repay_period_file_name = self.get_filename(repay_date)['bank_repay_period_file_name']
        bank_repay_period_path = self.get_filename(repay_date)['bank_repay_period_path']
        self.credit_temple_file(bank_repay_period_file_name, bank_repay_period_path)

        # 创建借据还款动账待写入文件
        bank_repay_loan_file_name = self.get_filename(repay_date)['bank_repay_loan_file_name']
        bank_repay_loan_path = self.get_filename(repay_date)['bank_repay_loan_path']
        self.credit_temple_file(bank_repay_loan_file_name, bank_repay_loan_path)

        # 获取用户借据信息
        total_term, loan_invoice_id = self.get_invoice_info()
        # 根据借据ID获取用户的申请费率
        key2 = "loan_invoice_id = '{}'".format(loan_invoice_id)
        credit_third_wait_loan_deal_info = self.MysqlBizImpl.get_credit_data_info(
            table="credit_third_wait_loan_deal_info", key=key2)
        interest_rate = credit_third_wait_loan_deal_info["interest_rate"]  # 年化利率

        temple = dict()
        temple['repay_date'] = repay_date
        temple['repay_type'] = '1'  # 提前还款
        temple['status'] = '1'
        temple['trade_timestamp'] = repay_date + " " + time.strftime('%H:%M:%S', time.localtime())

        # 按照期次依次写入还款数据
        repay_term_no = int(repay_term_no)
        with open(bank_repay_period_file_name, 'w', encoding='utf-8') as f:
            f.write("dataRowCount|+|{}".format(str(int(total_term) - repay_term_no + 1)))
        with open(bank_repay_loan_file_name, 'w', encoding='utf-8') as f:
            f.write("dataRowCount|+|{}".format(str(int(total_term) - repay_term_no + 1)))
        while int(total_term) >= repay_term_no:
            # temple['business_ref_no'] = str(round(time.time_ns())) + str(repay_term_no)
            # 根据借据Id和期次获取资产侧还款计划
            key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loan_invoice_id, str(repay_term_no))
            asset_repay_plan = self.MysqlBizImpl.get_asset_data_info(table="asset_repay_plan", key=key3)

            temple['plan_repay_date'] = str(asset_repay_plan["pre_repay_date"])
            temple['paid_prin_amt'] = str(int(asset_repay_plan["pre_repay_principal"] * 100))  # 本金
            # 利息=剩余本金*计息天数*年化利率/360
            days = get_day(asset_repay_plan["start_date"], repay_date)
            if days >= 0:
                temple['paid_int_amt'] = str(
                    round(asset_repay_plan['before_calc_principal'] * days * interest_rate / 360))  # 利息
                temple['repay_amt'] = str(int(temple['paid_prin_amt']) + int(temple['paid_int_amt']))  # 总金额
            else:
                temple['paid_int_amt'] = '0'  # 利息
                temple['repay_amt'] = str(int(asset_repay_plan["pre_repay_principal"] * 100))  # 总金额

            # 循环写入还款文件，当期次大于最大期次，退出循环
            # 期数动账文件赋值
            self.bank_repay_period_temple.update(temple)
            self.bank_repay_period_temple['plan_repay_date'] = repay_date
            self.bank_repay_period_temple['current_period'] = str(repay_term_no)
            self.bank_repay_period_temple['period_id'] = str(int(round(time.time() * 1000))) + str(
                random.randint(0, 9999)) + str(repay_term_no)
            self.bank_repay_period_temple['status'] = '1'
            # 开始写入文件内容
            bank_repay_period_file_name = self.get_filename(repay_date)['bank_repay_period_file_name']
            self.write_file(self.bank_repay_period_temple, self.repay_period_temple, bank_repay_period_file_name)

            # 借据还款动账文件赋值
            self.bank_repay_loan_temple.update(temple)
            self.bank_repay_loan_temple['card_no'] = self.user_data['bankid']
            # 开始写入文件内容
            bank_repay_loan_file_name = self.get_filename(repay_date)['bank_repay_loan_file_name']
            self.write_file(self.bank_repay_loan_temple, self.repay_loan_temple, bank_repay_loan_file_name)

            repay_term_no += 1
        self.log.demsg("还款文件数据写入完成：{}".format(data_save_path))


if __name__ == '__main__':
    # 美团按期还款、提前结清，按日收息
    data1 = {'name': '鲁宜云', 'cer_no': '512021200904250046', 'bankid': '6217237670539660703', 'telephone': '15208346597',
             'app_no': 'mt_app_no164621185656539901002'}  # hsit -> MeiTuan
    card_id = data1['cer_no']
    user_name = data1['name']
    t = MeiTuanRepayFile(data1, repay_type='01', repay_term_no='2')
    # t.bill_day_repay_file(repay_term_no='2')
    # t.pre_repay_file(repay_date="2022-04-01", repay_term_no='2')
    # t = MeiTuanLoanFile(data1, apply_date='2022-04-01')
