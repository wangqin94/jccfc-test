import unittest
from Component.BaiDu import Component
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 测试步骤 """

    def test_repay_notice(self):
        """ 测试步骤 """
        # 还款通知
        # 借据号默认为空取当前用户第一笔借据号，否则取赋值借据号
        bd = Component(data=data, loan_no=None, type="2")
        bd.notice(amount="100")


if __name__ == '__main__':
    unittest.main()
