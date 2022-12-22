# -*- coding: utf-8 -*-
"""
test case script
"""

import time
from src.impl.baidu.BaiDuBizImpl import BaiDuBizImpl
from person import *
from utils.Logger import MyLog
from src.impl.baidu.BaiDuSynBizImpl import BaiDuSynBizImpl


class TestCase(object):
    def __init__(self):
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 授信, 1: 授信查询, 2:支用申请, 3: 支用查询, 4: 授信失效 , 5:结清证明, 6:放款全流程]
    def process(self, flag=7):
        """ 测试步骤 """
        # 授信申请
        if flag == 0:
            bd = BaiDuBizImpl(data=None)
            bd.credit(initialAmount=3000000)

        # 授信查询
        elif flag == 1:
            bd = BaiDuBizImpl(data=data)
            bd.credit_query(credit_apply_id='Apply_Id16656292988401001')

        # 支用申请
        elif flag == 2:
            # repay_mode='02'随借随还，repay_mode='05'等额本息；
            bd = BaiDuBizImpl(data=data, repay_mode='02')
            bd.loan(cashAmount=100000, term=3)

        # 支用查询
        elif flag == 3:
            bd = BaiDuBizImpl(data=data)
            bd.loan_query(loan_apply_id='Loan_req16656293336541001')

        # 结清证明   0不需要返回base64 1需要  杜星
        elif flag == 5:
            bd = BaiDuBizImpl(data=data, encrypt_flag=False)
            bd.settlement(query_flag=1, username="仰敬胜")

        elif flag == 6:
            bd = BaiDuSynBizImpl(data=None, loanamount=1000000, month=3, loan_date='2022-11-21')
            bd.loan_flow()

        elif flag == 7:
            bd = BaiDuBizImpl(data=data)
            bd.notifyCloseLimit(idNo='')


        return self

    def postprocess(self):
        """ 后置条件处理 """
        pass


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    log = MyLog().get_log()
    log.info('程序运行时间：{}'.format(round(total)))
