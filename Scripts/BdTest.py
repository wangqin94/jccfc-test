# -*- coding: utf-8 -*-
"""
test case script
"""

import time
from Component.BaiDu import Component
from Scripts.person import *


class TestCase(object):
    def __init__(self):
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 授信, 1: 授信查询, 2:支用申请, 3: 支用查询, 4: 授信失效]
    def process(self, flag=2):
        """ 测试步骤 """
        # 授信申请
        if flag == 0:
            bd = Component(data=None)
            bd.credit(initialAmount=3000000)

        # 授信查询
        elif flag == 1:
            mt = Component(data=data)
            mt.credit_query()

        # 支用申请
        elif flag == 2:
            bd = Component(data=data)
            #bd.loan(cashAmount=60000, repayMode='32', dailyInterestRate='6.5', compreAnnualInterestRate='2234')
            bd.loan(cashAmount=60000, repayMode='22')

        # 支用查询
        elif flag == 3:
            mt = Component(data=data)
            mt.loan_query()

        return self

    def postprocess(self):
        """ 后置条件处理 """
        pass


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    print('程序运行时间：', total)
