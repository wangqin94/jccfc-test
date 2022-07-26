import unittest
from src.impl.MeiTuan.MeiTuan_CreateFileBizImpl import MeiTuanLoanFile, MeiTuanRepayFile
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    def setUp(self):
        pass

    """ 测试步骤 """
    def test_create_file(self, flag=1):
        """ 测试步骤
        @param flag: 0 放款；1 还款
        """

        """ 测试步骤 """
        # 生成借据文件、还款计划
        if flag == 0:
            # 放贷日期'2021-06-30', 为None时，取当前系统时间
            MeiTuanLoanFile(data, apply_date='2022-07-25')

        # 支用状态使用中方可生成还款文件
        # 生成还款文件、更新还款计划、减免文件
        elif flag == 1:
            # repay_date: 账务日期"2021-08-06"，提前结清必填 ps:提前结清和逾期还款必填
            # repay_term_no: 还款期次
            # repay_type: 还款类型：   按期还款：01； 提前结清：02； 逾期还款：03
            # loan_invoice_id: 借据号为None取用户第一笔借据，否则取自定义值
            # prin_amt: 还款本金，逾期部分还款选填
            # int_amt: 还款利息，逾期部分还款选填
            # pnlt_int_amt: 还款罚息，逾期部分还款选填
            MeiTuanRepayFile(data, loan_invoice_id=None, repay_type='01', repay_term_no='1', repay_date='2022-08-25')


if __name__ == '__main__':
    unittest.main()
