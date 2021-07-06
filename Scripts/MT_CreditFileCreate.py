# -*- coding: utf-8 -*-
"""
    Function: 美团借据/还款计划/还款文件生成
"""

import os
import sys
import time
from datetime import date, timedelta, datetime
import pymysql
from ComLib.Models import *
from Engine.Logger import Logs
from Config.global_config import *
from Scripts.person import data

_log = Logs()
_ProjectPath = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]  # 项目根目录
_FilePath = os.path.join(_ProjectPath, 'FilePath', PROJECT, TEST_ENV_INFO)  # 文件存放目录
if not os.path.exists(_FilePath):
    os.makedirs(_FilePath)


class Mysql(object):
    def __init__(self):
        _log.demsg('当前测试环境为 %s', TEST_ENV_INFO)
        self.general_database = ENV[TEST_ENV_INFO]['database']['%s_mysql' % TEST_ENV_INFO.lower()]
        self.credit_database_name = '%s_credit' % TEST_ENV_INFO.lower()
        self.user_database_name = '%s_user' % TEST_ENV_INFO.lower()
        self.__mysql_cursor, self.__mysql = self.create_mysql_conn()
        self.cursor = self.__mysql_cursor

    def __del__(self):
        self.__mysql_cursor.close()
        self.__mysql.close()

    def create_mysql_conn(self):
        _log.demsg('开始创建数据库全局对象')
        conn = pymysql.connect(host=self.general_database['host'],
                               user=self.general_database['username'],
                               password=self.general_database['password'],
                               port=self.general_database['port'],
                               charset='utf8')
        cursor = conn.cursor()
        # self.cursor_list.append(cursor)
        return cursor, conn

    def select_table_column(self, table_name='credit_apply', database=None):
        column_key = []
        database = self.credit_database_name if not database else database
        sql_column = "select COLUMN_NAME from information_schema.COLUMNS where table_name='{}' and table_schema='{}';".format(
            table_name, database)
        try:
            self.cursor.execute(sql_column)
        except Exception as e:
            _log.error(e)
        res_column = self.cursor.fetchall()
        if res_column:
            column_key = [item[0] for item in res_column]
        return column_key

    def select(self, sql):
        try:
            self.cursor.execute(sql)
        except Exception as e:
            _log.error(e)
        res_values = self.cursor.fetchall()
        return res_values

    def txt_crpyt(self):
        pass


class MtFile(Mysql):
    def __init__(self, certificate_no, user_name, apply_date=None, delay=(0, 0), loan_record=0):
        """
        :param certificate_no:  用户身份证号
        :param user_name:       用户姓名
        :param apply_date:      放贷日期, 为None时，取当前系统时间
        :param delay:           逾期数据, (逾期期数, 逾期天数)
        :param loan_record:     用户第几笔去用申请，0为第一笔，1为第二笔
        """
        super().__init__()
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
        # 获取数据库表用户信息
        self.data_info, self.data_info1 = self.get_user_data_info()

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
        self.amount = self.get_repay_period_amount()

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

    # 获取文件存放路径，借据文件名，还款计划文件名
    def get_filename(self):
        # 初始化文件存放路径，(用户_身份证号_时间戳)
        data_save_path = '%s_%s_%s' % (
            self.user_name, self.certificate_no, time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()))
        data_save_path = os.path.join(_FilePath, data_save_path)
        os.mkdir(data_save_path)
        # 借据文件名
        loan_create = os.path.join(data_save_path, 'bank_loan_create_%s.txt' % self.loan_date.replace('-', ''))
        # 还款计划文件名
        period_create = os.path.join(data_save_path, 'bank_period_create_%s.txt' % (self.loan_date.replace('-', '')))
        return data_save_path, loan_create, period_create

    # 日期计算
    @staticmethod
    def loan_and_period_date_parser(date_str, period, flag=True):
        """
        :param date_str: (str)借款日期  eg: '2020-01-09'
        :param period: (int)分期数  eg: 3
        :param flag:
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

    # 获取用户数据库表 hsit_credit.credit_loan_apply, hsit_user.user_financial_instrument_info信息
    def get_user_data_info(self):
        """
        :function: 获取用户数据库表中信息
        """
        # 查询的数据库表
        table = 'credit_loan_apply'
        table1 = 'user_financial_instrument_info'
        # 查询sql语句
        sql = "select * from {}.credit_loan_apply where certificate_no='{}';".format(self.credit_database_name,
                                                                                     self.certificate_no)
        sql1 = "select * from {}.user_financial_instrument_info where account_name='{}';".format(
            self.user_database_name, self.user_name)
        # 获取表属性字段名
        keys = self.select_table_column(table_name=table)
        keys1 = self.select_table_column(table_name=table1, database=self.user_database_name)
        # 获取查询内容
        values = self.select(sql)
        values1 = self.select(sql1)
        # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
        info = [dict(zip(keys, item)) for item in values][self.loan_record]
        info1 = [dict(zip(keys1, item)) for item in values1][0]
        return info, info1

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
        :param temple: 还款字段字典模板
        :param amount_tuple: 当前期应还本金和利息
        :param plan_repay_date: 计划还款日
        :param period_id: 还款期ID与还款计划相对应
        :param delay: 逾期天数
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
        temple['trade_timestamp'] = times
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


if __name__ == '__main__':
    # 美团按期还款、提前结清，按日收息
    card_id = data['cer_no']
    user_name = data['name']
    t = MtFile(certificate_no=card_id, user_name=user_name, loan_record=1)
