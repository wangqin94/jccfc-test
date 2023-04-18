import unittest
import warnings

import time

from src.enums.EnumsCommon import ProductIdEnum
from src.impl.common.YinLiuCreateFileBizImpl import YinLiuRepayFile
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl
from src.test_case.halo.person import data
from utils.Apollo import Apollo


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.repayPublicBizImpl = RepayPublicBizImpl()

    """ 测试步骤 """
    # 哈喽 G23E031
    def test_repay_apply(self, productId=ProductIdEnum.HALO.value, repayDate='2023-03-15'):
        """ 测试步骤 """
        repayDate = repayDate if repayDate else time.strftime('%Y-%m-%d', time.localtime())

        # 配置还款mock时间
        updateKeys = dict()
        updateKeys['credit.mock.repay.trade.date'] = "true"  # credit.mock.repay.trade.date
        updateKeys['credit.mock.repay.date'] = "{} 12:00:00".format(repayDate)
        Apollo().update_config(appId='loan2.1-public', namespace='JCXF.system', **updateKeys)

        # 还款环境配置,清理缓存配置账务时间
        self.repayPublicBizImpl.pre_repay_config(repayDate=repayDate)

        yinLiuRepayFile = YinLiuRepayFile(data, productId, repayTermNo='4', repayDate=repayDate, loanInvoiceId='000LI0002018084874027128009')
        yinLiuRepayFile.creditClaimFile()

        self.repayPublicBizImpl.job.update_job('引流代偿文件分片任务流', group=13, executeBizDateType='CUSTOMER', executeBizDate=repayDate.replace('-', ''))
        self.repayPublicBizImpl.job.trigger_job('引流代偿文件分片任务流', group=13)
        time.sleep(3)

        # 自动入账
        self.repayPublicBizImpl.job.trigger_job("自动入账处理任务流", group=13)
        # 输入指定借据号
        # self.repayRes = json.loads(HaLo.repay_apply(repay_scene='01', repay_type='1', loanInvoiceId="").get('body'))  # 按期还款

    """ 后置条件处理 """
    def tearDown(self):
        # 接口层校验授信结果是否符合预期
        pass


if __name__ == '__main__':
    unittest.main()
