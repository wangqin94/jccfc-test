import unittest
import warnings

from src.enums.EnumsCommon import ProductIdEnum
from src.impl.hair.HairBizImpl import HairBizImpl
from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl
from src.test_case.hair_dis.person import data


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.checkBizImpl = CheckBizImpl()
        self.repayPublicBizImpl = RepayPublicBizImpl()
        # 默认贴息产品号（主产品号）：G23E041， 否则非贴息产品号（子产品号）：G23E042
        self.productId = ProductIdEnum.HAIR_DISCOUNT.value
        self.hair = HairBizImpl(self.productId, data=data)

    """ 测试步骤 """
    def test_repay_apply(self, loanInvoiceId=None, term="1", repayDate='2023-05-21'):
        """ 测试步骤 """
        # 还款环境配置,清理缓存配置账务时间
        self.repayPublicBizImpl.pre_repay_config(repayDate=repayDate)

        # loanInvoiceId = '000LI0002174662201688194001'
        if not loanInvoiceId:
            credit_loan_invoice = self.hair.MysqlBizImpl.get_credit_database_info('credit_loan_invoice', certificate_no=data['cer_no'])
            loanInvoiceId = credit_loan_invoice['loan_invoice_id']
        self.loanInvoiceId = loanInvoiceId

        self.repayRes = self.hair.returnGoods_apply(loanInvoiceId=loanInvoiceId, term=term, repayDate=repayDate)

        # 自动入账
        self.repayPublicBizImpl.job.trigger_job_byId("751800549099302912")
        # 【引流】贴息入账自动处理定时任务
        self.repayPublicBizImpl.job.trigger_job_byId("859052136875552768")

    """ 后置条件处理 """
    def tearDown(self):
        # 数据库层校验还款状态
        self.checkBizImpl.check_channel_loan_compensation_status(loan_invoice_id=self.loanInvoiceId, compensation_type='02')


if __name__ == '__main__':
    unittest.main()
