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

    def test_repay(self, repay_date='2023-12-03'):
        """ 测试步骤 """
        # repay_mode 1-实还，2-代扣
        repay_mode = 2
        # rpyType 10-正常还款 30-提前结清 40-逾期还款
        rpyType = 30
        # term 还款期次
        self.term = 3
        fql_grt = FqlGrtBizImpl(data=data)
        RepayPublicBizImpl().pre_repay_config(repayDate=repay_date)
        if repay_mode == 1:
            fql_grt.repay(rpyType=rpyType, term=self.term, rpyDate=repay_date)
        elif repay_mode == 2:
            detail = fql_grt.withhold_detail(rpyType=rpyType, term=self.term, rpyDate=repay_date)
            detail_list = fql_grt.withhold_detail_list(detail)
            fql_grt.withhold(detail_list=detail_list)
        time.sleep(5)
        # 执行渠道还款任务流
        self.job.update_and_trigger_job_byJobId('793155649356820480', group=13, executeBizDateType='TODAY')

    """ 后置条件处理 """

    def tearDown(self):
        time.sleep(3)
        # 检查还款状态
        self.CheckBizImpl.check_channel_repay_status(third_loan_id=data['applyId'], repay_term=self.term)


if __name__ == '__main__':
    unittest.main()
