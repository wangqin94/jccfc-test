# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：HairBizImpl.py
@Author  ：jccfc
@Date    ：2022/7/13 9:51
"""
from utils.Apollo import *
from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.hair.HairBizImpl import HairBizImpl
from src.impl.hair.HairCheckBizImpl import HairCheckBizImpl
from utils.Models import *


class HairSynBizImpl(HairBizImpl):
    def __init__(self, productId=None, data=None, person=False):
        super().__init__(productId=productId, data=data, person=person)

        self.CheckBizImpl = CheckBizImpl()
        self.hairCheckBizImpl = HairCheckBizImpl(self.productId, self.data)

    # 准备借款数据
    def preLoanapply(self, bill_date=None, term=12):
        """
        多层接口业务组装关键字：放款
        @param bill_date: 首期账单日时间 格式："2021-12-12"
        @param term: 放款期数
        @return:
        """
        # 绑卡
        hair = HairBizImpl(data=None)
        res = hair.getCardRealNameMessage().get('body')
        hair.bindCardRealName(userId=res['userId'], tradeSerialNo=res['tradeSerialNo'])

        # ocr配置默认不校验 (1：不验证，0：验证)
        apollo_data = dict()
        apollo_data['hj.channel.ocr.mock'] = "1"
        Apollo().update_config(appId='loan2.1-hapi-web', namespace='000', **apollo_data)

        # 发起授信申请
        thirdApplyId = json.loads(hair.credit(applyAmount=1000).get('body'))['thirdApplyId']

        # 数据库陈校验授信结果是否符合预期
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=thirdApplyId)
        # 接口层校验授信结果是否符合预期
        self.hairCheckBizImpl.hair_check_credit_apply_status(thirdApplyId)

        # 发起支用申请  loan_date: 放款时间，默认当前时间 eg:2022-01-01
        loanDate = time.strftime('%Y-%m-%d', time.localtime())
        hair.applyLoan(loan_date=loanDate, loanAmt=1000, term=term)

        # 数据库陈校验授信结果是否符合预期
        self.CheckBizImpl.check_loan_apply_status(thirdpart_apply_id=thirdApplyId)
        # 接口层校验授信结果是否符合预期
        self.hairCheckBizImpl.hair_check_loan_apply_status(thirdApplyId)

        # 更新资产asset_loan_invoice_info放款时间,apply_loan_date=loan_date:
        loan_apply_info = self.MysqlBizImpl.get_loan_apply_info(thirdpart_apply_id=thirdApplyId)
        credit_loan_invoice = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                         loan_apply_id=loan_apply_info['loan_apply_id'])
        loan_date = str(loanDate).replace("-", '')
        self.MysqlBizImpl.update_asset_database_info('asset_loan_invoice_info', attr="loan_invoice_id='{}'".format(
            credit_loan_invoice['loan_invoice_id']), apply_loan_date=loan_date)

        return bill_date


if __name__ == "__main__":
    hairBizImpl = HairSynBizImpl()
    hairBizImpl.preLoanapply(bill_date="2023-05-24")
