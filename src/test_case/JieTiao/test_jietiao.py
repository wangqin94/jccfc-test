import os
import time

from src.impl.JieTiao.JieTiaoBizImpl import JieTiaoBizImpl
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

    # # [0: 放款请求接口,1:放款结果查询接口,2:代扣申请接口, 3:代扣申请结果查询,4:还款通知接口 5: 还款查询接口]
    def process(self, flag=0):
        """ 测试步骤 """
        # 放款请求接口
        if flag == 0:
            jt = JieTiaoBizImpl(data=None)
            jt.loan(loanAmt='10000', lnTerm='12')

        # 放款结果查询接口
        elif flag == 1:
            jt = JieTiaoBizImpl(data=data)
            jt.loan_query()

        # 代扣申请接口
        elif flag == 2:
            jt = JieTiaoBizImpl(data=data)
            jt.payment(totalAmt='200113')

        #代扣申请结果查询
        elif flag == 3:
            jt = JieTiaoBizImpl(data=data)
            jt.payment_query(tranNo='JCXJ2022051100004747')

        # 还款通知接口
        elif flag == 4:
            jt = JieTiaoBizImpl(data=data)
            # rpyType 提前还款:01(提前结清) 期供还款:02 (按指定期数进行还款，包含部分还款、提前还当期)   逾期还款：03（逾期还部分、逾期足额按期还）
            # rpyTerm 期供还款该字段必填,提前结清期数为空
            # rpyDate 还款日期
            # ifEnough 0:非足额 1:足额  rpyChannel 0:线下 1:线上
            # rpyPrinAmt 本金，rpyIntAmt 利息，rpyOintAmt 罚息，rpyRedLineAmt 红线减免，rpyDeductAmt 营销减免
            jt.repay_notice(rpyTerm='12', rpyType='01', rpyDate='2023-11-14')

        # 还款查询
        elif flag == 5:
            jt = JieTiaoBizImpl(data=data)
            jt.repay_query(loanReqNo='346177553668492058625', rpyReqNo='34624308793447451443306')

        elif flag == 6:
            for i in range(8):
                jt = JieTiaoBizImpl(data=None)
                jt.loan(loanDate='2022-03-23 00:00:00', loanAmt='2000', lnTerm='12', creditAmt='20',
                        feeRate='0.01845204', yearRate='0.2245', idValidDateStart='2022-01-10',
                        idValidDateEnd='2022-09-12')
        return self



    def postprocess(self):
        """ 后置条件处理 """
        pass


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    log = MyLog().get_log()
    log.info('程序运行时间：{}'.format(round(total)))
