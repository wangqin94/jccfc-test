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
        wld.repay(repay_date='2023-07-13', repay_term_no="1", repay_type="2", loan_invoice_id='000LI0001441459745766827043')

    """ 后置条件处理 """
    def tearDown(self):
        print("结果校验待开发")


if __name__ == '__main__':
    unittest.main()
