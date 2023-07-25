# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：Redis.py
@Author  ：jccfc
@Date    ：2022/1/4 16:54 
"""
import json

import redis

from config.TestEnvInfo import TEST_ENV_INFO
from utils import ReadConfig
from utils.Logger import MyLog

_log = MyLog.get_log()
_readconfig = ReadConfig.Config()


class Redis(object):
    def __init__(self):
        self.env = TEST_ENV_INFO
        self.host = _readconfig.get_redis(self.env)['host']
        self.port = _readconfig.get_redis(self.env)['port']
        self.password = _readconfig.get_redis(self.env)['password']
        self.redis = self.connect_redis()

    def connect_redis(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port, password=self.password, decode_responses=False)
        return redis.Redis(connection_pool=pool)

    def del_key(self, *args):
        for key in args:
            try:
                if self.redis.exists(key) == 1:
                    self.redis.delete(key)
                    _log.info("redis key:{} successfully delete".format(key))
            except Exception as err:
                _log.error("delete redis key error {}".format(err))

    def add_key(self, *args):
        for key in args:
            try:
                if self.redis.exists(key) == 1:
                    _log.info("redis key:{} 已存在".format(key))
                else:
                    self.redis.append(key, '1')
            except Exception as err:
                _log.error("append redis key error {}".format(err))

    def del_assert_repay_keys(self):
        self.del_key('000:ACCT:SysInfo:BIGACCT', '000:ACCT:AccountDate:BIGACCT')


if __name__ == '__main__':
    r = Redis()
    # print(r.redis.get('000:ACCT:SysInfo:BIGACCT').decode('utf-8', errors='ignore'))
    r.del_key('000:ACCT:SysInfo:BIGACCT')
    r.del_key('000:ACCT:AccountDate:BIGACCT')
