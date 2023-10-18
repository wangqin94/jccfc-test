import unittest

from src.impl.common.CheckBizImpl import *
from src.impl.FqlGrt.FqlGrtBizImpl import *
from src.impl.public.LoanPublicBizImpl import *
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """

    def setUp(self):
        self.CheckBizImpl = CheckBizImpl()
        self.MysqlBizImpl = MysqlBizImpl()

    """ 测试步骤 """

    def test_loan(self, loan_date='2023-09-27'):
        """ 测试步骤 """
        # 授信-授信校验-放款-放款校验
        fql_grt = FqlGrtBizImpl(data=None)
        amount = round(random.uniform(100, 10000), 2)
        # amount = 20000
        term = 12
        # orderType: 1-赊销 3-取现 4-乐花卡
        orderType = 3
        # 发起授信申请
        fql_grt.credit(orderType=orderType, loanPrincipal=amount, loanTerm=term)
        self.applyId = fql_grt.data['applyId']
        # 检查授信状态
        time.sleep(10)
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.applyId, product_id='G23E091')
        # 设置放款日mock  flag: True-使用mock, False-使用真实系统放款日
        LoanPublicBizImpl().updateLoanDateMock(date=loan_date, flag=False)
        # 发起支用申请
        fql_grt.loan(orderType=orderType, loanPrincipal=amount, loanTerm=term, fixedBillDay=12, fixedRepayDay=22,
                     loan_date=loan_date)

    """ 后置条件处理 """

    def tearDown(self):
        time.sleep(5)
        # 检查支用状态
        self.CheckBizImpl.check_loan_apply_status(thirdpart_apply_id=self.applyId, product_id='G23E091')
        sql = "update asset_loan_invoice_info set apply_loan_date = date_format(begin_profit_date,'%Y%m%d') " \
              "where apply_loan_date != date_format(begin_profit_date,'%Y%m%d')"
        self.MysqlBizImpl.mysql_asset.update(sql)


if __name__ == '__main__':
    unittest.main()