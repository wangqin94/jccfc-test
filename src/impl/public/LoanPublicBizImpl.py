# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：LoanPublicBizImpl.py
@Author  ：jccfc
@Date    ：2022/5/31 11:10 
"""
import time

from engine.MysqlInit import MysqlInit
from src.impl.common.MysqlBizImpl import MysqlBizImpl


class LoanPublicBizImpl(MysqlInit):
    def __init__(self):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()

    def updateLoanInfo(self, thirdLoanId, loanDate=None):
        """
        若放款使用mock时间，需要手动更新支用申请时间和借据放款时间
        @param thirdLoanId: 三方借据号
        @param loanDate: 放款时间 格式："2021-12-12", 默认当前时间
        @return:
        """
        self.log.demsg("更新loan_apply放款时间apply_time、loan_pay_time")
        loanDate = loanDate if loanDate else time.strftime('%Y-%m-%d', time.localtime())
        self.MysqlBizImpl.update_credit_database_info('credit_loan_apply', attr="third_loan_invoice_id='{}'".format(
            thirdLoanId), apply_time="{} 13:57:59".format(loanDate), loan_pay_time="{} 13:57:59".format(loanDate))

        self.log.demsg("更新credit_loan_invoice放款时间loan_pay_time")
        loanApplyInfo = self.MysqlBizImpl.get_loan_apply_info(third_loan_invoice_id=thirdLoanId)
        self.MysqlBizImpl.update_credit_database_info('credit_loan_invoice',
                                                      attr="loan_apply_id='{}'".format(loanApplyInfo['loan_apply_id']),
                                                      loan_pay_time="{} 13:57:59".format(loanDate))

        # 获取借据号
        loanInvoiceInfo = self.MysqlBizImpl.get_loan_invoice_info(loan_apply_id=loanApplyInfo['loan_apply_id'])
        loanInvoiceId = loanInvoiceInfo['loan_invoice_id']

        # 更新资产asset_loan_invoice_info放款时间,apply_loan_date=loan_date:
        self.log.demsg("更新asset_loan_invoice_info放款时间apply_loan_date")
        loanDateFormat = str(loanDate).replace("-", '')
        self.MysqlBizImpl.update_asset_database_info('asset_loan_invoice_info', attr="loan_invoice_id='{}'".format(
            loanInvoiceId), apply_loan_date=loanDateFormat)


if __name__ == '__main__':
    loanPublicBizImpl = LoanPublicBizImpl()
    loanPublicBizImpl.updateLoanInfo(thirdLoanId='thirdApplyId16600975192885739', loanDate='2022-07-10')