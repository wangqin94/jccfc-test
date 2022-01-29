from src.enums.EnumZhiXin import ZhiXinApiStatusEnum
from src.impl.common.CheckBizImpl import *
import allure
import pytest

from src.impl.common.MysqlBizImpl import *
from utils.Apollo import Apollo
from utils.Redis import *
from utils.JobCenter import *

log = MyLog().get_log()


@allure.step('前置操作：预置放款数据')
@pytest.fixture(scope="class")
def pre_loan_data(get_base_data_zhixin, zhiXinBizImpl, checkBizImpl, zhiXinCheckBizImpl, mysqlBizImpl, zhiXinSynBizImpl):
    data = get_base_data_zhixin
    job = JOB()
    apollo = Apollo()
    redis1 = Redis()
    with allure.step("前置条件-准备借据：借据逾期2期且为账单日"):
        bill_date = zhiXinSynBizImpl.preLoanapply(month=3)
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
        mysqlBizImpl.update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", last_date=last_date,
                                                  account_date=account_date, next_date=next_date)
    with allure.step("清理asset流水记录"):
        mysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')

    with allure.step("删除redis 大会计 key=000:ACCT:SysInfo:BIGACCT"):
        redis1.del_key('000:ACCT:SysInfo:BIGACCT')

    with allure.step("执行账务日终任务"):
        job.update_job("资产日终任务流", group=6, executeBizDateType='CUSTOMER', executeBizDate=last_date)
        job.trigger_job("资产日终任务流", group=6)

    with allure.step("校验当前借据是否已逾期：15s轮训等待"):
        zhiXinBizImpl.log.info('验当前借据状态')
        status = mysqlBizImpl.get_loan_apply_status(EnumLoanStatus.OVERDUE.value, thirdpart_user_id=data['userId'])
        assert EnumLoanStatus.OVERDUE.value == status, '当前支用单状态不为逾期状态，请检查账务日终任务执行结果'
    return repay_date


@pytest.mark.zhixin
@pytest.mark.smoke
@allure.feature("还款模块")
@allure.story("360智信渠道还款")
@allure.title("逾期还款-按期还款-提前结清")  # 标题
class TestCase(object):
    """ 预置条件处理 """
    """ 预置条件处理 """
    """ 测试步骤 """

    @allure.step("逾期还款")  # 测试报告显示步骤
    @pytest.mark.run(order=1)
    def test_overdue_repay(self, get_base_data_zhixin, zhiXinBizImpl, checkBizImpl, zhiXinCheckBizImpl, pre_loan_data, mysqlBizImpl):
        repay_date = pre_loan_data
        data = get_base_data_zhixin
        with allure.step("发起逾期还款申请"):
            log.debug('发起逾期还款申请')
            repayTime = "{}111111".format(repay_date.replace("-", ""))
            loan_apply_info = mysqlBizImpl.get_loan_apply_info(thirdpart_user_id=data['userId'])
            repayRes = json.loads(zhiXinBizImpl.applyRepayment(repay_type='3', loan_no=loan_apply_info['loan_apply_id'],
                                                        repayTime=repayTime).get('output'))  # 逾期还款
            assert ZhiXinApiStatusEnum.SUCCESS.value == repayRes['result'], '还款API接口请求失败，失败原因{}'.format(
                repayRes['reasonMsg'])
            assert ZhiXinApiStatusEnum.TO_DOING.value == repayRes['repayStatus'], '还款失败'

        with allure.step("数据库层校验支用结果是否符合预期"):
            status = checkBizImpl.check_channel_repay_status(third_repay_id=repayRes['repayApplyNo'])
            assert EnumChannelRepayStatus.SUCCESS.value == status, '还款失败'

        with allure.step("接口层校验支用结果是否符合预期"):
            status = zhiXinCheckBizImpl.check_repay_status(repayRes['userId'], repayRes['repayApplyNo'])
            assert ZhiXinApiStatusEnum.SUCCESS.value == status, '还款失败'

    @allure.step("按期还款")  # 测试报告显示步骤
    @pytest.mark.run(order=2)
    def test_billDate_repay(self, get_base_data_zhixin, zhiXinBizImpl, checkBizImpl, zhiXinCheckBizImpl, pre_loan_data, mysqlBizImpl):
        repay_date = pre_loan_data
        data = get_base_data_zhixin
        with allure.step("发起按期还款申请"):
            log.debug('发起按期还款申请')
            repayTime = "{}111111".format(repay_date.replace("-", ""))
            loan_apply_info = mysqlBizImpl.get_loan_apply_info(thirdpart_user_id=data['userId'])
            repayRes = json.loads(zhiXinBizImpl.applyRepayment(repay_type='1', loan_no=loan_apply_info['loan_apply_id'],
                                                        repayTime=repayTime).get('output'))  # 按期还款
            assert ZhiXinApiStatusEnum.SUCCESS.value == repayRes['result'], '还款API接口请求失败，失败原因{}'.format(
                repayRes['reasonMsg'])
            assert ZhiXinApiStatusEnum.TO_DOING.value == repayRes['repayStatus'], '还款失败'

        with allure.step("数据库层校验还款结果是否符合预期"):
            status = checkBizImpl.check_channel_repay_status(third_repay_id=repayRes['repayApplyNo'])
            assert EnumChannelRepayStatus.SUCCESS.value == status, '还款失败'

        with allure.step("接口层校验支用结果是否符合预期"):
            status = zhiXinCheckBizImpl.check_repay_status(repayRes['userId'], repayRes['repayApplyNo'])
            assert ZhiXinApiStatusEnum.SUCCESS.value == status, '还款失败'

    @allure.step("提前结清")  # 测试报告显示步骤
    @pytest.mark.run(order=3)
    def test_advance_repay(self, get_base_data_zhixin, zhiXinBizImpl, checkBizImpl, zhiXinCheckBizImpl, pre_loan_data, mysqlBizImpl):
        repay_date = pre_loan_data
        data = get_base_data_zhixin
        with allure.step("发起提前结清申请"):
            log.debug('发起提前结清申请')
            repayTime = "{}111111".format(repay_date.replace("-", ""))
            loan_apply_info = mysqlBizImpl.get_loan_apply_info(thirdpart_user_id=data['userId'])
            repayRes = json.loads(zhiXinBizImpl.applyRepayment(repay_type='2', loan_no=loan_apply_info['loan_apply_id'],
                                                        repayTime=repayTime).get('output'))  # 提前结清还款
            assert ZhiXinApiStatusEnum.SUCCESS.value == repayRes['result'], '还款API接口请求失败，失败原因{}'.format(
                repayRes['reasonMsg'])
            assert ZhiXinApiStatusEnum.TO_DOING.value == repayRes['repayStatus'], '还款失败'

        with allure.step("数据库层校验还款结果是否符合预期"):
            status = checkBizImpl.check_channel_repay_status(third_repay_id=repayRes['repayApplyNo'])
            assert EnumChannelRepayStatus.SUCCESS.value == status, '还款失败'

        with allure.step("接口层校验支用结果是否符合预期"):
            status = zhiXinCheckBizImpl.check_repay_status(repayRes['userId'], repayRes['repayApplyNo'])
            assert ZhiXinApiStatusEnum.SUCCESS.value == status, '还款失败'


if __name__ == "__main__":
    # pytest.main(['-s', '-q', '--alluredir', 'results/allure/allure-results/report/xml', 'test_auto_zhixin_loan.py'])
    pytest.main(['test_auto_zhixin_repay.py'])
