# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：Redis.py
@Author  ：jccfc
@Date    ：2022/1/4 16:54 
"""
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
        pool = redis.ConnectionPool(host=self.host, port=self.port, password=self.password, decode_responses=True)
        return redis.Redis(pool)

    def del_value(self, **kwargs):
        for key, value in kwargs:
            self.redis.hexists()


if __name__ == '__main__':
    r = Redis()