# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：JobCenter.py
@Author  ：jccfc
@Date    ：2022/1/4 10:32 
"""
import requests
from requests.cookies import RequestsCookieJar

from config.TestEnvInfo import TEST_ENV_INFO
from config.globalConfig import API, job_headers
from utils import ReadConfig
from utils.Logger import MyLog

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
        self.cookie = self.connect()

    def connect(self):
        """
        @return: 返回登录任务中心生成的cookies
        """
        url = self.host + '/job-admin/login'
        payload = dict()
        payload['userName'] = self.userName
        payload['password'] = self.password
        res = self.session.post(url=url, headers=job_headers, data=payload)
        cookieJar = requests.cookies.RequestsCookieJar()  # 利用RequestsCookieJar获取
        for cookie in res.cookies:
            cookieJar.set(cookie.name, cookie.value)
        res.cookies.update(cookieJar)
        cookie = res.cookies.get_dict()
        return cookie

    def get_job(self, desc, group=5, job_type='MAIN_TRIGGER_JOB'):
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
        res = self.session.post(url=url, headers=job_headers, cookies=self.cookie, data=payload, verify=False)
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

    def trigger_job(self, job_id):
        """
        任务执行接口
        @param job_id: 任务id 必填
        @return:
        """
        url = self.host + '/job-admin/jobinfo/trigger'
        payload = {'id': job_id}
        res = self.session.post(url=url, headers=job_headers, cookies=self.cookie, data=payload, verify=False)
        data = res.json()
        try:
            if data['code'] == 200 and data['msg'] == "任务触发成功":
                _log.demsg("任务:{}触发成功".format(job_id))
        except Exception as err:
            _log.error('trigger job failed! %s', err)


if __name__ == '__main__':
    job = JOB()
    s = job.get_job("互金支用风控轮询任务流")
    job.trigger_job(s)
