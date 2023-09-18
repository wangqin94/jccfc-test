# -*- coding: utf-8 -*-
"""
test case script
"""
import os
if not os.path.exists('person.py'):
    open('person.py', 'w')
import time
from person import *
from src.impl.FqlGrt.FqlGrtBizImpl import FqlZxBizImpl
from utils.Logger import MyLog


class TestCase(object):
    def __init__(self):
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    @staticmethod
    def process(flag=0):
        # 授信
        if flag == 0:
            fql_zx = FqlZxBizImpl(data=None)
            # orderType: 1-赊销 3-取现 4-乐花卡
            fql_zx.credit(orderType='1', creditAmount=30000, loanPrincipal=30000, loanTerm=3)

        # 授信查询
        if flag == 1:
            fql_zx = FqlZxBizImpl(data=data)
            fql_zx.credit_query()

        # 支用申请
        if flag == 2:
            fql_zx = FqlZxBizImpl(data=data)
            # orderType: 1-赊销 3-取现 4-乐花卡
            fql_zx.loan(orderType=1, loanPrincipal=30000, loanTerm=3, fixedBillDay=10, fixedRepayDay=20)

        # 支用查询
        if flag == 3:
            fql_zx = FqlZxBizImpl(data=data)
            fql_zx.loan_query()

        # 还款计划查询
        if flag == 4:
            fql_zx = FqlZxBizImpl(data=data)
            fql_zx.repayPlan_query()

        # 还款试算
        if flag == 5:
            fql_zx = FqlZxBizImpl(data=data)
            fql_zx.repay_trial()

        # 还款通知
        if flag == 6:
            fql_zx = FqlZxBizImpl(data=data)
            fql_zx.repay()

        # 还款通知查询
        if flag == 7:
            fql_zx = FqlZxBizImpl(data=data)
            fql_zx.repay_query()

        # 代扣申请
        if flag == 8:
            fql_zx = FqlZxBizImpl(data=data)
            fql_zx.withhold()

        # 代扣查询
        if flag == 9:
            fql_zx = FqlZxBizImpl(data=data)
            fql_zx.withhold_query()


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    log = MyLog().get_log()
    log.info('程序运行时间：{}'.format(round(total)))
