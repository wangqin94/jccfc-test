# -*- coding: utf-8 -*-
"""
test case script
"""
import os
import time
from multiprocessing import Process
from src.impl.juzi.JuZiBizImpl import JuZiBizImpl
if not os.path.exists('person.py'):
    open('person.py', 'w')
from src.test_case.juzi.person import data
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
            juzi = JuZiBizImpl(data=None)
            juzi.getCardRealNameMessage()

        # 确认绑卡
        elif flag == 1:
            juzi = JuZiBizImpl(data=data)
            juzi.bindCardRealName(tradeSerialNo='000DEF2024011000000093')

        # 协议共享
        if flag == 101:
            juzi = JuZiBizImpl(data=data)
            juzi.sharedWithholdingAgreement()

        # 确认绑卡
        elif flag == 99:
            juzi = JuZiBizImpl(data=data)
            res = juzi.getCardRealNameMessage(payerBankCardNum='6217851709103885570').get('body')
            juzi.bindCardRealName(userId=res['userId'], tradeSerialNo=res['tradeSerialNo'])

        # 绑卡查询
        elif flag == 2:
            juzi = JuZiBizImpl(data=data)
            juzi.queryWithholdingAgreement()

        # 授信
        elif flag == 3:
            juzi = JuZiBizImpl(data=data)
            juzi.credit(applyAmount=1000)

        # 授信查询
        elif flag == 4:
            juzi = JuZiBizImpl(data=data)
            juzi.queryCreditResult(thirdApplyId='YXH2024012214203100962708414')

        # 借款申请
        elif flag == 5:
            juzi = JuZiBizImpl(data=data)
            juzi.applyLoan(loanAmt=11000, loanTerm=6, thirdApplyId='thirdApplyId17091067497529264')

        # 借款查询
        elif flag == 6:
            juzi = JuZiBizImpl(data=data)
            juzi.queryLoanResult(thirdApplyId='thirdApplyId16928485803642059')

        # 还款计划查询
        elif flag == 7:
            juzi = JuZiBizImpl(data=data)
            juzi.repayPlan_query(loanInvoiceId='000LI0001177336437334182001')

        # 借据合同查询
        elif flag == 8:
            juzi = JuZiBizImpl(data=data)
            juzi.loanContract_query(loanInvoiceId='213')

        # 还款申请
        elif flag == 9:
            juzi = JuZiBizImpl(data=data)
            juzi.repay_apply(repay_scene='02', repay_type='2', loanInvoiceId="", repayDate="", paymentOrder='2022072222001425270501778318')

        # 还款查询
        elif flag == 10:
            juzi = JuZiBizImpl(data=data)
            juzi.repay_query(repayApplySerialNo='')

        # 附件补录
        elif flag == 11:
            juzi = JuZiBizImpl(data=data)
            juzi.supplementAttachment(thirdApplyId=None)

        # 省市区地址获取
        elif flag == 12:
            juzi = JuZiBizImpl(data=data)
            juzi.getAllAreaInfo()

        # LPR查询
        elif flag == 13:
            juzi = JuZiBizImpl(data=data)
            juzi.queryLprInfo("thirdApplyId16938109099508288")

        # 授信额度取消
        elif flag == 14:
            juzi = JuZiBizImpl(data=data)
            juzi.cancelCreditLine("thirdApplyId17053887503056410", reason="测是取消额度")

        # 代偿结果查询
        elif flag == 15:
            juzi = JuZiBizImpl(data=data)
            juzi.queryAccountResult(loanInvoiceId='000LI0001441081788467522174', term=2)

        # 结清证明申请
        elif flag == 16:
            juzi = JuZiBizImpl(data=data)
            juzi.applySettlementCer("thirdApplyId17061622981523740")

        # 结清证明下载
        elif flag == 17:
            juzi = JuZiBizImpl(data=data)
            juzi.settlementCerDownload("D0F63662C83048A0912537C2BF3F217C")

        # 还款计划试算
        elif flag == 18:
            juzi = JuZiBizImpl(data=data)
            juzi.repayPlanTrial(loanDate='2023-12-27')

        # 还款试算
        elif flag == 19:
            juzi = JuZiBizImpl(data=data)
            # repay_type： 还款类型 1 按期还款； 2 提前结清； 7 提前还当期
            juzi.repayTrial(loanInvoiceId='000LI0001730562584252754067', repayTerm='1', repayType='2', repayDate='2024-02-12')

        # 担保费同步
        elif flag == 20:
            juzi = JuZiBizImpl(data=data)
            juzi.syncGuaranteePlan(loanInvoiceId='000LI0001313126122804738015', flag="repay");

        # 代偿确认
        elif flag == 21:
            juzi = JuZiBizImpl(data=data)
            juzi.compensationConfirm(compensationNo="000DEF2024022700184445")

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
