# -*- coding: utf-8 -*-
"""
test case script
"""
import logging
import time

from src.impl.FQL.FqlBizImpl import FqlBizImpl
from person import *
from threading import Thread
from multiprocessing import Process
from src.impl.common.CheckBizImpl import *
log = logging.getLogger(__name__)

class TestCase(object):
    def __init__(self):
        self.cur_time = str(get_next_month_today(1))
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 授信, 1: 授信查询, 2:支用申请, 3: 支用查询, 4: 授信失效]
    def process(self, flag=8):
        """ 测试步骤 """
        # 授信申请
        if flag == 0:
            fql = FqlBizImpl(data=None)
            fql.credit(creditAmount=10000, loanAmount=10000, loanTerm=6, interestRate='24')

        # 授信查询
        elif flag == 1:
            fql = FqlBizImpl(data=data)
            fql.credit_query()

        # 支用申请
        elif flag == 2:
            fql = FqlBizImpl(data=data)
            # orderType: 订单类型 1取现；2赊销
            fql.loan(loanTerm=6, loanAmt=10000, orderType=2, firstRepayDate='2022-12-07', interestRate='24')

        # 支用查询
        elif flag == 3:
            fql = FqlBizImpl(data=data)
            fql.loan_query()

            # 还款试算
        elif flag == 5:
            fql = FqlBizImpl(data=data)
            # loanno: 锦程放款成功的借据申请号
            # loanterm: 还款期数
            # repaytype : 还款类别 10:按期（正常）还款 30:全部提前结清 40:逾期还款
            fql.repay_trial(loanno='000LI0001909130144309301082', loanterm='2', repaytype='30', rpyDate='2022-12-07')

        # 代扣申请
        elif flag == 6:
            fql = FqlBizImpl(data=data)
            # withholdAmt: 代扣总金额
            # rpyPrincipal: 实还本金，rpyFeeAmt: 实还利息，rpyMuclt: 实还罚息
            # rpyType: 10-正常还款,30-提前结清,40-逾期还款
            # rpyTerm: 还款期次
            # signNum: 签约协议号
            # capitalLoanNo: 借据号
            fql.payment(withholdAmt=348.07, rpyPrincipal=326.75, rpyFeeAmt=20.01, rpyMuclt=1.31,
                        signNum='S00202211090002', capitalLoanNo='000LI0001909130144309300085', rpyTerm='1',
                        rpyType='40', rpyDate='2022-12-07')

        # 代扣查询
        elif flag == 7:
            fql = FqlBizImpl(data=data)
            # withholadSerialNo: 代扣请求流水号
            fql.payment_query(withholadSerialNo='wsn1667526658605')

        # 上传文件
        elif flag == 8:
            wld = FqlBizImpl(data=None)
            resp = wld.fql_file_upload('/pw', 'C:\\Users\\jccfc\\Desktop\\1.jpg')
            wld.fql_file_upload_result(resp['seqNo'])

        # 下载文件
        elif flag == 9:
            fql = FqlBizImpl(data=None)
            resp = fql.fql_file_download('/pl/JC_payment_20220926.txt', 'C:\\Users\\jccfc\\Desktop\\JC_payment_20220926.txt')
            fql.fql_file_upload_result(resp['seqNo'])

        elif flag == 10:
            fql = FqlBizImpl(data=None, person=False)
            # 发起授信申请
            applyId = fql.credit(creditAmount=10000, loanAmount=10000, loanTerm=6, interestRate='23')['applyId']
            creditQueryRes = fql.credit_query()
            auditState = creditQueryRes['auditState']
            while auditState != '0':
                time.sleep(10)
                creditQueryRes = fql.credit_query()
                auditState = creditQueryRes['auditState']
            # 发起支用申请
            # orderType: 订单类型 1取现；2赊销
            fql.loan(orderType=1, loanTerm=6, loanAmt=10000, firstRepayDate='2022-12-09', interestRate='23')

        return self

    def postprocess(self):
        """ 后置条件处理 """
        pass

    def manythread(self):
        threads = []
        for x in range(100):  # 循环创建10个线程
            t = Thread(target=self.process())
            # t = Process(target=self.process())
            threads.append(t)
        for t in threads:  # 循环启动10个线程
            t.start()
if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    log = MyLog().get_log()
    log.info('程序运行时间：'.format(round(total)))
    # TestCase().manythread()
