import unittest
from src.impl.common.CheckBizImpl import *
from src.impl.baidu.BaiDuCreditFileBizImpl import *
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


    """ 测试步骤 """

    def test_repay(self):
        """ 测试步骤 """
        # 授信-授信校验-放款-放款校验
        # repay_mode='02'随借随还，repay_mode='05'等额本息
        # repay_type: 还款类型，01：按期还款；02：提前结清；03：逾期还款；04：提前还当期；05：提前还部分（仅支持随借随还）
        repay_mode = '05'
        repay_date = '2023-06-05'
        self.term = 1
        repay_type = '02'
        loan_invoice_id = '000LI0001424829632315448038'
        baidu = BaiduRepayFile(data, repay_mode=repay_mode, repay_date=repay_date, repay_term_no=self.term,
                               repay_type=repay_type, loan_invoice_id=loan_invoice_id)
        baidu.start_repay_file()
        self.loan_invoice_id = loan_invoice_id if loan_invoice_id else baidu.get_invoice_info()[1]
        # 清除分片流水
        self.MysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
        self.MysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
        self.MysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')
        # 设置账务日期
        account_date = str(repay_date).replace("-", '')
        last_date = str(get_custom_day(-1, repay_date)).replace("-", '')
        next_date = str(get_custom_day(1, repay_date)).replace("-", '')
        self.MysqlBizImpl.update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", last_date=last_date,
                                account_date=account_date, next_date=next_date, cutday_time=repay_date + ' 00:10:00')
        self.MysqlBizImpl.get_asset_job_ctl_info(job_date=last_date.replace('-', ''))
        # 删除分片流水
        self.redis.del_assert_repay_keys()
        # 执行日终资产任务
        self.job.update_job("资产日终任务流", group=6, executeBizDateType='CUSTOMER', executeBizDate=last_date)
        self.job.trigger_job("资产日终任务流", group=6)
        time.sleep(10)
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
