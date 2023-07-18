# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：RepayPublicBizImpl.py
@Author  ：jccfc
@Date    ：2022/5/31 11:10 
"""
import time

from engine.MysqlInit import MysqlInit
from src.enums.EnumsCommon import ProductEnum, EnumLoanStatus
from src.impl.MeiTuan.MeiTuanSynBizImpl import MeiTuanSynBizImpl
from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils.Apollo import Apollo
from utils.JobCenter import JOB
from utils.Models import get_custom_day
from utils.Redis import Redis


class RepayPublicBizImpl(MysqlInit):
    def __init__(self):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()
        self.redis = Redis()
        self.job = JOB()
        self.apollo = Apollo()
        self.checkBizImpl = CheckBizImpl()

    def pre_repay_config(self, repayDate=None, repayMock=True):
        """
        预制各产品的逾期数据
        @param repayDate: 还款时间 格式："2021-12-12", 默认当前时间
        @param repayMock: 还款mock 默认关闭
        @return:
        """
        self.log.demsg("设置大会计时间,账务时间=repay_date")
        repayDate = repayDate if repayDate else time.strftime('%Y-%m-%d', time.localtime())
        repay_date_format = repayDate.replace('-', '')
        last_date = str(get_custom_day(-1, repayDate)).replace("-", '')
        next_date = str(get_custom_day(1, repayDate)).replace("-", '')
        cut_time = repayDate + " 00:10:00"
        self.MysqlBizImpl.update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", last_date=last_date,
                                                       account_date=repay_date_format, next_date=next_date,
                                                       cutday_time=cut_time)
        # 配置还款mock时间
        apollo_data = dict()
        apollo_data['credit.mock.repay.trade.date'] = repayMock  # credit.mock.repay.trade.date
        apollo_data['credit.mock.repay.date'] = "{} 12:00:00".format(repayDate)
        self.apollo.update_config(appId='loan2.1-public', namespace='JCXF.system', **apollo_data)

        self.log.demsg('清除分片流水')
        self.MysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
        self.MysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
        self.MysqlBizImpl.del_assert_repay_history_data(last_date)

        self.log.demsg("删除redis中资产账务时间 key=000:ACCT:SysInfo:BIGACCT、000:ACCT:AccountDate:BIGACCT")
        self.redis.del_assert_repay_keys()

        self.log.demsg('新增资产卸数记录')
        self.MysqlBizImpl.get_asset_job_ctl_info(job_date=last_date)

        self.log.demsg("执行摊销文件任务流")
        self.job.update_job("摊销文件任务流", group=5, executeBizDateType='CUSTOMER', executeBizDate=last_date)
        self.job.trigger_job("摊销文件任务流", group=5)
        time.sleep(3)

        self.log.demsg("执行账务日终任务")
        self.job.update_job("资产日终任务流", group=6, executeBizDateType='CUSTOMER', executeBizDate=last_date)
        self.job.trigger_job("资产日终任务流", group=6)
        time.sleep(5)  # 等待任务执行

    def pre_overdue_repay_data(self, productId, loan_date=None):
        """
        预制各产品的逾期数据
        @param productId: 产品ID
        @param loan_date: 放款时间 格式："2021-12-12", 默认当前时间
        @return:
        """
        loan_invoice_id = None
        loanNo = None
        if productId == ProductEnum.MEITUAN.value:
            meiTuanSynBizImpl = MeiTuanSynBizImpl()
            meiTuanSynBizImpl.pre_meituan_Loan(loan_date=loan_date)
            loan_invoice_id = meiTuanSynBizImpl.globalMap.get('meituan_loan_invoice_id')
            loanNo = meiTuanSynBizImpl.globalMap.get('meituan_loanNo')
            loan_date = meiTuanSynBizImpl.globalMap.get('loan_date')

        # 更新资产asset_loan_invoice_info放款时间,apply_loan_date=loan_date:
        loan_date_temp = str(loan_date).replace("-", '')
        self.MysqlBizImpl.update_asset_database_info('asset_loan_invoice_info', attr="loan_invoice_id='{}'".format(
            loan_invoice_id), apply_loan_date=loan_date_temp)

        self.log.demsg("准备逾期借据数据")
        repay_date = get_custom_day(40, date=loan_date)
        self.pre_repay_config(repay_date)

        self.log.info("校验当前借据是否已逾期：15s查证等待")
        status = self.MysqlBizImpl.get_loan_apply_status(EnumLoanStatus.OVERDUE.value,
                                                         thirdpart_apply_id=loanNo)
        self.checkBizImpl.check_asset_repay_plan_overdue_days(max_overdue_days=2, current_num='1',
                                                              loan_invoice_id=loan_invoice_id)
        assert EnumLoanStatus.OVERDUE.value == status, '当前支用单状态不为逾期状态，请检查账务日终任务执行结果'


if __name__ == '__main__':
    RepayPublicBizImpl().pre_repay_config(repayDate='2023-07-18')
