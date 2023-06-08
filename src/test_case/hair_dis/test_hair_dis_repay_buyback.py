import unittest
import warnings
import time

from src.enums.EnumsCommon import ProductIdEnum
from src.impl.common.YinLiuCreateFileBizImpl import YinLiuRepayFile
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl
from src.test_case.hair_dis.person import data


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.repayPublicBizImpl = RepayPublicBizImpl()
        self.productId = ProductIdEnum.HAIR_DISCOUNT.value

    """ 测试步骤 """
    def test_repay_apply(self, repayDate='2024-01-15'):
        """ 测试步骤 """
        repayDate = repayDate if repayDate else time.strftime('%Y-%m-%d', time.localtime())

        # 还款环境配置,清理缓存配置账务时间
        self.repayPublicBizImpl.pre_repay_config(repayDate=repayDate)

        hairRepayFile = YinLiuRepayFile(data, self.productId, repayTermNo='7', repayDate=repayDate, loanInvoiceId='000LI0001362535425950765007')
        hairRepayFile.creditBuyBackFile()

        self.repayPublicBizImpl.job.update_job('【引流】回购清单文件分片任务流', group=13, executeBizDateType='CUSTOMER', executeBizDate=repayDate.replace('-', ''))
        self.repayPublicBizImpl.job.trigger_job('【引流】回购清单文件分片任务流', group=13)
        time.sleep(3)

        # 自动入账
        self.repayPublicBizImpl.job.trigger_job_byId("751800549099302912")
        # 【引流】贴息入账自动处理定时任务
        self.repayPublicBizImpl.job.trigger_job_byId("859052136875552768")

    """ 后置条件处理 """
    def tearDown(self):
        # 接口层校验授信结果是否符合预期
        pass


if __name__ == '__main__':
    unittest.main()
