from _pytest import unittest

from src.impl.JieTiao.JieTiaoCreateFileBizImpl import repayPlanFile, repayDetailFile


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 测试步骤 """
    def test_create_file(self,flag=0):

         #还款计划文件
        if flag == 0:
          jt = repayPlanFile()
          jt.start_repayPlanFile()

        #  #还款明细文件
        elif flag == 1:
          jt = repayDetailFile()
          jt.start_repayDetailFile()

if __name__ == '__main__':
    unittest.main()