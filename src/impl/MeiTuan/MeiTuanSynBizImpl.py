# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：ZhiXinBizImpl.py
@Author  ：jccfc
@Date    ：2022/1/13 9:51 
"""
from utils.Apollo import *
from src.enums.EnumZhiXin import *
from src.enums.EnumsCommon import *
from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.zhixin.ZhiXinBizImpl import ZhiXinBizImpl
from src.impl.zhixin.ZhiXinCheckBizImpl import ZhiXinCheckBizImpl
from utils.Models import *


def get_zhixin_bill_day():
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
    bill_day = bill_day - 4 if bill_day > 27 else bill_day
    bill_data = '{}-{}-{}'.format(str(bill_year), str("%02d" % bill_month), str("%02d" % bill_day))
    return bill_data


class MeiTuanSynBizImpl(ZhiXinBizImpl):
    def __init__(self, data=None, encrypt_flag=True, person=False):
        super().__init__(data=data, encrypt_flag=encrypt_flag, person=person)
        self.CheckBizImpl = CheckBizImpl()
        self.zhiXinCheckBizImpl = ZhiXinCheckBizImpl(data)

    # 准备借款数据
    def preLoanapply(self, month=3, bill_date=None, term='12'):
        """
        多层接口业务组装关键字：放款
        @param month: 放款时间月份时间 0：当前月 1：前一月
        @param bill_date: 首期账单日时间 格式："2021-12-12"
        @param term: 放款期数
        @return:
        """
        # 绑卡
        res = json.loads(self.applyCertification().get('output'))
        self.verifyCode(userId=res['userId'], certificationApplyNo=res['certificationApplyNo'],
                        cdKey=res['cdKey'])

        # 发起授信申请
        creditRes = json.loads(self.credit().get('output'))
        creditApplyNo = creditRes['creditApplyNo']

        # 数据库陈校验授信结果是否符合预期
        status = self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=creditApplyNo)
        assert EnumCreditStatus.SUCCESS.value == status, '授信失败'
        # 接口层校验授信结果是否符合预期
        status = self.zhiXinCheckBizImpl.check_credit_apply_status(creditRes['userId'], creditRes['creditApplyNo'])
        assert ZhiXinApiStatusEnum.SUCCESS.value == status, '授信失败'

        # 设置apollo放款mock时间 默认当前时间前两月日期month=3 eg:当前时间2022-01-13 放款时间2021-11-13 账单日2021-12-13
        bill_date = bill_date if bill_date else get_zhixin_bill_day()
        loan_date = get_custom_month(month=-month, date=bill_date)
        apollo_data = dict()
        apollo_data['credit.loan.trade.date.mock'] = "true"
        apollo_data['credit.loan.date.mock'] = loan_date
        Apollo().update_config(appId='loan2.1-public', namespace='JCXF.system', **apollo_data)

        # 发起支用申请
        loanRes = json.loads(self.applyLoan(loanAmt='1000', term=term).get('output'))
        loanApplyNo = loanRes['loanApplyNo']

        # 数据库陈校验授信结果是否符合预期
        status = self.CheckBizImpl.check_loan_apply_status(thirdpart_apply_id=loanApplyNo)
        assert EnumLoanStatus.ON_USE.value == status, '支用失败'
        # 接口层校验授信结果是否符合预期
        status = self.zhiXinCheckBizImpl.check_loan_apply_status(loanRes['userId'], loanRes['loanApplyNo'])
        assert ZhiXinApiStatusEnum.SUCCESS.value == status, '支用失败'

        # 更新资产asset_loan_invoice_info放款时间,apply_loan_date=loan_date:
        loan_apply_info = self.MysqlBizImpl.get_loan_apply_info(thirdpart_apply_id=loanApplyNo)
        credit_loan_invoice = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                         loan_apply_id=loan_apply_info['loan_apply_id'])
        loan_date = str(loan_date).replace("-", '')
        self.MysqlBizImpl.update_asset_database_info('asset_loan_invoice_info', attr="loan_invoice_id='{}'".format(
            credit_loan_invoice['loan_invoice_id']), apply_loan_date=loan_date)

        return bill_date


if __name__ == "__main__":
    # m = get_zhixin_bill_day()
    # print(m)
    ZhiXinBizImpl = ZhiXinSynBizImpl()
    ZhiXinBizImpl.preLoanapply(month=3)
