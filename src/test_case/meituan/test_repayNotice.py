import unittest
from src.impl.MeiTuan.MeiTuanBizImpl import MeiTuanBizImpl
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 测试步骤 """

    def test_repay_notice(self):
        """ 测试步骤 """
        # 还款通知:
        # principal 本金分为单位；
        # initerest 本金分为单位；
        # diniterest 本金分为单位；
        # type 还款类型，业务未处理，可不传；
        # termNo 期次；
        # finish_time 还款时间，可不传，入库后手动修改；
        # 借据号默认为空取当前用户第一笔借据号，否则取赋值借据号
        mt = MeiTuanBizImpl(data=data, loan_no=None)
        mt.repay_notice(principal=10000, initerest=100, diniterest=100, termNo="1")


if __name__ == '__main__':
    unittest.main()
