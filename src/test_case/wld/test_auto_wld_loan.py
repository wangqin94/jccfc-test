import time
import allure
import pytest
from src.enums.EnumWld import WldApiStatusEnum
from src.enums.EnumsCommon import EnumLoanStatus


@allure.feature("支用申请查询")
class TestCase(object):
    """ 预置条件处理 """
    """ 预置条件处理 """
    """ 测试步骤 """

    @pytest.mark.wld
    @pytest.mark.smoke
    @allure.title("绑卡申请-绑卡校验-授信申请-授信查询-支用申请-支用查询")  # 标题
    @allure.step("绑卡申请-绑卡校验-授信申请-授信查询-支用申请-支用查询")  # 测试报告显示步骤
    def test_loan(self, get_base_data_wld, wldBizImpl, checkBizImpl,wldCheckBizImpl):
        """ 测试步骤 """
        data = get_base_data_wld

        with allure.step("绑卡申请"):
            wldBizImpl.bind_card()
            bindres = wldBizImpl.confirm_bind_card()
            u_id = bindres['body']['userId']

        with allure.step("绑卡校验-接口"):
            qbindres = wldBizImpl.query_bind_card(user_id=u_id)
            qbindres2 = qbindres['body']['retDesc']

        print(qbindres2)

        # with allure.step("绑卡校验-数据库"):
        #     wldBizImpl.query_bind_card()

        with allure.step("发起授信申请"):
            creditres = wldBizImpl.credit()
            creditApplyNo = creditres['body']['thirdApplyId']


        with allure.step("数据库层校验授信结果是否符合预期"):
            time.sleep(5)
            checkBizImpl.check_credit_apply_status(thirdpart_apply_id=creditApplyNo)

        with allure.step("接口层校验授信结果是否符合预期"):
            wldCheckBizImpl.check_credit_apply_status(thirdapplyid=creditApplyNo )

        time.sleep(10)
        with allure.step("发起支用申请"):
            loanres = wldBizImpl.loan()
            loanapplyno = loanres['body']['thirdApplyId']

        with allure.step("数据库层校验支用结果是否符合预期"):
            time.sleep(5)
            status = checkBizImpl.check_loan_apply_status(thirdpart_apply_id=loanapplyno)
            assert EnumLoanStatus.ON_USE.value == status, '支用失败'

        with allure.step("接口层校验支用结果是否符合预期"):
            status = wldCheckBizImpl.check_loan_apply_status(loanres['body']['thirdApplyId'])
            assert WldApiStatusEnum.QUERY_LOAN_RESULT_S.value == status, '支用失败'



if __name__ == "__main__":
    pytest.main(['-s', '-q', '--alluredir', 'results/allure/allure-results/report/xml', 'test_auto_wld_loan.py'])