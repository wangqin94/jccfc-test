# -*- coding: utf-8 -*-
"""
test case script
"""
import os
if not os.path.exists('person.py'):
    open('person.py', 'w')
import time
from person import *
from src.impl.FqlGrt.FqlGrtBizImpl import FqlGrtBizImpl
from utils.Logger import MyLog


class TestCase(object):
    def __init__(self):
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    @staticmethod
    def process(flag=10):
        # 授信
        if flag == 0:
            fql_grt = FqlGrtBizImpl(data=None)
            # orderType: 1-赊销 3-取现 4-乐花卡
            fql_grt.credit(orderType='1', loanPrincipal=30000, loanTerm=15)

        # 授信查询
        if flag == 1:
            fql_grt = FqlGrtBizImpl(data=data)
            fql_grt.credit_query(applyId='123456789')

        # 支用申请
        if flag == 2:
            fql_grt = FqlGrtBizImpl(data=data)
            # orderType: 1-赊销 3-取现 4-乐花卡
            fql_grt.loan(orderType=1, loanPrincipal=30000, loanTerm=3, fixedBillDay=21, fixedRepayDay=20)

        # 支用查询
        if flag == 3:
            fql_grt = FqlGrtBizImpl(data=data)
            fql_grt.loan_query()

        # 还款计划查询
        if flag == 4:
            fql_grt = FqlGrtBizImpl(data=data)
            fql_grt.repayPlan_query()

        # 还款试算
        if flag == 5:
            fql_grt = FqlGrtBizImpl(data=data)
            fql_grt.repay_trial()

        # 还款通知
        if flag == 6:
            fql_grt = FqlGrtBizImpl(data=data)
            # rpyType 10-正常还款 30-提前结清 40-逾期还款
            fql_grt.repay(rpyType=30)

        # 还款通知查询
        if flag == 7:
            fql_grt = FqlGrtBizImpl(data=data)
            fql_grt.repay_query()

        # 代扣申请
        if flag == 8:
            fql_grt = FqlGrtBizImpl(data=data)
            # rpyType 10-正常还款 30-提前结清 40-逾期还款
            fql_grt.withhold(rpyType=10)

        # 代扣查询
        if flag == 9:
            fql_grt = FqlGrtBizImpl(data=data)
            fql_grt.withhold_query()

        # 生成代偿文件
        if flag == 10:
            fql_grt = FqlGrtBizImpl(data=data)
            fql_grt.compensation(repay_date='2023-11-04')


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    log = MyLog().get_log()
    log.info('程序运行时间：{}'.format(round(total)))
