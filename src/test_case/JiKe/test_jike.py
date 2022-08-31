# -*- coding: utf-8 -*-
"""
test case script
"""
import os
if not os.path.exists('person.py'):
    open('person.py', 'w')

import time
from multiprocessing import Process
from src.impl.JiKe.JiKeBizImpl import JiKeBizImpl
from person import *
from utils.Logger import MyLog


class TestCase(object):
    def __init__(self):
        self.process()
        # self.manythread()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 绑卡&短信验证, 1: 撞库, 2: 绑卡申请, 3: 授信]
    def process(self, flag=14):
        """ 测试步骤 """
        # 绑卡
        if flag == 0:
            jike = JiKeBizImpl(data=data)
            jike.sharedWithholdingAgreement()

        # 绑卡查询
        elif flag == 1:
            jike = JiKeBizImpl(data=data)
            jike.queryWithholdingAgreement()

        # 换卡申请
        elif flag == 2:
            jike = JiKeBizImpl(data=data)
            jike.updateWithholdCard('000LI0001256947949691194004')

        # 授信
        elif flag == 3:
            jike = JiKeBizImpl(data=None)
            jike.sharedWithholdingAgreement()
            jike.credit(applyAmount=1000)

        # 授信查询
        elif flag == 4:
            jike = JiKeBizImpl(data=data)
            jike.queryCreditResult(thirdApplyId='thirdApplyId166063196668864111')

        # 借款申请
        elif flag == 5:
            jike = JiKeBizImpl(data=data)
            jike.applyLoan(loanAmt=1000, term=12)

        # 借款查询
        elif flag == 6:
            jike = JiKeBizImpl(data=data)
            jike.queryLoanResult(thirdApplyId='')

        # 还款计划查询
        elif flag == 7:
            jike = JiKeBizImpl(data=data)
            jike.repayPlan_query(loanInvoiceId='')

        # 借据合同查询
        elif flag == 8:
            jike = JiKeBizImpl(data=data)
            jike.loanContract_query(loanInvoiceId='')

        # 还款查询
        elif flag == 9:
            jike = JiKeBizImpl(data=data)
            jike.repay_query(repayApplySerialNo='')

        # 退货申请
        elif flag == 10:
            jike = JiKeBizImpl(data=data)
            jike.returnGoods_apply(loanInvoiceId='')

        # 附件补录
        elif flag == 11:
            jike = JiKeBizImpl(data=data)
            jike.supplementAttachment(thirdApplyId='thirdApplyId16617429251224753')

        # 省市区地址获取
        elif flag == 12:
            jike = JiKeBizImpl(data=data)
            jike.getAllAreaInfo()

        # LPR查询
        elif flag == 13:
            jike = JiKeBizImpl(data=data)
            jike.queryLprInfo("thirdApplyId16617429251224753")

        # 授信额度取消
        elif flag == 14:
            jike = JiKeBizImpl(data=data)
            jike.cancelCreditLine("thirdApplyId16618505481928376")

    def postprocess(self):
        """ 后置条件处理 """
        pass

    def manythread(self):
        threads = []
        for x in range(10):  # 循环创建10个线程
            t = Process(target=self.process)
            threads.append(t)
        for t in threads:  # 循环启动10个线程
            t.start()


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    log = MyLog().get_log()
    log.info('程序运行时间：{}'.format(round(total)))
