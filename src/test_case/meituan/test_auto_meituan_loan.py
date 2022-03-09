# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：test_auto_meituan_loan.py
@Author  ：jccfc
@Date    ：2022/2/18 13:59 
"""
import time

import allure
import pytest

from src.impl.MeiTuan.MeiTuan_CreateFileBizImpl import MtFile, MeiTuanLoanFile


@allure.feature("支用申请查询")
class TestCase(object):

    @pytest.mark.meituan
    @pytest.mark.smoke
    @allure.title("授信申请-授信查询-支用申请-支用查询")  # 标题
    @allure.step("授信申请-授信查询-支用申请-支用查询")  # 测试报告显示步骤
    def test_loan(self, get_base_data_meituan, meiTuanBizImpl, checkBizImpl, meiTuanCheckBizImpl, mysqlBizImpl, job):
        """ 测试步骤 """
        data = get_base_data_meituan
        # 放款时间
        loan_date = time.strftime('%Y-%m-%d', time.localtime())
        with allure.step("发起授信申请"):
            APP_NO = meiTuanBizImpl.credit(APPLY_AMT=1000000)['app_no']
            with allure.step("数据库层校验授信结果是否符合预期"):
                checkBizImpl.check_credit_apply_status(thirdpart_apply_id=APP_NO)
            with allure.step("接口层校验授信结果是否符合预期"):
                meiTuanCheckBizImpl.check_credit_apply_status(APP_NO)

        with allure.step("发起支用申请"):
            res = meiTuanBizImpl.loan(TRADE_AMOUNT=60000, TRADE_PERIOD='3')
            third_appId = res.get('body')['APP_NO']
            with allure.step("数据库层校验支用结果是否符合预期"):
                checkBizImpl.check_file_loan_apply_status(thirdpart_apply_id=third_appId)
            with allure.step("接口层校验支用结果是否符合预期"):
                meiTuanCheckBizImpl.check_loan_apply_status(third_appId)

        with allure.step("构造放款对账文件"):
            MeiTuanLoanFile(data, apply_date=loan_date)

        with allure.step('清除分片流水'):
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
            mysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')

        with allure.step('执行任务流下载放款对账文件入库'):
            job.update_job('美团放款对账文件处理任务流', executeBizDateType='CUSTOMER', executeBizDate=loan_date.replace('-', ''))
            job.trigger_job('美团放款对账文件处理任务流')
            checkBizImpl.check_third_wait_loan_status(thirdpart_apply_id=third_appId)

        with allure.step('执行任务流放款'):
            job.update_job('线下自动放款', executeBizDateType='CUSTOMER', executeBizDate=loan_date.replace('-', ''))
            job.trigger_job('线下自动放款')

        with allure.step('数据库层校验支用状态-使用中'):
            checkBizImpl.check_loan_apply_status(thirdpart_apply_id=third_appId)


if __name__ == "__main__":
    # pytest.main(['-s', '-q', '--alluredir', 'results/allure/allure-results/report/xml', 'test_auto_zhixin_loan.py'])
    pytest.main(['test_auto_meituan_loan.py'])