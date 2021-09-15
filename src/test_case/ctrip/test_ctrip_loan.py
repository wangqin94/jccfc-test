# -*- coding: utf-8 -*-
"""
test case script
"""

import threading

from src.impl.ctrip.CtripBizImpl import CtripBizImpl
from src.impl.common.CommonCheckBizImpl import *
# from person import *
from utils.Models import *

CheckBizImpl = CheckBizImpl()


class TestCase(object):
    def __init__(self):
        self.cur_time = str(get_next_month_today(1)).replace("-", '') + time.strftime('%H%M%S')
        self.process()

    def process(self):
        """ 测试步骤 """
        ctrip = CtripBizImpl(data=None)

        # 发起授信申请
        open_id = ctrip.credit(advice_amount=10000)['open_id']
        # 检查授信状态
        time.sleep(10)
        CheckBizImpl.check_credit_apply_status(thirdpart_user_id=open_id)
        # 发起支用刚申请
        ctrip.loan(loan_amount=600, first_repay_date=self.cur_time)
        # 检查支用状态
        time.sleep(5)
        CheckBizImpl.check_loan_apply_status(thirdpart_user_id=open_id)

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
    print('程序运行时间：', round(total))
