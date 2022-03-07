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
    def test_loan(self, get_base_data_meituan, meiTuanBizImpl, checkBizImpl, meiTuanCheckBizImpl):
        """ 测试步骤 """
        data = get_base_data_meituan
        with allure.step("发起授信申请"):
            res = meiTuanBizImpl.credit(APPLY_AMT=1000000)['app_no']
            with allure.step("数据库层校验授信结果是否符合预期"):
                checkBizImpl.check_credit_apply_status(thirdpart_apply_id=res.get('body')['APP_NO'])
            with allure.step("接口层校验授信结果是否符合预期"):
                meiTuanCheckBizImpl.check_credit_apply_status(res.get('body')['APP_NO'])

        with allure.step("发起支用申请"):
            res = meiTuanBizImpl.loan(TRADE_AMOUNT=60000, TRADE_PERIOD='3')
            with allure.step("数据库层校验支用结果是否符合预期"):
                checkBizImpl.check_file_loan_apply_status(thirdpart_apply_id=res.get('body')['APP_NO'])
            with allure.step("接口层校验支用结果是否符合预期"):
                meiTuanCheckBizImpl.check_loan_apply_status(res.get('body')['APP_NO'])

        with allure.step("构造放款对账文件"):
            current_date = time.strftime('%Y-%m-%d', time.localtime())
            MeiTuanLoanFile(data, apply_date=current_date)

        with allure.step("解析放款对账文件"):
            MtFile(certificate_no=data['cer_no'], user_name=data['name'], loan_record=0, apply_date='2021-10-26')


if __name__ == "__main__":
    # pytest.main(['-s', '-q', '--alluredir', 'results/allure/allure-results/report/xml', 'test_auto_zhixin_loan.py'])
    pytest.main(['test_auto_meituan_loan.py'])