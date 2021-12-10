import allure
import pytest

from src.enums.EnumZhiXin import ZhiXinApiStatusEnum
from src.impl.common.CommonCheckBizImpl import *
import time


@allure.feature("支用申请查询")
class TestCase(object):
    """ 预置条件处理 """
    """ 预置条件处理 """
    """ 测试步骤 """

    @pytest.mark.zhixin
    @pytest.mark.smoke
    @allure.title("绑卡申请&校验")  # 标题
    @allure.step("绑卡申请&校验")  # 测试报告显示步骤
    def test_loan(self, get_base_data, zhixin, checkBizImpl, zhiXinCheckBizImpl):
        """ 测试步骤 """
        data = get_base_data
        with allure.step("绑卡申请"):
            res = json.loads(zhixin.applyCertification().get('output'))
        with allure.step("绑卡校验"):
            zhixin.verifyCode(userId=res['userId'], certificationApplyNo=res['certificationApplyNo'],
                              cdKey=res['cdKey'])

        with allure.step("发起授信申请"):
            creditRes = json.loads(zhixin.credit().get('output'))
            creditApplyNo = creditRes['creditApplyNo']

        with allure.step("数据库层校验授信结果是否符合预期"):
            time.sleep(5)
            checkBizImpl.check_credit_apply_status(thirdpart_apply_id=creditApplyNo)

        with allure.step("接口层校验授信结果是否符合预期"):
            zhiXinCheckBizImpl.check_credit_apply_status(data, creditRes['userId'],
                                                         creditRes['creditApplyNo'])

        with allure.step("发起支用申请"):
            loanRes = json.loads(zhixin.applyLoan(loanAmt='1000', term='6').get('output'))
            loanApplyNo = loanRes['loanApplyNo']

        with allure.step("数据库层校验支用结果是否符合预期"):
            time.sleep(5)
            status = checkBizImpl.check_loan_apply_status(thirdpart_apply_id=loanApplyNo)
            assert EnumLoanStatus.ON_USE.value == status, '支用失败'

        with allure.step("接口层校验支用结果是否符合预期"):
            status = zhiXinCheckBizImpl.check_loan_apply_status(data, loanRes['userId'],
                                                                loanRes['loanApplyNo'])
            assert ZhiXinApiStatusEnum.SUCCESS.value == status, '支用失败'


if __name__ == "__main__":
    # pytest.main(['-s', '-q', '--alluredir', 'results/allure/allure-results/report/xml', 'test_auto_zhixin_loan.py'])
    pytest.main(['test_auto_zhixin_loan.py'])
