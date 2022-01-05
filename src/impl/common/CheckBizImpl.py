# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：CtripCheckBizImpl.py
@Author  ：jccfc
@Date    ：2021/9/9 15:55 
"""
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
        flag = 10
        for n in range(flag):
            info = self.MysqlBizImpl.get_loan_apply_info(**kwargs)
            status = info['status']
            if status == EnumLoanStatus.ON_USE.value:
                self.log.demsg('支用成功')
                return status
            elif status == EnumLoanStatus.LOAN_PAY_FAILED.value:
                self.log.error('支用失败,状态：{}'.format(status))
                return status
            else:
                self.log.demsg("支用审批状态处理中，请等待....")
                time.sleep(5)
                if n == flag-1:
                    self.log.demsg("超过当前系统设置等待时间，请手动查看结果....")

    def check_file_loan_apply_status(self, **kwargs):
        """
        @param kwargs: 查询条件
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('文件放款支用结果校验...')
        flag = 10
        for n in range(flag):
            info = self.MysqlBizImpl.get_loan_apply_info(**kwargs)
            status = info['status']
            if status == EnumLoanStatus.TO_LOAN.value:
                self.log.demsg('支用成功')
                return status
            elif status == EnumLoanStatus.LOAN_PAY_FAILED.value:
                self.log.error('支用失败,状态：{}'.format(status))
                return status
            else:
                self.log.demsg("支用审批状态处理中，请等待....")
                time.sleep(5)
                if n == flag-1:
                    self.log.demsg("超过当前系统设置等待时间，请手动查看结果....")

    def check_credit_apply_status(self, **kwargs):
        """
        @param kwargs: 查询条件
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('数据库授信结果校验...')
        flag = 10
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
                    self.log.demsg("超过当前系统设置等待时间，请手动查看结果....")

