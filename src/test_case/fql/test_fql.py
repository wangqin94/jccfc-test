# -*- coding: utf-8 -*-
"""
test case script
"""
import logging
import time

from src.impl.FQL.FqlBizImpl import FqlBizImpl
from person import *
from utils.Logger import MyLog
from utils.Models import *

log = logging.getLogger(__name__)

class TestCase(object):
    def __init__(self):
        self.cur_time = str(get_next_month_today(1))
        # self.perm(['a','e','i','o','u'])
        self.process()


    # def perm(self,li):
    #     if len(li) == 1:
    #         return [li]
    #     r_list = []
    #     for i in range(len(li)):
    #         n_list = li[:i] + li[i+1:]
    #         result = self.perm(n_list)
    #         for j in result:
    #             r_list.append(li[i:i+1] + j)
    #     print(r_list)
    #     return r_list


    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 授信, 1: 授信查询, 2:支用申请, 3: 支用查询, 4: 授信失效]
    def process(self, flag=0):
        """ 测试步骤 """
        # 授信申请
        if flag == 0:
            fql = FqlBizImpl(data=None)
            fql.credit(creditAmount=1000, loanAmount=1000, loanTerm=3)

        # 授信查询
        elif flag == 1:
            fql = FqlBizImpl(data=data)
            fql.credit_query()

        # 支用申请
        elif flag == 2:
            fql = FqlBizImpl(data=data)
            # orderType: 订单类型 1取现；2赊销
            fql.loan(loanTerm=3, loanAmt=600, orderType=1, firstRepayDate=self.cur_time)

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
    log = MyLog().get_log()
    log.info('程序运行时间：'.format(round(total)))
