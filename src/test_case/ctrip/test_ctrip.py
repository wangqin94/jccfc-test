# -*- coding: utf-8 -*-
"""
test case script
"""

import time
import threading
from src.impl.ctrip.CtripBizImpl import CtripBizImpl
from utils.Logger import MyLog
from person import *


class TestCase(object):
    def __init__(self):
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 授信, 1: 授信查询, 2:支用申请, 3: 支用查询, 4: 还款通知]
    def process(self, flag=0):
        """ 测试步骤 """
        # 授信申请
        if flag == 0:
            xc = CtripBizImpl(data=None)
            xc.credit(advice_amount=30000)
            xc.update_apollo_amount()

        # 授信查询
        elif flag == 1:
            xc = CtripBizImpl(data=data)
            xc.credit_query()

        # 支用申请
        elif flag == 2:
            xc = CtripBizImpl(data=data)
            xc.loan(loan_amount=600, term=6, first_repay_date="20230325000000")  # first_repay_date=首期还款时间

        # 支用查询
        elif flag == 3:
            xc = CtripBizImpl(data=data)
            xc.loan_query()

        # 还款通知
        elif flag == 4:
            # repay_mode=还款类型: 必填参数 :1按期还款；2提前结清；3逾期还款
            # finish_time=实际还款时间： 提前结清必填参数"20210806"
            xc = CtripBizImpl(data=data, loan_invoice_id='000LI0001845942584803328036')
            xc.repay_notice(repay_mode="2", repay_term_no="2", repay_date='2022-09-10')

        elif flag == 5:
            num = 1
            for i in range(0, num):
                xc = CtripBizImpl(data=None)
                xc.credit(advice_amount=30000)
                for n in range(10):
                    status = xc.MysqlBizImpl.credit_query()
                    if status == '03':
                        xc.loan(loan_amount=1200, first_repay_date="20220821112233")
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
    log = MyLog().get_log()
    log.info('程序运行时间：{}'.format(round(total)))
