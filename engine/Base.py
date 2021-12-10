# -*- coding: utf-8 -*-
# # -------------------------------------------------
# # - 配置数据环境全局对象初始化
# # -------------------------------------------------

import sys
from config.TestEnvInfo import *
from utils.Mysql import Mysql
from utils.Logger import MyLog
from utils import Models
from utils.ReadConfig import *
from config.globalConfig import *


class INIT(object):
    def __init__(self):
        super().__init__()
        # 初始化日志引擎模块
        self.log = MyLog.get_log()
        # 环境配置获取
        self._envinit()

    def _envinit(self):
        if TEST_ENV_INFO not in EnvList:
            self.log.error('The test environment is invalid! Please check the config file of TestEnvInfo.py!')
            sys.exit(3)
        self.env = TEST_ENV_INFO

        # 配置文件初始化
        self._config = Config()

        self.host = API['request_host'].format(self.env)
        self.host_api = API['request_host_api'].format(self.env)
        self.mysql_data = '%s_mysql' % self.env.lower()
        self.credit_data = '%s_credit' % self.env.lower()
        self.asset_data = '%s_asset' % self.env.lower()
        self.user_data = '%s_user' % self.env.lower()
        self.credit_database = self._config.get_mysql(self.env, self.credit_data)
        self.asset_database = self._config.get_mysql(self.env, self.asset_data)
        self.user_database = self._config.get_mysql(self.env, self.user_data)
        self.credit_database_name = self._config.get_mysql(self.env, self.credit_data)['databaseName']
        self.asset_database_name = self._config.get_mysql(self.env, self.asset_data)['databaseName']
        self.user_database_name = self._config.get_mysql(self.env, self.user_data)['databaseName']
        self.headers = headers

        self.mysql_credit = Mysql(self.credit_database)
        self.mysql_asset = Mysql(self.asset_database)
        self.mysql_user = Mysql(self.user_database)

    def _function_init(self):
        for item in Models.__all__:
            f = '%s' % item
            vars(self)[f] = eval('Models.%s' % item)

    def get_credit_data_info(self, table='credit_loan_apply', key="查询条件", record=0):
        """
        :function: 获取credit数据库表中信息
        table : 表名
        key ： 查询关键字
        record ： 根据列表指定序列返回查询数据
        """
        sql = "select * from {}.{} where {};".format(self.credit_database_name, table, key)
        self.log.info(sql)
        # 获取表属性字段名
        keys = self.mysql_credit.select_table_column(table_name=table, database=self.credit_database_name)
        # 获取查询内容
        values = self.mysql_credit.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            return data
        except (IndexError, Exception):
            self.log.warning("SQL查询结果为空")

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
            self.log.warning("SQL查询结果为空")

    def credit_apply_query(self, data):
        """ # 接口数据payload解密
            :return:                查询状态
            """
        key = "certificate_no = '{}'".format(data['cer_no'])
        info = self.get_credit_data_info(table="credit_apply", key=key)
        try:
            status = info['status']
            return status
        except (IndexError, Exception):
            self.log.warning("SQL查询结果为空")

    def check_user_available(self, data):
        sql = "select * from credit_apply where user_tel='{}';".format(data['telephone'])
        res = self.mysql_credit.select(sql)
        if res:
            if data['cer_no'] not in res[0]:
                self.log.error('手机号已被注册, 主程序退出!')
                sys.exit(7)
            else:
                self.log.warning('提示：用户已存在授信信息\n继续流程...')


class DataGenerator(object):
    pass


if __name__ == '__main__':
    t = INIT()
    print(dir(t))
    print(t.credit_database_name)
