import unittest
import warnings

from src.impl.common.CheckBizImpl import *
from src.impl.yixin.YiXinBizImpl import YiXinBizImpl


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.CheckBizImpl = CheckBizImpl()

    """ 测试步骤 """

    def test_apply(self):
        """ 测试步骤 """
        yixin = YiXinBizImpl(data=None)

        # 发起授信申请
        self.thirdApplyId = yixin.credit(applyAmount=20000, loanTerm=3)['body']['thirdApplyId']

    """ 后置条件处理 """

    def tearDown(self):
        # 检查授信状态
        status = self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.thirdApplyId)
        self.assertEqual(EnumCreditStatus.SUCCESS.value, status, '授信失败')


if __name__ == '__main__':
    unittest.main()
