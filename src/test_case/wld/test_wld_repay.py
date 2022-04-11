import unittest
from src.impl.WLD.WldBizImpl import WldBizImpl
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        print("前置校验待开发")

    """ 测试步骤 """

    def test_loan(self):
        """ 测试步骤 """
        # 还款  repay_term_no还款期次   repay_type还款类型：1-按期还款，2-提前结清，4-逾期还款
        wld = WldBizImpl(data=data)
        # 提前结清repay_date必填，按期/逾期请修改apollo:credit还款mock时间：credit.mock.repay.date
        wld.repay( repay_term_no="1", repay_type="1", loan_invoice_id="000LI0002137107007488200014",repay_date='2022-05-07')
        # wld.repay(repayAmount=685.90, repayPrincipal=685.90, repayInterest=0)

    """ 后置条件处理 """
    def tearDown(self):
        print("结果校验待开发")


if __name__ == '__main__':
    unittest.main()
