import unittest
import warnings

import time

from src.enums.EnumsCommon import ProductIdEnum
from src.impl.public.YinLiuCreateFileBizImpl import YinLiuRepayFile
from src.impl.public.RepayPublicBizImpl import RepayPublicBizImpl
from src.test_case.juzi.person import data
from src.impl.juzi.JuZiBizImpl import JuZiBizImpl


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.repayPublicBizImpl = RepayPublicBizImpl()
        self.JuZiBizImpl = JuZiBizImpl(data=data)

    """ 测试步骤 """
    def test_repay_apply(self, productId=ProductIdEnum.JUZI.value, repayDate='2024-02-10'):
        """ 测试步骤 """
        repayDate = repayDate if repayDate else time.strftime('%Y-%m-%d', time.localtime())

        # 还款环境配置,清理缓存配置账务时间
        self.repayPublicBizImpl.pre_repay_config(repayDate=repayDate)

        yinLiuRepayFile = YinLiuRepayFile(data, productId, repayTermNo='1', repayDate=repayDate)
        yinLiuRepayFile.creditClaimFile()

        self.repayPublicBizImpl.job.update_job('【引流】代偿文件分片任务流', group=13, executeBizDateType='CUSTOMER', executeBizDate=repayDate.replace('-', ''))
        self.repayPublicBizImpl.job.trigger_job('【引流】代偿文件分片任务流', group=13)
        time.sleep(10)

        # # 代偿确认
        # self.JuZiBizImpl.compensationConfirm(loanInvoiceId="")

        # 自动入账
        self.repayPublicBizImpl.job.trigger_job_byId("751800549099302912")
        # 输入指定借据号
        # self.repayRes = json.loads(HaLo.repay_apply(repay_scene='01', repay_type='1', loanInvoiceId="").get('body'))  # 按期还款

    """ 后置条件处理 """
    def tearDown(self):
        # 接口层校验授信结果是否符合预期
        pass


if __name__ == '__main__':
    unittest.main()
