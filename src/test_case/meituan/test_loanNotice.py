import unittest
from src.impl.MeiTuan.MeiTuanBizImpl import MeiTuanBizImpl
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 测试步骤 """

    def test_loan_notice(self):
        """ 测试步骤 """
        # 放款通知，放款成功不进行任何处理，放款失败进行额度恢复处理
        # 借据号默认为空取当前用户第一笔借据号，否则取赋值借据号
        mt = MeiTuanBizImpl(data=data, loan_no=None, term="1")
        mt.loan_notice()


if __name__ == '__main__':
    unittest.main()