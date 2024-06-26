# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：CtripCheckBizImpl.py
@Author  ：jccfc
@Date    ：2021/9/9 15:55 
"""
import sys
from src.enums.EnumsCommon import *
from src.impl.common.CommonBizImpl import *
from src.impl.common.MysqlBizImpl import MysqlBizImpl


class CheckBizImpl(EnvInit):
    def __init__(self):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()

    def check_loan_apply_status(self, m=10, t=3, **kwargs):
        """
        @param kwargs: 查询条件
        @param t: 每次时间间隔, 默认5S
        @param m: 查证次数 默认10次
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('支用结果校验...')
        for i in range(m):
            info = self.MysqlBizImpl.get_loan_apply_info(**kwargs)
            if not info:
                self.log.info("credit_loan_apply未查询到支用记录，开始重试查证,当前第-{}-次".format(i))
                time.sleep(t)
                if i == m - 1:
                    self.log.error("超过当前系统设置等待时间，支用异常，请手动查看结果....")
                    raise AssertionError('{}内数据系统数据未插入数据库，测试终止'.format(m * t))
            else:
                self.log.info("支用记录已入loan_apply表")
                break
        for j in range(m):
            info = self.MysqlBizImpl.get_loan_apply_info(**kwargs)
            status = info['status']
            if status == EnumLoanStatus.ON_USE.value:
                self.log.demsg('支用成功')
                return status
            elif status == EnumLoanStatus.LOAN_PAY_FAILED.value:
                self.log.error('支用失败,状态：{},原因：{}'.format(status, info['fail_reason']))
                raise AssertionError(
                    '检验不符合期望，中断测试。期望值：{}，实际值：{}....失败原因：{}'.format(EnumCreditStatus.SUCCESS.value, status,
                                                                   info['fail_reason']))
            elif status == EnumLoanStatus.DEAL_FAILED.value:
                self.log.error('支用失败,状态：{},原因：{}'.format(status, info['fail_reason']))
                raise AssertionError(
                    '检验不符合期望，中断测试。期望值：{}，实际值：{}....失败原因：{}'.format(EnumCreditStatus.SUCCESS.value, status,
                                                                   info['fail_reason']))
            elif status == EnumLoanStatus.REJECT.value:
                self.log.error('支用失败,状态：{},原因：{}'.format(status, info['fail_reason']))
                raise AssertionError(
                    '检验不符合期望，中断测试。期望值：{}，实际值：{}....失败原因：{}'.format(EnumCreditStatus.SUCCESS.value, status,
                                                                   info['fail_reason']))
            else:
                self.log.demsg("支用审批状态处理中，请等待....")
                time.sleep(t)
                if j == m - 1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")
                    raise AssertionError('检验不符合期望，中断测试。当前状态：{}不为终态'.format(status))

    def check_loan_apply_status_with_expect(self, expect_status, m=10, t=3, **kwargs):
        """
        @param expect_status: 期望状态
        @param kwargs: 查询条件
        @param t: 每次时间间隔, 默认5S
        @param m: 查证次数 默认10次
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('支用结果校验...')
        for j in range(m):
            info = self.MysqlBizImpl.get_loan_apply_info(**kwargs)
            if not info:
                self.log.info("credit_loan_apply未查询到支用记录，开始重试查证,当前第-{}-次".format(j))
                time.sleep(t)
            else:
                status = info['status']
                if status == expect_status:
                    self.log.demsg('支用单状态校验成功，符合预期值[status={}]'.format(expect_status))
                    return status
                elif status == EnumLoanStatus.LOAN_PAY_FAILED.value:
                    self.log.error('支用失败,状态：{},原因：{}'.format(status, info['fail_reason']))
                    raise AssertionError(
                        '检验不符合期望，中断测试。期望值：{}，实际值：{}....失败原因：{}'.format(EnumCreditStatus.SUCCESS.value, status,
                                                                       info['fail_reason']))
                elif status == EnumLoanStatus.DEAL_FAILED.value:
                    self.log.error('支用失败,状态：{},原因：{}'.format(status, info['fail_reason']))
                    raise AssertionError(
                        '检验不符合期望，中断测试。期望值：{}，实际值：{}....失败原因：{}'.format(EnumCreditStatus.SUCCESS.value, status,
                                                                       info['fail_reason']))
                elif status == EnumLoanStatus.REJECT.value:
                    self.log.error('支用失败,状态：{},原因：{}'.format(status, info['fail_reason']))
                    raise AssertionError(
                        '检验不符合期望，中断测试。期望值：{}，实际值：{}....失败原因：{}'.format(EnumCreditStatus.SUCCESS.value, status,
                                                                       info['fail_reason']))
                else:
                    self.log.demsg("支用单状态不符合预期，期望值[{}]！= 实际值[{}]，当前第[{}]次查证....".format(expect_status, status, j + 1))
                    time.sleep(t)
                    if j == m - 1:
                        self.log.error("超过当前系统设置等待时间，支用单状态不符合预期，当前值[{}]！= 实际值[{}]".format(expect_status, status))
                        raise AssertionError('{}内数据系统数据未插入数据库，测试终止'.format(m * t))

    def check_file_loan_apply_status(self, m=20, t=3, **kwargs):
        """
        @param kwargs: 查询条件
        @param t: 每次时间间隔, 默认5S
        @param m: 查证次数 默认10次
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('文件放款支用结果校验...')
        for i in range(m):
            info = self.MysqlBizImpl.get_loan_apply_info(**kwargs)
            if not info:
                self.log.info("credit_loan_apply未查询到支用记录，开始重试查证,当前第-{}-次".format(i))
                time.sleep(t)
                if i == m - 1:
                    self.log.error("超过当前系统设置等待时间，支用异常，请手动查看结果....")
                    raise AssertionError('{}内数据系统数据未插入数据库，测试终止'.format(m * t))
            else:
                self.log.info("支用记录已入loan_apply表")
                break
        for j in range(m):
            info = self.MysqlBizImpl.get_loan_apply_info(**kwargs)
            status = info['status']
            if status == EnumLoanStatus.TO_LOAN.value:
                self.log.demsg('支用成功')
                return status
            elif status == EnumLoanStatus.LOAN_PAY_FAILED.value:
                self.log.error('支用失败,状态：{},原因：{}'.format(status, info['fail_reason']))
                raise AssertionError(
                    '检验不符合期望，中断测试。期望值：{}，实际值：{}....失败原因：{}'.format(EnumCreditStatus.SUCCESS.value, status,
                                                                   info['fail_reason']))
            elif status == EnumLoanStatus.DEAL_FAILED.value:
                self.log.error('支用失败,状态：{},原因：{}'.format(status, info['fail_reason']))
                raise AssertionError(
                    '检验不符合期望，中断测试。期望值：{}，实际值：{}....失败原因：{}'.format(EnumCreditStatus.SUCCESS.value, status,
                                                                   info['fail_reason']))
            elif status == EnumLoanStatus.REJECT.value:
                self.log.error('支用失败,状态：{},原因：{}'.format(status, info['fail_reason']))
                raise AssertionError(
                    '检验不符合期望，中断测试。期望值：{}，实际值：{}....失败原因：{}'.format(EnumCreditStatus.SUCCESS.value, status,
                                                                   info['fail_reason']))
            else:
                self.log.demsg("支用审批状态处理中，请等待....")
                time.sleep(t)
                if j == m - 1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")
                    raise AssertionError('检验不符合期望，中断测试。当前状态：{}不为终态'.format(status))

    def check_credit_apply_status(self, m=20, t=3, **kwargs):
        """
        @param kwargs: 查询条件
        @param t: 每次时间间隔, 默认5S
        @param m: 查证次数 默认10次
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('数据库授信结果校验...')
        for i in range(m):
            info = self.MysqlBizImpl.get_credit_apply_info(**kwargs)
            if not info:
                self.log.info("credit_apply未查询到授信记录，开始重试查证,当前第-{}-次".format(i))
                time.sleep(t)
                if i == m - 1:
                    self.log.error("超过当前系统设置等待时间，授信异常，请手动查看结果....")
                    raise AssertionError('{}内数据系统数据未插入数据库，测试终止'.format(m * t))
            else:
                self.log.info("授信记录已入credit_apply表")
                break
        for j in range(m):
            info = self.MysqlBizImpl.get_credit_apply_info(**kwargs)
            status = info['status']
            if status == EnumCreditStatus.SUCCESS.value:
                self.log.demsg('数据库层授信查询成功')
                return status
            elif status == EnumCreditStatus.FAIL.value:
                self.log.error('数据库层授信查询结果失败,状态：{}; 失败原因：{}'.format(status, info['fail_reason']))
                raise AssertionError(
                    '检验不符合期望，中断测试。期望值：{}，实际值：{}....失败原因：{}'.format(EnumCreditStatus.SUCCESS.value, status,
                                                                   info['fail_reason']))
            else:
                self.log.demsg("授信审批状态处理中，请等待....")
                time.sleep(t)
                if j == m - 1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")
                    raise AssertionError('检验不符合期望，中断测试。当前状态：{}不为终态'.format(status))

    def check_channel_repay_status(self, m=10, t=3, **kwargs):
        """
        还款表channel_repay结果校验
        @param kwargs: 查询条件
        @param t: 每次时间间隔, 默认5S
        @param m: 查证次数 默认10次
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('数据库还款结果校验...')
        for i in range(m):
            info = self.MysqlBizImpl.get_op_channel_database_info('channel_repay', **kwargs)
            if not info:
                self.log.info("channel_repay未查询到还款记录，开始重试查证,当前第-{}-次".format(i))
                time.sleep(t)
                if i == m - 1:
                    self.log.error("超过当前系统设置等待时间，还款异常，请手动查看结果....")
                    raise AssertionError('{}内数据系统数据未插入数据库，测试终止'.format(m * t))
            else:
                self.log.info("还款记录已入channel_repay表")
                break
        for j in range(m):
            info = self.MysqlBizImpl.get_op_channel_database_info('channel_repay', **kwargs)
            status = info['repay_status']
            if status == EnumChannelRepayStatus.SUCCESS.value:
                self.log.demsg('数据库层还款查询成功')
                return status
            elif status == EnumChannelRepayStatus.FAIL.value:
                self.log.error('数据库层还款查询结果为失败,状态：{}'.format(status))
                raise AssertionError(
                    '检验不符合期望，中断测试。期望值：{}，实际值：{}....失败原因：{}'.format(EnumCreditStatus.SUCCESS.value, status,
                                                                   info['fail_reason']))
            elif status == EnumChannelRepayStatus.CHECK_FAIL.value:
                self.log.error('数据库层还款查询结果为失败,状态：{}'.format(status))
                raise AssertionError('检验不符合期望，中断测试。期望值：{}，实际值：{}'.format(EnumChannelRepayStatus.SUCCESS.value, status))
            else:
                self.log.demsg("还款审批状态处理中，请等待....")
                time.sleep(t)
                if j == m - 1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")
                    raise AssertionError('检验不符合期望，中断测试。当前状态：{}不为终态'.format(status))

    def check_channel_repay_status_with_expect(self, expect_status, m=10, t=3, **kwargs):
        """
        @param expect_status: 期望状态
        @param kwargs: 查询条件
        @param t: 每次时间间隔, 默认5S
        @param m: 查证次数 默认10次
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('数据库还款结果校验...')
        for i in range(m):
            info = self.MysqlBizImpl.get_op_channel_database_info('channel_repay', **kwargs)
            if not info:
                self.log.info("channel_repay未查询到还款记录，开始重试查证,当前第-{}-次".format(i))
                time.sleep(t)
                if i == m - 1:
                    self.log.error("超过当前系统设置等待时间，还款异常，请手动查看结果....")
                    raise AssertionError('{}内数据系统数据未插入数据库，测试终止'.format(m * t))
            else:
                self.log.info("还款记录已入channel_repay表")
                break
        for j in range(m):
            info = self.MysqlBizImpl.get_op_channel_database_info('channel_repay', **kwargs)
            status = info['repay_status']
            if status == expect_status:
                self.log.demsg('数据库层还款状态符合预期')
                return status
            elif status == EnumChannelRepayStatus.FAIL.value:
                self.log.error('数据库层还款查询结果为失败,状态：{}'.format(status))
                raise AssertionError(
                    '检验不符合期望，中断测试。期望值：{}，实际值：{}....失败原因：{}'.format(EnumCreditStatus.SUCCESS.value, status,
                                                                   info['fail_reason']))
            elif status == EnumChannelRepayStatus.CHECK_FAIL.value:
                self.log.error('数据库层还款查询结果为失败,状态：{}'.format(status))
                raise AssertionError('检验不符合期望，中断测试。期望值：{}，实际值：{}'.format(EnumChannelRepayStatus.SUCCESS.value, status))
            else:
                self.log.demsg("还款审批状态处理中，请等待....")
                time.sleep(t)
                if j == m - 1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")
                    raise AssertionError('检验不符合期望，中断测试。当前状态：{}不为终态'.format(status))

    def check_channel_loan_compensation_status(self, m=10, t=3, **kwargs):
        """
        还款表channel_loan_compensation结果校验
        @param kwargs: 查询条件
        @param t: 每次时间间隔, 默认5S
        @param m: 查证次数 默认10次
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('数据库还款结果校验...')
        for i in range(m):
            info = self.MysqlBizImpl.get_op_channel_database_info('channel_loan_compensation', **kwargs)
            if not info:
                self.log.info("channel_loan_compensation未查询到还款记录，开始重试查证,当前第-{}-次".format(i))
                time.sleep(t)
                if i == m - 1:
                    self.log.error("超过当前系统设置等待时间，还款异常，请手动查看结果....")
                    raise AssertionError('{}内数据系统数据未插入数据库，测试终止'.format(m * t))
            else:
                self.log.info("还款记录已入channel_loan_compensation表")
                break
        for j in range(m):
            info = self.MysqlBizImpl.get_op_channel_database_info('channel_loan_compensation', **kwargs)
            status = info['list_status']
            if status == EnumChannelLoanCompensationStatus.ACCOUNT_SUCCESS.value:
                self.log.demsg('数据库层还款查询成功')
                return status
            elif status == EnumChannelLoanCompensationStatus.FAIL.value:
                self.log.error('数据库层还款查询结果为失败,状态：{}'.format(status))
                raise AssertionError(
                    '检验不符合期望，中断测试。期望值：{}，实际值：{}....失败原因：{}'.format(
                        EnumChannelLoanCompensationStatus.ACCOUNT_SUCCESS.value,
                        status, info['compensation_desc']))
            elif status == EnumChannelLoanCompensationStatus.FAIL_WAIT_BACK.value:
                self.log.error('数据库层还款查询结果为失败,状态：{}'.format(status))
                raise AssertionError('检验不符合期望，中断测试。期望值：{}，实际值：{}'.format(
                    EnumChannelLoanCompensationStatus.ACCOUNT_SUCCESS.value, status))
            else:
                self.log.demsg("还款审批状态处理中，请等待....")
                time.sleep(t)
                if j == m - 1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")
                    raise AssertionError('检验不符合期望，中断测试。当前状态：{}不为终态'.format(status))

    def check_H5_repay_status(self, m=10, t=5, **kwargs):
        """
        还款表credit_custom_payment_apply结果校验
        @param kwargs: 查询条件
        @param t: 每次时间间隔, 默认5S
        @param m: 查证次数 默认10次
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('数据库还款结果校验...')
        for i in range(m):
            info = self.MysqlBizImpl.get_credit_database_info('credit_custom_payment_apply', **kwargs)
            if not info:
                self.log.info("credit_custom_payment_apply未查询到还款记录，启动查证,当前第-{}-次".format(i))
                time.sleep(3)
                if i == m - 1:
                    self.log.error("超过当前系统设置等待时间，还款异常，请手动查看结果....")
                    raise AssertionError('{}内数据系统数据未插入数据库，测试终止'.format(m * t))
            else:
                self.log.info("还款记录已入credit_custom_payment_apply表")
                break
        for j in range(m):
            info = self.MysqlBizImpl.get_credit_database_info('credit_custom_payment_apply', **kwargs)
            status = info['deal_status']
            if status == EnumCustomPaymentStatus.SUCCESS.value:
                self.log.demsg('数据库层还款查询成功')
                return status
            elif status == EnumCustomPaymentStatus.FAIL.value:
                self.log.error('数据库层还款查询结果为失败,状态：{}'.format(status))
                raise AssertionError(
                    '检验不符合期望，中断测试。期望值：{}，实际值：{}....失败原因：{}'.format(EnumCreditStatus.SUCCESS.value, status,
                                                                   info['fail_message']))
            else:
                self.log.demsg("还款审批状态处理中，请等待....")
                time.sleep(t)
                if j == m - 1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")
                    raise AssertionError('检验不符合期望，中断测试。当前状态：{}不为终态'.format(status))

    def check_repay_notice_status(self, m=10, t=5, **kwargs):
        """
        还款表credit_ctrip_repay_notice_info结果校验
        @param kwargs: 查询条件
        @param t: 每次时间间隔, 默认5S
        @param m: 查证次数 默认10次
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('数据库还款结果校验...')
        for i in range(m):
            info = self.MysqlBizImpl.get_credit_database_info('credit_ctrip_repay_notice_info', **kwargs)
            if not info:
                self.log.info("credit_ctrip_repay_notice_info未查询到还款记录，开始重试查证,当前第-{}-次".format(i))
                time.sleep(t)
                if i == m - 1:
                    self.log.error("超过当前系统设置等待时间，还款异常，请手动查看结果....")
                    raise AssertionError('{}内数据系统数据未插入数据库，测试终止'.format(m * t))
            else:
                self.log.info("还款记录已入credit_ctrip_repay_notice_info表")
                break
        for j in range(m):
            info = self.MysqlBizImpl.get_credit_database_info('credit_ctrip_repay_notice_info', **kwargs)
            status = info['deal_status']
            if status == EnumHjRepayNoticeStatus.REPAY_SUCCESS.value:
                self.log.demsg('数据库层还款查询成功')
                return status
            elif status in (EnumHjRepayNoticeStatus.REPAY_FAIL.value, EnumHjRepayNoticeStatus.VALIDATE_FAIL.value):
                self.log.error('数据库层还款查询结果为失败,状态：{}'.format(status))
                raise AssertionError(
                    '检验不符合期望，中断测试...[期望值：{};实际值：{}]....失败原因：{}'.format(EnumHjRepayNoticeStatus.REPAY_SUCCESS.value,
                                                                       status,
                                                                       info['fail_reason']))
            else:
                self.log.demsg("还款审批状态处理中，请等待....")
                time.sleep(t)
                if j == m - 1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")
                    raise AssertionError('检验不符合期望，中断测试。当前状态：{}不为终态'.format(status))

    def check_third_wait_loan_status(self, t=5, **kwargs):
        """
        三方待放款建账明细信息credit_third_wait_loan_deal_info结果校验
        :param t: 每次时间间隔, 默认5S
        :param kwargs: 查询条件
        :return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('数据库三方放款结果校验...')
        flag = 3
        for i in range(flag + 1):
            info = self.MysqlBizImpl.get_credit_database_info('credit_third_wait_loan_deal_info', **kwargs)
            if not info:
                self.log.info("credit_third_wait_loan_deal_info未查询到还款记录，开始重试查证,当前第-{}-次".format(i))
                time.sleep(t)
                if i == flag:
                    self.log.error("超过当前系统设置等待时间，放款异常，请手动查看结果....")
                    sys.exit(7)
            else:
                try:
                    info['deal_status'] = EnumHjLoanDealStatus.INIT.value
                    self.log.info("放款记录已入credit_third_wait_loan_deal_info表")
                except AssertionError:
                    self.log.info("放款记录入库异常")
                break

    def get_repay_notice_info(self, m=6, t=3, **kwargs):
        """
        查询支用状态
        @param t: 每次时间间隔, 默认5S
        @param m: 查证次数 默认6次
        @param kwargs: 查询条件
        @return: status 支用单状态
        """
        self.log.demsg('获取还款通知表信息...')
        for i in range(m):
            info = self.MysqlBizImpl.get_credit_database_info('credit_ctrip_repay_notice_info', **kwargs)
            if not info:
                self.log.info("credit_ctrip_repay_notice_info未查询到还款记录，开始重试查证,当前第-{}-次".format(i))
                time.sleep(t)
                if i == m - 1:
                    self.log.error("超过当前系统设置等待时间，还款异常，请手动查看结果....")
                    raise AssertionError('{}内数据系统数据未插入数据库，测试终止'.format(m * t))
            else:
                self.log.info("还款记录已入credit_ctrip_repay_notice_info表")
                break

    def check_asset_repay_plan_overdue_days(self, max_overdue_days, m=6, t=5, **kwargs):
        """
        查询支用状态
        @param t: 每次时间间隔, 默认5S
        @param max_overdue_days: 期望的最大逾期天数
        @param m: 查证次数 默认6次
        @param kwargs: 查询条件
        @return: overdue_days 逾期天数
        """
        self.log.demsg('获取还款计划表最大逾期天数...')
        for i in range(m):
            info = self.MysqlBizImpl.get_asset_database_info("asset_repay_plan", **kwargs)
            overdue_days = info['overdue_days']
            if overdue_days >= max_overdue_days:
                self.log.demsg('asset_repay_plan获取借据最大逾期天数[overdue_days：{}]'.format(overdue_days))
                return overdue_days
            else:
                time.sleep(t)
                if i == m - 1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")
                    raise AssertionError('检验不符合期望，中断测试。当前逾期天数：{}'.format(overdue_days))

    def check_asset_table_status(self, table, query_key, expect_value, m=10, t=3, **kwargs):
        """
        查询资产数据表
        :param table: 表名
        :param query_key: 查询字段
        :param expect_value: 期望值
        :param m: 循环次数
        :param t: 循环间隔时间
        :param kwargs: 查询条件
        :return:
        """
        self.log.demsg('{}表状态检查...'.format(table))
        for i in range(m):
            info = self.MysqlBizImpl.get_asset_database_info(table, query_key, **kwargs)
            if not info:
                self.log.info("{}未查询到记录，启动查证,当前第-{}-次".format(table, i))
                time.sleep(3)
                if i == m - 1:
                    self.log.error("超过当前系统设置等待时间，还款异常，请手动查看结果....")
                    raise AssertionError('{}内数据系统数据未插入数据库，测试终止'.format(m * t))
            else:
                self.log.info("数据已入{}表".format(table))
                break
        status = ''
        for j in range(m):
            info = self.MysqlBizImpl.get_asset_database_info(table, query_key, **kwargs)
            status = info[query_key]
            if status == expect_value:
                self.log.demsg('数据库状态校验成功')
                return
            else:
                self.log.demsg("处理中，请等待....")
                time.sleep(t)
        else:
            self.log.error("超过当前系统设置等待时间，请手动查看结果....")
            raise AssertionError('检验不符合期望，中断测试。当前状态：{}'.format(status))


if __name__ == '__main__':
    # CheckBizImpl().check_channel_repay_status(id=999)
    CheckBizImpl().check_credit_apply_status(thirdpart_apply_id="thirdApplyId16794799870849850")
