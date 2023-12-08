# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：JiKeBizImpl.py
@Author  ：jccfc
@Date    ：2022/7/13 9:51
"""
from src.impl.public.LoanPublicBizImpl import LoanPublicBizImpl
from utils.Apollo import *
from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.JiKe.JiKeBizImpl import JiKeBizImpl
from src.impl.JiKe.JiKeCheckBizImpl import JiKeCheckBizImpl
from utils.GlobalVar import GlobalMap
from utils.Models import *


class JiKeSynBizImpl(JiKeBizImpl):
    def __init__(self, data=None, encrypt_flag=True, person=False):
        super().__init__(data=data, encrypt_flag=encrypt_flag, person=person)
        self.CheckBizImpl = CheckBizImpl()
        self.globalMap = GlobalMap()
        self.jikeCheckBizImpl = JiKeCheckBizImpl(data)

    # 准备借款数据
    def preLoanApply(self, loanDate=None, term=12, **kwargs):
        """
        多层接口业务组装关键字：放款  eg:2022-01-01
        @param loanDate: 放款时间，默认当前系统时间
        @param term: 放款期数
        @return:
        """
        # 绑卡
        jike = JiKeBizImpl(data=self.data)
        jike.sharedWithholdingAgreement()

        # ocr配置默认不校验 (1：不验证，0：验证)
        apollo_data = dict()
        apollo_data['hj.channel.ocr.mock'] = "1"
        Apollo().update_config(appId='loan2.1-hapi-web', namespace='000', **apollo_data)

        # 放款金额随机（规避同3分钟内有多笔放款规则）
        amount = random.randint(1000, 9999)

        # 发起授信申请
        thirdApplyId = jike.credit(applyAmount=amount, loanTerm=term)['body']['thirdApplyId']
        # 三方申请号thirdApplyId写入全局变量
        self.globalMap.set_map('thirdApplyId', thirdApplyId)

        # 数据库陈校验授信结果是否符合预期
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=thirdApplyId)
        # 接口层校验授信结果是否符合预期
        self.jikeCheckBizImpl.jike_check_credit_apply_status(thirdApplyId)

        # loanDate: 放款时间，默认当前时间 eg:2022-01-01
        loanDate = loanDate if loanDate else time.strftime('%Y-%m-%d', time.localtime())
        # 放款时间loanDate写入全局变量
        self.globalMap.set_map('loanDate', loanDate)

        # 配置放款时间mock
        apollo_data = dict()
        apollo_data['credit.loan.trade.date.mock'] = "true"
        apollo_data['credit.loan.date.mock'] = loanDate
        self.apollo.update_config(appId='loan2.1-public', namespace='JCXF.system', **apollo_data)
        # 发起支用申请
        loanRes = jike.applyLoan(loan_date=loanDate, loanAmt=amount, loanTerm=term, **kwargs)

        # 数据库陈校验放款结果是否符合预期
        self.CheckBizImpl.check_loan_apply_status(thirdpart_apply_id=thirdApplyId)
        # 接口层校验放款结果是否符合预期
        self.jikeCheckBizImpl.jike_check_loan_apply_status(thirdApplyId)

        # 更新放款时间
        loanPublicBizImpl = LoanPublicBizImpl()
        loanInvoiceId = loanPublicBizImpl.updateLoanInfo(thirdLoanId=thirdApplyId, loanDate=loanDate)

        # 关闭放款mock
        loanPublicBizImpl.updateLoanDateMock(flag=False)

        # 借据号loanInvoiceId写入全局变量
        self.globalMap.set_map('loanInvoiceId', loanInvoiceId)

        return loanRes


if __name__ == "__main__":
    JiKeBizImpl = JiKeSynBizImpl()
    JiKeBizImpl.preLoanApply(bill_date='2023-01-01')
