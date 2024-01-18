# -*- coding: utf-8 -*-
"""
test case script
"""
import os
import time
from multiprocessing import Process
from src.impl.yixin.YiXinBizImpl import YiXinBizImpl
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
    def process(flag=3):
        """ 测试步骤 """
        # 绑卡
        if flag == 0:
            yixin = YiXinBizImpl(data=data)
            yixin.getCardRealNameMessage()

        # 确认绑卡
        elif flag == 1:
            yixin = YiXinBizImpl(data=data)
            yixin.bindCardRealName(tradeSerialNo='000DEF2023020700000022')

        # 确认绑卡
        elif flag == 99:
            yixin = YiXinBizImpl(data=data)
            res = yixin.getCardRealNameMessage(payerBankCardNum='6216701676429127322').get('body')
            yixin.bindCardRealName(userId=res['userId'], tradeSerialNo=res['tradeSerialNo'])

        # 绑卡查询
        elif flag == 2:
            yixin = YiXinBizImpl(data=data)
            yixin.queryWithholdingAgreement()

        # 授信
        elif flag == 3:
            yixin = YiXinBizImpl(data=data)
            yixin.credit(applyAmount=1000)

        # 授信查询
        elif flag == 4:
            yixin = YiXinBizImpl(data=data)
            yixin.queryCreditResult(thirdApplyId='thirdApplyId16654556161833516')

        # 借款申请
        elif flag == 5:
            yixin = YiXinBizImpl(data=data)
            yixin.applyLoan(loanAmt=15000, loanTerm=12, thirdApplyId='thirdApplyId16938966556343764')

        # 借款查询
        elif flag == 6:
            yixin = YiXinBizImpl(data=data)
            yixin.queryLoanResult(thirdApplyId='thirdApplyId16928485803642059')

        # 还款计划查询
        elif flag == 7:
            yixin = YiXinBizImpl(data=data)
            yixin.repayPlan_query(loanInvoiceId='000LI0001177336437334182001')

        # 借据合同查询
        elif flag == 8:
            yixin = YiXinBizImpl(data=data)
            yixin.loanContract_query(loanInvoiceId='213')

        # 还款申请
        elif flag == 9:
            yixin = YiXinBizImpl(data=data)
            yixin.repay_apply(repay_scene='02', repay_type='2', loanInvoiceId="", repayDate="", paymentOrder='2022072222001425270501778318')

        # 还款查询
        elif flag == 10:
            yixin = YiXinBizImpl(data=data)
            yixin.repay_query(repayApplySerialNo='')

        # 附件补录
        elif flag == 11:
            yixin = YiXinBizImpl(data=data)
            yixin.supplementAttachment(thirdApplyId=None)

        # 省市区地址获取
        elif flag == 12:
            yixin = YiXinBizImpl(data=data)
            yixin.getAllAreaInfo()

        # LPR查询
        elif flag == 13:
            yixin = YiXinBizImpl(data=data)
            yixin.queryLprInfo("thirdApplyId16938109099508288")

        # 授信额度取消
        elif flag == 14:
            yixin = YiXinBizImpl(data=data)
            yixin.cancelCreditLine("thirdApplyId16618478194785960")

        # 代偿结果查询
        elif flag == 15:
            yixin = YiXinBizImpl(data=data)
            yixin.queryAccountResult(loanInvoiceId='000LI0001408714913972228005', term=2)

        # 结清证明申请
        elif flag == 16:
            yixin = YiXinBizImpl(data=data)
            yixin.applySettlementCer("thirdApplyId16917188971617615")

        # 结清证明下载
        elif flag == 17:
            yixin = YiXinBizImpl(data=data)
            yixin.settlementCerDownload("488958292D324978AC873742067CC783")

        # 还款计划试算
        elif flag == 18:
            yixin = YiXinBizImpl(data=data)
            yixin.repayPlanTrial(loanDate=None)

        # 还款试算
        elif flag == 19:
            yixin = YiXinBizImpl(data=data)
            yixin.repayTrial(loanInvoiceId='', repayTerm='', repayType='', repayDate=None)

        # 担保费同步
        elif flag == 20:
            yixin = YiXinBizImpl(data=data)
            # flag: 同步阶段标识 loan-放款阶段（只可同步一次）、repay-还款阶段（提前还当期后，同步后续期次保费）
            yixin.syncGuaranteePlan(loanInvoiceId="000LI0002281692788867167020", flag="repay", beginTerm=2, guaranteeAmt=0.02)

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
