import unittest
from src.impl.common.CheckBizImpl import *
from src.impl.MeiTuan.MeiTuanBizImpl import MeiTuanBizImpl
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        self.CheckBizImpl = CheckBizImpl()

    """ 测试步骤 """

    def test_loan(self):
        """ 测试步骤 """
        # 授信-授信校验-放款-放款校验
        MeiTuan = MeiTuanBizImpl(data=None)

        # 发起授信申请
        self.APP_NO = MeiTuan.credit(APPLY_AMT=1000000)['app_no']
        # 检查授信状态
        time.sleep(10)
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.APP_NO)
        # 发起支用刚申请
        MeiTuan.loan(TRADE_AMOUNT=60000, TRADE_PERIOD='3')

    """ 后置条件处理 """
    def tearDown(self):
        time.sleep(5)
        # 检查支用状态
        self.CheckBizImpl.check_file_loan_apply_status(thirdpart_apply_id=self.APP_NO)


if __name__ == '__main__':
    unittest.main()
