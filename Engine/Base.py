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
        self.mysql_database_name = '%s_mysql' % self.env.lower()
        self.credit_database_name = '%s_credit' % self.env.lower()
        self.asset_database_name = '%s_asset' % self.env.lower()
        self.general_database = ENV[self.env]['database'][self.mysql_database_name]
        self.credit_database = ENV[self.env]['database'][self.credit_database_name]
        self.asset_database = ENV[self.env]['database'][self.asset_database_name]
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


class DataGenerator(object):
    pass


if __name__ == '__main__':
    t = INIT()
    print(dir(t))
    print(t.credit_database_name)
