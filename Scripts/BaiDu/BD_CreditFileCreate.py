# -*- coding: utf-8 -*-
"""
    Function: 百度借据/费率/息费减免/还款计划/还款文件生成
"""

import os
import sys
import time
from datetime import date, timedelta, datetime
import pymysql
from ComLib.Models import *
from Engine.Logger import Logs
from Config.global_config import *
from person import data

_log = Logs()
_ProjectPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 项目根目录
_FilePath = os.path.join(_ProjectPath, 'FilePath', PROJECT, TEST_ENV_INFO)  # 文件存放目录
print("文件存放目录:{}".format(_FilePath))
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


class BaiduFile(Mysql):
    def __init__(self, data, cur_date=None, loan_record=0, repay_mode='02'):
        """ # 百度对账文件
        :param data:                用户四要素
        :param cur_date:            账务日期，默认None 为当前日期
        :param loan_record:         用户成功支用笔数，默认为0 为第1笔
        """
        super(BaiduFile, self).__init__()
        self.user_name = data['name']
        self.cer_no = data['cer_no']
        self.loan_record = loan_record
        self.repay_mode = repay_mode
        self.current_date = time.strftime('%Y%m%d', time.localtime())
        self.loan_id = 'LoanId' + str(int(round(time.time() * 1000)))
        # 获取借据及账单日期初始值
        self.cur_date = self.current_date if not cur_date else cur_date.replace('-', '')
        # 获取文件存储名
        self.open_csv, self.repay_plan, self.repay_item, self.reduce_csv, self.loan_rate_csv = self.get_filename()
        self.info = self.get_user_data_info()
        self.apply_date = self.info['apply_time'].strftime('%Y%m%d')
        self.period_list, self.bill_day = self.get_bill_day()

        self.amount_dict = {
            '500_3': [(19385, 1823), (20014, 1194), (20601, 606)],
            '600_3': [(19615, 1170), (19971, 814), (20414, 411)],
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
        self.amount = self.get_repay_period_amount()

        # 根据生息日获取对应的账单日和还款日列表
        self.period_date_list, self.bill_day = self.get_bill_day()

        # 获取数据库表用户信息
        self.data_info = self.get_user_data_info()

        # 文件生成入口
        self.start()

    # 文件生成入口
    def start(self):
        # 开始写入借据文件
        self.get_open_csv(self.open_csv_template)
        self.get_loan_rate_csv(self.loan_rate_csv_template)
        # 开始写入还款计划/还款 文件
        for amt in self.amount:
            # period_id = strings + "%03d" % syb
            self.get_repay_plan_csv(self.repay_plan_csv_template, amt)
            self.get_repay_item_csv(self.repay_item_csv_template, amt)
            self.get_reduce_csv(self.reduce_csv_template, amt)

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
    def get_filename(self):
        # 初始化文件存放路径，(用户_身份证号_时间戳)
        data_save_path = '%s_%s_%s' % (self.user_name, self.cer_no, time.strftime('%Y%m%d-%H%M%S', time.localtime()))
        data_save_path = os.path.join(_FilePath, data_save_path, str(self.cur_date))
        os.makedirs(data_save_path)

        # 借据文件名
        open_csv = os.path.join(data_save_path, 'open.csv')
        repay_plan = os.path.join(data_save_path, 'repay_plan.csv')
        repay_item = os.path.join(data_save_path, 'repay_item.csv')
        reduce_csv = os.path.join(data_save_path, 'reduce.csv')
        loan_rate = os.path.join(data_save_path, 'loan_rate.csv')

        return open_csv, repay_plan, repay_item, reduce_csv, loan_rate

    # 获取每期应还本金利息数据
    def get_repay_period_amount(self):
        flag = "%s_%s" % (str(int(self.info['apply_amount'])), str(int(self.info['apply_term'])))
        print(flag)
        if flag not in self.amount_dict:
            print("################ 放款金额或还款期数不支持, 请联系管理员... ###################")
            sys.exit()
        # 获取每期应还本金和利息
        return self.amount_dict[
            '%s_%s' % (str(int(self.info['apply_amount'])), str(int(self.info['apply_term'])))]

    def get_user_data_info(self):
        """
        :function: 获取用户数据库表中信息
        """
        # 查询的数据库表
        table = 'credit_loan_apply'
        table1 = 'user_financial_instrument_info'
        # 查询sql语句
        sql = "select * from {}.credit_loan_apply where certificate_no='{}' and fail_reason IS null and status = '15';".format(
            self.credit_database_name, self.cer_no)
        # 获取表属性字段名
        keys = self.select_table_column(table_name=table)
        # keys1 = self.select_table_column(table_name=table1, database=self.user_database_name)
        # 获取查询内容
        values = self.select(sql)
        # values1 = self.select(sql1)
        # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
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
        table_head = ','.join(self.open_csv_keys)
        val_list = map(str, [self.open_csv_template[key] for key in self.open_csv_keys])
        strings = ','.join(val_list)
        with open(self.open_csv, 'w', encoding='utf-8') as f:
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
        if term == 1:
            temple['start_date'] = self.apply_date
            table_head = ','.join(self.repay_plan_csv_keys)
            with open(self.repay_plan, 'w', encoding='utf-8') as f:
                f.write(table_head)
                f.write('\n')
        else:
            temple['start_date'] = self.period_date_list[term - 2]
        val_list = map(str, [self.repay_plan_csv_template[key] for key in self.repay_plan_csv_keys])
        strings = ','.join(val_list)
        with open(self.repay_plan, 'a+', encoding='utf-8') as f:
            f.write(strings)
            f.write('\n')

    def get_repay_item_csv(self, temple, amount_tuple):
        term = self.amount.index(amount_tuple) + 1
        temple['loan_id'] = self.loan_id
        temple['total_amt'] = str(amount_tuple[0] + amount_tuple[1])
        temple['income_amt'] = str(amount_tuple[0] + amount_tuple[1])
        temple['int_amt'] = str(amount_tuple[1])
        temple['prin_amt'] = str(amount_tuple[0])
        temple['tran_date'] = str(self.cur_date)
        temple['cur_date'] = str(self.cur_date)
        temple['seq_no'] = 'seq_no' + str(int(round(time.time() * 1000)))
        temple['term_no'] = int(term)
        if term == 1:
            table_head = ','.join(self.repay_item_csv_keys)
            with open(self.repay_item, 'w', encoding='utf-8') as f:
                f.write(table_head)
                f.write('\n')
        val_list = map(str, [self.repay_item_csv_template[key] for key in self.repay_item_csv_keys])
        strings = ','.join(val_list)
        with open(self.repay_item, 'a+', encoding='utf-8') as f:
            f.write(strings)
            f.write('\n')

    # 手工减免息费明细文件
    def get_reduce_csv(self, temple, amount_tuple):
        term = self.amount.index(amount_tuple) + 1
        temple['loan_id'] = self.loan_id
        temple['tran_date'] = str(self.cur_date)
        temple['cur_date'] = str(self.cur_date)
        temple['seq_no'] = 'seqNo' + str(int(round(time.time() * 1000)))
        temple['term_no'] = int(term)
        if term == 1:
            table_head = ','.join(self.reduce_csv_keys)
            with open(self.reduce_csv, 'w', encoding='utf-8') as f:
                f.write(table_head)
                f.write('\n')
        val_list = map(str, [self.reduce_csv_template[key] for key in self.reduce_csv_keys])
        strings = ','.join(val_list)
        with open(self.reduce_csv, 'a+', encoding='utf-8') as f:
            f.write(strings)
            f.write('\n')

    # 费率文件
    def get_loan_rate_csv(self, temple):
        temple['loan_id'] = self.loan_id
        temple['cur_date'] = self.cur_date
        temple['end_term'] = int(self.info["apply_term"])
        if self.repay_mode == "05":
            temple['repay_violate_rate'] = "4"
        table_head = ','.join(self.loan_rate_csv_keys)
        val_list = map(str, [self.loan_rate_csv_template[key] for key in self.loan_rate_csv_keys])
        strings = ','.join(val_list)
        with open(self.loan_rate_csv, 'w', encoding='utf-8') as f:
            s = '\n'.join([table_head, strings])
            f.write(s)


if __name__ == '__main__':
    # 等额本息按期还款、提前结清收取违约金（4%）、提前结清按期收息；随借随还按期还款、部分还款（重算还款计划）、提前结清按日计息
    # repay_mode='02'随借随还，repay_mode='05'等额本息
    t = BaiduFile(data, cur_date='20210411', loan_record=0, repay_mode='02')
