import unittest

from person import *
from src.impl.FqlGrt.FqlGrtBizImpl import *
from src.impl.public.RepayPublicBizImpl import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """

    def setUp(self):
        self.CheckBizImpl = CheckBizImpl()
        self.MysqlBizImpl = MysqlBizImpl()
        self.job = JOB()

    """ 测试步骤 """

    def test_overdue_repay(self, repay_date='2023-11-18'):
        """ 测试步骤 """
        # 追偿
        # 追偿借据号
        self.loan_invoice_id = '000LI0001220732786982914047'
        # term 追偿期次
        self.term = 1
        fql_grt = FqlGrtBizImpl(data=data)
        fql_grt.overdue_repay(loan_invoice_id=self.loan_invoice_id, term=self.term, repay_date=repay_date)
        time.sleep(5)
        # 执行追偿文件下载
        self.job.update_and_trigger_job_byJobId('901806617387986944', group=13,
                                                executeBizDate=repay_date.replace('-', ''))

    """ 后置条件处理 """

    def tearDown(self):
        time.sleep(3)
        # 检查还款状态
        self.CheckBizImpl.check_channel_repay_status(loan_invoice_id=self.loan_invoice_id, repay_term=self.term,
                                                     repay_kind=5)


if __name__ == '__main__':
    unittest.main()
