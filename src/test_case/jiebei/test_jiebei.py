import time

from src.impl.JieBei.JieBeiBizImpl import JieBeiBizImpl
from src.test_case.jiebei.person import data
from utils.Logger import MyLog


class TestCase(object):
    def __init__(self):
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 特征取数接口  1:初审数据准备 2:复审数据准备 3.授信通知接口]
    def process(self, flag=0):
        """ 测试步骤 """
        # 特征取数接口  初审："featureCodes":["JC_cs_result","JC_cs_failCode","JC_cs_failReason"]
        # 复审："featureCodes":["JC_fs_result","JC_fs_failCode","JC_fs_failReason"]
        # 支用： "featureCodes":["JC_loan_result","JC_loan_failCode","JC_loan_failReason"]    ⽀⽤bizActionType“LOAN_DECISION”
        if flag == 0:
            jt = JieBeiBizImpl(data=data)
            jt.feature(bizActionType='',featureCodes=["JC_cs_result","JC_cs_failCode","JC_cs_failReason"],applyNo='applyNo2022071800000000000001')

        # 初审数据准备
        elif flag == 1:
            jt = JieBeiBizImpl(data=None)
            jt.datapreCs(applyNo='applyNo1111111111123')

        # 复审数据准备
        elif flag == 2:
            jt = JieBeiBizImpl(data=data)
            jt.datapreFs(applyNo='200113')

        #授信通知接口
        elif flag == 3:
            jt = JieBeiBizImpl(data=data)
            jt.creditNotice(applyNo='JCXJ2022051100004747')




    def postprocess(self):
        """ 后置条件处理 """
        pass


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    log = MyLog().get_log()
    log.info('程序运行时间：{}'.format(round(total)))
