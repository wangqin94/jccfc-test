import unittest
from src.impl.common.CommonCheckBizImpl import *
import time
from src.impl.zhixin.ZhiXinBizImpl import ZhiXinBizImpl


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """

    def setUp(self):
        self.CheckBizImpl = CheckBizImpl()

    """ 测试步骤 """

    def test_apply(self):
        """ 测试步骤 """
        # 绑卡签约-绑卡确认-授信
        zhixin = ZhiXinBizImpl(data=None)
        res = json.loads(zhixin.applyCertification().get('output'))
        zhixin.verifyCode(userId=res['userId'], certificationApplyNo=res['certificationApplyNo'],
                          cdKey=res['cdKey'])
        # 发起授信申请
        self.creditApplyNo = json.loads(zhixin.credit(job='1').get('output'))['creditApplyNo']

    """ 后置条件处理 """

    def tearDown(self):
        # 检查授信状态
        time.sleep(10)
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.creditApplyNo)


if __name__ == '__main__':
    unittest.main()
