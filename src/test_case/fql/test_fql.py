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
    def process(self, flag=0):
        """ 测试步骤 """
        # 授信申请
        if flag == 0:
            fql = FqlBizImpl(data=None)
            fql.credit(creditAmount=10000, loanAmount=10000, loanTerm=6, interestRate='23')

        # 授信查询
        elif flag == 1:
            fql = FqlBizImpl(data=data)
            fql.credit_query(applyId='applyId1646985456136')

        # 支用申请
        elif flag == 2:
            fql = FqlBizImpl(data=data)
            # orderType: 订单类型 1取现；2赊销
            # loan_date: 放款日期，不传默认当天
            fql.loan(loanTerm=6, loanAmt=10000, orderType=1, firstRepayDate='2023-05-01',
                     interestRate='23', loan_date='2023-04-01')

        # 支用查询
        elif flag == 3:
            fql = FqlBizImpl(data=data)
            fql.loan_query(applyId='applyId1646985456136')

            # 还款试算
        elif flag == 5:
            fql = FqlBizImpl(data=data)
            # loanno: 锦程放款成功的借据申请号
            # loanterm: 还款期数
            # repaytype : 还款类别 10:按期（正常）还款 30:全部提前结清 40:逾期还款
            fql.repay_trial(loanno='000LI0001300516098981916025', loanterm='1', repaytype='30', repayDate='2023-05-25')

        # 代扣申请
        elif flag == 6:
            fql = FqlBizImpl(data=data)
            # withholdAmt: 代扣总金额
            # rpyPrincipal: 实还本金，rpyFeeAmt: 实还利息，rpyMuclt: 实还罚息
            # rpyType: 10-正常还款,30-提前结清,40-逾期还款
            # rpyTerm: 还款期次
            # signNum: 签约协议号
            # capitalLoanNo: 借据号
            fql.payment(withholdAmt=854.05, rpyPrincipal=841.15, rpyFeeAmt=12.9, rpyMuclt=0.0,
                        signNum='S00202211090002', capitalLoanNo='000LI0001300516098981904019', rpyTerm='2',
                        rpyType='30', rpyDate='2023-05-23')

        # 代扣查询
        elif flag == 7:
            fql = FqlBizImpl(data=data)
            # withholadSerialNo: 代扣请求流水号
            fql.payment_query(withholadSerialNo='wsn1667526658605')

        # 上传文件
        elif flag == 8:
            wld = FqlBizImpl(data=data)
            resp = wld.fql_file_upload('/yw', 'E:\\TestData\\身份证\\idcard_front.jpg')
            wld.fql_file_upload_result(resp['seqNo'])

        # 下载文件
        elif flag == 9:
            fql = FqlBizImpl(data=None)
            resp = fql.fql_file_download('/pl/aa.txt', 'C:\\Users\\jccfc\\Desktop\\aa1.txt')
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
