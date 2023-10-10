import time
import unittest

from src.impl.common.CheckBizImpl import CheckBizImpl, EnumLoanStatus
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
        self.thirdApplyId = self.Didi.credit(applyAmount=30000)['applicationId']
        # 授信申请查询
        self.Didi.queryCreditResult(self.thirdApplyId)
        # self.Didi.queryCreditResult("DC00202309231530321695454232938")
        # 检查授信结果
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.thirdApplyId)
        # 发起放款风控审核申请
        self.loanOrderId = self.Didi.loanRiskCheck(loanAmount=1000)['loanOrderId']
        time.sleep(5)
        self.Didi.queryLoanRiskCheck(thirdApplyId=self.thirdApplyId)
        status = self.CheckBizImpl.check_loan_apply_status_with_expect(expect_status=EnumLoanStatus.LOAN_AUDITING.value,
                                                                       thirdpart_apply_id=self.loanOrderId)
        # 发起放款
        self.Didi.applyLoan(thirdApplyId=self.thirdApplyId, loanAmount=1000,loanDate='2023-09-24')
        time.sleep(5)
        self.Didi.queryLoanResult()
        self.CheckBizImpl.check_loan_apply_status_with_expect(expect_status=EnumLoanStatus.ON_USE.value,
                                                              thirdpart_apply_id=self.loanOrderId)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
