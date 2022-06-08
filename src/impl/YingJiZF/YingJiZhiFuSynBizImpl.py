# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：YingJiZhiFuSynBizImpl.py
@Author  ：jccfc
@Date    ：2022/1/29 16:42 
"""
import sys
import time

from src.enums.EnumYingJiZF import ApiPaymentResultStatusCodeEnum
from src.enums.EnumsCommon import EnumH5PaymentStatus
from src.impl.YingJiZF.YingJiZFBizImpl import YingJiZFBizImpl


class YingJiZhiFuSynBizImpl(YingJiZFBizImpl):
    def __init__(self, data):
        super().__init__(data=data)

    def check_payment_result_status_with_success(self, m=10, t=3, **kwargs):
        """
        @param kwargs: 查询条件
        @param t: 每次时间间隔, 默认5S
        @param m: 查证次数 默认10次
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('接口层锦程H5还款结果校验...')
        for j in range(m):
            repayRes = self.payment_result(**kwargs)
            assert EnumH5PaymentStatus.SUCCESS.value == repayRes['head']['returnCode'], '还款API接口请求失败，失败原因{}'.format(
                repayRes['head']['returnMessage'])
            status = repayRes['body']['tradeStatusCode']
            if status == ApiPaymentResultStatusCodeEnum.SUCCESS.code:
                self.log.demsg('还款状态校验成功，符合预期值[tradeStatusCode={}]'.format(status))
                break
            elif status == ApiPaymentResultStatusCodeEnum.FAIL.code:
                self.log.demsg("还款状态不符合预期，期望值[{}]！= 实际值[{}]".format(ApiPaymentResultStatusCodeEnum.FAIL.code, status))
                break
            elif status == ApiPaymentResultStatusCodeEnum.TO_DOING.code:
                self.log.demsg("还款状态处理中，状态[{}]！当前第[{}]次查证....".format(status, j + 1))
                time.sleep(t)
                if j == m - 1:
                    self.log.error("超过当前系统设置等待时间，支用单状态不符合预期，还款一直处于处理中...")
                    sys.exit(7)


if __name__ == "__main__":
    data1 = {'name': '笪茂', 'cer_no': '370521199312039021', 'bankid': '6217854903427062621', 'telephone': '17724956083', 'userId': 'userId1643444743627'}
    mm = YingJiZhiFuSynBizImpl(data1)
    mm.check_payment_result_status_with_success(appOrderNo="appOrderNo164344480278485543")