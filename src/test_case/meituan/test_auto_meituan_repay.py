# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：test_auto_meituan_repay.py
@Author  ：jccfc
@Date    ：2022/3/07 13:59
"""
import allure
import pytest

from src.enums.EnumsCommon import EnumLoanStatus
from src.impl.MeiTuan.MeiTuan_CreateFileBizImpl import MeiTuanRepayFile
from utils.Logger import MyLog
from utils.Models import get_custom_day

log = MyLog().get_log()


@pytest.mark.meituan
@pytest.mark.smoke
@allure.feature("还款模块")
@allure.story("美团还款")
@allure.title("逾期还款-按期还款-提前结清")  # 标题
class TestCase(object):

    @allure.step("逾期还款")  # 测试报告显示步骤
    @pytest.mark.run(order=1)
    def test_overdue_repay(self, get_base_data_meituan, mysqlBizImpl, checkBizImpl, meiTuanSynBizImpl, redis, job):
        data = get_base_data_meituan
        with allure.step("准备逾期借据数据"):
            res = meiTuanSynBizImpl
            repay_date = get_custom_day(40, date=res['loan_date'])
            loan_invoice_id = res['loan_invoice_id']
            repay_date_ove = repay_date.replace('-', '')
            with allure.step("设置大会计时间,账务时间=repay_date"):
                last_date = str(get_custom_day(-1, repay_date)).replace("-", '')
                next_date = str(get_custom_day(1, repay_date)).replace("-", '')
                mysqlBizImpl.update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", last_date=last_date,
                                                          account_date=repay_date_ove, next_date=next_date)

            with allure.step('清除分片流水'):
                mysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
                mysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
                mysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')

            with allure.step("删除redis中资产账务时间 key=000:ACCT:SysInfo:BIGACCT、000:ACCT:AccountDate:BIGACCT"):
                redis.del_assert_repay_keys()

            with allure.step("执行账务日终任务"):
                job.update_job("资产日终任务流", group=6, executeBizDateType='CUSTOMER', executeBizDate=last_date)
                job.trigger_job("资产日终任务流", group=6)

            with allure.step("校验当前借据是否已逾期：15s轮训等待"):
                log.info('验当前借据状态')
                status = mysqlBizImpl.get_loan_apply_status(EnumLoanStatus.OVERDUE.value,
                                                            thirdpart_user_id=data['userId'])
                assert EnumLoanStatus.OVERDUE.value == status, '当前支用单状态不为逾期状态，请检查账务日终任务执行结果'

        with allure.step('准备还款条件'):
            with allure.step('新增资产卸数记录'):
                mysqlBizImpl.get_asset_job_ctl_info(job_date=last_date)

            with allure.step('生成逾期还款文件并上传SFTP'):
                MeiTuanRepayFile(data, repay_type='03', repay_term_no='1', repay_date=repay_date)

            with allure.step('执行任务流下载还款对账文件入库'):
                job.update_job('美团期数动账单解析任务流', executeBizDateType='CUSTOMER', executeBizDate=repay_date_ove)
                job.trigger_job('美团期数动账单解析任务流')

            with allure.step('更新还款通知表业务日期'):
                checkBizImpl.get_repay_notice_info(loan_invoice_id=loan_invoice_id, repay_term_no='1')
                key = "loan_invoice_id = '{}' and repay_term_no='1'".format(loan_invoice_id)
                mysqlBizImpl.update_credit_database_info('credit_ctrip_repay_notice_info', attr=key,
                                                         business_date=repay_date_ove)

        with allure.step('执行还款&结果校验'):
            with allure.step('执行任务流还款入账'):
                job.update_job('三方还款任务流', executeBizDateType='CUSTOMER', executeBizDate=repay_date_ove)
                job.trigger_job('三方还款任务流')

            with allure.step('检查是否还款成功'):
                checkBizImpl.check_repay_notice_status(loan_invoice_id=loan_invoice_id, repay_term_no='1')

    @allure.step("按期还款")  # 测试报告显示步骤
    @pytest.mark.run(order=2)
    def test_billDate_repay(self, get_base_data_meituan, mysqlBizImpl, checkBizImpl, meiTuanSynBizImpl, redis, job):
        data = get_base_data_meituan
        with allure.step('准备账单日还款条件'):
            loan_invoice_id = meiTuanSynBizImpl['loan_invoice_id']
            asset_repay_plan = mysqlBizImpl.get_asset_database_info("asset_repay_plan",
                                                                    loan_invoice_id=loan_invoice_id, current_num=2)
            repay_date = str(asset_repay_plan["pre_repay_date"])
            repay_date_bill = repay_date.replace('-', '')
            with allure.step("设置大会计时间,账务时间=repay_date"):
                last_date = str(get_custom_day(-1, repay_date)).replace("-", '')
                next_date = str(get_custom_day(1, repay_date)).replace("-", '')
                mysqlBizImpl.update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", last_date=last_date,
                                                          account_date=repay_date_bill, next_date=next_date)
            with allure.step('新增资产卸数记录'):
                mysqlBizImpl.get_asset_job_ctl_info(job_date=last_date)

            with allure.step("删除redis中的账务时间缓存"):
                redis.del_assert_repay_keys()

            with allure.step('生成逾期还款文件并上传SFTP'):
                MeiTuanRepayFile(data, repay_type='01', repay_term_no='2')

            with allure.step('清除分片流水'):
                mysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
                mysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
                mysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')

            with allure.step('执行任务流下载还款对账文件入库'):
                job.update_job('美团期数动账单解析任务流', executeBizDateType='CUSTOMER', executeBizDate=repay_date_bill)
                job.trigger_job('美团期数动账单解析任务流')

            with allure.step('更新还款通知表业务日期'):
                checkBizImpl.get_repay_notice_info(loan_invoice_id=loan_invoice_id, repay_term_no='2')
                key = "loan_invoice_id = '{}' and repay_term_no='2'".format(loan_invoice_id)
                mysqlBizImpl.update_credit_database_info('credit_ctrip_repay_notice_info', attr=key,
                                                         business_date=repay_date_bill)

        with allure.step('执行还款&结果校验'):
            with allure.step('执行任务流还款入账'):
                job.update_job('三方还款任务流', executeBizDateType='CUSTOMER', executeBizDate=repay_date_bill)
                job.trigger_job('三方还款任务流')

            with allure.step('检查是否还款成功'):
                checkBizImpl.check_repay_notice_status(loan_invoice_id=loan_invoice_id, repay_term_no='2')

    @allure.step("提前结清")  # 测试报告显示步骤
    @pytest.mark.run(order=3)
    def test_advance_settle_repay(self, get_base_data_meituan, mysqlBizImpl, checkBizImpl, meiTuanSynBizImpl, redis,
                                  job):
        data = get_base_data_meituan
        with allure.step('准备提前结清还款条件'):
            loan_invoice_id = meiTuanSynBizImpl['loan_invoice_id']
            asset_repay_plan = mysqlBizImpl.get_asset_database_info("asset_repay_plan",
                                                                    loan_invoice_id=loan_invoice_id, current_num=3)
            repay_date = str(asset_repay_plan["pre_repay_date"])
            repay_date = get_custom_day(-1, repay_date)
            repay_date_settle = repay_date.replace('-', '')
            with allure.step("设置大会计时间,账务时间=repay_date"):
                last_date = str(get_custom_day(-1, repay_date)).replace("-", '')
                next_date = str(get_custom_day(1, repay_date)).replace("-", '')
                mysqlBizImpl.update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", last_date=last_date,
                                                          account_date=repay_date_settle, next_date=next_date)
            with allure.step('新增资产卸数记录'):
                mysqlBizImpl.get_asset_job_ctl_info(job_date=last_date)

            with allure.step("删除redis中的账务时间缓存"):
                redis.del_assert_repay_keys()

            with allure.step('生成逾期还款文件并上传SFTP'):
                MeiTuanRepayFile(data, repay_type='02', repay_term_no='3', repay_date=repay_date)

            with allure.step('清除分片流水'):
                mysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
                mysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
                mysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')

            with allure.step('执行任务流下载还款对账文件入库'):
                job.update_job('美团期数动账单解析任务流', executeBizDateType='CUSTOMER', executeBizDate=repay_date_settle)
                job.trigger_job('美团期数动账单解析任务流')

            with allure.step('更新还款通知表业务日期'):
                checkBizImpl.get_repay_notice_info(loan_invoice_id=loan_invoice_id, repay_term_no='3')
                key = "loan_invoice_id = '{}' and repay_term_no='3'".format(loan_invoice_id)
                mysqlBizImpl.update_credit_database_info('credit_ctrip_repay_notice_info', attr=key,
                                                         business_date=repay_date_settle)

        with allure.step('执行还款&结果校验'):
            with allure.step('执行任务流还款入账'):
                job.update_job('三方还款任务流', executeBizDateType='CUSTOMER', executeBizDate=repay_date_settle)
                job.trigger_job('三方还款任务流')

            with allure.step('检查是否还款成功'):
                checkBizImpl.check_repay_notice_status(loan_invoice_id=loan_invoice_id, repay_term_no='3')


if __name__ == "__main__":
    pytest.main(['test_auto_meituan_repay.py'])
