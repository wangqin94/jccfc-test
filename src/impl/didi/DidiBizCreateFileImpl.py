from src.impl.common.YinLiuCreateFileBizImpl import YinLiuRepayFile


class DidiBizCreateFileImpl(YinLiuRepayFile):
    def __init__(self, userData, productId, loanInvoiceId=None, repayTermNo='1', repayDate="2021-08-06"):
        super().__init__(userData, productId, loanInvoiceId, repayTermNo, repayDate)

        # 6、repay_plan - 还款计划文件
        self.repay_plan_temple = {
            "loan_order_id", "trust_plan_no", "term_no", "start_date",
        }
        # 7、repay_loan_details - 还款(借据)明细文件
        self.repay_loan_details_temple = {
            "loan_order_id",
            "trust_plan_no",
            "seq_no",
            "payment_seq_no",
            "fund_seq_no",
            "loan_forms",
            "repay_acct_no",
            "repay_type",
            "repay_date",
            "repay_amt",
            "paid_prin_amt",
            "paid_int_amt",
            "paid_ovd_prin_pnlt_amt",
            "fee_amt",
            "int_fee_amt",
            "prin_pnlt_fee_amt",
            "loan_type",
            "fin_product_type",
            "paid_advance_clear_amt",
            "profit_advance_clear_amt",
            "ver_loan_forms",
            "paid_guarantee_fee_amt",
            "pay_channel"
        }

        # 8、repay_term_details - 还款(分期)明细文件
        self.repay_term_details_temple = {
            "loan_order_id",
            "trust_plan_no",
            "seq_no",
            "loan_forms",
            "repay_acct_no",
            "term_no",
            "repay_amt_type",
            "repay_type",
            "repay_date",
            "repay_amt",
            "paid_prin_amt",
            "paid_int_amt",
            "paid_ovd_prin_pnlt_amt",
            "fund_seq_no",
            "ver_loan_forms",
            "paid_guarantee_fee_amt",
            "pay_channel",
        }

        # 9、exempt_loan_details - 减免（借据）明细文件
        self.exempt_loan_details_temple = {
            "loan_order_id",
            "trust_plan_no",
            "seq_no",
            "loan_forms",
            "exempt_type",
            "exempt_date",
            "exempt_amt",
            "exempt_prin_amt",
            "exempt_int_amt",
            "exempt_ovd_prin_pnlt_amt",
            "loan_type",
            "exempt_advance_clear_amt",
            "fin_product_type",
            "ver_loan_forms"
        }

        # 10、exempt_term_details - 减免（分期）明细文件
        self.exempt_term_details_temple = {
            "loan_order_id",
            "trust_plan_no",
            "seq_no",
            "loan_forms",
            "exempt_type",
            "term_no",
            "exempt_amt",
            "exempt_prin_amt",
            "exempt_int_amt",
            "exempt_ovd_prin_pnlt_amt",
            "ver_loan_forms",
        }

        #