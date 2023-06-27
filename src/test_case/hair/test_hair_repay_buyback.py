import unittest
import warnings
import time

from src.enums.EnumsCommon import ProductIdEnum
from src.impl.common.YinLiuCreateFileBizImpl import YinLiuRepayFile
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl
from src.test_case.hair.person import data


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.repayPublicBizImpl = RepayPublicBizImpl()
        self.productId = ProductIdEnum.HAIR.value

    """ 测试步骤 """
    def test_repay_apply(self, repayDate='2023-06-26'):
        """ 测试步骤 """
        repayDate = repayDate if repayDate else time.strftime('%Y-%m-%d', time.localtime())

        # 还款环境配置,清理缓存配置账务时间
        self.repayPublicBizImpl.pre_repay_config(repayDate=repayDate)

        hairRepayFile = YinLiuRepayFile(data, self.productId, repayTermNo='1', repayDate=repayDate)
        hairRepayFile.creditHairDisBuyBackFile()

        self.repayPublicBizImpl.job.update_job_byJobId('856176818498170880', group=13, executeBizDateType='CUSTOMER', executeBizDate=repayDate.replace('-', ''))
        self.repayPublicBizImpl.job.trigger_job_byId('856176818498170880')
        time.sleep(3)

        # 自动入账
        # self.repayPublicBizImpl.job.trigger_job_byId("751800549099302912")
        # 输入指定借据号
        # self.repayRes = json.loads(HaLo.repay_apply(repay_scene='01', repay_type='1', loanInvoiceId="").get('body'))  # 按期还款

    """ 后置条件处理 """
    def tearDown(self):
        # 接口层校验授信结果是否符合预期
        pass


if __name__ == '__main__':
    unittest.main()
