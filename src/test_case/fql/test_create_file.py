import unittest
from src.impl.FQL.FqlCreditFileBizImpl import *
from person import *
from utils import GlobalVar as gl


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 测试步骤 """
    def test_create_file(self):
        """ 测试步骤 """

        gl._init()
        # 按期还款，提前结清（按日计息），提前结清
        # repay_mode:  还款模式，1：按期还款；3：提前结清；5；逾期还款
        # repay_type:  还款类型，1：清分；2：代扣
        fqlRepayFile(data, repay_date='2022-09-30', term_no="1", repay_mode='5')


if __name__ == '__main__':
    unittest.main()
