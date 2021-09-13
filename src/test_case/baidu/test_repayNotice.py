import unittest
from src.impl.baidu.BaiDuBizImpl import BaiDuBizImpl
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 测试步骤 """

    def test_repay_notice(self):
        """ 测试步骤 """
        # 还款通知
        # 借据号默认为空取当前用户第一笔借据号，否则取赋值借据号
        # type额度恢复类型:1-部分还款;2-借据结清;3-放款失败;4-银行退票
        bd = BaiDuBizImpl(data=data, loan_no=None, type="2")
        bd.notice(amount="100")


if __name__ == '__main__':
    unittest.main()
