import unittest
from src.impl.common.CheckBizImpl import *
from src.impl.MeiTuan.MeiTuanBizImpl import MeiTuanBizImpl
from person import *
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        self.repayPublicBizImpl = RepayPublicBizImpl()

    """ 测试步骤 """

    def test_loan(self):
        """ 测试步骤 """
        self.repayPublicBizImpl.pre_overdue_repay_data('MeiTuan')


if __name__ == '__main__':
    unittest.main()
