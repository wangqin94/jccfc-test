import sys
import time

from engine.EnvInit import EnvInit
from src.enums import global_var as gl
from src.enums.EnumsCommon import *
from src.impl.common.MysqlBizImpl import MysqlBizImpl


class FqlLoanCheckBizImpl(EnvInit):
    def __init__(self):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()

    def check_loan_apply_status(self, m=10, t=3, **kwargs):
        """
        @param kwargs: 查询条件
        @param t: 每次时间间隔, 默认5S
        @param m: 查询轮训次数 默认10次
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('支用结果校验...')
        flag = 2
        for i in range(flag + 1):
            loanApply = self.MysqlBizImpl.get_loan_apply_info(**kwargs)
            if not loanApply:
                self.log.info("credit_loan_apply未查询到支用记录，启动3次轮训")
                time.sleep(t)
                if i == flag:
                    self.log.error("超过当前系统设置等待时间，支用异常，请手动查看结果....")
                    sys.exit(7)
            else:
                self.log.info("支用记录已入loan_apply表")
                break
        for j in range(m):
            loanApply = self.MysqlBizImpl.get_loan_apply_info(**kwargs)
            status = loanApply['status']
            if (status != EnumLoanStatus.AUDITING.value) & (status != EnumLoanStatus.LOANING.value) & (status != EnumLoanStatus.LOAN_AUDITING.value):
                self.log.demsg('支用已终态-------')
                return loanApply
            else:
                self.log.demsg("支用审批状态处理中，请等待....")
                time.sleep(t)
                if j == m - 1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")


    def checkLoanApply1(self, loanApply):
        self.log.demsg(f"支用credit_loan_apply数据库信息校验----：{loanApply}")
        assert loanApply['status'] == '03', "授信成功"
        assert loanApply['product_id'] == 'F021108', "产品码"
        assert loanApply['product_catalog'] == 'F0210001', "产品种类"
        assert loanApply['apply_amount'] == '1000', "产品种类"
        assert loanApply['apply_term'] == 12, "支用期限"
        assert loanApply['apply_term_unit'] == '4', "支用期限单位"
        assert loanApply['repay_method'] == '1', "还款方式"
        assert loanApply['loan_pay_mode'] == '1', "支付模式"
        assert loanApply['loan_pay_type'] == '0', "放款方式"
        assert loanApply['loan_purpose'] == '5', "借款用途"
        assert loanApply['loan_type'] == '1', "支用期限单位"

