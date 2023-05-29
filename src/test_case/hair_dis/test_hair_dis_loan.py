import random
import unittest
import warnings

from config.TestEnvInfo import TEST_ENV_INFO
from src.enums.EnumYinLiu import YinLiuApiLoanStatusEnum
import time

from src.enums.EnumsCommon import *
from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.hair.HairBizImpl import HairBizImpl
from src.impl.hair.HairCheckBizImpl import HairCheckBizImpl
from src.impl.public.LoanPublicBizImpl import LoanPublicBizImpl
from utils.JobCenter import JOB
from utils.Logger import MyLog
from utils.Models import get_base_data


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 初始化日志引擎模块
        self.env = TEST_ENV_INFO
        self.data = get_base_data(str(self.env))
        # self.data = {'name': '鞠惜文', 'cer_no': '140430199903033121', 'telephone': '17725049631', 'bankid': '6212261681437589712'}
        self.log = MyLog.get_log()
        self.job = JOB()
        self.productId = ProductIdEnum.HAIR_DISCOUNT.value
        self.CheckBizImpl = CheckBizImpl()
        self.HairCheckBizImpl = HairCheckBizImpl(productId=self.productId, data=self.data)

    """ 测试步骤 """

    def test_apply(self, loan_date='2023-05-18'):
        """ 测试步骤 """
        # 绑卡签约
        Hair = HairBizImpl(self.productId, data=self.data)
        Hair.sharedWithholdingAgreement()

        term = 6
        amount = random.randrange(1000, 10000, 100)
        # amount = 5000

        self.loan_date = loan_date if loan_date else time.strftime('%Y-%m-%d', time.localtime())

        # 发起授信申请
        self.thirdApplyId = Hair.credit(applyAmount=amount, loanTerm=term).get('body')['thirdApplyId']

        # 数据库陈校验授信结果是否符合预期
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.thirdApplyId)
        # 接口层校验授信结果是否符合预期
        self.HairCheckBizImpl.hair_check_credit_apply_status(self.thirdApplyId)

        # 发起LPR查询
        Hair.queryLprInfo(thirdApplyId=self.thirdApplyId)

        # 发起支用申请  loan_date: 放款时间，默认当前时间 eg:2022-01-01
        Hair.applyLoan(loan_date=loan_date, loanAmt=amount, loanTerm=term, thirdApplyId=self.thirdApplyId)

    """ 后置条件处理 """

    def tearDown(self):
        time.sleep(5)
        # 数据库陈校验授信结果是否符合预期
        status = self.CheckBizImpl.check_loan_apply_status_with_expect(expect_status=EnumLoanStatus.TO_LOAN.value,
                                                                       thirdpart_apply_id=self.thirdApplyId)
        self.assertEqual(EnumLoanStatus.TO_LOAN.value, status, '支用失败')
        # 执行任务流放款
        self.job.update_job('线下自动放款', executeBizDateType='TODAY')
        self.job.trigger_job('线下自动放款')
        self.CheckBizImpl.check_loan_apply_status_with_expect(expect_status=EnumLoanStatus.ON_USE.value,
                                                              thirdpart_apply_id=self.thirdApplyId)
        # 接口层校验授信结果是否符合预期
        status = self.HairCheckBizImpl.hair_check_loan_apply_status(self.thirdApplyId)
        self.assertEqual(YinLiuApiLoanStatusEnum.SUCCESS.value, status, '支用失败')

        # 更新放款时间
        loanPublicBizImpl = LoanPublicBizImpl()
        loanPublicBizImpl.updateLoanInfo(thirdLoanId=self.thirdApplyId, loanDate=self.loan_date)


if __name__ == '__main__':
    unittest.main()
