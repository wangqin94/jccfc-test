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

    def test_compensation(self, repay_date='2023-11-17'):
        """ 测试步骤 """
        # 代偿
        # 代偿借据号
        self.loan_invoice_id = '000LI0001220732786982914047'
        # term 代偿期次
        self.term = 1
        fql_grt = FqlGrtBizImpl(data=data)
        RepayPublicBizImpl().pre_repay_config(repayDate=repay_date)
        fql_grt.compensation(loan_invoice_id=self.loan_invoice_id, repay_date=repay_date)
        time.sleep(5)
        # 执行代偿文件下载并入账任务流
        self.job.update_and_trigger_job_byJobId('900441321578295296', group=13,
                                                executeBizDate=repay_date.replace('-', ''))

    """ 后置条件处理 """

    def tearDown(self):
        time.sleep(3)
        # 检查还款状态
        self.CheckBizImpl.check_channel_loan_compensation_status(loan_invoice_id=self.loan_invoice_id,
                                                                 repay_term=self.term)


if __name__ == '__main__':
    unittest.main()
