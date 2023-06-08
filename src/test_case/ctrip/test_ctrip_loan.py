# -*- coding: utf-8 -*-
"""
test case script
"""


import unittest
from src.impl.ctrip.CtripBizImpl import CtripBizImpl
from src.impl.common.CheckBizImpl import *
from utils.Models import *
from person import *



class MyTestCase(unittest.TestCase):

    """ 预置条件处理 """
    def setUp(self):
        self.cur_time = str(get_next_month_today(1)).replace("-", '') + time.strftime('%H%M%S')
        self.CheckBizImpl = CheckBizImpl()
        self.MysqlBizImpl = MysqlBizImpl()

    """ 测试步骤 """
    def test_loan(self):
        ctrip = CtripBizImpl(data=None)
        # 发起授信申请
        self.open_id = ctrip.credit(advice_amount=10000)['open_id']
        ctrip.update_apollo_amount()
        # 检查授信状态
        time.sleep(10)
        self.CheckBizImpl.check_credit_apply_status(thirdpart_user_id=self.open_id)
        # 发起支用刚申请
        loan_date = '2023-06-01'
        first_repay_date = str(get_custom_month(1, loan_date)).replace("-", '') + time.strftime('%H%M%S')
        ctrip.loan(loan_amount=10000, term=6, first_repay_date=first_repay_date, loan_date=loan_date)


    """ 后置条件处理 """
    def tearDown(self):
        # 检查支用状态
        time.sleep(5)
        self.CheckBizImpl.check_loan_apply_status(thirdpart_user_id=self.open_id)
        sql = "update asset_loan_invoice_info set apply_loan_date = date_format(begin_profit_date,'%Y%m%d') where apply_loan_date != date_format(begin_profit_date,'%Y%m%d')"
        self.MysqlBizImpl.mysql_asset.update(sql)


if __name__ == '__main__':
    unittest.main()
