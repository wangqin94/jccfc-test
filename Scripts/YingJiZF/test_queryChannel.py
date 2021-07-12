import unittest
from Component.YingJiZF import Component
from Scripts.YingJiZF.person import *


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
        print("execute tearDown")

    """ 测试步骤 """
    def test_one(self):
        print('execute test_one')
        YingJiZF = Component(data=data)
        # YingJiZF.query_channel(channelName='度小满科技（北京）有限公司')
        YingJiZF.query_channel()


if __name__ == '__main__':
    unittest.main()
