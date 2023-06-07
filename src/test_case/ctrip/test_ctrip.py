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
            xc = CtripBizImpl(data=data)
            xc.credit(advice_amount=10000)
            xc.update_apollo_amount()

        # 授信查询
        elif flag == 1:
            xc = CtripBizImpl(data=data)
            xc.credit_query()

        # 支用申请
        elif flag == 2:
            xc = CtripBizImpl(data=data)
            # loan_date: 放款日期，不传默认当天
            # first_repay_date:  首期还款日
            xc.loan(loan_amount=1000, term=6, first_repay_date="20230525000000", loan_date='20230425')

        # 支用查询
        elif flag == 3:
            xc = CtripBizImpl(data=data)
            xc.loan_query(loan_request_no='request_no16801470629123', partner_loan_no='360829200102088969')

        # 还款通知
        elif flag == 4:
            # repay_mode=还款类型: 必填参数 :1按期还款；2提前结清；3逾期还款
            # finish_time=实际还款时间： 提前结清必填参数"20210806"
            xc = CtripBizImpl(data=data, loan_invoice_id='000LI0001235163876319233008')
            xc.repay_notice(repay_mode="3", repay_term_no="1", repay_date='2023-05-10')

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
