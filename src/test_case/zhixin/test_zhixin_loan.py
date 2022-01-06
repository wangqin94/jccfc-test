import json
import unittest

from config.TestEnvInfo import TEST_ENV_INFO
from src.enums.EnumZhiXin import ZhiXinApiStatusEnum
import time

from src.enums.EnumsCommon import *
from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.zhixin.ZhiXinBizImpl import ZhiXinBizImpl
from src.impl.zhixin.ZhiXinCheckBizImpl import ZhiXinCheckBizImpl
from src.test_case.zhixin.person import data
from utils.Logger import MyLog
from utils.Models import get_base_data


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """

    def setUp(self):
        # 初始化日志引擎模块
        self.log = MyLog.get_log()
        self.CheckBizImpl = CheckBizImpl()
        self.ZhiXinCheckBizImpl = ZhiXinCheckBizImpl()

    """ 测试步骤 """

    def test_apply(self):
        """ 测试步骤 """
        # 绑卡签约-绑卡确认-授信
        # self.data = get_base_data_temp('userId')
        self.env = TEST_ENV_INFO
        self.data = get_base_data(str(self.env) + ' -> ' + str(ProductEnum.ZHIXIN.value), 'userId')
        zhixin = ZhiXinBizImpl(data=self.data)
        res = json.loads(zhixin.applyCertification().get('output'))
        zhixin.verifyCode(userId=res['userId'], certificationApplyNo=res['certificationApplyNo'],
                          cdKey=res['cdKey'])
        # 发起授信申请
        creditRes = json.loads(zhixin.credit().get('output'))
        self.creditApplyNo = creditRes['creditApplyNo']

        # 数据库陈校验授信结果是否符合预期
        time.sleep(5)
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.creditApplyNo)
        # 接口层校验授信结果是否符合预期
        self.ZhiXinCheckBizImpl.check_credit_apply_status(self.data, creditRes['userId'], creditRes['creditApplyNo'])

        # 发起支用申请
        self.loanRes = json.loads(zhixin.applyLoan(loanAmt='1000', term='3').get('output'))
        self.loanApplyNo = self.loanRes['loanApplyNo']

    """ 后置条件处理 """

    def tearDown(self):
        time.sleep(5)
        # 数据库陈校验授信结果是否符合预期
        status = self.CheckBizImpl.check_loan_apply_status(thirdpart_apply_id=self.loanApplyNo)
        self.assertEqual(EnumLoanStatus.ON_USE.value, status, '支用失败')
        # 接口层校验授信结果是否符合预期
        status = self.ZhiXinCheckBizImpl.check_loan_apply_status(self.data, self.loanRes['userId'], self.loanRes['loanApplyNo'])
        self.assertEqual(ZhiXinApiStatusEnum.SUCCESS.value, status, '支用失败')


if __name__ == '__main__':
    unittest.main()
