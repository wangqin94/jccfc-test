# -*- coding: utf-8 -*-
# -----------------------------------------------------
# 百度放款流程
# -----------------------------------------------------
import time
import allure
import pytest
import datetime
from src.impl.baidu.BaiDuCreditFileBizImpl import BaiduFile
from src.enums.EnumBaiDu import *


class TestCase(object):
    @pytest.mark.baidu
    @pytest.mark.smoke
    @allure.title("授信放款流程")
    @allure.step("授信申请-授信查询-支用申请-支用查询-对账文件")
    def test_loan(self,get_base_data_baidu, baiduBizImpl, checkBizImpl, mysqlBizImpl, job):
        data = get_base_data_baidu
        loan_date = datetime.datetime.today().strftime('%Y-%m-%d')
        with allure.step('授信申请'):
            credit_apply_id = baiduBizImpl.credit(initialAmount='100000')['credit_apply_id']
            time.sleep(5)

        with allure.step('数据库层校验授信结果是否符合预期'):

            checkBizImpl.check_credit_apply_status(thirdpart_apply_id=credit_apply_id)

        with allure.step('接口层校验授信结果是否符合预期'):
            ris_code = baiduBizImpl.credit_query(credit_apply_id=credit_apply_id)['message']['expanding'][
                'risCode']
            assert EnumBaiDuRisCode.ACCEPT.value == ris_code, '授信失败'

        with allure.step('发起支用申请'):
            loan_apply_id = baiduBizImpl.loan(cashAmount='100000', term='3')['loan_apply_id']
            time.sleep(5)

        with allure.step('数据库层校验支用状态-待放款'):
            checkBizImpl.check_file_loan_apply_status(loan_apply_serial_id=loan_apply_id)

        with allure.step('接口层校验支用结果-待放款'):
            l_ris_code = baiduBizImpl.loan_query(loan_apply_id=loan_apply_id)['message']['expanding']['risCode']
            assert EnumBaiDuRisCode.ACCEPT.value == l_ris_code, '支用失败'

        with allure.step('生成放款文件并上传金山云'):
            bd = BaiduFile(data=data, cur_date=loan_date)
            bd.start()

        with allure.step('清除分片流水'):
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
            mysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
            mysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')

        with allure.step('执行任务流下载放款对账文件入库'):
            job.update_job('百度放款对账下载任务流-测试', executeBizDate=loan_date.replace('-', ''))
            job.trigger_job('百度放款对账下载任务流-测试')
            time.sleep(5)

        with allure.step('检查放款信息是否入三方待建账信息表'):
            checkBizImpl.check_third_wait_loan_status(certificate_no=data['cer_no'])

        with allure.step('执行任务流放款'):
            job.update_job('线下自动放款', executeBizDate=loan_date.replace('-', ''))
            job.trigger_job('线下自动放款')

        with allure.step('数据库层校验支用状态-使用中'):
            checkBizImpl.check_loan_apply_status(loan_apply_serial_id=loan_apply_id)


if __name__ == '__main__':
    pytest.main(['test_auto_baidu_loan.py'])


