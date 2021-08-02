# -*- coding: utf-8 -*-
"""
test case script
"""

import threading
import time
from Component.MeiTuan import Component
from person import *


class TestCase(object):
    def __init__(self):
        # threads = []
        # for x in range(5):  # 循环创建N个线程
        #     t1 = threading.Thread(target=self.process)
        #     threads.append(t1)
        # for t in threads:  # 循环启动N个线程
        #     t.start()
        self.process()

    def preprocess(self):
        """预置条件处理"""
        pass

    #   [0: 授信, 1: 授信查询, 2:支用申请, 3: 支用查询, 4: 授信失效]
    def process(self, flag=0):
        """测试步骤"""
        m = 1
        for _ in range(m):

            if flag == 0:
                mt = Component(data=None)

                mt.mt_credit_msg(APPLY_AMT=1000000)
                mt.mt_credit_test()
                # mt.mt_credit_result()

            # 授信查询
            elif flag == 1:
                mt = Component(data=data)
                mt.get_user_credit_apply_info()
                mt.mt_credit_query_msg()
                print(mt.credit_query_payload)
                mt.mt_credit_query_test()
                pass

            # 放款
            elif flag == 2:
                mt = Component(data=data)
                mt.get_user_credit_apply_info()
                print(mt.user_credit_apply_info)
                mt.update_bank_contract_no()
                mt.update_credit_app_no()
                # # mt.get_user_apply_info()
                # # mt.mt_credit_result()
                mt.mt_loan_msg(TRADE_AMOUNT=60000, TRADE_PERIOD='3')
                mt.mt_loan_test()
            #     threads = []
            #     for _ in range(5):
            #         mt.mt_loan_msg()
            #         # mt.mt_loan_test()
            # # print(mt.user_credit_apply_info)
            #         t1 = threading.Thread(target=mt.mt_loan_test())
            #         threads.append(t1)
            #         time.sleep(1)
            #     for t in threads:  # 循环启动N个线程
            #         t.start()

            # 支用查询
            elif flag == 3:
                mt = Component(data=data)
                mt.get_user_loan_apply_info(data['cer_no'])
                mt.mt_loan_query_msg()
                mt.mt_loan_query_test()

            elif flag == 4:
                mt = Component(data=data)
                mt.mt_credit_invalid_msg()
                mt.mt_credit_invalid_test()

    def postprocess(self):
        """后置条件处理"""
        pass


if __name__ == '__main__':
    start_time = time.time()
    nowdate = time.strftime('%Y%m%d%H%M%S')
    start = TestCase()
    print('主线程开始时间', nowdate)
