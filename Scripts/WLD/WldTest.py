# -*- coding: utf-8 -*-
"""
test case script
"""

import time
from Component.wld import Component
from person import *


class TestCase(object):
    def __init__(self):
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 绑卡, 3: 授信, 5: 支用, 6: 还款, 7: 绑卡&授信&支用]
    def process(self, flag=7):
        """ 测试步骤 """
        # 绑卡
        if flag == 0:
            wld = Component(data=data)
            wld.bind_card()
            wld.confirm_bind_card()

        # 绑卡查询
        elif flag == 1:
            wld = Component(data=data)
            wld.query_bind_card()

        # 换卡
        elif flag == 2:
            wld = Component(data=data)
            wld.update_card()

        # 授信
        elif flag == 3:
            wld = Component(data=data)
            wld.credit(loanTerm=3, applyAmount=1000)

        # 授信查询
        elif flag == 4:
            wld = Component(data=data)
            wld.credit_query()

        # 放款
        elif flag == 5:
            wld = Component(data=data)
            wld.loan()

        # 支用查询
        elif flag == 5:
            wld = Component(data=data)
            wld.loan_query()

        # 还款  repay_term_no还款期次   repay_type还款类型：1-按期还款，2-提前结清，4-逾期还款
        elif flag == 6:
            wld = Component(repay_term_no="1", repay_type="2", loan_invoice_id="000LI5674979767597940738332")
            wld.repay()

        # 批量造数
        elif flag == 7:
            for i in range(1):
                wld = Component(data=None)
                wld.bind_card()
                wld.confirm_bind_card()
                wld.credit(loanTerm=6, applyAmount=5000)
                for n in range(10):
                    status = wld.creditdata_query()
                    if status == '03':
                        wld.loan()
                        break
                    else:
                        time.sleep(5)
                        print("授信审批状态未通过，请等待....")

        return self

    def postprocess(self):
        """ 后置条件处理 """
        pass


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    print('程序运行时间：', total)
