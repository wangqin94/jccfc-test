import unittest
from person import data
from src.impl.baidu.BaiDuCreditFileBizImpl import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 测试步骤 """

    def test_one(self, flag=0):
        """ 测试步骤 """
        # 生成借据文件、费率文件、还款计划
        if flag == 0:
            # repay_mode='02'随借随还，repay_mode='05'等额本息； cur_date放款时间；loan_record支用查询列表
            bd = BaiduFile(data, cur_date='20211009', loan_record=0, repay_mode='02')
            bd.start()

        # 支用状态使用中方可生成还款文件
        # 生成还款文件、更新还款计划、减免文件
        elif flag == 1:
            # 等额本息按期还款、提前结清收取违约金（4%）、提前结清按期收息；随借随还按期还款、部分还款（重算还款计划）、提前结清按日计息
            # repay_mode='02'随借随还，repay_mode='05'等额本息
            # repay_date: 账务日期，提前结清必填
            # repay_term_no: 还款期次
            # repay_type: 还款类型，01：按期还款；02：提前结清；03：逾期还款；04：提前还当期；05：提前还部分（仅支持随借随还）
            # loan_invoice_id: 借据号为None取用户第一笔借据，否则取自定义值
            # prin_amt: 还款本金，随借随还部分还款必填
            # int_amt: 还款利息，随借随还部分还款必填
            # pnlt_int_amt: 还款罚息，随借随还部分还款必填
            bd = BaiduRepayFile(data, repay_mode='02', repay_date="2021-11-09", repay_term_no=1,
                                repay_type='01', loan_invoice_id=None)
            bd.start_repay_file()


if __name__ == '__main__':
    unittest.main()
