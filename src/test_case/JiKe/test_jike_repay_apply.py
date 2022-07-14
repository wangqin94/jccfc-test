import unittest

from src.enums.EnumJiKe import JiKeApiRepayStatusEnum
from src.impl.JiKe.JiKeCheckBizImpl import JiKeCheckBizImpl
from src.impl.common.CheckBizImpl import *
import time
from src.impl.JiKe.JiKeBizImpl import JiKeBizImpl
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl
from src.test_case.JiKe.person import data


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 当前时间
        self.log = MyLog().get_log()
        self.MysqlBizImpl = MysqlBizImpl()
        self.CheckBizImpl = CheckBizImpl()
        self.repayPublicBizImpl = RepayPublicBizImpl()
        self.jikeCheckBizImpl = JiKeCheckBizImpl(data)

    """ 测试步骤 """
    def test_repay_apply(self):
        """ 测试步骤 """

        # 还款环境配置
        self.repayPublicBizImpl.pre_repay_config(repayDate=None)

        jike = JiKeBizImpl(data=data)
        credit_loan_invoice = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice', certificate_no=data['cer_no'])
        # repayGuaranteeFee: 担保费， 0<担保费<24红线-利息
        # repay_scene: 还款场景 EnumRepayScene ("01", "线上还款"),("02", "线下还款"),（"04","支付宝还款通知"）（"05","逾期（代偿、回购后）还款通知"）
        # loanInvoiceId: 借据号 必填
        # repay_type： 还款类型 1 按期还款； 2 提前结清； 7 提前还当期
        self.repayRes = json.loads(jike.repay_apply(repay_scene='01', repay_type='1', loanInvoiceId=credit_loan_invoice['loan_invoice_id']).get('body'))  # 按期还款

        # 输入指定借据号
        # self.repayRes = json.loads(jike.repay_apply(repay_scene='01', repay_type='1', loanInvoiceId="").get('body'))  # 按期还款

    """ 后置条件处理 """
    def tearDown(self):
        # 接口层校验授信结果是否符合预期
        status = self.jikeCheckBizImpl.jike_check_repay_status(self.repayRes['repayApplySerialNo'])
        self.assertEqual(JiKeApiRepayStatusEnum.SUCCESS.value, status, '还款失败')


if __name__ == '__main__':
    unittest.main()

