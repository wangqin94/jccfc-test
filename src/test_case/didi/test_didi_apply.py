import time
import unittest
import warnings

from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.didi.DidiBizImpl import DidiBizImpl


class MyTestCase(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.CheckBizImpl = CheckBizImpl()
        self.Didi = DidiBizImpl(data=None)

    def test_apply(self):
        """
        授信申请查询
        :return:
        """
        # 发起授信申请
        self.thirdApplyId = self.Didi.credit(applyAmount=20000)['applicationId']
        self.Didi.queryCreditResult(self.thirdApplyId)

        # 检查授信结果
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.thirdApplyId, t=5)

    def test_user_score_advice(self):
        """
        贷中评分 修改  调额调价
        :return:
        """
        orderId = \
            self.Didi.userScoreAdvice(applicationId='DC00003080202310191116001697685361', scoreType=1, applyAmount=21000,
                                      scoreThree=975)[
                'orderId']

        while True:
            res = self.Didi.userScoreQuery(orderId)
            if res['status'] != 3:
                break
            time.sleep(1)

        self.Didi.queryCreditResult('DC00003080202310160916011697418962')


if __name__ == '__main__':
    unittest.main()
