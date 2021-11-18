import unittest

from src.impl.common.CommonCheckBizImpl import *
import time
from src.impl.zhixin.ZhiXinBizImpl import ZhiXinBizImpl
from src.impl.zhixin.ZhiXinCheckBizImpl import ZhiXinCheckBizImpl


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
        self.data = get_base_data_temp('userId')
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
        self.loanRes = json.loads(zhixin.applyLoan(loanAmt='1000', term='6').get('output'))
        self.loanApplyNo = self.loanRes['loanApplyNo']

    """ 后置条件处理 """

    def tearDown(self):
        time.sleep(5)
        # 数据库陈校验授信结果是否符合预期
        self.CheckBizImpl.check_loan_apply_status(thirdpart_order_id=self.loanApplyNo)
        # 接口层校验授信结果是否符合预期
        self.ZhiXinCheckBizImpl.check_loan_apply_status(self.data, self.loanRes['userId'], self.loanRes['loanApplyNo'])


if __name__ == '__main__':
    unittest.main()
