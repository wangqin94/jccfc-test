import logging
import time

import allure
import pytest

from src.enums.EnumsCommon import EnumLoanInvoiceStatus
from src.impl.FQL.FqlCreditFileBizImpl import fqlRepayFile
from utils import GlobalVar as gl
from utils.Models import get_custom_day

log = logging.getLogger(__name__)


@allure.step("放款流程数据准备")  # 测试报告显示步骤
@pytest.fixture(scope="class", autouse=True)
def pre_loan_data(fqlBizImpl, fqlCreditCheckBizImpl, fqlLoanCheckBizImpl):
    with allure.step("发起授信申请"):
        creditRes = fqlBizImpl.credit(creditAmount=2000, loanAmount=1000, loanTerm=3)
        creditStatus = creditRes['status']
        assert creditStatus == '0', "返回0说明授信申请成功"

    with allure.step("数据库层校验授信结果是否符合预期"):
        time.sleep(5)
        creditApply = fqlCreditCheckBizImpl.check_credit_apply_status(thirdpart_apply_id=creditRes['applyId'])
        fqlCreditCheckBizImpl.checkCreditApply1(creditApply)
        fqlCreditCheckBizImpl.checkCreditInfo1(thirdpart_apply_id=creditRes['applyId'])

    with allure.step("接口层校验授信结果是否符合预期"):
        creditQueryRes = fqlBizImpl.credit_query()
        auditState = creditQueryRes['auditState']
        assert auditState == '0', "返回0说明授信成功"

    with allure.step("发起支用申请"):
        loanRes = fqlBizImpl.loan(loanTerm=3, orderType=1, loanAmt=1000)
        loanStatus = loanRes['status']
        assert loanStatus == '0', "返回0说明支用申请成功"

    with allure.step("数据库层校验支用结果是否符合预期"):
        time.sleep(5)
        loanApply = fqlLoanCheckBizImpl.check_loan_apply_status(thirdpart_apply_id=loanRes['applyId'])
        fqlLoanCheckBizImpl.checkLoanApply1(loanApply)
        loanInvoice = fqlLoanCheckBizImpl.checkLoanInvoice1(loan_apply_id=loanApply['loan_apply_id'])
        loan = {}
        loan['loan_no'] = loanInvoice['loan_invoice_id']
        repayPlanInfo = fqlLoanCheckBizImpl.queryRepayPlanInfo(loan_invoice_id=loanInvoice['loan_invoice_id'],
                                                               current_num=1)
        loan['first_repay_date'] = repayPlanInfo['pre_repay_date']
        gl.set_value('loanInfo', loan)

    with allure.step("接口层校验支用结果是否符合预期"):
        loanQueryRes = fqlBizImpl.loan_query()
        loanResult = loanQueryRes['loanResult']
        assert loanResult == '0', "返回0说明支用成功"


@allure.feature("分期乐还款")
class TestCase(object):

    @allure.step("按期还款")
    def test_billDate_repay1(self, fqlRepayCheckBizImpl, job, redis):
        log.info('预放款数据-全局变量: {}'.format(gl))
        print('\n'.join(['%s:%s' % item for item in gl.__dict__.items()]))

        repay_date_bill = str(gl.get_value('loanInfo')['first_repay_date'])
        with allure.step('生成按期还款文件并上传金山云'):
            fqlRepayFile(gl.get_value('personData'), repay_mode='1', term_no="1", repay_date=repay_date_bill)

        with allure.step("设置大会计时间,账务时间=repay_date"):
            account_date = repay_date_bill.replace("-", '')
            last_date = str(get_custom_day(-1, repay_date_bill)).replace("-", '')
            next_date = str(get_custom_day(1, repay_date_bill)).replace("-", '')
            fqlRepayCheckBizImpl.updateBigacct('acct_sys_info', "sys_id='BIGACCT'", last_date=last_date,
                                               account_date=account_date, next_date=next_date)

        with allure.step('更新资产卸数'):
            fqlRepayCheckBizImpl.updateAssetJobCtl(job_date=last_date)

        with allure.step('清除分片流水'):
            fqlRepayCheckBizImpl.deleteSlice()

        with allure.step("删除redis 大会计 key=000:ACCT:SysInfo:BIGACCT"):
            redis.del_assert_repay_keys()
            time.sleep(5)

        log.info('按期还款日期---------------: {}'.format(account_date))
        with allure.step('分期乐下载文件并首次还款-任务流'):
            job.trigger_job_byJobId(job_group='5', job_type='MAIN_TRIGGER_JOB', id='545946619904192512',
                                    executeBizDate=account_date)
            time.sleep(5)

        with allure.step("数据库层校验还款入账结果"):
            fqlRepayCheckBizImpl.check_credit_file_repay1(apply_id=gl.get_value('personData')['applyId'], repay_num=1)
            fqlRepayCheckBizImpl.credit_repay_order1(loan_invoice_id=gl.get_value('loanInfo')['loan_no'], repay_term=1)

    @allure.step("逾期还款")
    def test_overdue_repay2(self, fqlRepayCheckBizImpl, job, redis):
        log.info('预放款数据-全局变量: {}'.format(gl))
        print('\n'.join(['%s:%s' % item for item in gl.__dict__.items()]))

        # 第二期账单日后10天，第一期账单日后40天
        repay_date_ove = get_custom_day(40, str(gl.get_value('loanInfo')['first_repay_date']))
        with allure.step("设置大会计时间,账务时间=repay_date"):
            account_date = repay_date_ove.replace("-", '')
            last_date = str(get_custom_day(-1, repay_date_ove)).replace("-", '')
            next_date = str(get_custom_day(1, repay_date_ove)).replace("-", '')
            fqlRepayCheckBizImpl.updateBigacct('acct_sys_info', "sys_id='BIGACCT'", last_date=last_date,
                                               account_date=account_date, next_date=next_date)

        with allure.step('更新资产卸数'):
            fqlRepayCheckBizImpl.updateAssetJobCtl(job_date=last_date)

        with allure.step('清除分片流水'):
            fqlRepayCheckBizImpl.deleteSlice()

        with allure.step("删除redis 大会计 key=000:ACCT:SysInfo:BIGACCT"):
            redis.del_assert_repay_keys()
            time.sleep(1)

        with allure.step("执行资产日终任务"):
            job.trigger_job_byJobId(job_group='6', job_type='MAIN_TRIGGER_JOB', id='336592602008784896',
                                    executeBizDate=last_date)
            time.sleep(10)

        with allure.step("校验当前借据状态"):
            info = fqlRepayCheckBizImpl.queryAssetLoanInvoiceInfo('asset_loan_invoice_info', attr=None,
                                                                  loan_invoice_id=gl.get_value('loanInfo')['loan_no'])
            assert EnumLoanInvoiceStatus.OVERDUE.value == info['loan_invoice_status'], "借据状态逾期"

        with allure.step('生成逾期还款文件并上传金山云'):
            fqlRepayFile(gl.get_value('personData'), repay_mode='5', term_no="2", repay_date=repay_date_ove)

        log.info('逾期还款日期---------------: {}'.format(account_date))
        with allure.step('分期乐下载文件并首次还款-任务流'):
            job.trigger_job_byJobId(job_type='MAIN_TRIGGER_JOB', id='545946619904192512',
                                    executeBizDate=account_date)
            time.sleep(5)

        with allure.step("数据库层校验还款入账结果"):
            fqlRepayCheckBizImpl.check_credit_file_repay1(apply_id=gl.get_value('personData')['applyId'],
                                                          repay_num=2)
            fqlRepayCheckBizImpl.credit_repay_order1(loan_invoice_id=gl.get_value('loanInfo')['loan_no'], repay_term=2)

    @allure.step("提前结清")
    def test_settle_repay3(self, fqlRepayCheckBizImpl, job, redis):
        log.info('预放款数据-全局变量: {}'.format(gl))
        print('\n'.join(['%s:%s' % item for item in gl.__dict__.items()]))

        # 第二期账单日后10天，第一期账单日后40天
        repay_date_ove = get_custom_day(40, str(gl.get_value('loanInfo')['first_repay_date']))
        with allure.step('清除分片流水'):
            fqlRepayCheckBizImpl.deleteSlice()

        with allure.step('生成提前还款文件并上传金山云'):
            fqlRepayFile(gl.get_value('personData'), repay_mode='3', term_no="3", repay_date=repay_date_ove)

        log.info('提前还款日期---------------: {}'.format(repay_date_ove))
        with allure.step('分期乐下载文件并首次还款-任务流'):
            job.trigger_job_byJobId(job_type='MAIN_TRIGGER_JOB', id='545946619904192512',
                                    executeBizDate=repay_date_ove.replace("-", ''))
            time.sleep(5)

        with allure.step("数据库层校验还款入账结果"):
            fqlRepayCheckBizImpl.check_credit_file_repay1(apply_id=gl.get_value('personData')['applyId'],
                                                          repay_num=3)
            fqlRepayCheckBizImpl.credit_repay_order1(loan_invoice_id=gl.get_value('loanInfo')['loan_no'], repay_term=3)


if __name__ == '__main__':
    pytest.main(["test_auto_fql_repay.py"])
