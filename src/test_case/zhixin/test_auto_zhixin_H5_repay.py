# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：test_auto_zhixin_H5_repay.py
@Author  ：jccfc
@Date    ：2022/1/26 16:38 
"""
from src.impl.YingJiZF.YingJiZFBizImpl import YingJiZFBizImpl
from src.impl.YingJiZF.YingJiZhiFuSynBizImpl import YingJiZhiFuSynBizImpl
from src.impl.common.CheckBizImpl import *
import allure
import pytest

from src.impl.common.MysqlBizImpl import *
from utils.Apollo import Apollo
from utils.JobCenter import *

log = MyLog().get_log()


@allure.step('前置操作：预置放款数据')
@pytest.fixture(scope="class", autouse=True)
def pre_loan_data(get_base_data_zhixin, zhiXinSynBizImpl, checkBizImpl, zhiXinCheckBizImpl, mysqlBizImpl, redis):
    data = get_base_data_zhixin
    job = JOB()
    apollo = Apollo()
    with allure.step("前置条件-准备借据：借据逾期2期且为账单日"):
        bill_date = zhiXinSynBizImpl.preLoanapply(month=3)
    with allure.step("设置H5还款mock时间, 第二期账单日"):
        repay_date = str(get_custom_month(-1, bill_date))
        apollo_data = dict()
        apollo_data['api.mock.repay.trade.date'] = "true"
        apollo_data['api.mock.repay.date'] = "{} 00:00:00".format(repay_date)
        apollo.update_config(appId='loan2.1-jcxf-app-web', **apollo_data)

    with allure.step("设置credit还款mock时间, 第二期账单日"):
        # 设置apollo还款mock时间 默认当前时间
        repay_date = str(get_custom_month(-1, bill_date))
        apollo_data = dict()
        apollo_data['credit.mock.repay.trade.date'] = "true"
        apollo_data['credit.mock.repay.date'] = "{} 00:00:00".format(repay_date)
        apollo.update_config(**apollo_data)

    with allure.step("设置大会计时间,账务时间=repay_date"):
        account_date = repay_date.replace("-", '')
        last_date = str(get_custom_day(-1, repay_date)).replace("-", '')
        next_date = str(get_custom_day(1, repay_date)).replace("-", '')
        cut_time = repay_date + " 00:10:00"
        mysqlBizImpl.update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", last_date=last_date,
                                                  account_date=account_date, next_date=next_date,
                                                  cutday_time=cut_time)
    with allure.step("清理asset流水记录"):
        mysqlBizImpl.del_assert_repay_history_data(account_date)

    with allure.step("删除redis 大会计 key=000:ACCT:SysInfo:BIGACCT"):
        redis.del_assert_repay_keys()

    with allure.step("执行账务日终任务"):
        job.update_job("资产日终任务流", group=6, executeBizDateType='CUSTOMER', executeBizDate=last_date)
        job.trigger_job("资产日终任务流", group=6)

    with allure.step("校验当前借据是否已逾期：15s轮训等待"):
        log.info('验当前借据状态')
        status = mysqlBizImpl.get_loan_apply_status(EnumLoanStatus.OVERDUE.value, thirdpart_user_id=data['userId'])
        loan_apply_info = mysqlBizImpl.get_loan_apply_info(thirdpart_user_id=data['userId'])
        credit_loan_invoice = mysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                    loan_apply_id=loan_apply_info['loan_apply_id'])
        checkBizImpl.check_asset_repay_plan_overdue_days(max_overdue_days=20, current_num='1',
                                                         loan_invoice_id=credit_loan_invoice['loan_invoice_id'])
        assert EnumLoanStatus.OVERDUE.value == status, '当前支用单状态不为逾期状态，请检查账务日终任务执行结果'
    return repay_date


@pytest.mark.zhixin
@pytest.mark.smoke
@allure.feature("还款模块")
@allure.story("锦程H5还款")
@allure.title("逾期还款-按期还款-提前结清")  # 标题
class TestCase(object):
    """ 预置条件处理 """
    """ 预置条件处理 """
    """ 测试步骤 """

    @allure.step("逾期还款")  # 测试报告显示步骤
    @pytest.mark.run(order=1)
    def test_overdue_repay(self, get_base_data_zhixin, mysqlBizImpl, checkBizImpl):
        data = get_base_data_zhixin
        with allure.step("发起逾期还款申请"):
            log.debug('发起逾期还款申请')
            loan_apply_info = mysqlBizImpl.get_loan_apply_info(thirdpart_user_id=data['userId'])
            credit_loan_invoice = mysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                        loan_apply_id=loan_apply_info['loan_apply_id'])
            YingJiZF = YingJiZFBizImpl(data=data)
            strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
            appOrderNo = 'appOrderNo' + strings + "3"
            repayRes = YingJiZF.payment(loanInvoiceId=credit_loan_invoice['loan_invoice_id'], paymentType='5',
                                        repay_type="0", periods="1", appOrderNo=appOrderNo)
            assert EnumH5PaymentStatus.SUCCESS.value == repayRes['head']['returnCode'], '还款API接口请求失败，失败原因{}'.format(
                repayRes['head']['returnMessage'])

        with allure.step("数据库层校验支用结果是否符合预期"):
            status = checkBizImpl.check_H5_repay_status(payment_order_no=appOrderNo)
            assert EnumCustomPaymentStatus.SUCCESS.value == status, '还款失败'

        with allure.step("校验支用单状态是否符合预期"):
            status = checkBizImpl.check_loan_apply_status_with_expect(EnumLoanStatus.ON_USE.value,
                                                                      thirdpart_user_id=data['userId'])
            assert EnumLoanStatus.ON_USE.value == status, '支用单状态未从逾期更新为正常，还款失败'

        with allure.step("接口层查询还款结果是否符合预期"):
            yingJiZhiFuSynBizImpl = YingJiZhiFuSynBizImpl(data)
            yingJiZhiFuSynBizImpl.check_payment_result_status_with_success(appOrderNo=appOrderNo)

    @allure.step("按期还款")  # 测试报告显示步骤
    @pytest.mark.run(order=2)
    def test_billDate_repay(self, get_base_data_zhixin, checkBizImpl, mysqlBizImpl):
        data = get_base_data_zhixin
        with allure.step("发起按期还款申请"):
            log.debug('发起按期还款申请')
            loan_apply_info = mysqlBizImpl.get_loan_apply_info(thirdpart_user_id=data['userId'])
            credit_loan_invoice = mysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                        loan_apply_id=loan_apply_info[
                                                                            'loan_apply_id'])
            YingJiZF = YingJiZFBizImpl(data=data)
            strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
            appOrderNo = 'appOrderNo' + strings + "3"
            repayRes = YingJiZF.payment(loanInvoiceId=credit_loan_invoice['loan_invoice_id'], paymentType='1',
                                        repay_type="0", periods="2", appOrderNo=appOrderNo)
            assert EnumH5PaymentStatus.SUCCESS.value == repayRes['head']['returnCode'], '还款API接口请求失败，失败原因{}'.format(
                repayRes['head']['returnMessage'])

        with allure.step("数据库层校验支用结果是否符合预期"):
            status = checkBizImpl.check_H5_repay_status(payment_order_no=appOrderNo)
            assert EnumCustomPaymentStatus.SUCCESS.value == status, '还款失败'

        with allure.step("接口层查询还款结果是否符合预期"):
            yingJiZhiFuSynBizImpl = YingJiZhiFuSynBizImpl(data)
            yingJiZhiFuSynBizImpl.check_payment_result_status_with_success(appOrderNo=appOrderNo)

    @allure.step("提前结清")  # 测试报告显示步骤
    @pytest.mark.run(order=3)
    def test_advance_repay(self, get_base_data_zhixin, checkBizImpl, mysqlBizImpl):
        data = get_base_data_zhixin
        with allure.step("发起提前结清申请"):
            log.debug('发起提前结清申请')
            loan_apply_info = mysqlBizImpl.get_loan_apply_info(thirdpart_user_id=data['userId'])
            credit_loan_invoice = mysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                        loan_apply_id=loan_apply_info[
                                                                            'loan_apply_id'])
            YingJiZF = YingJiZFBizImpl(data=data)
            loan_bill = YingJiZF.loan_bill(applyNo=credit_loan_invoice['loan_invoice_id'], billType='2')
            assert EnumH5PaymentStatus.SUCCESS.value == loan_bill['head']['returnCode'], '还款API接口请求失败，失败原因{}'.format(
                loan_bill['head']['returnMessage'])
            repayAmt = loan_bill['body'][0]['billAmt']
            strings = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
            appOrderNo = 'appOrderNo' + strings + "3"
            repayRes = YingJiZF.payment(loanInvoiceId=credit_loan_invoice['loan_invoice_id'], paymentType='5',
                                        repay_type="1", periods="3,4,5,6,7,8,9,10,11,12", repayAmt=repayAmt,
                                        appOrderNo=appOrderNo)
            assert EnumH5PaymentStatus.SUCCESS.value == repayRes['head']['returnCode'], '还款API接口请求失败，失败原因{}'.format(
                repayRes['head']['returnMessage'])

        with allure.step("数据库层校验支用结果是否符合预期"):
            status = checkBizImpl.check_H5_repay_status(payment_order_no=appOrderNo)
            assert EnumCustomPaymentStatus.SUCCESS.value == status, '还款失败'

        with allure.step("接口层查询还款结果是否符合预期"):
            yingJiZhiFuSynBizImpl = YingJiZhiFuSynBizImpl(data)
            yingJiZhiFuSynBizImpl.check_payment_result_status_with_success(appOrderNo=appOrderNo)


if __name__ == "__main__":
    # pytest.main(['-s', '-q', '--alluredir', 'results/allure/allure-results/report/xml', 'test_auto_zhixin_loan.py'])
    pytest.main(['test_auto_zhixin_H5_repay.py'])
