import unittest

from src.impl.JieBei.JieBeiCreateFileBizImpl import creditFile, loanApplyFile, loandetailFile
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 测试步骤 """

    def test_create_file(self, flag=3):

        # 银河授信文件
        if flag == 0:
            jb = creditFile(data)
            jb.start_creditFile()

        # 银河支用文件
        elif flag == 1:
            jb = loanApplyFile(data)
            jb.start_loanApplyFile()

        # 银数放款合约+分期
        elif flag == 2:
            jb = loandetailFile(data)
            jb.start_loandetailFile()

        # 银数 还款
        elif flag == 3:
            jb = loandetailFile(data)
            jb.start_repayDetailFile()


if __name__ == '__main__':
    unittest.main()