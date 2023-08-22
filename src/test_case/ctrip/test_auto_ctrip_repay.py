import logging

import allure
import pytest

from src.enums.EnumsCommon import *
from src.impl.common.MysqlBizImpl import *
from utils.Apollo import *

log = logging.getLogger(__name__)


@allure.step('前置操作：预置放款数据')
@pytest.fixture(scope="class")
def pre_loan_repay_data(ctripBizImpl, ctripCreditCheckBizImpl, ctripLoanCheckBizImpl):
    """ 测试步骤 """
    with allure.step("修改apollo放款mock"):
        apollo_data = dict()
        apollo_data['credit.loan.trade.date.mock'] = "false"
        Apollo().update_config(appId='loan2.1-public', namespace='JCXF.system', **apollo_data)

    with allure.step("设置credit还款mock时间, 第3期账单日"):
        # 设置apollo还款mock时间 默认当前时间
        apollo_data = dict()
        apollo_data['credit.mock.repay.trade.date'] = "false"  # credit.mock.repay.trade.date
        Apollo().update_config(appId='loan2.1-public', namespace='JCXF.system', **apollo_data)

    with allure.step("发起授信申请"):
        creditRes = ctripBizImpl.credit(advice_amount=30000)
        ctripBizImpl.update_apollo_amount()
        log.info(f"授信申请接口结果----：{creditRes}")
        creditStatus = creditRes['credit_status']
        assert creditStatus == '0', "返回0说明授信申请成功"

    with allure.step("数据库层校验授信结果是否符合预期"):
        time.sleep(20)
        creditApply = ctripCreditCheckBizImpl.check_credit_apply_status(thirdpart_user_id=creditRes['open_id'])
        ctripCreditCheckBizImpl.checkCreditApply1(creditApply)
        ctripCreditCheckBizImpl.checkCreditInfo1(thirdpart_apply_id=creditApply['credit_apply_serial_id'])

    with allure.step("发起支用申请"):
        loanRes = ctripBizImpl.loan(loan_amount=600, first_repay_date=ctripLoanCheckBizImpl.get_zhixin_bill_day())
        log.info(f"支用申请结果----：{loanRes}")
        time.sleep(10)
        loanStatus = loanRes['loan_status']
        assert loanStatus == '0', "返回0说明支用申请成功"

    with allure.step("数据库层校验支用结果是否符合预期"):
        time.sleep(20)
        loanApply = ctripLoanCheckBizImpl.check_loan_apply_status(thirdpart_user_id=creditRes['open_id'])
        ctripLoanCheckBizImpl.checkLoanApply1(loanApply)
        return loanApply


@pytest.mark.ctrip
@pytest.mark.smoke
@allure.feature("还款模块")
@allure.story("携程渠道还款")
@allure.title("按期还款-逾期还款-提前结清")  # 标题
class TestCase(object):

    @allure.step("按期还款")  # 测试报告显示步骤
    @pytest.mark.run(order=1)
    def test_overdue_repay(self, mysqlBizImpl, job, ctripBizImpl, pre_loan_repay_data):
        loanApply = pre_loan_repay_data
        asset_repay_plan = mysqlBizImpl.get_asset_database_info("asset_repay_plan",
                                                                borrower_user_id=loanApply["user_id"], current_num=1)
        repay_date_ove = str(asset_repay_plan["pre_repay_date"])
        account_date = str(repay_date_ove).replace("-", '')

        with allure.step('更新还款通知表业务日期'):
            ctripBizImpl.repay_notice(repay_mode="1", repay_term_no="1")
            time.sleep(5)
            key1 = "third_user_id = '" + loanApply["thirdpart_user_id"] + "'"
            repay_notic = mysqlBizImpl.get_credit_data_info('credit_ctrip_repay_notice_info', key=key1)
            mysqlBizImpl.update_credit_database_info('credit_ctrip_repay_notice_info', business_date=account_date,
                                                     attr="loan_invoice_id = '" + repay_notic["loan_invoice_id"] + "'")

        with allure.step('执行任务流还款入账'):
            job.update_job('三方还款任务流', executeBizDate=repay_date_ove.replace('-', ''))
            job.trigger_job('三方还款任务流')
            time.sleep(5)

        with allure.step('检查是否还款成功'):
            time.sleep(20)
            info = mysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                        loan_invoice_id=repay_notic['loan_invoice_id'], current_num=1)
            assert info["repay_plan_status"] == "3", "还款成功"

    @allure.step("逾期还款")  # 测试报告显示步骤
    @pytest.mark.run(order=2)
    def test_billDate_repay(self, mysqlBizImpl, job, ctripBizImpl, pre_loan_repay_data):
        loanApply = pre_loan_repay_data
        repay_date_bill = get_next_day(70).strftime('%Y-%m-%d')
        account_date = str(repay_date_bill).replace("-", '')

        with allure.step('更新还款通知表业务日期'):
            ctripBizImpl.repay_notice(repay_mode="3", repay_term_no="2", repay_date=repay_date_bill)
            key1 = "third_user_id = '" + loanApply["thirdpart_user_id"] + "'"
            repay_notic = mysqlBizImpl.get_credit_data_info('credit_ctrip_repay_notice_info', key=key1)
            mysqlBizImpl.update_credit_database_info('credit_ctrip_repay_notice_info', business_date=account_date,
                                                     attr="loan_invoice_id = '" + repay_notic[
                                                         "loan_invoice_id"] + "' and repay_term_no = '2'")

        with allure.step("校验当前借据是否已逾期：15s查证等待"):
            log.info('验当前借据状态')
            status = mysqlBizImpl.get_loan_apply_status(EnumLoanStatus.OVERDUE.value, user_id=loanApply['user_id'])
            assert EnumLoanStatus.OVERDUE.value == status, '当前支用单状态不为逾期状态，请检查账务日终任务执行结果'

        with allure.step('执行任务流还款入账'):
            job.update_job('三方还款任务流', executeBizDate=repay_date_bill.replace('-', ''))
            job.trigger_job('三方还款任务流')
            time.sleep(5)

        with allure.step('检查是否还款成功'):
            info = mysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                        loan_invoice_id=repay_notic['loan_invoice_id'], current_num=2)
            assert info["repay_plan_status"] == "6", "还款成功"

    @allure.step("提前结清")  # 测试报告显示步骤
    @pytest.mark.run(order=3)
    def test_advance_repay(self, mysqlBizImpl, job, ctripBizImpl, pre_loan_repay_data):
        loanApply = pre_loan_repay_data
        repay_date_bill = get_next_day(70).strftime('%Y-%m-%d')
        account_date = str(repay_date_bill).replace("-", '')

        with allure.step('更新还款通知表业务日期'):
            ctripBizImpl.repay_notice(repay_mode="2", repay_term_no="3", repay_date=repay_date_bill)
            key1 = "third_user_id = '" + loanApply["thirdpart_user_id"] + "'"
            repay_notic = mysqlBizImpl.get_credit_data_info('credit_ctrip_repay_notice_info', key=key1)
            mysqlBizImpl.update_credit_database_info('credit_ctrip_repay_notice_info', business_date=account_date,
                                                     attr="loan_invoice_id = '" + repay_notic[
                                                         "loan_invoice_id"] + "' and repay_term_no = '3'")
            time.sleep(5)

        with allure.step('执行任务流还款入账'):
            job.update_job('三方还款任务流', executeBizDate=repay_date_bill.replace('-', ''))
            job.trigger_job('三方还款任务流')
            time.sleep(5)

        with allure.step('检查是否还款成功'):
            info = mysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                        loan_invoice_id=repay_notic['loan_invoice_id'],
                                                        current_num=3)
            assert info["repay_plan_status"] == "3", "还款成功"


if __name__ == '__main__':
    pytest.main(['test_auto_ctrip_repay.py'])
