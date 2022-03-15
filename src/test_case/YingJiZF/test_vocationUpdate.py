import unittest

from person import *
from src.impl.YingJiZF.YingJiZFBizImpl import YingJiZFBizImpl


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
        self.jsonData = YingJiZF.vocation_update(idCard='370000198207305208', vocation='X')


if __name__ == '__main__':
    unittest.main()
