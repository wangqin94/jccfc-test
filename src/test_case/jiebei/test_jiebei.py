import base64
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
    def process(self, flag=2):
        """ 测试步骤 """
        # 特征取数接口  初审："featureCodes":["jc_cs_result","jc_cs_failCode","jc_cs_failReason"]
        # 复审："featureCodes":["jc_fs_result","jc_fs_failCode","jc_fs_failReason","jc_fs_pbocBlankAccLevel"]
        # 支用： "featureCodes":["jc_loan_result","jc_loan_failCode","jc_loan_failReason"]    ⽀⽤bizActionType“LOAN_DECISION”
        if flag == 0:
            jt = JieBeiBizImpl(data=data)
            jt.feature(bizActionType='LOAN_DECISION',featureCodes=["jc_loan_result","jc_loan_failCode","jc_loan_failReason"],applyNo='loanNo202208300000000000000005',creditNo='applyNo202208300000000000000004')

        # 初审数据准备
        elif flag == 1:
            jt = JieBeiBizImpl(data=data)
            jt.datapreCs(applyNo='applyNo202208310000000000000006')

        # 复审数据准备
        elif flag == 2:
            jt = JieBeiBizImpl(data=data)
            jt.datapreFs(applyNo='applyNo202208310000000000000006',creditNo='applyNo202208310000000000000006')

        #授信通知接口
        elif flag == 3:
            jt = JieBeiBizImpl(data=data)
            jt.creditNotice(applyNo='applyNo202208250000000000000016')

        elif flag == 4:
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
