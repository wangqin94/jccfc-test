import unittest
from src.impl.common.CheckBizImpl import *
from src.impl.FQL.FqlBizImpl import *
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        self.cur_time = str(get_next_month_today(1))
        self.CheckBizImpl = CheckBizImpl()
        self.MysqlBizImpl = MysqlBizImpl()

    """ 测试步骤 """

    def test_loan(self, loan_date='2023-07-13'):
        """ 测试步骤 """
        # 授信-授信校验-放款-放款校验
        fql = FqlBizImpl(data=None)
        # 发起授信申请
        self.applyId = fql.credit(creditAmount=10000, loanAmount=10000, loanTerm=3, interestRate='23')['applyId']
        # 检查授信状态
        time.sleep(10)
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.applyId)
        # 发起支用申请
        firstRepayDate = str(get_custom_month(1, loan_date))
        # orderType: 订单类型 1取现；2赊销
        fql.loan(orderType=2, loanTerm=3, loanAmt=10000, firstRepayDate=firstRepayDate,
                 fixedRepayDay=firstRepayDate[-2:], interestRate='23', loan_date=loan_date)

    """ 后置条件处理 """
    def tearDown(self):
        time.sleep(5)
        # 检查支用状态
        self.CheckBizImpl.check_loan_apply_status(thirdpart_apply_id=self.applyId)
        sql = "update asset_loan_invoice_info set apply_loan_date = date_format(begin_profit_date,'%Y%m%d') " \
              "where apply_loan_date != date_format(begin_profit_date,'%Y%m%d')"
        self.MysqlBizImpl.mysql_asset.update(sql)


if __name__ == '__main__':
    unittest.main()
