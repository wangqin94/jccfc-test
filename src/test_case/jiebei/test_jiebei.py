import base64
import os
import time

from src.impl.JieBei.JieBeiBizImpl import JieBeiBizImpl
from utils.Logger import MyLog
if not os.path.exists('person.py'):
    open('person.py', 'w')
from person import *


class TestCase(object):
    def __init__(self):
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 特征取数接口（2次）  1:初审数据准备 2:复审数据准备（多次调用） 3.授信通知接口 4.结清证明开具]
    def process(self, flag=0):
        """ 测试步骤 """
        # 特征取数接口  初审："featureCodes":["jc_cs_result","jc_cs_failCode","jc_cs_failReason"]
        # 复审："featureCodes":["jc_fs_result","jc_fs_failCode","jc_fs_failReason","jc_fs_pbocBlankAccLevel"]   ........
        # 支用："featureCodes":["jc_loan_result","jc_loan_failCode","jc_loan_failReason"]    ⽀⽤bizActionType"LOAN_DECISION"
        # 提额："featureCodes":["jc_limit_up_result","jc_limit_up_failCode","jc_limit_up_failReason"]
        # 降额："featureCodes":["jc_limit_down_result","jc_limit_down_failCode","jc_limit_down_failReason"]
        if flag == 0:
            jb = JieBeiBizImpl(data=None)
            jb.feature(bizActionType='LOAN_DECISION', featureCodes=["jc_loan_result","jc_loan_failCode","jc_loan_failReason"])

        # 初审数据准备
        elif flag == 1:
            jb = JieBeiBizImpl(data=None)
            jb.datapreCs()

        # 复审数据准备 applyType:#授信 ADMIT_APPLY；提额 ADJUST_AMT_APPLY；降额 DECREASE_AMT_APPLY
        elif flag == 2:
            jb = JieBeiBizImpl(data=data)
            jb.datapreFs(applyType='ADMIT_APPLY')

        #授信通知接口 ADMIT_APPLY授信申请 LOAN_APPLY支用申请 ADJUST_AMT_APPLY提额申请 DECREASE_AMT_APPLY降额申请 ADJUST_RATE_APPLY提价申请 DECREASE_RATE_APPLY降价
        elif flag == 3:
            jb = JieBeiBizImpl(data=data)
            jb.creditNotice(bizType='ADMIT_APPLY', creditAmt=5000000)


        elif flag == 5:
            c = ('浙江省杭州市⻄湖区学院路128号A1座12').encode()
            a = base64.b64encode(c)
            print(a)



    def postprocess(self):
        """ 后置条件处理 """
        pass


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    log = MyLog().get_log()
    log.info('程序运行时间：{}'.format(round(total)))
