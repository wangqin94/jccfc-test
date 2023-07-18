import unittest
from src.impl.common.CheckBizImpl import *
from src.impl.baidu.BaiDuCreditFileBizImpl import *
from src.impl.public.RepayPublicBizImpl import *
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


    """ 测试步骤 """

    def test_repay(self):
        """ 测试步骤 """
        # 授信-授信校验-放款-放款校验
        # repay_mode='02'随借随还，repay_mode='05'等额本息
        # repay_type: 还款类型，01：按期还款；02：提前结清；03：逾期还款；04：提前还当期；05：提前还部分（仅支持随借随还）
        repay_mode = '05'
        repay_date = '2023-07-13'
        self.term = 1
        repay_type = '02'
        loan_invoice_id = '000LI0001441803343143005051'
        # 还款前置任务
        self.RepayPublicBizImpl.pre_repay_config(repayDate=repay_date)

        baidu = BaiduRepayFile(data, repay_mode=repay_mode, repay_date=repay_date, repay_term_no=self.term,
                               repay_type=repay_type, loan_invoice_id=loan_invoice_id)
        baidu.start_repay_file()
        self.loan_invoice_id = loan_invoice_id if loan_invoice_id else baidu.get_invoice_info()[1]
        # 执行任务流下载文件入库
        self.job.update_job('百度还款对账文件下载任务流', executeBizDate=repay_date.replace('-', ''),
                           executeBizDateType='CUSTOMER')
        self.job.trigger_job('百度还款对账文件下载任务流')
        time.sleep(5)
        # 更新还款通知表
        key = "loan_invoice_id = '" + self.loan_invoice_id + "' and notice_type = '1' order by create_time desc limit 1"
        self.MysqlBizImpl.update_credit_database_info('credit_ctrip_repay_notice_info', attr=key,
                                                 business_date=repay_date.replace('-', ''))
        # 检查是否入三方待建账信息
        self.job.update_job('三方还款任务流', executeBizDate=repay_date.replace('-', ''),
                       executeBizDateType='CUSTOMER')
        self.job.trigger_job('三方还款任务流')
        time.sleep(5)


    """ 后置条件处理 """
    def tearDown(self):
        time.sleep(5)
        # 数据库层校验还款是否成功
        self.CheckBizImpl.check_repay_notice_status(loan_invoice_id=self.loan_invoice_id, repay_term_no=self.term)


if __name__ == '__main__':
    unittest.main()
