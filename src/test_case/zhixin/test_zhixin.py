# -*- coding: utf-8 -*-
"""
test case script
"""
import json
import time
from src.impl.zhixin.ZhiXinBizImpl import ZhiXinBizImpl
from person import *
from utils.Logger import MyLog


class TestCase(object):
    def __init__(self):
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 绑卡&短信验证, 1: 撞库, 2: 绑卡申请, 3: 授信]
    def process(self, flag=6):
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
            zhixin.queryCreditResult(userId="userId1636703906300", creditApplyNo="creditApplyNo1636703906300")

        # 借款试算
        elif flag == 5:
            zhixin = ZhiXinBizImpl(data=data)
            zhixin.loanTrial()

        # 借款申请
        elif flag == 6:
            zhixin = ZhiXinBizImpl(data=data)
            zhixin.applyLoan(loanAmt='1000', term='6')

        # 借款查询
        elif flag == 7:
            zhixin = ZhiXinBizImpl(data=data)
            zhixin.queryLoanResult()

    def postprocess(self):
        """ 后置条件处理 """
        pass


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    log = MyLog.get_log()
    log.info('程序运行时间：{}'.format(round(total)))
