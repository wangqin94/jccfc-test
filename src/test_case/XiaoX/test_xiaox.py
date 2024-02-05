# -*- coding: utf-8 -*-
"""
test case script
"""
import os

if not os.path.exists('person.py'):
    open('person.py', 'w')

import time
from multiprocessing import Process
from src.impl.XiaoX.XiaoXBizImpl import XiaoXBizImpl
from person import *
from utils.Logger import MyLog
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl


class TestCase(object):
    def __init__(self):
        self.process()
        # self.manythread()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 绑卡&短信验证, 1: 撞库, 2: 绑卡申请, 3: 授信]
    def process(self, flag=99, merchantId='G23E01XIAX'):
        """ 测试步骤 """
        # 绑卡
        if flag == 0:
            XiaoX = XiaoXBizImpl(merchantId, data=None)
            XiaoX.getCardRealNameMessage()

        # 确认绑卡
        elif flag == 1:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            XiaoX.bindCardRealName(tradeSerialNo='000DEF2023020700000022')

        # 确认绑卡
        elif flag == 99:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            res = XiaoX.getCardRealNameMessage().get('body')
            XiaoX.bindCardRealName(userId=res['userId'], tradeSerialNo=res['tradeSerialNo'])

        # 绑卡查询
        elif flag == 2:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            XiaoX.queryWithholdingAgreement()

        # 授信
        elif flag == 3:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            XiaoX.credit(applyAmount=1000, loanTerm=3)

        # 授信查询
        elif flag == 4:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            XiaoX.queryCreditResult(thirdApplyId='thirdApplyId16654556161833516')

        # 借款申请
        elif flag == 5:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            XiaoX.applyLoan(loanAmt=20000, loanTerm=3)

        # 借款查询
        elif flag == 6:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            XiaoX.queryLoanResult(thirdApplyId='thirdApplyId1676441886237783')

        # 还款计划查询
        elif flag == 7:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            XiaoX.repayPlan_query(loanInvoiceId='000LI0001359580488327206022')

        # 借据合同查询
        elif flag == 8:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            XiaoX.loanContract_query(loanInvoiceId='213')

        # 还款查询
        elif flag == 9:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            XiaoX.repay_query(repayApplySerialNo='')

        # 退货申请
        elif flag == 10:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            XiaoX.returnGoods_apply(loanInvoiceId='', term='', repayDate='')

        # 附件补录
        elif flag == 11:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            XiaoX.supplementAttachment(thirdApplyId='')

        # 省市区地址获取
        elif flag == 12:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            XiaoX.getAllAreaInfo()

        # LPR查询
        elif flag == 13:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            XiaoX.queryLprInfo("thirdApplyId16764287336017088")

        # 授信额度取消
        elif flag == 14:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            XiaoX.cancelCreditLine("thirdApplyId16618478194785960")

        # 代偿结果查询
        elif flag == 15:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            # XiaoX.queryAccountResult("GoodsSerialNo16624470361285455", loanInvoiceId='000LI0001739049438658571059', term=2)
            # XiaoX.queryAccountResult("GoodsSerialNo16624470361285455", term=2)
            XiaoX.queryAccountResult(loanInvoiceId='000LI0001408714913972228005', term=2)

        # 统一还款
        elif flag == 16:
            XiaoX = XiaoXBizImpl(merchantId, data=data)
            repayType = '02'
            if (repayType != '02'):
                XiaoX.repay_apply(loanInvoiceId='000LI0001900746367639750011', repay_scene=repayType, repay_type='1',
                                  repayTerm=None, repayGuaranteeFee=1.11, repayDate=None)
            else:
                i = 0
                while i < 5:
                    i += 1
                    XiaoX.repay_apply(loanInvoiceId='000LI0001900746367639750011', repay_scene=repayType,
                                      repay_type='1', repayTerm=None, repayGuaranteeFee=1.11, repayDate=None)
                    # 自动入账
                    self.repayPublicBizImpl = RepayPublicBizImpl()
                    self.repayPublicBizImpl.job.trigger_job("自动入账处理任务流", group=13)
                    time.sleep(3)

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
