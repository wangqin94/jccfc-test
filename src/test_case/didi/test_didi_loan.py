import time
import unittest

from src.impl.common.CheckBizImpl import CheckBizImpl, EnumLoanStatus
from src.impl.didi.DidiBizImpl import DidiBizImpl
from src.impl.public.LoanPublicBizImpl import LoanPublicBizImpl
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """
        前置
        :return:
        """
        self.CheckBizImpl = CheckBizImpl()
        self.repayPublicBizImpl = RepayPublicBizImpl()
        self.Didi = DidiBizImpl(data=None)
        self.repayDate = '2023-11-09'
        self.loanDate = '2023-11-09'
        # 设置账务时间
        self.repayPublicBizImpl.pre_repay_config(repayDate=self.repayDate)

    def test_apply(self):
        """
        发起授信申请
        :return:
        """
        self.thirdApplyId = self.Didi.credit(applyAmount=30000)['applicationId']
        while True:
            res = self.Didi.queryCreditResult(self.thirdApplyId)
            if res['status'] != 3:
                break
            time.sleep(3)
            # 检查授信结果
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.thirdApplyId, t=5)

    def test_loan_Risk_Check(self):
        """
        支用风控审核
        :return:
        """
        self.loanOrderId = self.Didi.loanRiskCheck(loanAmount=20000)['loanOrderId']
        time.sleep(5)
        self.Didi.queryLoanRiskCheck(thirdApplyId=self.thirdApplyId)
        while True:
            res = self.Didi.queryLoanRiskCheck(thirdApplyId=self.thirdApplyId)
            if res['status'] != 3:
                break
            time.sleep(2)
        status = self.CheckBizImpl.check_loan_apply_status_with_expect(expect_status=EnumLoanStatus.LOAN_AUDITING.value,
                                                                       thirdpart_apply_id=self.loanOrderId)

    def test_loan_apply(self):
        """
        放款申请
        :return:
        """

        # 发起放款
        self.Didi.applyLoan(thirdApplyId=self.thirdApplyId, loanAmount=20000, loanDate=self.loanDate)
        while True:
            res = self.Didi.queryLoanResult()
            if res['status'] != 3:
                break
            time.sleep(1)
        time.sleep(5)
        self.CheckBizImpl.check_loan_apply_status_with_expect(expect_status=EnumLoanStatus.ON_USE.value,
                                                              thirdpart_apply_id=self.loanOrderId)

        # 更改放款时间
        loanPublicBizImpl = LoanPublicBizImpl()

        loanPublicBizImpl.updateLoanInfo(thirdLoanId=self.loanOrderId, loanDate=self.loanDate)

    def test_loan(self):
        """
        授信申请-》支用申请
        :return:
        """

        # 发起授信申请
        self.thirdApplyId = self.Didi.credit(applyAmount=20000)['applicationId']
        # 授信申请查询
        while True:
            res = self.Didi.queryCreditResult(self.thirdApplyId)
            if res['status'] != 3:
                break
            time.sleep(3)
            # 检查授信结果
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.thirdApplyId, t=5)
        # 发起放款风控审核申请
        self.loanOrderId = self.Didi.loanRiskCheck(loanAmount=12000)['loanOrderId']

        time.sleep(5)
        while True:
            res = self.Didi.queryLoanRiskCheck(thirdApplyId=self.thirdApplyId)
            if res['status'] != 3:
                break
            time.sleep(2)
        status = self.CheckBizImpl.check_loan_apply_status_with_expect(expect_status=EnumLoanStatus.LOAN_AUDITING.value,
                                                                       thirdpart_apply_id=self.loanOrderId)
        # 发起放款
        self.Didi.applyLoan(thirdApplyId=self.thirdApplyId, loanAmount=12000, loanDate=self.loanDate)
        while True:
            res = self.Didi.queryLoanResult()
            if res['status'] != 3:
                break
            time.sleep(1)
        time.sleep(5)
        self.CheckBizImpl.check_loan_apply_status_with_expect(expect_status=EnumLoanStatus.ON_USE.value,
                                                              thirdpart_apply_id=self.loanOrderId)

        # 更改放款时间
        loanPublicBizImpl = LoanPublicBizImpl()

        loanPublicBizImpl.updateLoanInfo(thirdLoanId=self.loanOrderId, loanDate=self.loanDate)

    def test_async_repay_plan(self):
        self.Didi.create_channel_didi_repay_plan(loan_order_id='20231106094015',
                                                 loan_invoice_id='000LI0002363640764457310003')


if __name__ == '__main__':
    unittest.main()
