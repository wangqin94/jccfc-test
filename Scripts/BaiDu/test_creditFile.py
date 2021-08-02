import unittest
from person import data
from BD_CreditFileCreate import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 测试步骤 """

    def test_one(self, flag=1):
        """ 测试步骤 """
        # 生成借据文件、费率文件、还款计划
        if flag == 0:
            # repay_mode='02'随借随还，repay_mode='05'等额本息； cur_date放款时间；loan_record支用查询列表
            BaiduFile(data, cur_date='20210729', loan_record=0, repay_mode='02')

        # 支用状态使用中方可生成还款文件
        # 生成还款文件、更新还款计划、减免文件
        elif flag == 1:
            # 等额本息按期还款、提前结清收取违约金（4%）、提前结清按期收息；随借随还按期还款、部分还款（重算还款计划）、提前结清按日计息
            # repay_mode='02'随借随还，repay_mode='05'等额本息
            # repay_date: 账务日期，提前结清必填
            # repay_term_no: 还款期次
            # repay_type: 还款类型，01：按期还款；02：提前结清；03：逾期还款
            # loan_invoice_id: 借据号为None取用户第一笔借据，否则取自定义值
            BaiduRepayFile(repay_mode='05', repay_date="2021-08-06", repay_term_no=1, repay_type='02')


if __name__ == '__main__':
    unittest.main()
