# -*- coding: utf-8 -*-
"""
test case script
"""
import os
import time
from multiprocessing import Process
from src.impl.weicai.WeiCaiBizImpl import WeiCaiBizImpl
if not os.path.exists('person.py'):
    open('person.py', 'w')
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
    @staticmethod
    def process(flag=7):
        """ 测试步骤 """
        # 绑卡
        if flag == 0:
            wc = WeiCaiBizImpl(data=None)
            wc.sharedWithholdingAgreement()

        # 绑卡查询
        elif flag == 2:
            wc = WeiCaiBizImpl(data=data)
            wc.queryWithholdingAgreement()

        # 授信
        elif flag == 3:
            wc = WeiCaiBizImpl(data=None)
            wc.credit(applyAmount=10000)

        # 授信查询
        elif flag == 4:
            wc = WeiCaiBizImpl(data=data)
            wc.queryCreditResult(thirdApplyId='thirdApplyId16654556161833516')

        # 借款申请
        elif flag == 5:
            wc = WeiCaiBizImpl(data=data)
            wc.applyLoan(loanAmt=1000, loanTerm=6)

        # 借款查询
        elif flag == 6:
            wc = WeiCaiBizImpl(data=data)
            wc.queryLoanResult(thirdApplyId='thirdApplyId16928485803642059')

        # 还款计划查询
        elif flag == 7:
            wc = WeiCaiBizImpl(data=data)
            wc.repayPlan_query(loanInvoiceId='000LI0001861095229792369046')

        # 借据合同查询
        elif flag == 8:
            wc = WeiCaiBizImpl(data=data)
            wc.loanContract_query(loanInvoiceId='213')

        # 还款查询
        elif flag == 9:
            wc = WeiCaiBizImpl(data=data)
            wc.repay_query(repayApplySerialNo='')

        # 退货申请
        elif flag == 10:
            wc = WeiCaiBizImpl(data=data)
            wc.returnGoods_apply(loanInvoiceId='', term='', repayDate='')

        # 附件补录
        elif flag == 11:
            wc = WeiCaiBizImpl(data=data)
            wc.supplementAttachment(thirdApplyId=None)

        # 省市区地址获取
        elif flag == 12:
            wc = WeiCaiBizImpl(data=data)
            wc.getAllAreaInfo()

        # LPR查询
        elif flag == 13:
            wc = WeiCaiBizImpl(data=data)
            wc.queryLprInfo("thirdApplyId16781807201451053")

        # 授信额度取消
        elif flag == 14:
            wc = WeiCaiBizImpl(data=data)
            wc.cancelCreditLine("thirdApplyId16618478194785960")

        # 代偿结果查询
        elif flag == 15:
            wc = WeiCaiBizImpl(data=data)
            wc.queryAccountResult(loanInvoiceId='000LI0001408714913972228005', term=2)

        # 结清证明申请
        elif flag == 16:
            wc = WeiCaiBizImpl(data=data)
            wc.applySettlementCer("thirdApplyId16917188971617615")

        # 结清证明下载
        elif flag == 17:
            wc = WeiCaiBizImpl(data=data)
            wc.settlementCerDownload("488958292D324978AC873742067CC783")

        # 担保费同步
        elif flag == 18:
            wc = WeiCaiBizImpl(data=data)
            wc.syncGuaranteePlan(loanInvoiceId = "488958292D324978AC873742067CC783")

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
