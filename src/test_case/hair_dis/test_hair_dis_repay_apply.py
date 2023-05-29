import unittest
import warnings

from src.enums.EnumYinLiu import YinLiuApiRepayStatusEnum, StatusCodeEnum
from src.enums.EnumsCommon import ProductIdEnum
from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.hair.HairCheckBizImpl import HairCheckBizImpl
import time
from src.impl.hair.HairBizImpl import HairBizImpl
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl
from src.test_case.hair_dis.person import data


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 当前时间
        self.repayPublicBizImpl = RepayPublicBizImpl()
        self.checkBizImpl = CheckBizImpl()
        # 默认贴息产品号（主产品号）：G23E041， 否则非贴息产品号（子产品号）：G23E042
        self.productId = ProductIdEnum.HAIR_DISCOUNT.value
        self.hairCheckBizImpl = HairCheckBizImpl(self.productId, data)
        self.hair = HairBizImpl(self.productId, data=data)

    """ 测试步骤 """
    def test_repay_apply(self, repayDate="2023-05-16"):
        """ 测试步骤 """
        repayDate = repayDate if repayDate else time.strftime('%Y-%m-%d', time.localtime())
        # 还款环境配置
        self.repayPublicBizImpl.pre_repay_config(repayDate=repayDate)

        credit_loan_invoice = self.hair.MysqlBizImpl.get_credit_database_info('credit_loan_invoice', certificate_no=data['cer_no'])
        # repayGuaranteeFee: 担保费， 0<担保费<24红线-利息
        # repay_scene: 还款场景 EnumRepayScene ("01", "线上还款"),("02", "线下还款"),（"04","支付宝还款通知"）（"05","逾期（代偿、回购后）还款通知"）
        # loanInvoiceId: 借据号 必填
        # repay_type： 还款类型 1 按期还款； 2 提前结清； 7 提前还当期
        self.repayRes = self.hair.repay_apply(repay_scene='01', repay_type='2', loanInvoiceId=credit_loan_invoice['loan_invoice_id'], repayGuaranteeFee=30, repayDate=repayDate)  # 按期还款
        # self.repayRes = hair.repay_apply(repay_scene='01', repay_type='1', repayTerm=1, loanInvoiceId='000LI0001362535425950508001', repayGuaranteeFee=10, repayDate=repayDate)  # 按期还款

        self.assertEqual(StatusCodeEnum.SUCCESS.code, self.repayRes['head']['returnCode'], '还款接口层失败')

        # 自动入账定时任务
        self.repayPublicBizImpl.job.trigger_job_byId("751800549099302912")
        # 【引流】账单日机构贴息批量还款入账定时任务流
        self.repayPublicBizImpl.job.trigger_job_byId("859053695655079936")

    """ 后置条件处理 """
    def tearDown(self):
        # 接口层校验授信结果是否符合预期
        status = self.hairCheckBizImpl.hair_check_repay_status(self.repayRes['body']['repayApplySerialNo'])
        self.assertEqual(YinLiuApiRepayStatusEnum.REPAY_SUCCESS.value, status, '还款失败')

        # 数据库层校验还款状态
        self.checkBizImpl.check_channel_repay_status(third_repay_id=self.repayRes['body']['repayApplySerialNo'])


if __name__ == '__main__':
    unittest.main()
