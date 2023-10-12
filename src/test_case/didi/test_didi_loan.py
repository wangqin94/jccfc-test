import time
import unittest

from src.impl.common.CheckBizImpl import CheckBizImpl, EnumLoanStatus
from src.impl.didi.DidiBizImpl import DidiBizImpl
from src.impl.public.LoanPublicBizImpl import LoanPublicBizImpl
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.CheckBizImpl = CheckBizImpl()
        self.repayPublicBizImpl = RepayPublicBizImpl()
        self.Didi = DidiBizImpl(data=None)
        self.repayDate = '2023-10-12'
        self.loanDate = '2023-09-12'
    def test_loan(self):
        """
        授信申请-》支用申请
        :return:
        """

        # 发起授信申请
        self.thirdApplyId = self.Didi.credit(applyAmount=30000)['applicationId']
        # 授信申请查询
        self.Didi.queryCreditResult(self.thirdApplyId)
        # 检查授信结果
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.thirdApplyId, t=5)
        # 发起放款风控审核申请
        self.loanOrderId = self.Didi.loanRiskCheck(loanAmount=1000)['loanOrderId']
        time.sleep(5)
        self.Didi.queryLoanRiskCheck(thirdApplyId=self.thirdApplyId)
        status = self.CheckBizImpl.check_loan_apply_status_with_expect(expect_status=EnumLoanStatus.LOAN_AUDITING.value,
                                                                       thirdpart_apply_id=self.loanOrderId)
        # 发起放款
        self.Didi.applyLoan(thirdApplyId=self.thirdApplyId, loanAmount=1000, loanDate=self.loanDate)
        time.sleep(5)
        self.Didi.queryLoanResult()
        self.CheckBizImpl.check_loan_apply_status_with_expect(expect_status=EnumLoanStatus.ON_USE.value,
                                                              thirdpart_apply_id=self.loanOrderId)
        loanPublicBizImpl = LoanPublicBizImpl()
        loanPublicBizImpl.updateLoanInfo(thirdLoanId=self.loanOrderId, loanDate=self.loanDate)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
