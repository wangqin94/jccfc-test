import unittest

from src.impl.JieBei.jieBeiCreateFileBizImpl import creditFile, loanApplyFile


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 测试步骤 """

    def test_create_file(self, flag=0):

        #银河授信文件
        if flag == 0:
            jb = creditFile()
            jb.start_creditFile()

        #银数支用文件
        elif flag == 1:
            jb = loanApplyFile()
            jb.start_loanApplyFile(withhold_id='000RPI2022071100000001')


if __name__ == '__main__':
    unittest.main()