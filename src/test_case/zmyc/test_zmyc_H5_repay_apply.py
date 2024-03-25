import unittest
import warnings

from src.enums.EnumYinLiu import YinLiuApiRepayStatusEnum, StatusCodeEnum
from src.impl.zmyc.ZMYCCheckBizImpl import ZMYCCheckBizImpl
import time
from src.impl.zmyc.ZMYCBizImpl import ZMYCBizImpl
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl
from src.test_case.zmyc.person import data


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 当前时间
        self.repayPublicBizImpl = RepayPublicBizImpl()
        # self.ZMYCCheckBizImpl = ZMYCCheckBizImpl(merchantId=None, data=data)

    """ 测试步骤 """
    def test_repay_apply(self, repayDate="2023-06-10"):
        """ 测试步骤 """
        repayDate = repayDate if repayDate else time.strftime('%Y-%m-%d', time.localtime())
        # 还款环境配置
        # self.repayPublicBizImpl.pre_repay_config(repayDate=repayDate)

        zmyc = ZMYCBizImpl(data=data)
        # repayType：0 按期还款；1 提前结清
        # paymentType： 1 支付宝主动还款 5 银行卡主动还款
        self.repayRes = zmyc.payment(loan_invoice_id='000LI0001312335848820098052', paymentType='5', repayType="0", repayTerm="1")  # 按期还款

        self.assertEqual(StatusCodeEnum.SUCCESS.code, self.repayRes['head']['returnCode'], '还款接口层失败')

        # 更新H5还款订单状态--credit_offline_payment_apply
        time.sleep(20)
        self.repayPublicBizImpl.job.trigger_job("贷后H5线下还款状态更新任务流", group=13)

    """ 后置条件处理 """
    def tearDown(self):
        # 接口层校验授信结果是否符合预期
        pass


if __name__ == '__main__':
    unittest.main()
