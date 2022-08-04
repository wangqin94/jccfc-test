# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：JiKeCheckBizImpl.py
@Author  ：jccfc
@Date    ：2022/07/06 15:55
"""
import time

from src.enums.EnumJiKe import StatusCodeEnum, JiKeApiCreditStatusEnum, JiKeApiLoanStatusEnum, JiKeApiRepayStatusEnum
from src.impl.JiKe.JiKeBizImpl import JiKeBizImpl


class JiKeCheckBizImpl(JiKeBizImpl):
    def __init__(self, data=None, encrypt_flag=True, person=False):
        super().__init__(data=data, encrypt_flag=encrypt_flag, person=person)

    def jike_check_credit_apply_status(self, thirdApplyId):
        """
        @param thirdApplyId:  授信申请单号
        @return:
        """
        self.log.demsg('接口层授信结果校验...')
        flag = 6
        for n in range(flag):
            res = self.queryCreditResult(thirdApplyId=thirdApplyId)
            head = res['head']
            try:
                if head['returnCode'] == StatusCodeEnum.SUCCESS.code and head['returnMessage'] == StatusCodeEnum.SUCCESS.msg:
                    status = res['body']['creditResult']
                    if status == JiKeApiCreditStatusEnum.SUCCESS.value:
                        self.log.demsg('接口层查询：授信成功')
                        return status
                    elif status == JiKeApiCreditStatusEnum.FAIL.value:
                        self.log.error('接口层授信失败,状态：{},失败原因{}'.format(status, res['body']['rejectMsg']))
                        raise AssertionError('支用失败，接口层状态不符合预期')
                    elif status == JiKeApiCreditStatusEnum.TO_DOING.value:
                        self.log.demsg("授信审批状态处理中，请等待....")
                        time.sleep(3)
                        if n == flag-1:
                            self.log.warning("超过当前系统设置等待时间，请手动查看结果....")
                            raise AssertionError('支用失败，接口层状态不符合预期')
                if head['returnCode'] == StatusCodeEnum.NO_HOURLY.code and head['returnMessage'] == StatusCodeEnum.NO_HOURLY.msg:
                    self.log.demsg("请勿频繁请求，请等待....")
                    time.sleep(15)
            except Exception as r:
                raise r

    def jike_check_loan_apply_status(self, thirdApplyId):
        """
        @param thirdApplyId:  授信申请单号
        @return:
        """
        self.log.demsg('接口层支用结果校验...')
        flag = 6
        for n in range(flag):
            res = self.queryLoanResult(thirdApplyId=thirdApplyId)
            head = res['head']
            try:
                if head['returnCode'] == StatusCodeEnum.SUCCESS.code and head['returnMessage'] == StatusCodeEnum.SUCCESS.msg:
                    status = res['body']['loanResult']
                    if status == JiKeApiLoanStatusEnum.SUCCESS.value:
                        self.log.demsg('支用成功')
                        return status
                    elif status == JiKeApiLoanStatusEnum.FAIL.value:
                        self.log.error('支用失败,状态：{},失败原因{}'.format(status, res['body']['loanResultDesc']))
                        raise AssertionError('支用失败，接口层状态不符合预期')
                    elif status == JiKeApiLoanStatusEnum.TO_DOING.value:
                        self.log.demsg("支用审批状态处理中，请等待....")
                        time.sleep(3)
                        if n == flag-1:
                            self.log.warning("超过当前系统设置等待时间，请手动查看结果....")
                            raise AssertionError('支用失败，接口层状态不符合预期')
                if head['returnCode'] == StatusCodeEnum.NO_HOURLY.code and head['returnMessage'] == StatusCodeEnum.NO_HOURLY.msg:
                    self.log.demsg("请勿频繁请求，请等待....")
                    time.sleep(15)
            except Exception as r:
                raise r

    def jike_check_repay_status(self, repayApplySerialNo):
        """
        @param repayApplySerialNo:  三方还款申请单号
        @return:
        """
        self.log.demsg('接口层还款结果校验...')
        flag = 6
        for n in range(flag):
            res = self.repay_query(repayApplySerialNo=repayApplySerialNo)
            returnCode = res['head']['returnCode']
            returnMessage = res['head']['returnMessage']
            try:
                if returnCode == StatusCodeEnum.SUCCESS.code and returnMessage == StatusCodeEnum.SUCCESS.msg:
                    status = res['body']['repayStatus']
                    if status == JiKeApiRepayStatusEnum.REPAY_SUCCESS.value:
                        self.log.demsg('还款成功')
                        return status
                    elif status == JiKeApiRepayStatusEnum.REPAY_FAIL.value:
                        self.log.error('还款失败,状态：{},失败原因{}'.format(status, res['body']['repayStatusDesc']))
                        raise AssertionError('还款失败，接口层状态不符合预期')
                    elif status == JiKeApiRepayStatusEnum.REPAY_REPAYING.value:
                        self.log.demsg("还款审批状态处理中，请等待....")
                        time.sleep(3)
                        if n == flag-1:
                            self.log.error("超过当前系统设置等待时间，请手动查看结果....")
                            raise AssertionError('还款失败，状态处理中，接口层状态不符合预期')
                elif returnCode == StatusCodeEnum.SYS_ERROR.code and returnMessage == StatusCodeEnum.SYS_ERROR.msg:
                    self.log.error('还款失败,状态：{},失败原因{}'.format(returnCode, returnMessage))
                    raise AssertionError('系统服务错误')
                elif returnCode == StatusCodeEnum.SYS_ERROR1.code and returnMessage == StatusCodeEnum.SYS_ERROR1.msg:
                    self.log.error('还款失败,状态：{},失败原因{}'.format(returnCode, returnMessage))
                    raise AssertionError('系统服务错误')
                elif returnCode == StatusCodeEnum.NO_HOURLY.code and returnMessage == StatusCodeEnum.NO_HOURLY.msg:
                    self.log.demsg("请勿频繁请求，请等待....")
                    time.sleep(15)
            except Exception as r:
                raise r


if __name__ == '__main__':
    pass
    # JiKeCheckBizImpl().jike_check_credit_apply_status("creditApplyNo16435111528004788")
