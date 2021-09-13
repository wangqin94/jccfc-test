import unittest
from src.impl.common.CommonCheckBizImpl import *
from src.impl.baidu.BaiDuBizImpl import *
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        self.CheckBizImpl = CheckBizImpl()

    """ 测试步骤 """

    def test_loan_loan(self):
        """ 测试步骤 """
        # 授信-授信校验-放款-放款校验
        baidu = BaiDuBizImpl(data=None)

        # 发起授信申请
        self.applyId = baidu.credit(initialAmount=3000000)['applyId']
        # 检查授信状态
        time.sleep(5)
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.applyId)
        # 发起支用刚申请
        self.orderId = baidu.loan(cashAmount=60000, repayMode='22')['orderId']

    """ 后置条件处理 """
    def tearDown(self):
        time.sleep(5)
        # 检查支用状态
        self.CheckBizImpl.check_file_loan_apply_status(thirdpart_order_id=self.orderId)


if __name__ == '__main__':
    unittest.main()
