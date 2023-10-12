import time
import unittest

from src.impl.common.CheckBizImpl import CheckBizImpl, EnumLoanStatus
from src.impl.didi.DidiBizImpl import DidiBizImpl
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.CheckBizImpl = CheckBizImpl()
        self.repayPublicBizImpl = RepayPublicBizImpl()
        self.Didi = DidiBizImpl(data=None)
        self.repayDate = '2023-10-12'

    def test_loan(self):
        """
        授信申请-》支用申请
        :return:
        """
        # 还款环境配置,清理缓存配置账务时间
        # self.repayPublicBizImpl.pre_repay_config(repayDate=self.repayDate)

        self.Didi.repay()
        time.sleep(5)
        self.Didi.queryRepayResult(loanOrderId='20231012171343',payId='202310121502550002150ff9df70b0l1')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
