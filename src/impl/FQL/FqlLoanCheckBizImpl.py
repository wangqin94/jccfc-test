import sys
import time

from engine.EnvInit import EnvInit
from src.enums.EnumsCommon import *
from utils import GlobalVar as gl
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
            if (status != EnumLoanStatus.AUDITING.value) & (status != EnumLoanStatus.LOANING.value) & (status != EnumLoanStatus.LOAN_AUDITING.value) & (status != EnumLoanStatus.INITIALIZATION.value) & (status != EnumLoanStatus.TO_LOAN.value) :
                self.log.demsg('支用已终态-------')
                return loanApply
            else:
                self.log.demsg("支用审批状态处理中，请等待....")
                time.sleep(t)
                if j == m - 1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")
                    raise Exception("Invalid level!")


    def checkLoanApply1(self, loanApply):
        self.log.demsg(f"支用credit_loan_apply数据库信息校验----：{loanApply}")
        assert loanApply['status'] == '17', "支用成功"
        assert loanApply['product_id'] == ProductIdEnum.FQL.value, "产品码"
        assert loanApply['product_catalog'] == 'F0210001', "产品种类"
        assert loanApply['apply_amount'] == gl.get_value('loanRequestData')['body']['loanAmt'], "支用金额"
        assert loanApply['apply_term'] == gl.get_value('loanRequestData')['body']['loanTerm'], "支用期限"
        assert loanApply['apply_term_unit'] == '4', "支用期限单位"
        assert loanApply['repay_method'] == '1', "还款方式"
        assert loanApply['loan_pay_mode'] == '1', "支付模式：1自主支付"
        assert loanApply['loan_pay_type'] == '0', "放款方式：0线上"
        assert loanApply['loan_purpose'] == '5', "借款用途"
        assert loanApply['loan_type'] == '1', "支用类型：1借款一体"
        assert loanApply['user_name'] == gl.get_value('loanRequestData')['body']['name']
        assert loanApply['merchant_id'] == EnumMerchantId.FQL.value, "商户号"
        assert float(loanApply['apply_rate']) == float(gl.get_value('loanRequestData')['body']['interestRate']), "年利率"
        assert loanApply['user_tel'] == gl.get_value('loanRequestData')['body']['mobileNo'], "手机号"
        assert loanApply['certificate_type'] == '0', "证件类型"
        assert loanApply['certificate_no'] == gl.get_value('personData')['cer_no'], "身份证号"


    def checkLoanInvoice1(self,**kwargs):
        loanInvoice = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice', **kwargs)
        self.log.demsg(f"支用credit_loan_invoice数据库信息校验----：{loanInvoice}")
        assert loanInvoice['product_id'] == ProductIdEnum.FQL.value, "产品码"
        assert loanInvoice['product_catalog'] == 'F0210001', "产品种类"
        assert loanInvoice['user_name'] == gl.get_value('loanRequestData')['body']['name']
        assert loanInvoice['loan_amount'] == gl.get_value('loanRequestData')['body']['loanAmt'], "支用金额"
        assert float(loanInvoice['rate']) == float(gl.get_value('loanRequestData')['body']['interestRate']), "年利率"
        assert loanInvoice['status'] == '1', "状态：1使用中"
        assert loanInvoice['loan_type'] == '1', "放款方式"
        assert loanInvoice['merchant_id'] == EnumMerchantId.FQL.value, "商户号"
        assert loanInvoice['installment_amount'] == gl.get_value('loanRequestData')['body']['loanAmt'], "分期金额"
        assert loanInvoice['installment_num'] == gl.get_value('loanRequestData')['body']['loanTerm'], "分期期数"
        assert loanInvoice['user_tel'] == gl.get_value('loanRequestData')['body']['mobileNo'], "手机号"
        assert loanInvoice['certificate_type'] == '0', "证件类型"
        assert loanInvoice['certificate_no'] == gl.get_value('personData')['cer_no'], "身份证号"

        return loanInvoice


    def queryRepayPlanInfo(self,**kwargs):
        repayPlanInfo = self.MysqlBizImpl.get_asset_database_info('asset_repay_plan', **kwargs)
        self.log.demsg(f"资产还款计划asset_repay_plan信息----：{repayPlanInfo}")
        return repayPlanInfo