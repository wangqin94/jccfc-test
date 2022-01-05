import unittest
from src.impl.common.CheckBizImpl import *
import time
from src.impl.zhixin.ZhiXinBizImpl import ZhiXinBizImpl
from src.test_case.zhixin.person import data


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    """ 预置条件处理 """

    def setUp(self):
        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 当前时间
        self.log = MyLog().get_log()
        self.MysqlBizImpl = MysqlBizImpl()
        self.CheckBizImpl = CheckBizImpl()

    """ 测试步骤 """

    def test_apply(self):
        """ 测试步骤 """
        # 绑卡签约-绑卡确认-授信
        zhixin = ZhiXinBizImpl(data=data)
        # 默认取person文件中的userid
        loan_apply_info = self.MysqlBizImpl.get_loan_apply_info(thirdpart_user_id=data['userId'])
        # loan_no 锦城支用申请单号，必填  可根据person文件userid关联查询，也可手动输入支用刚申请单号
        # res = zhixin.repayTrial(loan_no="000LA2021111900000005")
        # repay_type还款类型： 1 按期还款； 2 提前结清； 3 按金额还款
        # repayAmt还款金额： repay_type=3时，还款金额必填
        # zhixin.repayTrial(repay_type='1', loan_no=loan_apply_info['loan_apply_id'], repayTime=20220130111111)  # 按期还款
        # zhixin.repayTrial(loan_no=loan_apply_info['loan_apply_id'], repay_type='2', repayTime=20211125111111)  # 提前结清
        zhixin.repayTrial(loan_no=loan_apply_info['loan_apply_id'], repayType='3', repayAmt='1074.26', repayTime='20220130111111')  # 按金额还款

    """ 后置条件处理 """

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
