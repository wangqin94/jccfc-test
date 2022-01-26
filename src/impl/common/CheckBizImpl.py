# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：CtripCheckBizImpl.py
@Author  ：jccfc
@Date    ：2021/9/9 15:55 
"""
import sys

from engine.EnvInit import EnvInit
from src.enums.EnumsCommon import *
from src.impl.common.CommonBizImpl import *
from src.impl.common.MysqlBizImpl import MysqlBizImpl


class CheckBizImpl(EnvInit):
    def __init__(self):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()

    def check_loan_apply_status(self, **kwargs):
        """
        @param kwargs: 查询条件
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('支用结果校验...')
        flag_n = 10
        flag_m = 2
        for m in range(flag_m+1):
            info = self.MysqlBizImpl.get_loan_apply_info(**kwargs)
            if not info:
                self.log.info("credit_loan_apply未查询到支用记录，启动3次轮训")
                time.sleep(3)
                if m == flag_m:
                    self.log.error("超过当前系统设置等待时间，支用异常，请手动查看结果....")
                    sys.exit(7)
            else:
                self.log.info("支用记录已入loan_apply表")
                break
        for n in range(flag_n):
            info = self.MysqlBizImpl.get_loan_apply_info(**kwargs)
            status = info['status']
            if status == EnumLoanStatus.ON_USE.value:
                self.log.demsg('支用成功')
                return status
            elif status == EnumLoanStatus.LOAN_PAY_FAILED.value:
                self.log.error('支用失败,状态：{},原因：{}'.format(status, info['fail_reason']))
                return status
            elif status == EnumLoanStatus.DEAL_FAILED.value:
                self.log.error('支用失败,状态：{},原因：{}'.format(status, info['fail_reason']))
                return status
            elif status == EnumLoanStatus.REJECT.value:
                self.log.error('支用失败,状态：{},原因：{}'.format(status, info['fail_reason']))
                return status
            else:
                self.log.demsg("支用审批状态处理中，请等待....")
                time.sleep(5)
                if n == flag_n-1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")

    def check_file_loan_apply_status(self, **kwargs):
        """
        @param kwargs: 查询条件
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('文件放款支用结果校验...')
        flag_n = 10
        flag_m = 2
        for m in range(flag_m+1):
            info = self.MysqlBizImpl.get_loan_apply_info(**kwargs)
            if not info:
                self.log.info("credit_loan_apply未查询到支用记录，启动3次轮训")
                time.sleep(3)
                if m == flag_m:
                    self.log.error("超过当前系统设置等待时间，支用异常，请手动查看结果....")
                    sys.exit(7)
            else:
                self.log.info("支用记录已入loan_apply表")
                break
        for n in range(flag_n):
            info = self.MysqlBizImpl.get_loan_apply_info(**kwargs)
            status = info['status']
            if status == EnumLoanStatus.TO_LOAN.value:
                self.log.demsg('支用成功')
                return status
            elif status == EnumLoanStatus.LOAN_PAY_FAILED.value:
                self.log.error('支用失败,状态：{},原因：{}'.format(status, info['fail_reason']))
                return status
            elif status == EnumLoanStatus.DEAL_FAILED.value:
                self.log.error('支用失败,状态：{},原因：{}'.format(status, info['fail_reason']))
                return status
            elif status == EnumLoanStatus.REJECT.value:
                self.log.error('支用失败,状态：{},原因：{}'.format(status, info['fail_reason']))
                return status
            else:
                self.log.demsg("支用审批状态处理中，请等待....")
                time.sleep(5)
                if n == flag_n-1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")

    def check_credit_apply_status(self, **kwargs):
        """
        @param kwargs: 查询条件
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('数据库授信结果校验...')
        flag = 10
        flag_m = 2
        for m in range(flag_m+1):
            info = self.MysqlBizImpl.get_credit_apply_info(**kwargs)
            if not info:
                self.log.info("credit_apply未查询到授信记录，启动3次轮训")
                time.sleep(3)
                if m == flag_m:
                    self.log.error("超过当前系统设置等待时间，授信异常，请手动查看结果....")
                    sys.exit(7)
            else:
                self.log.info("授信记录已入credit_apply表")
                break
        for n in range(10):
            info = self.MysqlBizImpl.get_credit_apply_info(**kwargs)
            status = info['status']
            if status == EnumCreditStatus.SUCCESS.value:
                self.log.demsg('数据库层授信查询成功')
                return status
            elif status == EnumCreditStatus.FAIL.value:
                self.log.error('数据库层授信查询结果失败,状态：{}'.format(status))
                return status
            else:
                self.log.demsg("授信审批状态处理中，请等待....")
                time.sleep(5)
                if n == flag-1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")

    def check_channel_repay_status(self, **kwargs):
        """
        还款表channel_repay结果校验
        @param kwargs: 查询条件
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('数据库还款结果校验...')
        flag = 10
        flag_m = 2
        for m in range(flag_m + 1):
            info = self.MysqlBizImpl.get_op_channel_database_info('channel_repay', **kwargs)
            if not info:
                self.log.info("channel_repay未查询到还款记录，启动3次轮训")
                time.sleep(3)
                if m == flag_m:
                    self.log.error("超过当前系统设置等待时间，还款异常，请手动查看结果....")
                    sys.exit(7)
            else:
                self.log.info("还款记录已入channel_repay表")
                break
        for n in range(10):
            info = self.MysqlBizImpl.get_op_channel_database_info('channel_repay', **kwargs)
            status = info['repay_status']
            if status == EnumChannelRepayStatus.SUCCESS.value:
                self.log.demsg('数据库层还款查询成功')
                return status
            elif status == EnumChannelRepayStatus.FAIL.value:
                self.log.error('数据库层还款查询结果为失败,状态：{}'.format(status))
                return status
            elif status == EnumChannelRepayStatus.CHECK_FAIL.value:
                self.log.error('数据库层还款查询结果为失败,状态：{}'.format(status))
                return status
            else:
                self.log.demsg("还款审批状态处理中，请等待....")
                time.sleep(5)
                if n == flag - 1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")


if __name__ == '__main__':
    CheckBizImpl().check_channel_repay_status(id=999)
