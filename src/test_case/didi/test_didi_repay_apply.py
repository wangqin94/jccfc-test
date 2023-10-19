import unittest

from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.didi.DidiBizImpl import DidiBizImpl
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.CheckBizImpl = CheckBizImpl()
        self.repayPublicBizImpl = RepayPublicBizImpl()
        self.Didi = DidiBizImpl(data=None)
        self.repayDate = '2023-10-17'

    def test_loan(self):
        """
        授信申请-》支用申请
        :return:
        """
        # 还款环境配置,清理缓存配置账务时间
        self.repayPublicBizImpl.pre_repay_config(repayDate=self.repayDate)

        res = self.Didi.repay(loanOrderId='20231017141641', repay_date=self.repayDate,
                              repay_term_no='1,2,3,4,5,6,7,8,9,10,11,12', repayType=2)

        while True:
            res = self.Didi.queryRepayResult(loanOrderId=res['loanOrderId'], payId=res['payId'])
            if res['status'] !=3:
                break

        self.Didi.repayNotify(loanOrderId=res['loanOrderId'], payId=res['payId'],
                              repay_date=self.repayDate, repay_term_no='1,2,3,4,5,6,7,8,9,10,11,12', repayType=2)


if __name__ == '__main__':
    unittest.main()
