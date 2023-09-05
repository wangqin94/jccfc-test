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
        self.MysqlBizImpl = MysqlBizImpl()

    """ 测试步骤 """
    def test_repay(self, repay_pri='3000000', repay_int='300', settle_status='CLEAR'):
        """
        还款流程
        :param repay_pri: 还款本金
        :param repay_int: 还款利息
        :param settle_status: 结清状态 NORMAL-正常，OVD-逾期，CLEAR-结清
        :return:
        """
        jb_repay_file = loandetailFile(data=data)
        self.third_loan_no = jb_repay_file.contract_no
        # 创建还款文件
        jb_repay_file.start_repayDetailFile(repay_pri=repay_pri, repay_int=repay_int, settle_status=settle_status)
        # 执行还款消息入还款表任务
        self.job.update_job('借呗还款消息分组入还款表任务', group=13, job_type='VIRTUAL_JOB', executeBizDateType='TODAY')
        self.job.trigger_job('借呗还款消息分组入还款表任务', group=13, job_type='VIRTUAL_JOB')
        # 执行还款消息入还款额度恢复表任务
        self.job.update_job('还款消息入还款额度恢复表任务', group=13, job_type='VIRTUAL_JOB', executeBizDateType='TODAY')
        self.job.trigger_job('还款消息入还款额度恢复表任务', group=13, job_type='VIRTUAL_JOB')
        # 检查还款消息是否入还款表
        self.CheckBizImpl.check_channel_repay_status_with_expect('00', third_loan_id=self.third_loan_no)
        # 设置资产卸数
        last_date = str(get_custom_day(-1, time.strftime('%Y-%m-%d', time.localtime()))).replace("-", '')
        self.MysqlBizImpl.get_asset_job_ctl_info(job_date=last_date)
        # 执行渠道还款任务
        self.job.update_job('渠道还款任务(新核心)', group=13, job_type='VIRTUAL_JOB', executeBizDateType='TODAY')
        self.job.trigger_job('渠道还款任务(新核心)', group=13, job_type='VIRTUAL_JOB')
        # 执行渠道还款额度恢复任务
        self.job.update_job('渠道还款额度恢复任务', group=13, job_type='VIRTUAL_JOB', executeBizDateType='TODAY')
        self.job.trigger_job('渠道还款额度恢复任务', group=13, job_type='VIRTUAL_JOB')

    """ 后置条件处理 """
    def tearDown(self):
        # 数据库层校验支用状态-使用中
        self.CheckBizImpl.check_channel_repay_status(third_loan_id=self.third_loan_no)


if __name__ == '__main__':
    unittest.main()
