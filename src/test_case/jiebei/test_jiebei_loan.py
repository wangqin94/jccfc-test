import unittest
from src.impl.common.CheckBizImpl import *
from src.impl.JieBei.JieBeiCheckBizImpl import *
from src.impl.JieBei.JieBeiCreateFileBizImpl import *
from utils.JobCenter import *
from utils.Redis import *
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    def setUp(self):
        self.CheckBizImpl = CheckBizImpl()
        self.job = JOB()
        self.redis = Redis()

    """ 测试步骤 """
    def test_loan(self):
        jb = JieBeiCheckBizImpl(data=None)
        jb_apply_file = creditFile(data=jb.data)
        jb_loanapply_file = loanApplyFile(data=jb.data)
        jb_loandetail_file = loandetailFile(data=jb.data)
        self.third_loan_no = jb_loandetail_file.contract_no
        # 初审
        jb.datapreCs()
        self.applyNo = jb.data['applyno']
        # 检查初审结果
        jb.jiebei_check_feature_detail('jc_cs_result', self.applyNo)
        # 复审
        jb.datapreFs(applyType='ADMIT_APPLY', tc_NoSource_ToPlatformOne='Y')
        # 检查复审结果
        jb.jiebei_check_feature_detail('jc_fs_result', self.applyNo)
        # 授信通知
        jb.creditNotice(bizType='ADMIT_APPLY', creditAmt=5000000)
        # 创建授信文件
        jb_apply_file.start_creditFile()
        # 执行授信对账文件处理任务
        self.job.update_job('借呗授信对账文件处理任务', group=13, job_type='VIRTUAL_JOB', executeBizDateType='TODAY')
        self.job.trigger_job('借呗授信对账文件处理任务', group=13, job_type='VIRTUAL_JOB')
        # 创建支用文件
        jb_loanapply_file.start_loanApplyFile()
        # 执行创建支用单任务
        self.job.update_job('借呗支用文件（创建支用单）处理任务', group=13, job_type='VIRTUAL_JOB', executeBizDateType='TODAY')
        self.job.trigger_job('借呗支用文件（创建支用单）处理任务', group=13, job_type='VIRTUAL_JOB')
        # 检查是否入三方待建账信息
        self.CheckBizImpl.check_loan_apply_status_with_expect('09', third_loan_invoice_id=self.third_loan_no)
        # 创建放款合约+分期
        jb_loandetail_file.start_loandetailFile()
        # 删除保存待放款redis
        self.redis.del_key('000:OBJ:SAVE_THIRD_LOAN:{}'.format(datetime.datetime.now().strftime('%Y%m%d')))
        # 创建放款失败+在途处理完成redis
        self.redis.add_key('000:OBJ:PUSH_LOAN_TO_ASSET:{}'.format(datetime.datetime.now().strftime('%Y%m%d')))
        # 执行放款登记入库
        self.job.update_job('借呗step5-借呗放款登记入线下待放款表任务流(轮询)', group=13, executeBizDateType='TODAY')
        self.job.trigger_job('借呗step5-借呗放款登记入线下待放款表任务流(轮询)', group=13)
        # 检查是否入三方待建账信息
        self.CheckBizImpl.check_third_wait_loan_status(third_loan_no=jb_loandetail_file.contract_no)
        # 执行任务流放款
        self.job.update_job('线下自动放款', executeBizDateType='TODAY')
        self.job.trigger_job('线下自动放款')


    """ 后置条件处理 """
    def tearDown(self):
        # 数据库层校验支用状态-使用中
        self.CheckBizImpl.check_loan_apply_status(third_loan_invoice_id=self.third_loan_no)


if __name__ == '__main__':
    unittest.main()
