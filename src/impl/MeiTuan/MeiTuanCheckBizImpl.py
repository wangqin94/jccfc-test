# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：ZhiXinCheckBizImpl.py
@Author  ：jccfc
@Date    ：2021/11/17 15:55
"""
import time

from src.enums.EnumMeiTuan import ApiStatusCodeEnum
from src.impl.MeiTuan.MeiTuanBizImpl import MeiTuanBizImpl
from src.impl.common.MysqlBizImpl import MysqlBizImpl


class MeiTuanCheckBizImpl(MeiTuanBizImpl):
    def __init__(self, data=None, encrypt_flag=True, person=False):
        super().__init__(data=data, encrypt_flag=encrypt_flag, person=person)
        self.MysqlBizImpl = MysqlBizImpl()

    def check_credit_apply_status(self, appNo, m=10, t=3):
        """
        @param appNo:  授信申请单号
        @param t: 每次时间间隔, 默认5S
        @param m: 查证次数 默认10次
        @return:
        """
        self.log.demsg('接口层授信结果校验...')
        for n in range(m):
            res = self.credit_query(app_no=appNo)
            try:
                code = res.get('head')['returnCode']
                if code == ApiStatusCodeEnum.SUCCESS.code:
                    status = res.get('body')['STATUS']
                    if status == ApiStatusCodeEnum.PASS.code:
                        self.log.demsg('接口层查询：授信成功')
                        return status
                    elif status == ApiStatusCodeEnum.FAIL.code:
                        self.log.error('接口层授信失败,状态：{},失败原因{}'.format(status, res.get('body')['REJECT_MSG']))
                        raise AssertionError('授信状态失败')
                    elif status == ApiStatusCodeEnum.NOT_EXIST.code:
                        self.log.error('接口层授信单号不存在,状态：{}'.format(status))
                        raise AssertionError('授信单号不存在')
                    elif status == ApiStatusCodeEnum.TO_DOING.code:
                        self.log.demsg("授信审批状态处理中，请等待....")
                        time.sleep(t)
                        if n == m-1:
                            self.log.warning("超过当前系统设置等待时间，请手动查看结果....")
                            raise AssertionError('授信状态为处理中')
                if code == ApiStatusCodeEnum.NO_HOURLY.code:
                    self.log.demsg("系统异常")
                    raise AssertionError('服务异常，接口返回code码：{}'.format(code))
            except Exception as r:
                self.log.error("系统错误:{}".format(r))
                raise

    def check_loan_apply_status(self, appNo, m=10, t=3):
        """
        @param appNo:  支用申请单号
        @param t: 每次时间间隔, 默认5S
        @param m: 查证次数 默认10次
        @return:
        """
        self.log.demsg('接口层支用结果校验...')
        for n in range(m):
            res = self.loan_query(app_no=appNo)
            try:
                code = res.get('head')['returnCode']
                if code == ApiStatusCodeEnum.SUCCESS.code:
                    status = res.get('body')['STATUS']
                    if status == ApiStatusCodeEnum.PASS.code:
                        self.log.demsg('接口层查询：支用成功')
                        return status
                    elif status == ApiStatusCodeEnum.FAIL.code:
                        self.log.error('接口层支用失败,状态：{},失败原因{}'.format(status, res.get('body')['REJECT_MSG']))
                        raise AssertionError('支用状态失败')
                    elif status == ApiStatusCodeEnum.NOT_EXIST.code:
                        self.log.error('接口层支用单号不存在,状态：{}'.format(status))
                        raise AssertionError('支用单号不存在')
                    elif status == ApiStatusCodeEnum.TO_DOING.code:
                        self.log.demsg("支用审批状态处理中，请等待....")
                        time.sleep(t)
                        if n == m-1:
                            self.log.warning("超过当前系统设置等待时间，请手动查看结果....")
                            raise AssertionError('支用状态为处理中')
                if code == ApiStatusCodeEnum.NO_HOURLY.code:
                    self.log.demsg("系统异常")
                    raise
            except Exception as r:
                self.log.error("系统错误:{}".format(r))
                raise


if __name__ == '__main__':

    MeiTuanCheckBizImpl().check_loan_apply_status("loanApplyNo16454996996268918")