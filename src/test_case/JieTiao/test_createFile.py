import unittest
import time

from src.impl.JieTiao.JieTiaoCreateFileBizImpl import repayPlanFile, repayDetailFile


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 测试步骤 """

    def test_create_file(self, flag=1):

        # 还款计划文件
        if flag == 0:
            jt = repayPlanFile()
            jt.start_repayPlanFile(loan_invoice_id='000LI0001706338967756802001')

        #  #还款明细文件
        elif flag == 1:
            jt = repayDetailFile()
            jt.start_repayDetailFile(withhold_id='000RPI2022071100000001')

        #  附件校验压测造数
        elif flag == 2:
            jt = repayDetailFile()
            for i in range(1000):
                check_id = "000DEF" + str(int(round(time.time() * 1000)))
                jt.start(check_id)


if __name__ == '__main__':
    unittest.main()
