# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：JuZiBizImpl.py
@Author  ：jccfc
@Date    ：2022/7/13 9:51
"""
from src.impl.public.LoanPublicBizImpl import LoanPublicBizImpl
from utils.Apollo import *
from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.juzi.JuZiBizImpl import JuZiBizImpl
from src.impl.juzi.JuZiCheckBizImpl import JuZiCheckBizImpl
from utils.Models import *


class JuZiSynBizImpl(JuZiBizImpl):
    def __init__(self, data=None, person=False):
        super().__init__(data=data, person=person)

        self.CheckBizImpl = CheckBizImpl()
        self.juziCheckBizImpl = JuZiCheckBizImpl(self.productId, self.data)

    # 准备借款数据
    def preLoanApply(self, bill_date=None, term=12):
        """
        多层接口业务组装关键字：放款
        @param bill_date: 首期账单日时间 格式："2021-12-12"
        @param term: 放款期数
        @return:
        """
        # 绑卡
        juzi = JuZiBizImpl(data=None)
        res = juzi.getCardRealNameMessage().get('body')
        juzi.bindCardRealName(userId=res['userId'], tradeSerialNo=res['tradeSerialNo'])

        # ocr配置默认不校验 (1：不验证，0：验证)
        apollo_data = dict()
        apollo_data['hj.channel.ocr.mock'] = "1"
        Apollo().update_config(appId='loan2.1-hapi-web', namespace='000', **apollo_data)

        # 发起授信申请
        thirdApplyId = json.loads(self.credit(applyAmount=1000).get('body'))['thirdApplyId']

        # 数据库陈校验授信结果是否符合预期
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=thirdApplyId)
        # 接口层校验授信结果是否符合预期
        self.juziCheckBizImpl.juzi_check_credit_apply_status(thirdApplyId)

        # 发起支用申请  loan_date: 放款时间，默认当前时间 eg:2022-01-01
        loanDate = time.strftime('%Y-%m-%d', time.localtime())
        self.applyLoan(loan_date=loanDate, loanAmt=1000, term=term)

        # 数据库陈校验授信结果是否符合预期
        self.CheckBizImpl.check_loan_apply_status(thirdpart_apply_id=thirdApplyId)
        # 接口层校验授信结果是否符合预期
        self.juziCheckBizImpl.juzi_check_loan_apply_status(thirdApplyId)

        # 更新放款时间
        loanPublicBizImpl = LoanPublicBizImpl()
        loanPublicBizImpl.updateLoanInfo(thirdLoanId=thirdApplyId, loanDate=loanDate)

        # 关闭放款mock
        loanPublicBizImpl.updateLoanDateMock(flag=False)

        return bill_date


if __name__ == "__main__":
    juziBizImpl = JuZiSynBizImpl()
    juziBizImpl.preLoanApply(bill_date="2023-05-24")
