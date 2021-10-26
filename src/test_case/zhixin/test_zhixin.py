# -*- coding: utf-8 -*-
"""
test case script
"""
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

    # # [0: 绑卡, 3: 授信, 5: 支用, 6: 还款, 7: 绑卡&授信&支用]
    def process(self, flag=0):
        """ 测试步骤 """
        # 绑卡
        if flag == 0:
            zhixin = ZhiXinBizImpl(data=None)
            res = zhixin.applyCertification()
            zhixin.verifyCode(userId=res['userId'], certificationApplyNo=res['certificationApplyNo'], cdKey=res['cdKey'])

        # 撞库
        elif flag == 1:
            zhixin = ZhiXinBizImpl(data=data)
            zhixin.checkUser(data['cer_no'], data['telephone'])

        # 绑卡申请
        elif flag == 2:
            ZhiXinBizImpl(data=None)

        # 授信
        elif flag == 3:
            zhixin = ZhiXinBizImpl(data=data)
            zhixin.credit()

    def postprocess(self):
        """ 后置条件处理 """
        pass


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    log = MyLog.get_log()
    log.info('程序运行时间：{}'.format(round(total)))
