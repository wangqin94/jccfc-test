# -*- coding: utf-8 -*-
# # -------------------------------------------------
# # - 配置数据环境全局对象初始化
# # -------------------------------------------------

import sys
from config.TestEnvInfo import *
from utils.Mysql import Mysql
from utils.Logger import MyLog
from utils.ReadConfig import *
from config.globalConfig import *


class MysqlInit(object):
    def __init__(self):
        super().__init__()
        # 初始化日志引擎模块
        self.log = MyLog().get_log()
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
        self.base_data = '%s_base' % self.env.lower()
        self.bigacct_data = '%s_bigacct' % self.env.lower()
        self.op_channel_data = '%s_op_channeldb' % self.env.lower()
        self.credit_database = self._config.get_mysql(self.env, self.credit_data)
        self.asset_database = self._config.get_mysql(self.env, self.asset_data)
        self.user_database = self._config.get_mysql(self.env, self.user_data)
        self.base_database = self._config.get_mysql(self.env, self.base_data)
        self.bigacct_database = self._config.get_mysql(self.env, self.bigacct_data)
        self.op_channel_database = self._config.get_mysql(self.env, self.op_channel_data)
        self.credit_database_name = self._config.get_mysql(self.env, self.credit_data)['databaseName']
        self.asset_database_name = self._config.get_mysql(self.env, self.asset_data)['databaseName']
        self.user_database_name = self._config.get_mysql(self.env, self.user_data)['databaseName']
        self.base_database_name = self._config.get_mysql(self.env, self.base_data)['databaseName']
        self.bigacct_database_name = self._config.get_mysql(self.env, self.bigacct_data)['databaseName']
        self.op_channel_database_name = self._config.get_mysql(self.env, self.op_channel_data)['databaseName']
        self.headers = headers

        self.mysql_credit = Mysql(self.credit_database)
        self.mysql_asset = Mysql(self.asset_database)
        self.mysql_user = Mysql(self.user_database)
        self.mysql_base = Mysql(self.base_database)
        self.mysql_bigacct = Mysql(self.bigacct_database)
        self.mysql_op_channel = Mysql(self.op_channel_database)


class DataGenerator(object):
    pass


if __name__ == '__main__':
    t = MysqlInit()
    print(dir(t))
    print(t.credit_database_name)

