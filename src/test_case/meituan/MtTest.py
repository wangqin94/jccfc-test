# -*- coding: utf-8 -*-
"""
test case script
"""

import time
from src.impl.MeiTuan.MeiTuanBizImpl import MeiTuanBizImpl
from person import *
from utils.Logger import MyLog


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
                mt = MeiTuanBizImpl(data=None)
                mt.credit(APPLY_AMT=1000000)
                # mt.mt_credit_result()

            # 授信查询
            elif flag == 1:
                mt = MeiTuanBizImpl(data=data)
                mt.credit_query()
                pass

            # 放款
            elif flag == 2:
                mt = MeiTuanBizImpl(data=data)
                mt.loan(TRADE_AMOUNT=60000, TRADE_PERIOD='6')

            # 支用查询
            elif flag == 3:
                mt = MeiTuanBizImpl(data=data)
                mt.loan_query(app_no='MTAPP_NO16312605132121002')

    def postprocess(self):
        """后置条件处理"""
        pass


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    log = MyLog.get_log()
    log.info('程序运行时间：'.format(total))
