# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：RepayPublicBizImpl.py
@Author  ：jccfc
@Date    ：2022/5/31 11:10 
"""
import time

from src.enums.EnumsCommon import ProductEnum, EnumLoanStatus
from src.impl.MeiTuan.MeiTuanSynBizImpl import MeiTuanSynBizImpl
from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils.JobCenter import JOB
from utils.Logger import MyLog
from utils.Models import get_custom_day
from utils.Redis import Redis


class RepayPublicBizImpl:
    def __init__(self):
        self.MysqlBizImpl = MysqlBizImpl()
        self.meiTuanSynBizImpl = MeiTuanSynBizImpl()
        self.log = MyLog().get_log()
        self.redis = Redis()
        self.job = JOB()
        self.checkBizImpl = CheckBizImpl()

    def pre_repay_config(self, repayDate=None):
        """
        预制各产品的逾期数据
        @param repayDate: 放款时间 格式："2021-12-12", 默认当前时间
        @return:
        """
        self.log.info("设置大会计时间,账务时间=repay_date")
        repayDate = repayDate if repayDate else time.strftime('%Y-%m-%d', time.localtime())
        repay_date_format = repayDate.replace('-', '')
        last_date = str(get_custom_day(-1, repayDate)).replace("-", '')
        next_date = str(get_custom_day(1, repayDate)).replace("-", '')
        cut_time = repayDate + " 00:10:00"
        self.MysqlBizImpl.update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", last_date=last_date,
                                                       account_date=repay_date_format, next_date=next_date,
                                                       cutday_time=cut_time)

        self.log.info('清除分片流水')
        self.MysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
        self.MysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
        self.MysqlBizImpl.del_assert_repay_history_data(repay_date_format)

        self.log.info("删除redis中资产账务时间 key=000:ACCT:SysInfo:BIGACCT、000:ACCT:AccountDate:BIGACCT")
        self.redis.del_assert_repay_keys()

        self.log.info('新增资产卸数记录')
        self.MysqlBizImpl.get_asset_job_ctl_info(job_date=last_date)

        self.log.info("执行账务日终任务")
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
            self.meiTuanSynBizImpl.pre_meituan_Loan(loan_date=loan_date)
            loan_invoice_id = self.meiTuanSynBizImpl.globalMap.get('meituan_loan_invoice_id')
            loanNo = self.meiTuanSynBizImpl.globalMap.get('meituan_loanNo')
            loan_date = self.meiTuanSynBizImpl.globalMap.get('loan_date')

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