import unittest
from src.impl.common.CheckBizImpl import *
from src.impl.JieBei.JieBeiCreateFileBizImpl import *
from utils.JobCenter import *
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    def setUp(self):
        self.CheckBizImpl = CheckBizImpl()
        self.job = JOB()

    """ 测试步骤 """
    def test_loan(self):
        jb_repay_file = loandetailFile(data=data)
        self.third_loan_no = jb_repay_file.contract_no
        # 创建还款文件
        jb_repay_file.start_repayDetailFile()
        # 执行还款消息入还款表任务
        self.job.update_job('借呗还款消息分组入还款表任务', group=13, job_type='VIRTUAL_JOB', executeBizDateType='TODAY')
        self.job.trigger_job('借呗还款消息分组入还款表任务', group=13, job_type='VIRTUAL_JOB')
        # 执行还款消息入还款额度恢复表任务
        self.job.update_job('还款消息入还款额度恢复表任务', group=13, job_type='VIRTUAL_JOB', executeBizDateType='TODAY')
        self.job.trigger_job('还款消息入还款额度恢复表任务', group=13, job_type='VIRTUAL_JOB')
        time.sleep(3)
        # 执行渠道还款任务
        self.job.update_job('渠道还款任务', group=13, job_type='VIRTUAL_JOB', executeBizDateType='TODAY')
        self.job.trigger_job('渠道还款任务', group=13, job_type='VIRTUAL_JOB')
        # 执行渠道还款额度恢复任务
        self.job.update_job('渠道还款额度恢复任务', group=13, job_type='VIRTUAL_JOB', executeBizDateType='TODAY')
        self.job.trigger_job('渠道还款额度恢复任务', group=13, job_type='VIRTUAL_JOB')


    """ 后置条件处理 """
    def tearDown(self):
        # 数据库层校验支用状态-使用中
        self.CheckBizImpl.check_channel_repay_status(third_loan_id=self.third_loan_no)


if __name__ == '__main__':
    unittest.main()
