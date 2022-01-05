import unittest
from src.impl.YingJiZF.YingJiZFBizImpl import YingJiZFBizImpl
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """

    @classmethod
    def setUpClass(self):
        print("execute setUpClass")

    """ 后置条件处理 """

    @classmethod
    def tearDownClass(self):
        print("execute tearDownClass")

    """ 预置条件处理 """

    def setUp(self):
        print("execute setUp")

    """ 后置条件处理 """

    def tearDown(self):
        self.assertIn("head", self.jsonData)
        if "head" in self.jsonData:
            returnMessage = self.jsonData["head"]["returnMessage"]
            self.assertEqual(returnMessage, '成功', "接口响应失败")

    """ 测试步骤 """

    def test_one(self):
        YingJiZF = YingJiZFBizImpl(data=data)
        # repayType：0 按期还夸；1 提前结清
        # paymentType： 1 支付宝主动还款 5 银行卡主动还款
        self.jsonData = YingJiZF.payment(loanInvoiceId='000LI0001389679618621551007', paymentType='5', repayType="0", periods="1,2,3", repayAmt=300)
        # self.jsonData = YingJiZF.payment(loanInvoiceId='000LI0001195925053932400040', paymentType='5', repayType="1", periods="2,3", repayAmt=69.65)


if __name__ == '__main__':
    unittest.main()
