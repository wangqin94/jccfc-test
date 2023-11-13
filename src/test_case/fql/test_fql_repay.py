import unittest
from src.impl.common.CheckBizImpl import *
from src.impl.FQL.FqlCreditFileBizImpl import *
from src.impl.FQL.FqlBizImpl import *
from src.enums.EnumFql import FqlRepayMode
from src.impl.public.RepayPublicBizImpl import *
from utils import GlobalVar as gl
from utils.JobCenter import *
from utils.Redis import *
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        self.CheckBizImpl = CheckBizImpl()
        self.MysqlBizImpl = MysqlBizImpl()
        self.job = JOB()
        self.redis = Redis()
        self.RepayPublicBizImpl = RepayPublicBizImpl()
        gl._init()


    """ 测试步骤 """

    def test_repay(self):
        """ 测试步骤 """
        # 授信-授信校验-放款-放款校验
        # 按期还款，提前结清（按日计息），提前结清
        # repay_mode:  还款模式，1：按期还款；3：提前结清；5；逾期还款
        # repay_type:  还款类型，1：清分；2：代扣
        # repay:  还款方式枚举，兼容清分和代扣
        repay = FqlRepayMode.settle
        repay_mode = repay.value[0]
        repay_date = '2023-10-25'
        self.term = 3
        repay_type = '2'
        self.RepayPublicBizImpl.pre_repay_config(repayDate=repay_date)
        if repay_type == '1':
            fqlRepayFile(data, repay_date=repay_date, term_no=self.term, repay_mode=repay_mode, repay_type=repay_type)
            # 执行任务流下载文件入库
            self.job.update_job('分期乐还款-下载文件并入库', executeBizDate=repay_date.replace('-', ''),
                               executeBizDateType='CUSTOMER')
            self.job.trigger_job('分期乐还款-下载文件并入库')
            time.sleep(5)
            # 执行轮训还款任务流
            self.job.update_job('分期乐还款-轮询还款', executeBizDate=repay_date.replace('-', ''),
                           executeBizDateType='CUSTOMER')
            self.job.trigger_job('分期乐还款-轮询还款')
            time.sleep(5)
        else:
            fql = FqlBizImpl(data=data)
            fql.payment(rpyTerm=self.term, rpyType=repay.value[1])
            time.sleep(5)
            # 执行任务流下载文件入库
            self.job.update_job('分期乐代扣轮询还款入账任务流', executeBizDateType='TODAY')
            self.job.trigger_job('分期乐代扣轮询还款入账任务流')


    """ 后置条件处理 """
    def tearDown(self):
        # time.sleep(5)
        # 数据库层校验还款是否成功
        # self.CheckBizImpl.check_repay_notice_status(loan_invoice_id=self.loan_invoice_id, repay_term_no=self.term)
        pass


if __name__ == '__main__':
    unittest.main()
