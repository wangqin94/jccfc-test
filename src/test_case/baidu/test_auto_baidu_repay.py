# -*- coding: utf-8 -*-
# -----------------------------------------------------
# 百度还款流程
# -----------------------------------------------------
import allure
import pytest
from src.impl.baidu.BaiDuCreditFileBizImpl import BaiduRepayFile
from src.enums.EnumsCommon import *
from utils.Models import *


class TestCase(object):

    @pytest.mark.baidu
    @allure.step("逾期还款")
    def test_overdue_repay(self, baiduBizSynImpl, mysqlBizImpl, job, redis):
        data = baiduBizSynImpl
        period = 1
        asset_repay_plan = mysqlBizImpl.get_asset_database_info("asset_repay_plan",
                                                                loan_invoice_id=data['loan_no'], current_num=period)
        repay_date_bill = str(asset_repay_plan["pre_repay_date"])
        repay_date_ove = get_custom_day(10, repay_date_bill)
        with allure.step("设置大会计时间,账务时间=repay_date"):
            account_date = str(repay_date_ove).replace("-", '')
            last_date = str(get_custom_day(-1, repay_date_ove)).replace("-", '')
            next_date = str(get_custom_day(1, repay_date_ove)).replace("-", '')
            mysqlBizImpl.update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", last_date=last_date,
                                                      account_date=account_date, next_date=next_date)
        with allure.step('更新资产卸数'):
            mysqlBizImpl.get_asset_job_ctl_info(job_date=last_date.replace('-', ''))

        with allure.step("清理分片流水"):
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
            mysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')

        with allure.step("删除redis 大会计"):
            redis.del_assert_repay_keys()

        with allure.step("执行账务日终任务"):
            job.update_job("资产日终任务流", group=6, executeBizDateType='CUSTOMER', executeBizDate=last_date)
            job.trigger_job("资产日终任务流", group=6)
            time.sleep(10)

        with allure.step("校验当前借据状态"):
            time.sleep(5)
            info = mysqlBizImpl.get_asset_database_info('asset_loan_invoice_info', loan_invoice_id=data['loan_no'])
            assert EnumLoanInvoiceStatus.OVERDUE.value == info['loan_invoice_status'], "借据状态非逾期"

        with allure.step('生成逾期还款文件并上传金山云'):
            bd = BaiduRepayFile(data=data, repay_date=repay_date_ove, repay_type='03', repay_term_no=period)
            bd.start_repay_file()

        with allure.step('更新百度还款计划'):
            key2 = "loan_id in (select third_loan_no from credit_third_wait_loan_deal_info where certificate_no = '" \
                   + data['cer_no'] + "')"
            mysqlBizImpl.update_credit_database_info('credit_baid_repay_plan_info', attr=key2,
                                                     batch_date=repay_date_ove.replace('-', ''))

        with allure.step('执行任务流下载还款对账文件入库'):
            job.update_job('百度还款对账文件下载任务流', executeBizDate=repay_date_ove.replace('-', ''),
                           executeBizDateType='CUSTOMER')
            job.trigger_job('百度还款对账文件下载任务流')
            time.sleep(5)

        with allure.step('更新还款通知表业务日期'):
            key = "loan_invoice_id = '" + data['loan_no'] + "' and notice_type = '1' order by create_time desc limit 1"
            mysqlBizImpl.update_credit_database_info('credit_ctrip_repay_notice_info', attr=key,
                                                     business_date=repay_date_ove.replace('-', ''))

        with allure.step('执行任务流还款入账'):
            job.update_job('三方还款任务流', executeBizDate=repay_date_ove.replace('-', ''),
                           executeBizDateType='CUSTOMER')
            job.trigger_job('三方还款任务流')
            time.sleep(5)

        with allure.step('执行任务流还款入账'):
            job.update_job('三方还款任务流', executeBizDate=repay_date_ove.replace('-', ''),
                           executeBizDateType='CUSTOMER')
            job.trigger_job('三方还款任务流')
            time.sleep(5)

        with allure.step('检查是否还款成功'):
            info = mysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                        loan_invoice_id=data['loan_no'], current_num=period)
            assert EnumRepayPlanStatus.OVERDUE_REPAY.value == info['repay_plan_status'], '还款失败'

    @pytest.mark.baidu
    @allure.step("按期还款")
    def test_billDate_repay(self, baiduBizSynImpl, mysqlBizImpl, job, redis):
        data = baiduBizSynImpl
        period = 2
        asset_repay_plan = mysqlBizImpl.get_asset_database_info("asset_repay_plan",
                                                                loan_invoice_id=data['loan_no'], current_num=period)
        repay_date_bill = str(asset_repay_plan["pre_repay_date"])
        with allure.step("设置大会计时间,账务时间=repay_date"):
            account_date = repay_date_bill.replace("-", '')
            last_date = str(get_custom_day(-1, repay_date_bill)).replace("-", '')
            next_date = str(get_custom_day(1, repay_date_bill)).replace("-", '')
            mysqlBizImpl.update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", last_date=last_date,
                                                      account_date=account_date, next_date=next_date)
        with allure.step('更新资产卸数'):
            mysqlBizImpl.get_asset_job_ctl_info(job_date=last_date.replace('-', ''))

        with allure.step('清除分片流水'):
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
            mysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')

        with allure.step("删除redis 大会计"):
            redis.del_assert_repay_keys()

        with allure.step('生成按期还款文件并上传金山云'):
            bd = BaiduRepayFile(data=data, repay_date=repay_date_bill, repay_type='01', repay_term_no=period)
            bd.start_repay_file()

        with allure.step('更新百度还款计划'):
            key2 = "loan_id in (select third_loan_no from credit_third_wait_loan_deal_info where certificate_no = '" \
                   + data['cer_no'] + "')"
            mysqlBizImpl.update_credit_database_info('credit_baid_repay_plan_info', attr=key2,
                                                     batch_date=repay_date_bill.replace('-', ''))

        with allure.step('执行任务流下载还款对账文件入库'):
            job.update_job('百度还款对账文件下载任务流', executeBizDate=repay_date_bill.replace('-', ''),
                           executeBizDateType='CUSTOMER')
            job.trigger_job('百度还款对账文件下载任务流')
            time.sleep(10)

        with allure.step('更新还款通知表业务日期'):
            key = "loan_invoice_id = '" + data['loan_no'] + "' and notice_type = '1' order by create_time desc limit 1"
            mysqlBizImpl.update_credit_database_info('credit_ctrip_repay_notice_info', attr=key,
                                                     business_date=repay_date_bill.replace('-', ''))
        with allure.step('执行任务流还款入账'):
            job.update_job('三方还款任务流', executeBizDate=repay_date_bill.replace('-', ''),
                           executeBizDateType='CUSTOMER')
            job.trigger_job('三方还款任务流')
            time.sleep(5)

        with allure.step('执行任务流还款入账'):
            job.update_job('三方还款任务流', executeBizDate=repay_date_bill.replace('-', ''),
                           executeBizDateType='CUSTOMER')
            job.trigger_job('三方还款任务流')
            time.sleep(5)

        with allure.step('检查是否还款成功'):
            info = mysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                        loan_invoice_id=data['loan_no'], current_num=period)
            assert EnumRepayPlanStatus.REPAY.value == info['repay_plan_status'], '还款失败'

    @pytest.mark.baidu
    @allure.step("提前结清")
    def test_settle_repay(self, baiduBizSynImpl, mysqlBizImpl, job, redis):
        data = baiduBizSynImpl
        period = 3
        asset_repay_plan = mysqlBizImpl.get_asset_database_info("asset_repay_plan",
                                                                loan_invoice_id=data['loan_no'], current_num=period)
        repay_date_bill = str(asset_repay_plan["pre_repay_date"])
        repay_date_settle = get_custom_day(-1, repay_date_bill)
        with allure.step("设置大会计时间,账务时间=repay_date"):
            account_date = repay_date_settle.replace("-", '')
            last_date = str(get_custom_day(-1, repay_date_settle)).replace("-", '')
            next_date = str(get_custom_day(1, repay_date_settle)).replace("-", '')
            mysqlBizImpl.update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", last_date=last_date,
                                                      account_date=account_date, next_date=next_date)
        with allure.step('更新资产卸数'):
            mysqlBizImpl.get_asset_job_ctl_info(job_date=last_date.replace('-', ''))

        with allure.step('清除分片流水'):
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
            mysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')

        with allure.step("删除redis 大会计"):
            redis.del_assert_repay_keys()

        with allure.step('生成提前结清还款文件并上传金山云'):
            bd = BaiduRepayFile(data=data, repay_date=repay_date_settle, repay_type='02', repay_term_no=period)
            bd.start_repay_file()

        with allure.step('更新百度还款计划'):
            key2 = "loan_id in (select third_loan_no from credit_third_wait_loan_deal_info where certificate_no = '" \
                   + data['cer_no'] + "')"
            mysqlBizImpl.update_credit_database_info('credit_baid_repay_plan_info', attr=key2,
                                                     batch_date=repay_date_settle.replace('-', ''))

        with allure.step('执行任务流下载还款对账文件入库'):
            job.update_job('百度还款对账文件下载任务流', executeBizDate=repay_date_settle.replace('-', ''),
                           executeBizDateType='CUSTOMER')
            job.trigger_job('百度还款对账文件下载任务流')
            time.sleep(5)

        with allure.step('更新还款通知表业务日期'):
            key = "loan_invoice_id = '" + data['loan_no'] + "' and notice_type = '1' order by create_time desc limit 1"
            mysqlBizImpl.update_credit_database_info('credit_ctrip_repay_notice_info', attr=key,
                                                     business_date=repay_date_settle.replace('-', ''))

        with allure.step('执行任务流还款入账'):
            job.update_job('三方还款任务流', executeBizDate=repay_date_settle.replace('-', ''),
                           executeBizDateType='CUSTOMER')
            job.trigger_job('三方还款任务流')
            time.sleep(5)

        with allure.step('执行任务流还款入账'):
            job.update_job('三方还款任务流', executeBizDate=repay_date_settle.replace('-', ''),
                           executeBizDateType='CUSTOMER')
            job.trigger_job('三方还款任务流')
            time.sleep(5)

        with allure.step("校验当前借据状态"):
            info = mysqlBizImpl.get_asset_database_info('asset_loan_invoice_info',
                                                        loan_invoice_id=data['loan_no'])
            assert EnumLoanInvoiceStatus.SETTLE.value == info['loan_invoice_status'], "借据状态非结清"


if __name__ == '__main__':
    pytest.main(['test_auto_baidu_repay.py'])
