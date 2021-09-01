# -*- coding: utf-8 -*-
# # -------------------------------------------------
# # - 配置数据环境全局对象初始化
# # -------------------------------------------------

import sys
from Config.global_config import *
from ComLib.Mysql import Mysql
from Engine.Logger import Logs
from ComLib import Models


class INIT(object):
    def __init__(self):
        super().__init__()
        # 初始化日志引擎模块
        self.log = Logs()
        # 环境配置获取
        self._envinit()
        # 解析项目特性配置
        self._parser_cfg()

    def _envinit(self):
        self.log.demsg('当前测试环境 %s', TEST_ENV_INFO)
        if TEST_ENV_INFO not in EnvList:
            self.log.error('The test environment is invalid! Please check the config file of TestEnvInfo.py!')
            sys.exit(3)
        self.env = TEST_ENV_INFO
        self.project = PROJECT
        self.host = ENV[self.env]['request_host']
        self.host_fql = ENV[self.env]['request_host_fql']
        self.mysql_data = '%s_mysql' % self.env.lower()
        self.credit_data = '%s_credit' % self.env.lower()
        self.asset_data = '%s_asset' % self.env.lower()
        self.general_database = ENV[self.env]['database'][self.mysql_data]
        self.credit_database = ENV[self.env]['database'][self.credit_data]
        self.asset_database = ENV[self.env]['database'][self.asset_data]
        self.credit_database_name = ENV[self.env]['database'][self.credit_data]['databaseName']
        self.asset_database_name = ENV[self.env]['database'][self.asset_data]['databaseName']
        self.headers = headers

        self.log.demsg('数据库初始化.')
        self.mysql = Mysql(self.general_database, self.credit_database)
        self.mysql_asset = Mysql(self.general_database, self.asset_database)

    def _function_init(self):
        for item in Models.__all__:
            f = '%s' % item
            vars(self)[f] = eval('Models.%s' % item)

    def _parser_cfg(self):
        self.cfg = eval(PROJECT)

    def check_user_available(self, data):
        sql = "select * from credit_apply where user_tel='{}';".format(data['telephone'])
        res = self.mysql.select(sql)
        if res:
            if data['cer_no'] not in res[0]:
                self.log.error('手机号已被注册, 主程序退出!')
                sys.exit(7)
            else:
                self.log.warning('提示：用户已存在授信信息\n继续流程...')

    def get_credit_data_info(self, table='credit_loan_apply', key="查询条件", record=0):
        """
        :function: 获取credit数据库表中信息
        table : 表名
        key ： 查询关键字
        record ： 根据列表指定序列返回查询数据
        """
        sql = "select * from {}.{} where {};".format(self.credit_database_name, table, key)
        # self.log.info(sql)
        # 获取表属性字段名
        keys = self.mysql.select_table_column(table_name=table, database=self.credit_database_name)
        # 获取查询内容
        values = self.mysql.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            return data
        except (IndexError, Exception):
            self.log.info("SQL查询结果为空，借据不存在，请排查")

    def get_asset_data_info(self, table='asset_loan_apply', key="查询条件", record=0):
        """
        :function: 获取asset数据库表中信息
        table : 表名
        key ： 查询关键字
        record ： 根据列表指定序列返回查询数据
        """
        sql = "select * from {}.{} where {};".format(self.asset_database_name, table, key)
        # self.log.info(sql)
        # 获取表属性字段名
        keys = self.mysql_asset.select_table_column(table_name=table, database=self.asset_database_name)
        # 获取查询内容
        values = self.mysql_asset.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            return data
        except (IndexError, Exception):
            self.log.info("SQL查询结果为空，查询条件异常，请排查")

    def credit_query(self, data):
        """ # 接口数据payload解密
            :return:                查询状态
            """
        key = "certificate_no = '{}'".format(data['cer_no'])
        info = self.get_credit_data_info(table="credit_apply", key=key)
        try:
            status = info['status']
        except (IndexError, Exception):
            status = "x"
            self.log.info("未查询到数据")
        return status


class DataGenerator(object):
    pass


if __name__ == '__main__':
    t = INIT()
    print(dir(t))
    print(t.credit_database_name)
