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
            self.Didi.userScoreAdvice(applicationId='DD00003080202310191125314b595e', scoreType=1, applyAmount=200000,
                                      )[
                'orderId']

        while True:
            res = self.Didi.userScoreQuery(orderId)
            if res['status'] != 3:
                break
            time.sleep(1)

        self.Didi.queryCreditResult('DD00003080202310191125314b595e')


if __name__ == '__main__':
    unittest.main()
