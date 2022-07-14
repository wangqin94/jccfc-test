import time

from src.impl.JieTiao.JieTiaoBizImpl import JieTiaoBizImpl
from src.test_case.JieTiao.person import data
from utils.Logger import MyLog


class TestCase(object):
    def __init__(self):
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 放款请求接口,1:放款结果查询接口,2:代扣申请接口, 3:代扣申请结果查询,4:还款通知接口 5: 还款查询接口]
    def process(self, flag=4):
        """ 测试步骤 """
        # 放款请求接口
        if flag == 0:
            jt = JieTiaoBizImpl(data=data)
            jt.loan(loanDate='2022-03-23 00:00:00', loanAmt='1000', lnTerm='24', creditAmt='20', feeRate='0.00065452', yearRate='0.2389', idValidDateStart='2022-01-10', idValidDateEnd='2023-10-12')

        # 放款结果查询接口
        elif flag == 1:
            jt = JieTiaoBizImpl(data=None)
            jt.loan_query(loanReqNo='loanReqNo16575230073452')

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
            jt = JieTiaoBizImpl(data=None)
            jt.repay_notice(loanReqNo='', rpyType='', rpyTerm='', rpyReqNo='', tranNo='', rpyDate='', rpyPrinAmt='', rpyIntAmt='', rpyOintAmt='', rpyDeductAmt='', rpyRedLineAmt='', ifEnough='',rpyChannel='')

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
