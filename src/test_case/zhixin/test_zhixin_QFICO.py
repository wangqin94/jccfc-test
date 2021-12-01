import unittest

from src.impl.common.CommonCheckBizImpl import *
import time
from src.impl.zhixin.ZhiXinBizImpl import ZhiXinBizImpl
from src.impl.zhixin.ZhiXinCheckBizImpl import ZhiXinCheckBizImpl
from src.test_case.zhixin.person import data


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """

    def setUp(self):
        # 初始化日志引擎模块
        self.log = MyLog.get_log()

    """ 测试步骤 """

    def test_apply(self):
        """ 测试步骤 """
        # 信用评估申请
        zhixin = ZhiXinBizImpl(data=data)
        zhixin.applyQFICO(qficoApplyNo='qficoApplyNo1637570100177_1300')
        # zhixin.queryQFICO(qficoApplyNo='qficoApplyNo1637570100167_1300')

    """ 后置条件处理 """

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
