# -*- coding: utf-8 -*-
"""
test case script
"""
import logging
import time

from src.impl.FQL.FqlBizImpl import FqlBizImpl
from person import *
from utils.Logger import MyLog
from utils.Models import *

log = logging.getLogger(__name__)

class TestCase(object):
    def __init__(self):
        self.cur_time = str(get_next_month_today(1))
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 授信, 1: 授信查询, 2:支用申请, 3: 支用查询, 4: 授信失效]
    def process(self, flag=9):
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
            fql.loan(loanTerm=6, loanAmt=10000, orderType=1, firstRepayDate='2022-10-26', interestRate='34')

        # 支用查询
        elif flag == 3:
            fql = FqlBizImpl(data=data)
            fql.loan_query()

        # 上传文件
        elif flag == 8:
            wld = FqlBizImpl(data=None)
            resp = wld.fql_file_upload('/pw', 'C:\\Users\\jccfc\\Desktop\\aaa.jpg')
            wld.fql_file_upload_result(resp['seqNo'])

        # 下载文件
        elif flag == 9:
            wld = FqlBizImpl(data=None)
            resp = wld.fql_file_download('/pl/JC_payment_20220926.txt', 'C:\\Users\\jccfc\\Desktop\\JC_payment_20220926.txt')
            wld.fql_file_upload_result(resp['seqNo'])

        return self

    def postprocess(self):
        """ 后置条件处理 """
        pass


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    log = MyLog().get_log()
    log.info('程序运行时间：'.format(round(total)))
