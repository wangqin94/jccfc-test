# -*- coding: utf-8 -*-
"""
test case script
"""
import os

from src.enums.EnumsCommon import ProductIdEnum

if not os.path.exists('person.py'):
    open('person.py', 'w')

import time
from multiprocessing import Process
from src.impl.hair.HairBizImpl import HairBizImpl
from person import *
from utils.Logger import MyLog


class TestCase(object):
    def __init__(self):
        self.process()
        # self.manythread()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    @staticmethod
    def process(flag=5, productId=ProductIdEnum.HAIR_DISCOUNT.value):
        """
        @param flag: 标签
        @param productId: 默认贴息产品号（主产品号）：G23E041， 否则非贴息产品号（子产品号）：G23E042
        @return:
        """
        # 绑卡
        if flag == 0:
            hair = HairBizImpl(productId, data=None)
            # hair.getCardRealNameMessage()
            hair.getCardRealNameMessage()

        # 确认绑卡
        elif flag == 1:
            hair = HairBizImpl(productId, data=data)
            hair.bindCardRealName(tradeSerialNo='000DEF2023020700000022')

        # 确认绑卡
        elif flag == 99:
            hair = HairBizImpl(productId, data=data)
            res = hair.getCardRealNameMessage(payerBankCardNum='6216701676429127322').get('body')
            hair.bindCardRealName(userId=res['userId'], tradeSerialNo=res['tradeSerialNo'])

        # 绑卡查询
        elif flag == 2:
            hair = HairBizImpl(productId, data=data)
            hair.queryWithholdingAgreement()

        # 授信
        elif flag == 3:
            hair = HairBizImpl(productId, data=data)
            # hair.sharedWithholdingAgreement(mobileNo=None)
            hair.credit(applyAmount=1000)

        # 授信查询
        elif flag == 4:
            hair = HairBizImpl(productId, data=data)
            hair.queryCreditResult(thirdApplyId='thirdApplyId16824023942629508')

        # 借款申请
        elif flag == 5:
            hair = HairBizImpl(productId, data=data)
            hair.applyLoan(loanAmt=1000, loanTerm=12)

        # 借款查询
        elif flag == 6:
            hair = HairBizImpl(productId, data=data)
            hair.queryLoanResult(thirdApplyId='202210131431422562436865')

        # 还款计划查询
        elif flag == 7:
            hair = HairBizImpl(productId, data=data)
            hair.repayPlan_query(loanInvoiceId='000LI0002174662201688190001')

        # 借据合同查询
        elif flag == 8:
            hair = HairBizImpl(productId, data=data)
            hair.loanContract_query(loanInvoiceId='000LI0001408714913972228005')

        # 还款查询
        elif flag == 9:
            hair = HairBizImpl(productId, data=data)
            hair.repay_query(repayApplySerialNo='')

        # 退货申请
        elif flag == 10:
            hair = HairBizImpl(productId, data=data)
            hair.returnGoods_apply(loanInvoiceId='', term='', repayDate='')

        # 附件补录
        elif flag == 11:
            hair = HairBizImpl(productId, data=data)
            hair.supplementAttachment(thirdApplyId='')

        # 省市区地址获取
        elif flag == 12:
            hair = HairBizImpl(productId, data=data)
            hair.getAllAreaInfo()

        # LPR查询
        elif flag == 13:
            hair = HairBizImpl(productId, data=data)
            hair.queryLprInfo("thirdApplyId16708148970374646")

        # 授信额度取消
        elif flag == 14:
            hair = HairBizImpl(productId, data=data)
            hair.cancelCreditLine("thirdApplyId16618478194785960")

        # 代偿结果查询
        elif flag == 15:
            hair = HairBizImpl(productId, data=data)
            # hair.queryAccountResult("GoodsSerialNo16624470361285455", loanInvoiceId='000LI0001739049438658571059', term=2)
            # hair.queryAccountResult("GoodsSerialNo16624470361285455", term=2)
            hair.queryAccountResult(loanInvoiceId='000LI0001408714913972228005', term=2)

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
