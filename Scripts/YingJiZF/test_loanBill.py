import unittest
from Component.YingJiZF import Component
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
        YingJiZF = Component(data=data)
        jsonData = YingJiZF.query_channel(channelName='度小满科技（北京）有限公司')

        # 获取应急支付渠道号
        self.channelNo = jsonData.get("body")[0].get("channelNo")

    """ 后置条件处理 """
    def tearDown(self):
        self.assertIn("head", self.jsonData)
        if "head" in self.jsonData:
            returnMessage = self.jsonData["head"]["returnMessage"]
            self.assertEqual(returnMessage, '成功', "接口响应失败")

    """ 测试步骤 """
    def test_one(self):
        YingJiZF = Component(data=data)
        self.jsonData = YingJiZF.loan_bill(channelNo=self.channelNo)


if __name__ == '__main__':
    unittest.main()
