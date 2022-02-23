# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：JobCenter.py
@Author  ：jccfc
@Date    ：2022/1/4 10:32 
"""
import json
import sys

import requests
from requests.cookies import RequestsCookieJar

from config.TestEnvInfo import TEST_ENV_INFO
from config.globalConfig import API, job_headers
from utils import ReadConfig
from utils.Logger import MyLog
from utils.Models import DataUpdate

_log = MyLog.get_log()
_readconfig = ReadConfig.Config()
__all__ = ['JOB']


class JOB(object):
    def __init__(self):
        self.env = TEST_ENV_INFO
        self.host = API['request_job_host'].format(self.env)
        self.userName = _readconfig.get_job('userName')
        self.password = _readconfig.get_job('password')
        self.session = requests.session()
        self.cookie = self.login()

    def login(self):
        """
        @return: 返回登录任务中心生成的cookies
        """
        url = self.host + '/job-admin/login'
        payload = dict()
        payload['userName'] = self.userName
        payload['password'] = self.password
        # cookieJar = requests.cookies.RequestsCookieJar()  # 利用RequestsCookieJar获取
        # for cookie in res.cookies:
        #     cookieJar.set(cookie.name, cookie.value)
        # res.cookies.update(cookieJar)

        # 发起登陆接口请求，allow_redirects=False允许重定向
        res = self.session.post(url=url, headers=job_headers, data=payload, allow_redirects=True)
        # 获取登陆接口生成的Set-Cookie
        cookie = res.cookies.get_dict()
        try:
            if cookie:
                return cookie
            else:
                raise AssertionError
        except Exception as err:
            _log.error("cookies id None, login job center error {}".format(err))
            sys.exit()

    def get_job_info(self, desc, group=5, job_type='MAIN_TRIGGER_JOB'):
        """
        任务过滤接口，按条件过滤，记录为1命中搜索
        @param desc: 任务描述 必填
        @param group: 执行器ID 5：credit； 6：assert
        @param job_type: 任务层级 MAIN_TRIGGER_JOB：任务流； VIRTUAL_JOB=任务；
        @return:
        """
        url = self.host + '/job-admin/jobinfo/pageList'
        payload = {
            'jobGroup': group,
            'jobDesc': desc,
            'jobLevelType': job_type,
            'jobOrganizationSource': '',
            'start': 0,
            'length': 25
        }
        res = self.session.post(url=url, headers=job_headers, cookies=self.cookie, data=payload)
        data = res.json()['data']
        try:
            if len(data) > 1:
                _log.error("按描述搜索记录超过1条，请重新输入搜索条件")
                return
            if data is not None:
                jobInfo = data[0]
                return jobInfo
        except Exception as err:
            _log.error('search job failed! %s', err)

    def get_jobId(self, desc, group=5, job_type='MAIN_TRIGGER_JOB'):
        """
        任务过滤接口，按条件过滤，记录为1命中搜索
        @param desc: 任务描述 必填
        @param group: 执行器ID 5：credit； 6：assert
        @param job_type: 任务层级 MAIN_TRIGGER_JOB：任务流； VIRTUAL_JOB=任务；
        @return: 任务id
        """
        url = self.host + '/job-admin/jobinfo/pageList'
        payload = {
            'jobGroup': group,
            'jobDesc': desc,
            'jobLevelType': job_type,
            'jobOrganizationSource': '',
            'start': 0,
            'length': 25
        }
        res = self.session.post(url=url, headers=job_headers, cookies=self.cookie, data=payload)
        data = res.json()['data']
        try:
            if len(data) > 1:
                _log.error("按描述搜索记录超过1条，请重新输入搜索条件")
                return
            if data is not None:
                jobId = data[0].get('id')
                return jobId
        except Exception as err:
            _log.error('search job failed! %s', err)

    def update_job(self, desc, group=5, job_type='MAIN_TRIGGER_JOB', **kwargs):
        """
        任务更新接口
        @param kwargs: 更新数据 必填
        @param desc: 任务描述 必填
        @param group: 执行器ID 5：credit； 6：assert
        @param job_type: 任务层级 MAIN_TRIGGER_JOB：任务流； VIRTUAL_JOB=任务；
        """
        url = self.host + '/job-admin/jobinfo/update'
        # 获取配置信息
        payload = {
            'jobDesc': '资产日终任务流',
            "jobOrganizationSource": "PRODUCT_JOB",
            "jobLevelType": "MAIN_TRIGGER_JOB",
            "executorBlockStrategy": "SERIAL_EXECUTION",
            "executorRouteStrategy": "FIRST",
            "alarmMobile": "",
            "alarmEmail": "",
            "executeBizDateType": "CUSTOMER",
            "executeBizDate": "20210612",
            "author": "huangyl",
            "jobCron": "0 5 1 * * ? ",
            "executorTimeout": "0",
            "executorShardParam": "",
            "executorParam": "",
            "id": "336592602008784896"
        }
        # 获取任务的配置信息并更新
        jobInfo = self.get_job_info(desc, group=group, job_type=job_type)
        parser = DataUpdate(payload, **jobInfo)
        active_payload = parser.parser
        # 根据输入字段更新配置信息
        parser = DataUpdate(active_payload, **kwargs)
        active_payload = parser.parser

        res = self.session.post(url=url, headers=job_headers, cookies=self.cookie, data=active_payload, verify=False)
        data = res.json()
        try:
            if data['code'] == 200:
                _log.demsg("任务'{}'更新成功，更新内容：{}".format(desc, kwargs))
            else:
                _log.demsg("任务'{}'更新失败,response msg {}".format(desc, data))
        except Exception as err:
            _log.error('update job failed! %s', err)

    def trigger_job(self, desc, group=5, job_type='MAIN_TRIGGER_JOB'):
        """
        任务执行接口
        @param desc: 任务描述 必填
        @param group: 执行器ID 5：credit； 6：assert
        @param job_type: 任务层级 MAIN_TRIGGER_JOB：任务流； VIRTUAL_JOB=任务；
        @return:
        """
        url = self.host + '/job-admin/jobinfo/trigger'
        job_id = self.get_jobId(desc, group=group, job_type=job_type)
        payload = {'id': job_id}
        res = self.session.post(url=url, headers=job_headers, cookies=self.cookie, data=payload, verify=False)
        data = res.json()
        try:
            if data['code'] == 200 and data['msg'] == "任务触发成功":
                _log.demsg("任务:{}触发成功".format(job_id))
        except Exception as err:
            _log.error('trigger job failed! %s', err)

    def trigger_job_byJobId(self, job_group='5', job_type='MAIN_TRIGGER_JOB', id="" ,executeBizDate=""):
        """
        任务执行接口
        @param desc: 任务描述 必填
        @param group: 执行器ID 5：credit； 6：assert
        @param job_type: 任务层级 MAIN_TRIGGER_JOB：任务流； VIRTUAL_JOB=任务；
        @return:
        """
        query_url = self.host + '/job-admin/jobinfo/pageList'
        query_payload = {
            'jobGroup': job_group,
            'jobDesc': "",
            'jobLevelType': job_type,
            'jobOrganizationSource': '',
            'start': 0,
            'length': 250
        }
        query_res = self.session.post(url=query_url, headers=job_headers, cookies=self.cookie, data=query_payload).json()['data']
        for data in query_res:
            if data['id'] == id:
               data['executeBizDate'] = executeBizDate
               updateData = data
               break

        update_url = self.host + '/job-admin/jobinfo/update'
        trigger_url = self.host + '/job-admin/jobinfo/trigger'

        # 获取配置信息
        self.update_temple = {
            'jobDesc',
            "jobOrganizationSource",
            "jobLevelType",
            "executorBlockStrategy",
            "executorRouteStrategy",
            "alarmMobile",
            "alarmEmail",
            "executeBizDateType",
            "executeBizDate",
            "author",
            "jobCron",
            "executorTimeout",
            "executorShardParam",
            "executorParam",
            "id"
        }

        triggerData = {}
        for key in self.update_temple:
           triggerData[key] = updateData[key]

        _log.demsg("更新内容：{}".format(triggerData))
        update_res = self.session.post(url=update_url, headers=job_headers, cookies=self.cookie, data=triggerData, verify=False).json()
        try:
            if update_res['code'] == 200:
                _log.demsg("任务'{}'更新成功，更新内容：{}".format(id, triggerData))
                trigger_res = self.session.post(url=trigger_url, headers=job_headers, cookies=self.cookie,
                                        data={'id': id}, verify=False).json()
                if trigger_res['code'] == 200 and trigger_res['msg'] == "任务触发成功":
                    _log.demsg("任务:{}触发成功".format(id))
            else:
                _log.demsg("任务'{}'更新失败,response msg {}".format(id, update_res))
        except Exception as err:
            _log.error('update job failed! %s', err)


if __name__ == '__main__':
    job = JOB()
    # s = job.get_jobId("资产日终任务流", group=6)
    job.update_job("资产日终任务流", group=6, executeBizDateType='CUSTOMER', executeBizDate='20220119')
    # job.trigger_job(s)
