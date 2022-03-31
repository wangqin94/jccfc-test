import sys
import time

from engine.EnvInit import EnvInit
from src.enums.EnumsCommon import *
from src.impl.common.MysqlBizImpl import MysqlBizImpl


class CtripLoanCheckBizImpl(EnvInit):
    def __init__(self):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()

    def get_zhixin_bill_day(self):
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
        assert loanApply['status'] == '17', "支用成功"
        assert loanApply['product_id'] == 'F20B021', "产品码"
        assert loanApply['product_catalog'] == 'F0210001', "产品种类"
        assert loanApply['apply_term_unit'] == '4', "支用期限单位"
        assert loanApply['repay_method'] == '1', "还款方式"
        assert loanApply['loan_pay_mode'] == '1', "支付模式"
        assert loanApply['loan_pay_type'] == '0', "放款方式"
