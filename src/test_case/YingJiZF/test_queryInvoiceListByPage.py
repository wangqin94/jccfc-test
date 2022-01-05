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
        pass
        # YingJiZF = YingJiZFBizImpl(data=data)
        # jsonData = YingJiZF.query_channel(channelName='上海淇毓信息科技有限公司')

        # 获取应急支付渠道号
        # self.channelNo = jsonData.get("body")[0].get("channelNo")

    """ 后置条件处理 """
    def tearDown(self):
        self.assertIn("head", self.jsonData)
        if "head" in self.jsonData:
            returnMessage = self.jsonData["head"]["returnMessage"]
            self.assertEqual(returnMessage, '成功', "接口响应失败")

    """ 测试步骤 """
    def test_one(self):
        YingJiZF = YingJiZFBizImpl(data=data)
        self.jsonData = YingJiZF.query_invoice_list(channelNo="F21E04ZHIX")


if __name__ == '__main__':
    unittest.main()
