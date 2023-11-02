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

    def test_loan(self, loan_date='2023-10-10'):
        """ 测试步骤 """
        # 授信-授信校验-放款-放款校验
        self.loan_date = loan_date if loan_date else time.strftime('%Y-%m-%d', time.localtime())
        fql_grt = FqlGrtBizImpl(data=None)
        amount = round(random.uniform(100, 15000), 2)
        # amount = 1000
        term = 6
        # orderType: 1-赊销 3-取现 4-乐花卡
        orderType = 1
        # 发起授信申请
        fql_grt.credit(orderType=orderType, loanPrincipal=amount, loanTerm=term)
        self.applyId = fql_grt.data['applyId']
        # 检查授信状态
        time.sleep(10)
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.applyId, product_id='G23E091')
        # 设置放款日mock  flag: True-使用mock, False-使用真实系统放款日
        LoanPublicBizImpl().updateLoanDateMock(date=loan_date, flag=True)
        # 发起支用申请
        """
        fixedBillDay：出账日，fixedRepayDay：还款日
        出账日为1-18：
        1）若放款日<出账日，则首期还款日在放款日当月
        2）若放款日>=出账日，则首期还款日在放款日当月下个月
        出账日为22-28：
        1）若放款日<出账日，则首期还款日期在放款日的下个月
        2）若放款日>=出账日，则首期还款日期在放款日的下下个月
        出账日与还款日对应关系：
        1-11,2-12,3-13,4-14,5-15,6-16,7-17,8-18,9-19,10-20,11-21,12-22,13-23,14-24,15-25,16-26,17-27,18-18,22-1,23-2,24-3
        25-4,26-5,27-6,28-7,28-9,28-10
        """
        fql_grt.loan(orderType=orderType, loanPrincipal=amount, loanTerm=term, fixedBillDay=23, fixedRepayDay=2,
                     loan_date=loan_date)

    """ 后置条件处理 """

    def tearDown(self):
        time.sleep(5)
        # 检查支用状态
        self.CheckBizImpl.check_loan_apply_status(thirdpart_apply_id=self.applyId, product_id='G23E091')
        LoanPublicBizImpl().updateLoanInfo(thirdLoanId=self.applyId, loanDate=self.loan_date)


if __name__ == '__main__':
    unittest.main()
