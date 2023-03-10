import unittest
import warnings

import time

from src.enums.EnumsCommon import ProductIdEnum
from src.impl.common.YinLiuCreateFileBizImpl import YinLiuRepayFile
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl
from src.test_case.halo.person import data


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.repayPublicBizImpl = RepayPublicBizImpl()

    """ 测试步骤 """
    # 哈喽 G23E031
    def test_repay_apply(self, productId=ProductIdEnum.HALO.value, repayDate=None):
        """ 测试步骤 """
        repayDate = repayDate if repayDate else time.strftime('%Y-%m-%d', time.localtime())

        # 还款环境配置,清理缓存配置账务时间
        self.repayPublicBizImpl.pre_repay_config(repayDate=repayDate)

        xiaoXRepayFile = YinLiuRepayFile(data, productId, repayTermNo='2', repayDate=repayDate)
        xiaoXRepayFile.creditBuyBackFile()

        self.repayPublicBizImpl.job.update_job('引流回购清单文件分片任务流', group=13, executeBizDateType='CUSTOMER', executeBizDate=repayDate.replace('-', ''))
        self.repayPublicBizImpl.job.trigger_job('引流回购清单文件分片任务流', group=13)
        time.sleep(3)

        # 自动入账
        # self.repayPublicBizImpl.job.trigger_job("自动入账处理任务流", group=13)
        # 输入指定借据号
        # self.repayRes = json.loads(HaLo.repay_apply(repay_scene='01', repay_type='1', loanInvoiceId="").get('body'))  # 按期还款

    """ 后置条件处理 """
    def tearDown(self):
        # 接口层校验授信结果是否符合预期
        pass


if __name__ == '__main__':
    unittest.main()
