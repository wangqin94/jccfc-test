import unittest
import warnings

from config.TestEnvInfo import TEST_ENV_INFO
from src.enums.EnumYinLiu import YinLiuApiLoanStatusEnum
import time

from src.enums.EnumsCommon import *
from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.zmyc.ZMYCBizImpl import ZMYCBizImpl
from src.impl.zmyc.ZMYCCheckBizImpl import ZMYCCheckBizImpl
from src.impl.public.LoanPublicBizImpl import LoanPublicBizImpl
from utils.JobCenter import JOB
from utils.Logger import MyLog
from utils.Models import get_base_data


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        # 初始化日志引擎模块
        self.env = TEST_ENV_INFO
        self.data = get_base_data(str(self.env))
        # self.data = {'name': '蔡徐坤', 'cer_no': '513231198111064950', 'telephone': '13998645372', 'bankid': '6217851709103885570', 'bankcode': '0104'}  # hqas -> juzi
        self.log = MyLog.get_log()
        self.job = JOB()
        self.CheckBizImpl = CheckBizImpl()
        self.loanPublicBizImpl = LoanPublicBizImpl()
        self.zmycCheckBizImpl = ZMYCCheckBizImpl(data=self.data)

    """ 测试步骤 """

    def test_apply(self, loan_date='2024-01-04'):
        """ 测试步骤 """

        zmyc = ZMYCBizImpl(data=self.data)
        # 绑卡签约
        # res = juzi.getCardRealNameMessage().get('body')
        # juzi.bindCardRealName(userId=res['userId'], tradeSerialNo=res['tradeSerialNo'])
        # amount = random.randrange(1000, 2000, 100)
        zmyc.sharedWithholdingAgreement()
        amount = 1000

        self.loan_date = loan_date if loan_date else time.strftime('%Y-%m-%d', time.localtime())

        # 发起授信申请
        self.thirdApplyId = zmyc.credit(applyAmount=amount).get('body')['thirdApplyId']

        # 数据库陈校验授信结果是否符合预期
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.thirdApplyId)
        # 接口层校验授信结果是否符合预期
        self.zmycCheckBizImpl.ZMYC_check_credit_apply_status(self.thirdApplyId)

        # 发起LPR查询
        zmyc.queryLprInfo(thirdApplyId=self.thirdApplyId)

        # 发起支用申请  loan_date: 放款时间，默认当前时间 eg:2022-01-01
        zmyc.applyLoan(loan_date=loan_date, loanAmt=amount, thirdApplyId=self.thirdApplyId)

        # 数据库陈校验授信结果是否符合预期
        self.CheckBizImpl.check_loan_apply_status_with_expect(expect_status=EnumLoanStatus.ON_USE.value,
                                                              thirdpart_apply_id=self.thirdApplyId)
        # 接口层校验授信结果是否符合预期
        status = self.ZMYCCheckBizImpl.ZMYC_check_loan_apply_status(self.thirdApplyId)
        self.assertEqual(YinLiuApiLoanStatusEnum.SUCCESS.value, status, '支用失败')

        # 更新放款时间
        self.loanPublicBizImpl.updateLoanInfo(thirdLoanId=self.thirdApplyId, loanDate=self.loan_date)

    """ 后置条件处理 """

    def tearDown(self):
        # 关闭放款mock
        self.loanPublicBizImpl.updateLoanDateMock(flag=False)


if __name__ == '__main__':
    unittest.main()
