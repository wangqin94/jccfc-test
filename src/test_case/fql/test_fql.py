# -*- coding: utf-8 -*-
"""
test case script
"""

import time
from src.impl.FQL.FqlBizImpl import FqlBizImpl
from person import *
from utils.Logger import MyLog
from utils.Models import get_next_month_today


class TestCase(object):
    def __init__(self):
        self.cur_time = str(get_next_month_today(1))
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 授信, 1: 授信查询, 2:支用申请, 3: 支用查询, 4: 授信失效]
    def process(self, flag=0):
        """ 测试步骤 """
        # 授信申请
        if flag == 0:
            fql = FqlBizImpl(data=None, credit_amount=2000)
            fql.credit(creditAmount=2000)

        # 授信查询
        elif flag == 1:
            fql = FqlBizImpl(data=data)
            fql.credit_query()

        # 支用申请
        elif flag == 2:
            fql = FqlBizImpl(data=data, loan_amount=600)
            # orderType: 订单类型 1取现；2赊销
            fql.loan(orderType=1, firstRepayDate=self.cur_time)

        # 支用查询
        elif flag == 3:
            fql = FqlBizImpl(data=data)
            fql.loan_query()

        return self

    def postprocess(self):
        """ 后置条件处理 """
        pass


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    log = MyLog.get_log()
    log.info('程序运行时间：'.format(total))
