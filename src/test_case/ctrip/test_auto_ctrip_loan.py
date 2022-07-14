import allure
import pytest
from src.impl.common.CheckBizImpl import *
import logging

log = logging.getLogger(__name__)


@allure.feature("支用申请查询")
class TestCase(object):
    """ 预置条件处理 """
    """ 预置条件处理 """
    """ 测试步骤 """

    @pytest.mark.ctrip
    @pytest.mark.smoke
    @allure.title("授信申请-授信查询-支用申请-支用查询")  # 标题
    @allure.step("授信申请-授信查询-支用申请-支用查询")  # 测试报告显示步骤
    def Test_loan(self, ctripBizImpl, ctripCreditCheckBizImpl,ctripLoanCheckBizImpl):
        """ 测试步骤 """

        with allure.step("发起授信申请"):
            creditRes = ctripBizImpl.credit(advice_amount=12000)
            log.info(f"授信申请接口结果----：{creditRes}")
            creditStatus = creditRes['credit_status']
            assert creditStatus == '0', "返回0说明授信申请成功"

        with allure.step("数据库层校验授信结果是否符合预期"):
            time.sleep(5)
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
            time.sleep(10)
            loanApply = ctripLoanCheckBizImpl.check_loan_apply_status(thirdpart_user_id=creditRes['open_id'])
            ctripLoanCheckBizImpl.checkLoanApply1(loanApply)




