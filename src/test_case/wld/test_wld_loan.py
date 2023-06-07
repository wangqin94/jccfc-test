import unittest
from src.impl.common.CheckBizImpl import *
from src.impl.WLD.WldBizImpl import WldBizImpl
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        self.CheckBizImpl = CheckBizImpl()
        self.MysqlBizImpl = MysqlBizImpl()

    """ 测试步骤 """

    def test_loan(self):
        """ 测试步骤 """
        # 绑卡签约-绑卡确认-授信-授信校验-放款-放款校验
        wld = WldBizImpl(data=None)
        # 绑卡
        wld.bind_card()
        wld.confirm_bind_card()

        # 发起授信申请
        self.applyId = wld.credit(loanTerm=6, applyAmount=1000).get('body')['thirdApplyId']
        # 检查授信状态
        time.sleep(10)
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.applyId)
        # 发起支用申请
        loan_date = '2023-04-25'
        wld.loan(loan_date=loan_date)

    """ 后置条件处理 """
    def tearDown(self):
        time.sleep(5)
        # 检查支用状态
        self.CheckBizImpl.check_loan_apply_status(thirdpart_apply_id=self.applyId)
        sql = "update asset_loan_invoice_info set apply_loan_date = date_format(begin_profit_date,'%Y%m%d') where apply_loan_date != date_format(begin_profit_date,'%Y%m%d')"
        self.MysqlBizImpl.mysql_asset.update(sql)


if __name__ == '__main__':
    unittest.main()
