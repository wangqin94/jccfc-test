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
    def process(self, flag=16):
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
            jike = JiKeBizImpl(data=data)
            jike.sharedWithholdingAgreement(liveAddress=None)
            jike.credit(applyAmount=1000)

        # 授信查询
        elif flag == 4:
            jike = JiKeBizImpl(data=data)
            jike.queryCreditResult(thirdApplyId='thirdApplyId17017651015432692')

        # 借款申请
        elif flag == 5:
            jike = JiKeBizImpl(data=data)
            jike.applyLoan(loanAmt=1000, loanTerm=12, thirdApplyId='thirdApplyId16661464674479646')

        # 借款查询
        elif flag == 6:
            jike = JiKeBizImpl(data=data)
            jike.queryLoanResult(thirdApplyId='202210131431422562436865')

        # 还款计划查询
        elif flag == 7:
            jike = JiKeBizImpl(data=data)
            jike.repayPlan_query(loanInvoiceId='000LI0002174662201688190001')

        # 借据合同查询
        elif flag == 8:
            jike = JiKeBizImpl(data=data)
            jike.loanContract_query(loanInvoiceId='000LI0001408714913972228005')

        # 还款查询
        elif flag == 9:
            jike = JiKeBizImpl(data=data)
            jike.repay_query(repayApplySerialNo='')

        # 退货申请
        elif flag == 10:
            jike = JiKeBizImpl(data=data)
            jike.returnGoods_apply(loanInvoiceId='', term='', repayDate='')

        # 附件补录
        elif flag == 11:
            jike = JiKeBizImpl(data=data)
            jike.supplementAttachment(thirdApplyId='thirdApplyId16669445241678573')

        # 省市区地址获取
        elif flag == 12:
            jike = JiKeBizImpl(data=data)
            jike.getAllAreaInfo()

        # LPR查询
        elif flag == 13:
            jike = JiKeBizImpl(data=data)
            jike.queryLprInfo("thirdApplyId16660821110787033")

        # 授信额度取消
        elif flag == 14:
            jike = JiKeBizImpl(data=data)
            jike.cancelCreditLine("thirdApplyId16618478194785960")

        # 代偿结果查询
        elif flag == 15:
            jike = JiKeBizImpl(data=data)
            # jike.queryAccountResult("GoodsSerialNo16624470361285455", loanInvoiceId='000LI0001739049438658571059', term=2)
            # jike.queryAccountResult("GoodsSerialNo16624470361285455", term=2)
            jike.queryAccountResult(loanInvoiceId='000LI0001408714913972228005', term=2)

        # 担保费同步
        elif flag == 16:
            jike = JiKeBizImpl(data=data)
            # flag: 同步阶段标识 loan-放款阶段（只可同步一次）、repay-还款阶段（提前还当期后，同步后续期次保费）
            jike.syncGuaranteePlan(loanInvoiceId="000LI0002281692788867167020", flag="repay", beginTerm=2, guaranteeAmt=0.02)

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
