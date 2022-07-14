# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test
@File    ：ZhiXinBizImpl.py
@Author  ：jccfc
@Date    ：2022/1/13 9:51
"""
import pytest

from src.impl.WLD.WldBizImpl import WldBizImpl
from src.impl.WLD.WldCheckBizImpl import WldCheckBizImpl
from utils.Apollo import *
from src.enums.EnumWld import *
from src.enums.EnumsCommon import *
from src.impl.common.CheckBizImpl import CheckBizImpl
from utils.Models import *


def get_wld_bill_day():
    """
    :return: 返回首期账单日
    """
    date = time.strftime('%Y-%m-%d', time.localtime())  # 当前时间

    date_list = str(date).split('-')
    bill_year, bill_month, bill_day = map(int, date_list)
    bill_month += 1
    if bill_month > 12:
        bill_year += 1
        bill_month -= 12
    bill_day =  28 if bill_day > 28 else bill_day

    bill_data = '{}-{}-{}'.format(str(bill_year), str("%02d" % bill_month), str("%02d" % bill_day))
    return bill_data


class WldSynBizImpl(WldBizImpl):
    def __init__(self, data=None, encrypt_flag=True, person=False):
        super().__init__(data=data, encrypt_flag=encrypt_flag, person=person)
        self.checkBizImpl = CheckBizImpl()
        self.wldCheckBizImpl = WldCheckBizImpl(data)

    # 准备借款数据

    def  preLoanapply(self, month=0, bill_date=None, term='12'):
        """
        多层接口业务组装关键字：放款
        @param month: 放款时间月份时间 0：当前月 1：前一月
        @param bill_date: 首期账单日时间 格式："2021-12-12"
        @param term: 放款期数
        @return:
        """
        # 绑卡
        self.bind_card()
        bindres = self.confirm_bind_card()
        u_id = bindres['body']['userId']

        # 绑卡-校验
        qbindres = self.query_bind_card(user_id=u_id)
        qbindres2 = qbindres['body']['retDesc']

        # 授信
        creditres = self.credit(loanTerm=term, applyAmount=3000)
        creditApplyNo = creditres['body']['thirdApplyId']

        # 授信校验-数据库层
        time.sleep(5)
        self.checkBizImpl.check_credit_apply_status(thirdpart_apply_id=creditApplyNo)

        # 授信校验-接口
        self.wldCheckBizImpl.check_credit_apply_status(thirdapplyid=creditApplyNo)

        # 设置apollo放款mock时间 默认当前时间
        bill_date = bill_date if bill_date else get_wld_bill_day()
        print(bill_date)
        loan_date = get_custom_month(month=-1, date=bill_date)
        apollo_data = dict()
        apollo_data['credit.loan.trade.date.mock'] = "true"
        apollo_data['credit.loan.date.mock'] = loan_date
        Apollo().update_config(appId='loan2.1-public', namespace='JCXF.system', **apollo_data)



        # 支用
        loanres = self.loan()
        loanapplyno = loanres['body']['thirdApplyId']

        # 支用校验-数据库层
        time.sleep(5)
        status = self.checkBizImpl.check_loan_apply_status(thirdpart_apply_id=loanapplyno)
        assert EnumLoanStatus.ON_USE.value == status, '支用失败'

        # 支用授信校验-接口
        status = self.wldCheckBizImpl.check_loan_apply_status(loanres['body']['thirdApplyId'])
        assert WldApiStatusEnum.QUERY_LOAN_RESULT_S.value == status, '支用失败'


        # 更新资产asset_loan_invoice_info放款时间,apply_loan_date=loan_date:
        loan_apply_info = self.MysqlBizImpl.get_loan_apply_info(thirdpart_apply_id=loanapplyno)
        credit_loan_invoice = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                         loan_apply_id=loan_apply_info['loan_apply_id'])
        loan_date = str(loan_date).replace("-", '')
        self.MysqlBizImpl.update_asset_database_info('asset_loan_invoice_info', attr="loan_invoice_id='{}'".format(
            credit_loan_invoice['loan_invoice_id']), apply_loan_date=loan_date)

        return bill_date


if __name__ == "__main__":
    # m = get_zhixin_bill
    # _day()
    # print(m)
    # WldBizImpl = WldSynBizImpl()
    # WldBizImpl.preLoanapply(month=0)
    a = get_wld_bill_day()
    print(a)




