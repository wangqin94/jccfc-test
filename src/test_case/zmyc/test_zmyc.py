# -*- coding: utf-8 -*-
"""
test case script
"""
import os
import time
from multiprocessing import Process
from src.impl.zmyc.ZMYCBizImpl import ZMYCBizImpl
if not os.path.exists('person.py'):
    open('person.py', 'w')
from src.test_case.zmyc.person import data
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
    def process(flag=101):
        """ 测试步骤 """
        # 绑卡
        if flag == 0:
            zmyc = ZMYCBizImpl(data=None)
            zmyc.getCardRealNameMessage()

        # 确认绑卡
        elif flag == 1:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.bindCardRealName(tradeSerialNo='000DEF2024011000000093')

        # 协议共享
        if flag == 101:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.sharedWithholdingAgreement()

        # 确认绑卡
        elif flag == 99:
            zmyc = ZMYCBizImpl(data=data)
            res = zmyc.getCardRealNameMessage(payerBankCardNum='6217851709103885570').get('body')
            zmyc.bindCardRealName(userId=res['userId'], tradeSerialNo=res['tradeSerialNo'])

        # 绑卡查询
        elif flag == 2:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.queryWithholdingAgreement()

        # 授信
        elif flag == 3:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.credit(applyAmount=1000)

        # 授信查询
        elif flag == 4:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.queryCreditResult(thirdApplyId='YXH2024012214203100962708414')

        # 借款申请
        elif flag == 5:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.applyLoan(loanAmt=11000, loanTerm=6, thirdApplyId='thirdApplyId17091067497529264')

        # 借款查询
        elif flag == 6:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.queryLoanResult(thirdApplyId='thirdApplyId16928485803642059')

        # 还款计划查询
        elif flag == 7:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.repayPlan_query(loanInvoiceId='000LI0001177336437334182001')

        # 借据合同查询
        elif flag == 8:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.loanContract_query(loanInvoiceId='213')

        # 还款申请
        elif flag == 9:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.repay_apply(repay_scene='02', repay_type='2', loanInvoiceId="", repayDate="", paymentOrder='2022072222001425270501778318')

        # 还款查询
        elif flag == 10:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.repay_query(repayApplySerialNo='')

        # 附件补录
        elif flag == 11:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.supplementAttachment(thirdApplyId=None)

        # 省市区地址获取
        elif flag == 12:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.getAllAreaInfo()

        # LPR查询
        elif flag == 13:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.queryLprInfo("thirdApplyId16938109099508288")

        # 授信额度取消
        elif flag == 14:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.cancelCreditLine("thirdApplyId17053887503056410", reason="测是取消额度")

        # 代偿结果查询
        elif flag == 15:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.queryAccountResult(loanInvoiceId='000LI0001441081788467522174', term=2)

        # 结清证明申请
        elif flag == 16:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.applySettlementCer("thirdApplyId17061622981523740")

        # 结清证明下载
        elif flag == 17:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.settlementCerDownload("D0F63662C83048A0912537C2BF3F217C")

        # 还款计划试算
        elif flag == 18:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.repayPlanTrial(loanDate='2023-12-27')

        # 还款试算
        elif flag == 19:
            zmyc = ZMYCBizImpl(data=data)
            # repay_type： 还款类型 1 按期还款； 2 提前结清； 7 提前还当期
            zmyc.repayTrial(loanInvoiceId='000LI0001730562584252754067', repayTerm='1', repayType='2', repayDate='2024-02-12')

        # 担保费同步
        elif flag == 20:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.syncGuaranteePlan(loanInvoiceId='000LI0001313126122804738015', flag="repay");

        # 代偿确认
        elif flag == 21:
            zmyc = ZMYCBizImpl(data=data)
            zmyc.compensationConfirm(compensationNo="000DEF2024022700184445")

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
