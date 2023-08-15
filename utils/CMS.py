# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：Apollo.py
@Author  ：jccfc
@Date    ：2022/1/6 13:59 
"""
import json
import sys
import requests

from config.TestEnvInfo import TEST_ENV_INFO
from config.globalConfig import API, cms_headers, headers
from utils import ReadConfig
from utils.Enums import *
from utils.Logger import MyLog

_log = MyLog.get_log()
_readconfig = ReadConfig.Config()


class CMS(object):
    def __init__(self):
        self.env = TEST_ENV_INFO
        self.host = API['cms_host'].format(self.env)
        self.platformHost = API['platform_host'].format(self.env)
        self.userName = _readconfig.get_cms('userName')
        self.password = _readconfig.get_cms('password')
        self.session = requests.session()
        # self.cookie = self.login()

    def login(self):
        """
        @return: 返回登录apollo生成的cookies
        """
        url = self.host + '/loanv2-guard/hsjry/guard/v1/userlogin/byPassword'
        # url = self.host + '/login'
        payload = dict()
        payload['loginAccount'] = self.userName
        payload['password'] = self.password
        payload['picCode'] = ""
        # 发起登陆接口请求，allow_redirects=False禁止重定向
        res = self.session.post(url=url, headers=cms_headers, data=json.dumps(payload), allow_redirects=False)
        # 获取登陆接口生成的Set-Cookie
        try:
            if res.status_code == 200:
                _log.debug("请求[{}]的状态码为:{}:".format(self.host, res.status_code))
                _log.debug("login CMS success, Save TOKEN in cookies")
                token = res.json()['data']['token']
                return token
            else:
                _log.error("login {} error".format(self.host))
                sys.exit()
        except Exception as err:
            _log.error("login CMS failed {}".format(err))
            raise AssertionError(err)

    def get_configMng(self, **kwargs):
        """
        配置过滤接口，按条件过滤
        @param kwargs: 任空过滤条件key、name、server
        @return:
        """
        url = self.platformHost + '/hsjry/platform/v1/configMng/list'
        payload = dict()
        payload['pageNum'] = 1
        payload['pageSize'] = 10
        payload.update(kwargs)
        res = self.session.post(url=url, headers=headers, data=json.dumps(payload))
        # 接口校验
        if res.status_code == EnumStatusCode.SUCCESS.value:
            _log.info("请求[{}]的状态码为:{}:".format(url, res.status_code))
        total = res.json()['data']['total']
        try:
            if total == 1:
                _log.info("search config success.")
                configMsg = res.json()['data']['list'][0]
                _log.info(configMsg)
                return configMsg
            else:
                _log.error('search failed! cannot get config:{}'.format(kwargs))
                raise ValueError("get config error")
        except Exception as err:
            raise ValueError(err)

    def update_config(self, value, **kwargs):
        """
        配置过滤接口，按条件过滤
        @param value: 待更新值
        @param kwargs: 任空过滤条件key、name、server
        @return:
        """
        url = self.platformHost + '/hsjry/platform/v1/configMng/modify'
        # 调取参数模糊查询接口，返回配置信息
        configMsg = self.get_configMng(**kwargs)
        payload = dict()
        payload['id'] = configMsg['id']
        payload['server'] = configMsg['useType']
        payload['key'] = configMsg['key']
        payload['name'] = configMsg['name']
        payload['remark'] = configMsg['remark']
        payload['value'] = value
        res = self.session.post(url=url, headers=headers, data=json.dumps(payload))
        try:
            # 接口校验
            if res.status_code == EnumStatusCode.SUCCESS.value:
                _log.info("请求[{}]的状态码为:{}:".format(url, res.status_code))
            else:
                _log.error('update failed!')
                raise ValueError("update api failed. {}".format(url))
        except Exception as err:
            raise ValueError(err)


if __name__ == '__main__':
    cms = CMS()
    cms.update_config(key='hair.first.balance.amount', name='海尔', server='op-channel', value=200000)
