# -*- coding: utf-8 -*-
"""
test case script
"""

import time
import threading
from src.impl.ctrip.CtripBizImpl import CtripBizImpl
from person import *
from utils.Logger import MyLog


class TestCase(object):
    def __init__(self):
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 授信, 1: 授信查询, 2:支用申请, 3: 支用查询, 4: 授信失效]
    def process(self, flag=0):
        """ 测试步骤 """
        # 授信申请
        if flag == 0:
            xc = CtripBizImpl(data=None)
            xc.credit(advice_amount=12000)

        if flag == 10:
            xc = CtripBizImpl(data=None)
            xc.pre_credit(advice_amount=12000)
            # time.sleep(2)
            # xc.credit(advice_amount=10000)

        # 授信查询
        elif flag == 1:
            xc = CtripBizImpl(data=data)
            xc.credit_query()

        # 支用申请
        elif flag == 2:
            xc = CtripBizImpl(data=data)
            xc.loan(loan_amount=600, first_repay_date="20210924121311")  # first_repay_date=首期还款时间

        # 支用查询
        elif flag == 3:
            xc = CtripBizImpl(data=data)
            xc.loan_query()

        # 还款通知
        elif flag == 4:
            # repay_mode=还款类型: 必填参数 :1按期还款；2提前结清；3逾期还款
            # finish_time=实际还款时间： 提前结清必填参数"20210806"
            xc = CtripBizImpl(data=data, repay_mode="1", repay_term_no="1", loan_invoice_id=None)
            xc.repay_notice()

        elif flag == 5:
            num = 1
            for i in range(0, num):
                xc = CtripBizImpl(data=None)
                xc.pre_credit(advice_amount=10000)
                xc.credit(advice_amount=10000)
                for n in range(10):
                    status = xc.credit_query()
                    if status == '03':
                        xc.loan(loan_amount=600, first_repay_date="20210725121311")
                        break
                    else:
                        time.sleep(5)
                        print("授信审批状态未通过，请等待....")

        return self

    def manythread(self):
        threads = []
        for x in range(5):  # 循环创建10个线程
            t = threading.Thread(target=self.process)
            threads.append(t)
        for t in threads:  # 循环启动10个线程
            t.start()

    def postprocess(self):
        """ 后置条件处理 """
        pass


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    log = MyLog.get_log()
    log.info('程序运行时间：'.format(total))
