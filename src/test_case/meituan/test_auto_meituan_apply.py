# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：test_auto_meituan_apply.py
@Author  ：jccfc
@Date    ：2022/3/10 17:27 
"""
import time

import allure
import pytest


@allure.feature("支用授信查询")
class TestCase(object):

    @pytest.mark.meituan
    @pytest.mark.smoke
    @allure.title("授信申请-授信查询")  # 标题
    @allure.step("授信申请-授信查询")  # 测试报告显示步骤
    def test_apply(self, meiTuanBizImpl, checkBizImpl, meiTuanCheckBizImpl):
        """ 测试步骤 """
        with allure.step("发起授信申请"):
            APP_NO = meiTuanBizImpl.credit(APPLY_AMT=1000000)['app_no']
            with allure.step("数据库层校验授信结果是否符合预期"):
                checkBizImpl.check_credit_apply_status(thirdpart_apply_id=APP_NO)
            with allure.step("接口层校验授信结果是否符合预期"):
                meiTuanCheckBizImpl.check_credit_apply_status(APP_NO)


if __name__ == "__main__":
    pytest.main(['test_auto_meituan_apply.py'])
