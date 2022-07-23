import unittest
from src.impl.ctrip.CtripBizImpl import CtripBizImpl
from person import *


class MyTestCase(unittest.TestCase):
    """ 后置条件处理 """
    def tearDown(self):
        self.assertIn("result_msg", self.jsonData)
        if "result_msg" in self.jsonData:
            returnMessage = self.jsonData["result_msg"]
            self.assertEqual(returnMessage, '成功', "接口响应失败")

    """ 测试步骤 """
    def test_one(self):
        # repay_mode=还款类型: 必填参数 :1按期还款；2提前结清；3逾期还款；4提前当期还款
        # finish_time=实际还款时间： 提前结清必填参数"2021-08-06"
        ctrip = CtripBizImpl(data=data)
        self.jsonData = ctrip.repay_notice(repay_mode="1", repay_term_no="1", repay_date='2022-08-19', loan_invoice_id=None)


if __name__ == '__main__':
    unittest.main()
