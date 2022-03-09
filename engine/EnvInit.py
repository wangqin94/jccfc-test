# -*- coding: utf-8 -*-
# # -------------------------------------------------
# # - 配置数据环境全局对象初始化
# # -------------------------------------------------

import sys
from config.TestEnvInfo import *
from utils.Logger import MyLog
from utils.ReadConfig import *
from config.globalConfig import *
from utils.SFTP import SFTP


class EnvInit(object):
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


class DataGenerator(object):
    pass


if __name__ == '__main__':
    t = EnvInit()
    print(dir(t))
