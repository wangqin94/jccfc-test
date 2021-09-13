import unittest
from src.impl.MeiTuan.MeiTuan_CreateFileBizImpl import MtFile
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 测试步骤 """
    def test_create_file(self):
        """ 测试步骤 """
        t = MtFile(certificate_no=data['cer_no'], user_name=data['name'], loan_record=0, apply_date='2021-08-19')


if __name__ == '__main__':
    unittest.main()
