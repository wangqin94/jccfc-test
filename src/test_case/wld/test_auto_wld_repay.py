from src.enums.EnumWld import WldApiStatusEnum, StatusCodeEnum
from src.impl.common.CheckBizImpl import *
import allure
import pytest

from src.impl.common.MysqlBizImpl import *
from utils.Apollo import Apollo
from utils.Redis import *
from utils.JobCenter import *

log = MyLog().get_log()



@pytest.mark.wld
@pytest.mark.smoke
@allure.story("我来贷")
@allure.title("逾期还款-按期还款-提前结清")  # 标题
@allure.feature("还款")
class TestCase(object):

    @pytest.mark.wld
    @allure.title("逾期还款")
    @allure.step("逾期还款")
    def test_overdue_repay(self,  wldBizImpl, checkBizImpl, wldCheckBizImpl, mysqlBizImpl,
                           wldSynBizImpl):
        apollo = Apollo()
        redis1 = Redis()
        job = JOB()
        data = wldSynBizImpl

        with allure.step("前置条件-准备借据：逾期还款"):
            bill_date = wldSynBizImpl['bill_date']
            print(bill_date)
            repay_date = str(get_custom_month(1, bill_date))
            print(repay_date)
        with allure.step("设置credit还款mock时间, 第二期账单日"):
            # 设置apollo还款mock时间 默认当前时间
            repay_date = str(get_custom_month(1, bill_date))
            apollo_data = dict()
            apollo_data['credit.mock.repay.trade.date'] = "true"  # credit.mock.repay.trade.date
            apollo_data['credit.mock.repay.date'] = "{} 00:00:00".format(repay_date)
            apollo.update_config(**apollo_data)

        repay_time = str(get_custom_day(-1, repay_date)).replace("-", '')

        with allure.step("设置大会计时间,账务时间=repay_date"):
            account_date = repay_date.replace("-", '')
            last_date = str(get_custom_day(-1, repay_date)).replace("-", '')
            next_date = str(get_custom_day(1, repay_date)).replace("-", '')
            mysqlBizImpl.update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", last_date=last_date,
                                                      account_date=account_date, next_date=next_date)

        with allure.step("执行账务日终任务"):
            job.update_job("资产日终任务流", group=6, executeBizDateType='CUSTOMER', executeBizDate=last_date)
            job.trigger_job("资产日终任务流", group=6)


        with allure.step("清理分片流水"):
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
            mysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')

        with allure.step("删除redis 大会计 key=000:ACCT:SysInfo:BIGACCT"):
            redis1.del_key('000:ACCT:SysInfo:BIGACCT')
            redis1.del_key('000:ACCT:AccountDate:BIGACCT')

        with allure.step("校验当前借据是否已逾期：15s轮训等待"):
            wldBizImpl.log.info('验当前借据状态')
            status = mysqlBizImpl.get_loan_apply_status(EnumLoanStatus.OVERDUE.value,
                                                        thirdpart_apply_id=data['applyid'])
            assert EnumLoanStatus.OVERDUE.value == status, '当前支用单状态不为逾期状态，请检查账务日终任务执行结果'

        # set_ctl_time
        # mysqlBizImpl.update_asset_database_info(table='asset_job_ctl', attr="job_type = 'ASSET_BI_JOB_FINISH'",
        #                                         job_date=repay_time)

        mysqlBizImpl.get_asset_job_ctl_info(job_date=repay_time)
        u_id = mysqlBizImpl.get_loan_apply_info(thirdpart_apply_id=data['applyid'])['user_id']

        loan_invoiceid = mysqlBizImpl.get_loan_invoice_info(user_id=u_id)['loan_invoice_id']

        repayRes = wldBizImpl.repay(repay_term_no="1", repay_type="4", loan_invoice_id=loan_invoiceid,
                                    repay_date=repay_date)

        repayResstatus = repayRes['body']['repayApplyList'][0]['repayStatus']

        # repayApplySerialNo = repayRes['body']['repayApplyList'][0]['repayApplySerialNo']

        assert StatusCodeEnum.SUCCESS.msg == repayRes['head']['returnMessage'], '还款API接口请求失败，失败原因{}'.format(
            repayRes['reasonMsg'])
        assert WldApiStatusEnum.QUERY_REPAY_RESULT_D.value == repayResstatus, '还款失败'

        # 接口层验证

        # with allure.step("接口层校验支用结果是否符合预期"):
        #     status = wldCheckBizImpl.check_repay_status(repayApplySerialNo)
        #     assert WldApiStatusEnum.QUERY_REPAY_RESULT_S.value == status, '还款失败'

        # 数据库层验证
        with allure.step("数据库层校验还款结果是否符合预期"):
            time.sleep(5)
            status = mysqlBizImpl.get_asset_database_info('asset_repay_plan', loan_invoice_id=loan_invoiceid,
                                                          current_num=1)['repay_plan_status']

            assert EnumRepayPlanStatus.OVERDUE_REPAY.value == status, '还款失败'

    @pytest.mark.wld
    @allure.title("按期还款")
    @allure.step("按期还款")
    def test_nomal_repay(self,  wldBizImpl, checkBizImpl, wldCheckBizImpl, mysqlBizImpl,
                         wldSynBizImpl):
        apollo = Apollo()
        redis1 = Redis()
        data = wldSynBizImpl

        with allure.step("前置条件-准备借据：按期还款"):
            bill_date = wldSynBizImpl['bill_date']
            print(bill_date)
            repay_date = str(get_custom_month(1, bill_date))
            print(repay_date)
        with allure.step("设置credit还款mock时间, 第二期账单日"):
            # 设置apollo还款mock时间 默认当前时间
            repay_date = str(get_custom_month(1, bill_date))
            apollo_data = dict()
            apollo_data['credit.mock.repay.trade.date'] = "true"  # credit.mock.repay.trade.date
            apollo_data['credit.mock.repay.date'] = "{} 00:00:00".format(repay_date)
            apollo.update_config(**apollo_data)

        with allure.step("设置大会计时间,账务时间=repay_date"):
            account_date = repay_date.replace("-", '')
            last_date = str(get_custom_day(-1, repay_date)).replace("-", '')
            next_date = str(get_custom_day(1, repay_date)).replace("-", '')
            mysqlBizImpl.update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", last_date=last_date,
                                                      account_date=account_date, next_date=next_date)




        with allure.step("清理分片流水"):
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
            mysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')



        with allure.step("删除redis 大会计 key=000:ACCT:SysInfo:BIGACCT"):
            redis1.del_key('000:ACCT:SysInfo:BIGACCT')
            redis1.del_key('000:ACCT:AccountDate:BIGACCT')



        repay_time = str(get_custom_day(-1, repay_date)).replace("-", '')
        # set_ctl_time
        # mysqlBizImpl.update_asset_database_info(table='asset_job_ctl', attr="job_type = 'ASSET_BI_JOB_FINISH'", job_date=repay_time)
        mysqlBizImpl.get_asset_job_ctl_info(job_date=repay_time)
        u_id = mysqlBizImpl.get_loan_apply_info(thirdpart_apply_id=data['applyid'])['user_id']

        loan_invoiceid = mysqlBizImpl.get_loan_invoice_info(user_id=u_id)['loan_invoice_id']

        repayRes = wldBizImpl.repay(repay_term_no="2", repay_type="1", loan_invoice_id=loan_invoiceid,
                                    repay_date=repay_date)

        repayResstatus = repayRes['body']['repayApplyList'][0]['repayStatus']
        repayApplySerialNo = repayRes['body']['repayApplyList'][0]['repayApplySerialNo']


        assert StatusCodeEnum.SUCCESS.msg == repayRes['head']['returnMessage'], '还款API接口请求失败，失败原因{}'.format(
            repayRes['reasonMsg'])
        assert WldApiStatusEnum.QUERY_REPAY_RESULT_D.value == repayResstatus, '还款失败'

        # 接口层验证
        # with allure.step("接口层校验支用结果是否符合预期"):
        #     status = wldCheckBizImpl.check_repay_status(repayApplySerialNo)
        #     assert WldApiStatusEnum.QUERY_REPAY_RESULT_S.value == status, '还款失败'

        # 数据库层验证
        with allure.step("数据库层校验还款结果是否符合预期"):
            time.sleep(5)
            status = mysqlBizImpl.get_asset_database_info('asset_repay_plan',loan_invoice_id=loan_invoiceid,
                                                          current_num=2)['repay_plan_status']

            assert EnumRepayPlanStatus.REPAY.value == status, '还款失败'


    @pytest.mark.wld
    @allure.title("提前结清")
    @allure.step("提前结清")
    def test_advance_repay(self, wldBizImpl, checkBizImpl, wldCheckBizImpl, mysqlBizImpl,wldSynBizImpl
                         ):
        apollo = Apollo()
        redis1 = Redis()
        data = wldSynBizImpl
        job = JOB()


        with allure.step("前置条件-准备借据：提前结清"):

            bill_date =wldSynBizImpl['bill_date']
            print(bill_date)
            repay_date = str(get_custom_month(2, bill_date))
            print(repay_date)
        with allure.step("设置credit还款mock时间, 第3期账单日"):
            # 设置apollo还款mock时间 默认当前时间
            repay_date = str(get_custom_month(2, bill_date))
            apollo_data = dict()
            apollo_data['credit.mock.repay.trade.date'] = "true"  # credit.mock.repay.trade.date
            apollo_data['credit.mock.repay.date'] = "{} 00:00:00".format(repay_date)
            apollo.update_config(**apollo_data)

        with allure.step("设置大会计时间,账务时间=repay_date"):
            account_date = repay_date.replace("-", '')
            last_date = str(get_custom_day(-1, repay_date)).replace("-", '')
            next_date = str(get_custom_day(1, repay_date)).replace("-", '')
            mysqlBizImpl.update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", last_date=last_date,
                                                  account_date=account_date, next_date=next_date)


        with allure.step("清理分片流水"):
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
            mysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')


        with allure.step("执行账务日终任务"):
            job.update_job("资产日终任务流", group=6, executeBizDateType='CUSTOMER', executeBizDate=last_date)
            job.trigger_job("资产日终任务流", group=6)



        with allure.step("清理分片流水"):
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
            mysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')

        with allure.step("删除redis 大会计 key=000:ACCT:SysInfo:BIGACCT"):
            redis1.del_key('000:ACCT:SysInfo:BIGACCT')
            redis1.del_key('000:ACCT:AccountDate:BIGACCT')



        repay_time = str(get_custom_day(-1, repay_date)).replace("-", '')
        # set_ctl_time
        # mysqlBizImpl.update_asset_database_info(table='asset_job_ctl', attr="job_type = 'ASSET_BI_JOB_FINISH'", job_date=repay_time)
        mysqlBizImpl.get_asset_job_ctl_info(job_date=repay_time)
        u_id = mysqlBizImpl.get_loan_apply_info(thirdpart_apply_id=data['applyid'])['user_id']

        loan_invoiceid = mysqlBizImpl.get_loan_invoice_info(user_id=u_id)['loan_invoice_id']

        repayRes = wldBizImpl.repay(repay_date="2022-06-10",repay_term_no="3", repay_type="2", loan_invoice_id=loan_invoiceid
                                    )



        # repayApplySerialNo = repayRes['body']['repayApplyList'][0]['repayApplySerialNo']

        assert StatusCodeEnum.SUCCESS.msg == repayRes['head']['returnMessage'], '还款API接口请求失败，失败原因{}'.format(
            repayRes['reasonMsg'])

        repayResstatus = repayRes['body']['repayApplyList'][0]['repayStatus']

        assert WldApiStatusEnum.QUERY_REPAY_RESULT_D.value == repayResstatus, '还款失败'

        # 接口层验证
        # with allure.step("接口层校验支用结果是否符合预期"):
        #     status = wldCheckBizImpl.check_repay_status(repayApplySerialNo)
        #     assert WldApiStatusEnum.QUERY_REPAY_RESULT_S.value == status, '还款失败'

        # 数据库层验证

        with allure.step("数据库层校验还款结果是否符合预期"):
            time.sleep(5)
            status = mysqlBizImpl.get_asset_database_info('asset_repay_plan', loan_invoice_id=loan_invoiceid,
                                                          current_num=3)['repay_plan_status']

            assert EnumRepayPlanStatus.REPAY.value == status, '还款失败'





if __name__ == "__main__":
    # pytest.main(['-s', '-q', '--alluredir', 'results/allure/allure-results/report/xml', 'test_auto_wld_loan.py'])
    pytest.main(['test_auto_wld_repay.py'])
