# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：ZhiXinCheckBizImpl.py
@Author  ：jccfc
@Date    ：2021/11/17 15:55
"""
from src.enums.EnumZhiXin import *
from src.impl.common.CommonUtils import *
from src.impl.zhixin.ZhiXinBizImpl import ZhiXinBizImpl


class ZhiXinCheckBizImpl(INIT):
    def __init__(self):
        super().__init__()
        self.getSqlData = GetSqlData()

    def check_credit_apply_status(self, data, userid, credit_apply_no):
        """
        @param data: 四要素
        @param userid: 三方用户ID
        @param credit_apply_no:  授信申请单号
        @return:
        """
        self.log.demsg('授信结果校验...')
        flag = 10
        for n in range(flag):
            zhixin = ZhiXinBizImpl(data=data)
            res = json.loads(zhixin.queryCreditResult(userId=userid, creditApplyNo=credit_apply_no).get('output'))
            status = res['status']
            if status == ZhiXinApiStatusEnum.SUCCESS.value:
                self.log.demsg('授信成功')
                break
            elif status == ZhiXinApiStatusEnum.FAIL.value:
                self.log.error('授信失败,状态：{},失败原因{}'.format(status, res['resultMsg']))
                break
            elif status == ZhiXinApiStatusEnum.TO_DOING.value:
                self.log.demsg("授信审批状态处理中，请等待....")
                time.sleep(5)
                if n == flag-1:
                    self.log.warning("超过当前系统设置等待时间，请手动查看结果....")

    def check_loan_apply_status(self, data, userid, loan_apply_no):
        """
        @param data: 四要素
        @param userid: 三方用户ID
        @param loan_apply_no:  授信申请单号
        @return:
        """
        self.log.demsg('支用结果校验...')
        flag = 10
        for n in range(flag):
            zhixin = ZhiXinBizImpl(data=data)
            res = json.loads(zhixin.queryLoanResult(userId=userid, loanApplyNo=loan_apply_no).get('output'))
            status = res['status']
            if status == ZhiXinApiStatusEnum.SUCCESS.value:
                self.log.demsg('支用成功')
                break
            elif status == ZhiXinApiStatusEnum.FAIL.value:
                self.log.error('支用失败,状态：{},失败原因{}'.format(status, res['resultMsg']))
                break
            elif status == ZhiXinApiStatusEnum.TO_DOING.value:
                self.log.demsg("支用审批状态处理中，请等待....")
                time.sleep(5)
                if n == flag-1:
                    self.log.warning("超过当前系统设置等待时间，请手动查看结果....")
