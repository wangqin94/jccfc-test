import unittest
from src.impl.common.CommonCheckBizImpl import *
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
        wld = WldBizImpl(data=data, repay_term_no="2", repay_type="2", loan_invoice_id="000LI1762723297796214007")
        wld.repay()
        # wld.repay(repayAmount=685.90, repayPrincipal=685.90, repayInterest=0)

    """ 后置条件处理 """
    def tearDown(self):
        print("结果校验待开发")


if __name__ == '__main__':
    unittest.main()
