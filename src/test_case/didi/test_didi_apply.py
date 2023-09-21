import unittest
import warnings

from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.didi.DidiBizImpl import DidiBizImpl


class MyTestCase(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.CheckBizImpl = CheckBizImpl()
        self.Didi = DidiBizImpl(data=None)

    def test_apply(self):
        """
        授信申请查询
        :return:
        """
        # 发起授信申请
        self.thirdApplyId = self.Didi.credit(applyAmount=20000)


if __name__ == '__main__':
    unittest.main()
