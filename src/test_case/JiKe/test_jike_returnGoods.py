import time
import unittest
import warnings

from src.impl.JiKe.JiKeBizImpl import JiKeBizImpl
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl
from src.test_case.JiKe.person import data


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.jike = JiKeBizImpl(data=data)
        self.repayPublicBizImpl = RepayPublicBizImpl()

    """ 测试步骤 """
    def test_repay_apply(self, loanInvoiceId=None, repayDate=None, repayTerm=2):
        """ 测试步骤 """
        repayDate = repayDate if repayDate else time.strftime('%Y-%m-%d', time.localtime())
        # 还款环境配置--退货无法切日，只能当前时间发起退货
        self.repayPublicBizImpl.pre_repay_config(repayDate=repayDate)
        if not loanInvoiceId:
            credit_loan_invoice = self.jike.MysqlBizImpl.get_credit_database_info('credit_loan_invoice', certificate_no=data['cer_no'])
            loanInvoiceId = credit_loan_invoice['loan_invoice_id']
        self.jike.returnGoods_apply(loanInvoiceId=loanInvoiceId, term=repayTerm, repayDate=repayDate)

        # 自动入账
        self.repayPublicBizImpl.job.trigger_job_byId("751800549099302912")

    """ 后置条件处理 """
    def tearDown(self):
        # 接口层校验授信结果是否符合预期
        pass


if __name__ == '__main__':
    unittest.main()
