# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：test_auto_jike_repay_bank.py
@Author  ：jccfc
@Date    ：2023/12/04 13:59
"""
import allure
import pytest

from utils.GlobalVar import GlobalMap
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl
from utils.Models import *

log = MyLog().get_log()
globalMap = GlobalMap()
repayPublicBizImpl = RepayPublicBizImpl()


@pytest.mark.jike
@pytest.mark.smoke
@allure.feature("还款模块")
@allure.story("即科融担银行卡还款")
@allure.title("按期还款-提前还款-提前结清")  # 标题
class TestCase(object):
    @allure.step("按期还款")  # 测试报告显示步骤
    @pytest.mark.run(order=1)
    def test_billDate_repay(self, jikeBizImpl, jikeLoanApply, mysqlBizImpl, checkBizImpl, jikeCheckBizImpl):
        with allure.step("准备按期还款数据"):
            loanInvoiceId = globalMap.get('loanInvoiceId')
            repayTerm = 1
            asset_repay_plan = mysqlBizImpl.get_asset_database_info("asset_repay_plan",
                                                                    loan_invoice_id=loanInvoiceId, current_num=repayTerm)
            repayDate = str(asset_repay_plan['pre_repay_date'])
            # 还款环境配置
            repayPublicBizImpl.pre_repay_config(repayDate=repayDate)

        with allure.step("发起银行卡还款请求"):
            self.repayRes = jikeBizImpl.repay_apply(repay_scene='01', repay_type='1', loanInvoiceId=loanInvoiceId, repayDate=repayDate, repayTerm=repayTerm)  # 按期还款

        with allure.step("接口层校验结果是否符合预期"):
            jikeCheckBizImpl.jike_check_repay_status(repayApplySerialNo=self.repayRes['body']['repayApplySerialNo'])

        with allure.step('检查是否还款成功'):
            checkBizImpl.check_channel_repay_status(loan_invoice_id=loanInvoiceId, repay_term=1)

    @allure.step("提前还款")  # 测试报告显示步骤
    @pytest.mark.run(order=2)
    def test_advance_repay(self, jikeBizImpl, mysqlBizImpl, checkBizImpl, jikeCheckBizImpl):
        with allure.step("准备提前还款数据"):
            loanInvoiceId = globalMap.get('loanInvoiceId')
            repayTerm = 2
            asset_repay_plan = mysqlBizImpl.get_asset_database_info("asset_repay_plan",
                                                                    loan_invoice_id=loanInvoiceId, current_num=repayTerm)
            repayDate = get_custom_day(-1, date=str(asset_repay_plan['pre_repay_date']))

            # 还款环境配置
            repayPublicBizImpl.pre_repay_config(repayDate=repayDate)

        with allure.step("发起银行卡还款请求"):
            self.repayRes = jikeBizImpl.repay_apply(repay_scene='01', repay_type='7', loanInvoiceId=loanInvoiceId, repayDate=repayDate, repayTerm=repayTerm)  # 按期还款

        with allure.step("接口层校验结果是否符合预期"):
            jikeCheckBizImpl.jike_check_repay_status(repayApplySerialNo=self.repayRes['body']['repayApplySerialNo'])

        with allure.step('检查是否还款成功'):
            checkBizImpl.check_channel_repay_status(loan_invoice_id=loanInvoiceId, repay_term=repayTerm)

    @allure.step("提前结清还款")  # 测试报告显示步骤
    @pytest.mark.run(order=3)
    def test_advance_settle_repay(self, jikeBizImpl, mysqlBizImpl, checkBizImpl, jikeCheckBizImpl):
        with allure.step("准备提前结清还款数据"):
            loanInvoiceId = globalMap.get('loanInvoiceId')
            repayTerm = 3
            asset_repay_plan = mysqlBizImpl.get_asset_database_info("asset_repay_plan",
                                                                    loan_invoice_id=loanInvoiceId, current_num=repayTerm)
            repayDate = get_custom_day(-1, date=str(asset_repay_plan['pre_repay_date']))

            # 还款环境配置
            repayPublicBizImpl.pre_repay_config(repayDate=repayDate)

        with allure.step("发起银行卡还款请求"):
            self.repayRes = jikeBizImpl.repay_apply(repay_scene='01', repay_type='2', loanInvoiceId=loanInvoiceId, repayDate=repayDate, repayTerm=repayTerm)  # 按期还款

        with allure.step("接口层校验结果是否符合预期"):
            jikeCheckBizImpl.jike_check_repay_status(repayApplySerialNo=self.repayRes['body']['repayApplySerialNo'])

        with allure.step('检查是否还款成功'):
            checkBizImpl.check_channel_repay_status(loan_invoice_id=loanInvoiceId, repay_term=repayTerm)


if __name__ == "__main__":
    pytest.main(['test_auto_jike_repay_bank.py'])
