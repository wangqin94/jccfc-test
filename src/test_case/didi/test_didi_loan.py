import unittest

from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.didi.DidiBizImpl import DidiBizImpl


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.CheckBizImpl = CheckBizImpl()
        self.Didi = DidiBizImpl(data=None)

    def test_loan(self):
        """
        授信申请-》支用申请
        :return:
        """

        # 发起授信申请
        self.thirdApplyId = self.Didi.credit(applyAmount=20000)
        # 授信申请查询
        self.Didi.queryCreditResult(123123)
        # 检查授信结果
        # self.CheckBizImpl.check_credit_apply_status(123123)
        # 发起授信申请
        self.Didi.loanRiskCheck()


    def tearDown(self):
        pass
