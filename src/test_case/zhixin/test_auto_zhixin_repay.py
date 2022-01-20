import json

from src.enums.EnumZhiXin import ZhiXinApiStatusEnum
from src.impl.common.CheckBizImpl import *
import time
import allure
import pytest

from src.impl.common.MysqlBizImpl import *
from src.impl.zhixin.ZhiXinBizImpl import ZhiXinBizImpl
from utils.Apollo import Apollo
from utils.Redis import *
from utils.JobCenter import *


class TestCase(object):
    """ 预置条件处理 """
    """ 预置条件处理 """
    """ 测试步骤 """

    @pytest.mark.zhixin
    @pytest.mark.smoke
    @allure.title("逾期还款-按期还款-提前结清")  # 标题
    @allure.step("逾期还款-按期还款-提前结清")  # 测试报告显示步骤
    def test_repay(self, get_base_data, zhixin, checkBizImpl, zhiXinCheckBizImpl):
        """ 测试步骤 """
        data = get_base_data
        job = JOB()
        with allure.step("前置条件-准备借据：借据逾期2期且为账单日"):
            bill_date = ZhiXinBizImpl().preLoanapply(month=3)
        with allure.step("设置credit还款mock时间, 第二期账单日"):
            # 设置apollo还款mock时间 默认当前时间
            repay_date = str(get_custom_month(-1, bill_date))
            apollo_data = dict()
            apollo_data['credit.mock.repay.trade.date'] = "true"
            apollo_data['credit.mock.repay.date'] = "{} 00:00:00".format(repay_date)
            Apollo().update_config(**apollo_data)

        with allure.step("设置大会计时间,账务时间=repay_date"):
            account_date = repay_date.replace("-", '')
            last_date = str(get_custom_day(-1, repay_date)).replace("-", '')
            next_date = str(get_custom_day(1, repay_date)).replace("-", '')
            MysqlBizImpl().update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", last_date=last_date, account_date=account_date, next_date=next_date)

        with allure.step("删除redis 大会计 key=000:ACCT:SysInfo:BIGACCT"):
            Redis().del_key('000:ACCT:SysInfo:BIGACCT')

        with allure.step("执行账务日终任务"):
            job.update_job("资产日终任务流", group=6, executeBizDateType='CUSTOMER', executeBizDate=last_date)
            job.trigger_job("资产日终任务流", group=6)

        # with allure.step("发起逾期还款申请"):
        #     repayTime = "{}111111".format(repay_date.replace("-", ""))
        #     loan_apply_info = MysqlBizImpl().get_loan_apply_info(thirdpart_user_id=data['userId'])
        #     self.repayRes = json.loads(zhixin.applyRepayment(repay_type='1', loan_no=loan_apply_info['loan_apply_id'], repayTime=repayTime).get('output'))  # 按期还款
        #     creditApplyNo = self.repayRes['creditApplyNo']
        #
        # with allure.step("数据库层校验支用结果是否符合预期"):
        #     time.sleep(5)
        #     status = checkBizImpl.check_loan_apply_status(thirdpart_apply_id=loanApplyNo)
        #     assert EnumLoanStatus.ON_USE.value == status, '支用失败'
        #
        # with allure.step("接口层校验支用结果是否符合预期"):
        #     status = zhiXinCheckBizImpl.check_loan_apply_status(data, loanRes['userId'],
        #                                                         loanRes['loanApplyNo'])
        #     assert ZhiXinApiStatusEnum.SUCCESS.value == status, '支用失败'


if __name__ == "__main__":
    # pytest.main(['-s', '-q', '--alluredir', 'results/allure/allure-results/report/xml', 'test_auto_zhixin_loan.py'])
    pytest.main(['test_auto_zhixin_repay.py'])
