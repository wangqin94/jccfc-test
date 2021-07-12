# -*- coding: utf-8 -*-
"""
test case script
"""

import time
from Component.XieCheng import Component
from person import *

class TestCase(object):
    def __init__(self):
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 授信, 1: 授信查询, 2:支用申请, 3: 支用查询, 4: 授信失效]
    def process(self, flag=4):
        """ 测试步骤 """
        # 授信申请
        if flag == 0:
            xc = Component(data=None)
            xc.pre_credit(advice_amount=10000)
            time.sleep(5)
            xc.credit(advice_amount=10000)

        if flag == 11:
            xc = Component(data=data)
            xc.credit(advice_amount=10000)

        # 授信查询
        elif flag == 1:
            xc = Component(data=data)
            xc.credit_query()

        # 支用申请
        elif flag == 2:
            xc = Component(data=data)
            xc.loan(loan_amount=600, first_repay_date="20210806121311")  # first_repay_date=首期还款时间

        # 支用查询
        elif flag == 3:
            xc = Component(data=data)
            xc.loan_query()

        # 还款通知
        elif flag == 4:
            xc = Component(data=data, repay_term_no="1")
            # 提前结清
            repay_detail = {
                "repay_principal": 600,
                "repay_interest": 0.60,
                "repay_penalty_amount": 0,
                "actual_repay_amount": 600.600,
                "repay_fee": 0
            }
            # xc.notice(repay_type="2", repay_detail=repay_detail, finish_time="20210609111213")  # finish_time=实际还款时间
            # 按期还款
            xc.notice(repay_term_no="1", finish_time="20210806121311")  # finish_time=实际还款时间

        return self

    def postprocess(self):
        """ 后置条件处理 """
        pass


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    print('程序运行时间：', total)
