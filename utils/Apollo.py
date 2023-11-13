# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：Apollo.py
@Author  ：jccfc
@Date    ：2022/1/6 13:59 
"""
import sys
import time

import requests

from config.TestEnvInfo import TEST_ENV_INFO, hj, credit
from config.globalConfig import API, apollo_headers, json_headers
from utils import ReadConfig
from utils.Enums import *
from utils.Logger import MyLog

_log = MyLog.get_log()
_readconfig = ReadConfig.Config()


def getApolloEnv(env):
    # apolloEnv = None
    try:
        if env in hj:
            apolloEnv = _readconfig.get_apollo('envCredit')
            return apolloEnv
        elif env in credit:
            apolloEnv = _readconfig.get_apollo('envAsset')
            return apolloEnv
        else:
            raise Exception("[{}] not in env list".format(env))
    except Exception as err:
        _log.error("env error. {}".format(err))
        raise err
        # sys.exit()


class Apollo(object):
    def __init__(self):
        self.env = TEST_ENV_INFO
        self.apolloEnv = getApolloEnv(self.env)
        self.host = API['request_apollo_host'].format(self.apolloEnv)
        self.index_url = API['apollo_index_host'].format(self.apolloEnv)
        self.userName = _readconfig.get_apollo('userName')
        self.password = _readconfig.get_apollo('password')
        self.session = requests.session()
        self.cookie = self.login()

    def login(self):
        """
        @return: 返回登录apollo生成的cookies
        """
        url = self.host + '/signin'
        payload = dict()
        payload['username'] = self.userName
        payload['password'] = self.password
        payload['login-submit'] = "登录"
        # 发起登陆接口请求，allow_redirects=False禁止重定向
        res = self.session.post(url=url, headers=apollo_headers, data=payload, allow_redirects=False)
        # 获取登陆接口生成的Set-Cookie
        try:
            if res.headers['Location'] == self.index_url:
                _log.debug("请求[{}]的状态码为:{}:".format(url, res.status_code))
                _log.debug("pre login apollo success, get cookies")
                cookie = res.cookies.get_dict()
                # header中添加cookies后发起登陆重定向接口
                res = self.session.get(url=self.host, cookies=cookie, allow_redirects=False)
                if res.status_code == 200:
                    _log.debug("请求[{}]的状态码为:{}:".format(self.host, res.status_code))
                    _log.debug("login apollo success, Save cookies on the client")
                    return cookie
                else:
                    _log.error("login {} error".format(self.host))
                    sys.exit()
            else:
                _log.error("Location url return fault: {}".format(res.headers['Location']))
        except Exception as err:
            _log.error("login apollo failed {}".format(err))
            raise AssertionError(err)

    def get_config(self, key, appId='loan2.1-jcxf-credit', namespace='000'):
        """
        配置过滤接口，按条件过滤
        @param key: 搜索条件 必填
        @param appId: 服务ID
        @param namespace: 任空间名称
        @return:
        """
        url = self.host + '/apps/{}/envs/{}/clusters/default/namespaces/{}'.format(appId, self.env.upper(), namespace)
        res = self.session.get(url=url, headers=json_headers, cookies=self.cookie, verify=False)
        items = res.json()['items']
        try:
            for item in items:
                if key == item['item']['key']:
                    return item['item']
            else:
                _log.error('search failed! namespaces:{} cannot get config:{}'.format(namespace, key))
                raise ValueError("get config error")
        except Exception as err:
            raise ValueError(err)

    def releases(self, appId='loan2.1-jcxf-credit', namespace='000'):
        """
        发布任务
        @param appId: 服务ID
        @param namespace: 任空间名称
        @return:
        """
        payload = dict()
        payload['isEmergencyPublish'] = False
        payload['releaseComment'] = ''
        payload['releaseTitle'] = "{}-release".format(time.strftime('%Y%m%d%H%M%S', time.localtime()))
        url = self.host + '/apps/{}/envs/{}/clusters/default/namespaces/{}/releases'.format(appId, self.env.upper(),
                                                                                            namespace)
        res = self.session.post(url=url, headers=json_headers, cookies=self.cookie, json=payload)
        if res.status_code == EnumStatusCode.SUCCESS.value:
            _log.debug("请求[{}]的状态码为:{}:".format(url, res.status_code))
            _log.info("releases configuration success")

    def update_config(self, appId='loan2.1-jcxf-credit', namespace='000', **kwargs):
        """
        任务更新接口
        @param kwargs: 更新键值 必填
        @param appId: 服务ID
        @param namespace: 任空间名称
        @return:
        """
        url = self.host + '/apps/{}/envs/{}/clusters/default/namespaces/{}/item'.format(appId, self.env.upper(),
                                                                                        namespace)
        for key, value in kwargs.items():
            data = self.get_config(key, appId=appId, namespace=namespace)
            data['tableViewOperType'] = "update"
            data['value'] = value
            res = self.session.put(url=url, headers=json_headers, cookies=self.cookie, json=data)
            # 校验
            if res.status_code == EnumStatusCode.SUCCESS.value:
                _log.debug("请求[{}]的状态码为:{}:".format(url, res.status_code))
        _log.warning("更新apollo配置: {}".format(kwargs))
        _log.info("update configuration success")
        #  执行发布
        self.releases(appId=appId, namespace=namespace)
        time.sleep(1)


if __name__ == '__main__':
    apollo = Apollo()
    updateKeys = dict()
    # 设置还款mock时间
    # updateKeys['credit.mock.repay.trade.date'] = "true"
    # updateKeys['credit.mock.repay.date'] = "2022-01-18 00:00:00"
    # apollo.update_config(**updateKeys)

    # 设置H5还款mock时间
    # updateKeys['api.mock.repay.trade.date'] = "true"
    # updateKeys['api.mock.repay.date'] = "2022-01-18 00:00:00"
    # apollo.update_config(appId='loan2.1-jcxf-app-web', **updateKeys)

    # 设置放款mock时间
    # updateKeys['credit.loan.trade.date.mock'] = "true"
    # updateKeys['credit.loan.date.mock'] = "2023-08-04"
    # apollo.update_config(appId='loan2.1-public', namespace='JCXF.system', **updateKeys)

    # 配置还款mock时间
    updateKeys['credit.mock.repay.trade.date'] = "true"  # credit.mock.repay.trade.date
    updateKeys['credit.mock.repay.date'] = "{} 13:40:00".format("2023-10-09")
    apollo.update_config(appId='loan2.1-public', namespace='JCXF.system', **updateKeys)
