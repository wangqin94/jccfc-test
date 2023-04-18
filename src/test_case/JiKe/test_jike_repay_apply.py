import json
import unittest
import warnings

from src.enums.EnumJiKe import JiKeApiRepayStatusEnum, StatusCodeEnum
from src.impl.JiKe.JiKeCheckBizImpl import JiKeCheckBizImpl
import time
from src.impl.JiKe.JiKeBizImpl import JiKeBizImpl
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl
from src.test_case.JiKe.person import data


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 当前时间
        self.repayPublicBizImpl = RepayPublicBizImpl()
        self.jikeCheckBizImpl = JiKeCheckBizImpl(data)

    """ 测试步骤 """
    def test_repay_apply(self, repayDate="2023-04-17"):
        """ 测试步骤 """
        repayDate = repayDate if repayDate else time.strftime('%Y-%m-%d', time.localtime())
        # 还款环境配置
        self.repayPublicBizImpl.pre_repay_config(repayDate=repayDate)

        jike = JiKeBizImpl(data=data)
        credit_loan_invoice = jike.MysqlBizImpl.get_credit_database_info('credit_loan_invoice', certificate_no=data['cer_no'])
        # repayGuaranteeFee: 担保费， 0<担保费<24红线-利息
        # repay_scene: 还款场景 EnumRepayScene ("01", "线上还款"),("02", "线下还款"),（"04","支付宝还款通知"）（"05","逾期（代偿、回购后）还款通知"）
        # loanInvoiceId: 借据号 必填
        # repay_type： 还款类型 1 按期还款； 2 提前结清； 7 提前还当期
        # self.repayRes = jike.repay_apply(repay_scene='02', repay_type='7', loanInvoiceId=credit_loan_invoice['loan_invoice_id'], repayGuaranteeFee=30, repayDate=repayDate)  # 按期还款
        self.repayRes = jike.repay_apply(repay_scene='04', repay_type='7', repayTerm=1, loanInvoiceId='000LI0001362535425950508001', repayGuaranteeFee=10, repayDate=repayDate)  # 按期还款

        self.assertEqual(StatusCodeEnum.SUCCESS.code, self.repayRes['head']['returnCode'], '还款接口层失败')

        # 自动入账
        self.repayPublicBizImpl.job.trigger_job("自动入账处理任务流", group=13)
        # 输入指定借据号
        # self.repayRes = json.loads(jike.repay_apply(repay_scene='01', repay_type='1', loanInvoiceId="").get('body'))  # 按期还款

    """ 后置条件处理 """
    def tearDown(self):
        # 接口层校验授信结果是否符合预期
        status = self.jikeCheckBizImpl.jike_check_repay_status(self.repayRes['body']['repayApplySerialNo'])
        self.assertEqual(JiKeApiRepayStatusEnum.REPAY_SUCCESS.value, status, '还款失败')


if __name__ == '__main__':
    unittest.main()
