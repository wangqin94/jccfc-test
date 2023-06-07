import unittest
from src.impl.common.CheckBizImpl import *
from src.impl.baidu.BaiDuBizImpl import *
from src.impl.baidu.BaiDuCreditFileBizImpl import *
from utils.JobCenter import *
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        self.CheckBizImpl = CheckBizImpl()
        self.MysqlBizImpl = MysqlBizImpl()
        self.job = JOB()

    """ 测试步骤 """

    def test_loan(self):
        """ 测试步骤 """
        # 授信-授信校验-放款-放款校验
        # repay_mode='02'随借随还，repay_mode='05'等额本息
        repay_mode = '05'
        loan_date = '20230507'
        baidu = BaiDuBizImpl(data=None, repay_mode=repay_mode)

        # 发起授信申请
        self.applyId = baidu.credit(initialAmount=1000000)['credit_apply_id']
        # 检查授信状态
        time.sleep(10)
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.applyId)
        # 发起支用刚申请
        self.loan_apply_id = baidu.loan(cashAmount=100000, term=6)['loan_apply_id']
        # 检查支用状态为待放款
        self.CheckBizImpl.check_file_loan_apply_status(loan_apply_serial_id=self.loan_apply_id)
        # 上传文件
        baidufile = BaiduFile(baidu.data, cur_date=loan_date, loan_record=0, repay_mode=repay_mode)
        baidufile.start()
        # 清除分片流水
        self.MysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
        self.MysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
        self.MysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')
        # 执行任务流下载文件入库
        self.job.update_job('百度放款对账下载任务流-测试', executeBizDate=loan_date.replace('-', ''))
        self.job.trigger_job('百度放款对账下载任务流-测试')
        time.sleep(5)
        # 检查是否入三方待建账信息
        self.CheckBizImpl.check_third_wait_loan_status(certificate_no=baidu.data['cer_no'])
        # 执行任务流放款
        self.job.update_job('线下自动放款', executeBizDate=datetime.now().strftime('%Y%m%d'))
        self.job.trigger_job('线下自动放款')


    """ 后置条件处理 """
    def tearDown(self):
        time.sleep(5)
        # 数据库层校验支用状态-使用中
        self.CheckBizImpl.check_loan_apply_status(loan_apply_serial_id=self.loan_apply_id)
        sql = "update asset_loan_invoice_info set apply_loan_date = date_format(begin_profit_date,'%Y%m%d') " \
              "where apply_loan_date != date_format(begin_profit_date,'%Y%m%d')"
        self.MysqlBizImpl.mysql_asset.update(sql)


if __name__ == '__main__':
    unittest.main()
