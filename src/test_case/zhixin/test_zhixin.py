# -*- coding: utf-8 -*-
"""
test case script
"""
import json
import time
from multiprocessing import Process

from src.impl.common.MysqlBizImpl import MysqlBizImpl
from src.impl.zhixin.ZhiXinBizImpl import ZhiXinBizImpl
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
    def process(self, flag=4):
        """ 测试步骤 """
        # 绑卡
        if flag == 0:
            zhixin = ZhiXinBizImpl(data=data)
            res = json.loads(zhixin.applyCertification().get('output'))
            zhixin.verifyCode(userId=res['userId'], certificationApplyNo=res['certificationApplyNo'],
                              cdKey=res['cdKey'])

        # 撞库
        elif flag == 1:
            zhixin = ZhiXinBizImpl(data=data)
            zhixin.checkUser(data['telephone'])

        # 绑卡申请
        elif flag == 2:
            zhixin = ZhiXinBizImpl(data=None)
            zhixin.applyCertification()

        # 授信
        elif flag == 3:
            zhixin = ZhiXinBizImpl(data=data)
            zhixin.credit()

        # 授信查询
        elif flag == 4:
            zhixin = ZhiXinBizImpl(data=data)
            zhixin.queryCreditResult()

        # 借款试算
        elif flag == 5:
            zhixin = ZhiXinBizImpl(data=data)
            zhixin.loanTrial()

        # 借款申请
        elif flag == 6:
            zhixin = ZhiXinBizImpl(data=data)
            zhixin.applyLoan(loanAmt='1000', term='12', loanPurpose='06')

        # 借款查询
        elif flag == 7:
            zhixin = ZhiXinBizImpl(data=data)
            zhixin.queryLoanResult(userId="SUR1678250090", loanApplyNo="SLN4301654300")

        # 还款结果查询
        elif flag == 8:
            zhixin = ZhiXinBizImpl(data=data)
            zhixin.queryRepayResult(userId="userId1642402917009", repayApplyNo="repayApplyNo16424043945925851")

        # 还款
        elif flag == 9:
            zhixin = ZhiXinBizImpl(data=data)
            # 默认取person文件中的userid
            loan_apply_info = MysqlBizImpl().get_loan_apply_info(thirdpart_user_id=data['userId'])
            zhixin.applyRepayment(repay_type='1', loan_no="000LA2021122300000068")  # 按期还款

        # 额度&产品查询
        elif flag == 10:
            zhixin = ZhiXinBizImpl(data=data)
            zhixin.queryCreditProduct()

        # 借款&还款计划查询
        elif flag == 11:
            zhixin = ZhiXinBizImpl(data=data)
            zhixin.queryLoanPlan()

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
