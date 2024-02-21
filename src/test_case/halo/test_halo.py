# -*- coding: utf-8 -*-
"""
test case script
"""
import os
import time
from multiprocessing import Process
from src.impl.halo.HaLoBizImpl import HaLoBizImpl

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
    def process(flag=21):
        """ 测试步骤 """
        # 绑卡
        merchantId = 'G23E03HALO'
        if flag == 0:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.sharedWithholdingAgreement()

        # 绑卡查询
        elif flag == 2:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.queryWithholdingAgreement()

        # 授信
        elif flag == 3:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.credit(applyAmount=1000)

        # 授信查询
        elif flag == 4:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.queryCreditResult(thirdApplyId='thirdApplyId16654556161833516')

        # 借款申请
        elif flag == 5:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.applyLoan(loanAmt=20000, loanTerm=3)

        # 借款查询
        elif flag == 6:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.queryLoanResult(thirdApplyId='thirdApplyId1676441886237783')

        # 还款计划查询
        elif flag == 7:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.repayPlan_query(loanInvoiceId='000LI0001359580488327206022')

        # 借据合同查询
        elif flag == 8:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.loanContract_query(loanInvoiceId='213')

        # 还款查询
        elif flag == 9:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.repay_query(repayApplySerialNo='')

        # 退货申请
        elif flag == 10:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.returnGoods_apply(loanInvoiceId='', term='', repayDate='')

        # 附件补录
        elif flag == 11:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.supplementAttachment(thirdApplyId='')

        # 省市区地址获取
        elif flag == 12:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.getAllAreaInfo()

        # LPR查询
        elif flag == 13:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.queryLprInfo("thirdApplyId16781807201451053")

        # 授信额度取消
        elif flag == 14:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.cancelCreditLine("thirdApplyId16618478194785960")

        # 代偿结果查询
        elif flag == 15:
            HaLo = HaLoBizImpl(merchantId, data=data)
            # HaLo.queryAccountResult("GoodsSerialNo16624470361285455", loanInvoiceId='000LI0001739049438658571059', term=2)
            # HaLo.queryAccountResult("GoodsSerialNo16624470361285455", term=2)
            HaLo.queryAccountResult(loanInvoiceId='000LI0001408714913972228005', term=2)

        # 结清证明申请
        elif flag == 16:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.applySettlementCer("thirdApplyId16917188971617615")

        # 结清证明下载
        elif flag == 17:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.settlementCerDownload("488958292D324978AC873742067CC783")

        # H5还款订单查询
        elif flag == 18:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.queryRepaymentApply("488958292D324978AC873742067CC783")

        # 渠道线下还款申请
        elif flag == 19:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.offlineRepayApply(loanInvoiceId='000LI0002002451194721947024', repayType=2, repayTerm=1)

        # 还款试算
        elif flag == 20:
            HaLo = HaLoBizImpl(merchantId, data=data)
            HaLo.repayTrial(loanInvoiceId='000LI0002002451194722440007', repayType=2, repayTerm=1,
                            repayDate='2024-02-07')

        # 担保费同步
        elif flag == 21:
            HaLo = HaLoBizImpl(data=data)
            # flag: 同步阶段标识 loan-放款阶段（只可同步一次）、repay-还款阶段（提前还当期后，同步后续期次保费）
            HaLo.syncGuaranteePlan(loanInvoiceId="000LI0001195890696886561078", flag="repay", beginTerm=2,
                                   guaranteeAmt=1.58)

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
