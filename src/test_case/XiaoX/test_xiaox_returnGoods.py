import unittest
import warnings

from src.impl.XiaoX.XiaoXBizImpl import XiaoXBizImpl
from src.test_case.XiaoX.person import data


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.XiaoX = XiaoXBizImpl(data=data)

    """ 测试步骤 """
    def test_repay_apply(self):
        """ 测试步骤 """
        loanInvoiceId = '000LI0002174662201688194001'
        if not loanInvoiceId:
            credit_loan_invoice = self.XiaoX.MysqlBizImpl.get_credit_database_info('credit_loan_invoice', certificate_no=data['cer_no'])
            loanInvoiceId = credit_loan_invoice['loan_invoice_id']
        self.XiaoX.returnGoods_apply(loanInvoiceId=loanInvoiceId, term=1, repayDate='2022-07-01')

    """ 后置条件处理 """
    def tearDown(self):
        # 接口层校验授信结果是否符合预期
        pass


if __name__ == '__main__':
    unittest.main()
