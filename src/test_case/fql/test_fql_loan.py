import unittest
from src.impl.common.CommonCheckBizImpl import *
from src.impl.FQL.FqlBizImpl import *
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        self.cur_time = str(get_next_month_today(1))
        self.CheckBizImpl = CheckBizImpl()

    """ 测试步骤 """

    def test_loan(self):
        """ 测试步骤 """
        # 授信-授信校验-放款-放款校验
        fql = FqlBizImpl(data=None)
        # 发起授信申请
        self.applyId = fql.credit(creditAmount=2000)['applyId']
        # 检查授信状态
        time.sleep(10)
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.applyId)
        # 发起支用刚申请
        # orderType: 订单类型 1取现；2赊销
        fql.loan(orderType=1, firstRepayDate=self.cur_time)

    """ 后置条件处理 """
    def tearDown(self):
        time.sleep(5)
        # 检查支用状态
        self.CheckBizImpl.check_loan_apply_status(thirdpart_apply_id=self.applyId)


if __name__ == '__main__':
    unittest.main()
