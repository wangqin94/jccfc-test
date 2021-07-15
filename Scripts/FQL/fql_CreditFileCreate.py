# -*- coding: utf-8 -*-
"""
    Function: 分期乐还款文件生成
"""

import os
import time
from datetime import date, timedelta, datetime

from Engine.Base import INIT
from ComLib.Mysql import Mysql
from Engine.Logger import Logs
from Config.global_config import *
from person import data

_log = Logs()
_ProjectPath = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]  # 项目根目录
_FilePath = os.path.join(_ProjectPath, 'FilePath', PROJECT, TEST_ENV_INFO)  # 文件存放目录
if not os.path.exists(_FilePath):
    os.makedirs(_FilePath)


class FQL(INIT):
    def __init__(self, data, repay_mode='1', term_no='1', repay_date='2021-08-09'):
        """
        :param data:  四要素
        :param repay_mode:  还款模式，1：按期还款；3：提前结清；5；逾期还款
        :param term_no:     还款期数
        :param repay_date:    还款时间
        """
        super().__init__()
        _log.demsg('当前测试环境为 %s', TEST_ENV_INFO)
        self.general_database = ENV[TEST_ENV_INFO]['database']['%s_mysql' % TEST_ENV_INFO.lower()]
        self.credit_database_name = '%s_credit' % TEST_ENV_INFO.lower()
        self.user_database_name = '%s_user' % TEST_ENV_INFO.lower()
        self.applyId = data['applyId']
        self.repay_mode = repay_mode
        self.term_no = term_no
        self.repay_date = repay_date
        self.data_save_path = ''
        self.repay_filename = ""
        self.current_date = time.strftime('%Y-%m-%d', time.localtime())

        # 数据库表初始化
        _log.demsg('数据库初始化.')
        self.credit = Mysql(self.general_database, self.credit_database)
        self.mysql_asset = Mysql(self.general_database, self.asset_database)
        self.asset_database_name = '%s_asset' % TEST_ENV_INFO.lower()

        # 还款 字段名列表，(文件生成时字符串拼接使用)
        self.repay_key_temple = [
            'applyId',
            'term_no',
            'repay_date',
            'repay_amt',
            'paid_prin_amt',
            'paid_int_amt',
            'repay_mode',
            'reserve',
        ]

        # 还款 键值对字典数据模板
        self.repay_temple = {
            'applyId': "",  # applyid
            'term_no': "1",  # 还款期次
            'repay_date': "",  # 还款时间
            'repay_amt': "",  # 还款本金
            'paid_prin_amt': "",  # 还款利息
            'paid_int_amt': "",  # 还款罚息
            'repay_mode': "",  # 还款方式
            'reserve': "",  # 备注字段
        }
        # 执行
        self.start()

    def get_asset_data_info(self, table='asset_loan_apply', key="查询条件"):
        """
        :function: 获取asset数据库表中信息
        table : 表名
        key ： 查询关键字
        """
        sql = "select * from {}.{} where {};".format(self.asset_database_name, table, key)
        # 获取表属性字段名
        keys = self.mysql_asset.select_table_column(table_name=table, database=self.asset_database_name)
        # 获取查询内容
        values = self.mysql_asset.select(sql)
        # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
        data = [dict(zip(keys, item)) for item in values][0]
        return data

    def get_credit_data_info(self, table='credit_loan_apply', key="查询条件"):
        """
        :function: 获取credit数据库表中信息
        table : 表名
        key ： 查询关键字
        """
        sql = "select * from {}.{} where {};".format(self.credit_database_name, table, key)
        # 获取表属性字段名
        keys = self.credit.select_table_column(table_name=table, database=self.credit_database_name)
        # 获取查询内容
        values = self.credit.select(sql)
        # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
        data = [dict(zip(keys, item)) for item in values][0]
        return data

    # 文件生成入口
    def start(self):
        # 开始写入还款文件
        self.repayment_acct_period(self.repay_temple)

    # 计算还款时间和放款时间差，天为单位
    def get_day(self, time1, time2):
        """
        :param time1: 时间1
        :param time2: 时间2
        :return: 差异天数
        """
        try:
            day_num = 0
            day1 = time.strptime(str(time1), '%Y-%m-%d')
            day2 = time.strptime(str(time2), '%Y-%m-%d')
            if type == 'day':
                day_num = (int(time.mktime(day2)) - int(time.mktime(day1))) / (24 * 60 * 60)
            return abs(int(day_num))
        except Exception:
            print("Error: 系统错误")

    # 获取文件存放路径，还款文件名
    def get_filename(self, repay_date):
        # 初始化文件存放路径，(用户_身份证号_时间戳)
        data_save_path = '%s_%s' % (
            data['name'], time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()))
        data_save_path = os.path.join(_FilePath, data_save_path)
        os.mkdir(data_save_path)
        # 借据文件名
        repayment_acct = os.path.join(data_save_path,  'JC_repayment_acct_%s.txt' % (repay_date.replace('-', '')))
        return data_save_path, repayment_acct

    # 还款文件生成
    def repayment_acct_period(self, temple):
        """
        :param temple: 还款字段字典模板
        :param repay_date: 计划还款日
        :return:
        """
        temple['applyId'] = self.applyId
        temple['repay_mode'] = self.repay_mode
        temple['term_no'] = self.term_no

        # 根据applyId查询还款计划中的借据号
        key1 = "apply_id = '{}'".format(self.applyId)
        credit_repay_plan = self.get_credit_data_info(table="credit_repay_plan", key=key1)
        loan_invoice_id = credit_repay_plan["loan_invoice_id"]

        # 根据applyId查询还款计划中的借据号
        key2 = "thirdpart_apply_id = '{}'".format(self.applyId)
        credit_loan_apply = self.get_credit_data_info(table="credit_loan_apply", key=key2)
        apply_rate = credit_loan_apply["apply_rate"]

        # 根据借据Id和期次获取资产侧还款计划
        key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loan_invoice_id, self.term_no)
        asset_repay_plan = self.get_asset_data_info(table="asset_repay_plan", key=key3)
        temple['repay_amt'] = str('{:.2f}'.format(asset_repay_plan["pre_repay_principal"]))
        temple['paid_prin_amt'] = str('{:.2f}'.format(asset_repay_plan["pre_repay_interest"]))
        temple['paid_int_amt'] = str('{:.2f}'.format(asset_repay_plan["pre_repay_fee"]))
        # 按期还款
        if self.repay_mode == "1":
            temple['repay_date'] = str(asset_repay_plan["pre_repay_date"]).replace("-", "")
            self.repay_date = asset_repay_plan["pre_repay_date"]
            # 获取文件名及存放路径
            self.repay_filename = self.get_filename(str(self.repay_date))[1]

        # 逾期还款
        elif self.repay_mode == "5":
            temple['repay_date'] = str(asset_repay_plan["calc_overdue_fee_date"]).replace("-", "")
            self.repay_date = asset_repay_plan["calc_overdue_fee_date"]
            self.repay_filename = self.get_filename(str(self.repay_date))[1]

        # 提前结清
        elif self.repay_mode == "3":
            temple['repay_date'] = self.repay_date.replace("-", "")
            self.repay_filename = self.get_filename(str(self.repay_date))[1]
            temple['repay_amt'] = str("{:.2f}".format(asset_repay_plan["before_calc_principal"]))  # 剩余应还本金
            # 计算提前结清利息:剩余还款本金*（实际还款时间-本期开始时间）*日利率
            days = self.get_day(asset_repay_plan["start_date"], self.repay_date)
            # 利息
            paid_prin_amt = asset_repay_plan["left_principal"] * days * apply_rate / (100 * 360)
            temple['paid_prin_amt'] = str('{:.2f}'.format(paid_prin_amt))
            temple['paid_int_amt'] = 0

        # 写入单期还款文件
        val_list = map(str, [temple[key] for key in self.repay_temple])
        strs = '|'.join(val_list)
        with open(self.repay_filename, 'a+', encoding='utf-8') as f:
            f.write(strs)
            f.write("|")


if __name__ == '__main__':
    # 按期还款，提前结清（按日计息），提前结清
    # repay_mode:  还款模式，1：按期还款；3：提前结清；5；逾期还款
    t = FQL(data, repay_date='2021-06-22', term_no="1", repay_mode='1')
