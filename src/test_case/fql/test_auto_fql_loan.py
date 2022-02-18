import json
import logging
import time

import allure

log = logging.getLogger(__name__)


@allure.feature("分期乐支用")
class TestCase(object):

    @allure.title("授信申请-授信查询-支用申请-支用查询：支用成功")  # 标题
    @allure.step("授信申请-授信查询-支用申请-支用查询：支用成功")  # 测试报告显示步骤
    def test_loan_success1(self, fqlBizImpl, fqlCreditCheckBizImpl, fqlLoanCheckBizImpl):
        with allure.step("发起授信申请"):
            creditRes = fqlBizImpl.credit(creditAmount=2000, loanAmount=1000, loanTerm=3)
            log.info(f"授信申请接口结果----：{creditRes}")
            creditStatus = creditRes['status']
            assert creditStatus == '0', "返回0说明授信申请成功"

        with allure.step("数据库层校验授信结果是否符合预期"):
            time.sleep(5)
            creditApply = fqlCreditCheckBizImpl.check_credit_apply_status(thirdpart_apply_id=creditRes['applyId'])
            fqlCreditCheckBizImpl.checkCreditApply1(creditApply)
            fqlCreditCheckBizImpl.checkCreditInfo1(thirdpart_apply_id=creditRes['applyId'])

        with allure.step("接口层校验授信结果是否符合预期"):
            creditQueryRes = fqlBizImpl.credit_query()
            log.info(f"授信查询接口结果----：{creditQueryRes}")
            auditState = creditQueryRes['auditState']
            assert auditState == '0', "返回0说明授信成功"

        with allure.step("发起支用申请"):
            loanRes = fqlBizImpl.loan(loanTerm=3, orderType=1, loanAmt=1000)
            log.info(f"支用申请结果----：{loanRes}")
            loanStatus = loanRes['status']
            assert loanStatus == '0', "返回0说明支用申请成功"

        with allure.step("数据库层校验支用结果是否符合预期"):
            time.sleep(5)
            loanApply = fqlLoanCheckBizImpl.check_loan_apply_status(thirdpart_apply_id=loanRes['applyId'])
            fqlLoanCheckBizImpl.checkLoanApply1(loanApply)
            fqlLoanCheckBizImpl.checkLoanInvoice1(loan_apply_id=loanApply['loan_apply_id'])

        with allure.step("接口层校验支用结果是否符合预期"):
            loanQueryRes = fqlBizImpl.loan_query()
            log.info(f"支用查询接口结果----：{loanQueryRes}")
            loanResult = loanQueryRes['loanResult']
            assert loanResult == '0', "返回0说明支用成功"
