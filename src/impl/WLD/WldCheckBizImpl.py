# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test
@File    ：ZhiXinCheckBizImpl.py
@Author  ：jccfc
@Date    ：2021/11/17 15:55
"""
import json
import time

from src.enums.EnumWld import StatusCodeEnum, WldApiStatusEnum
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from src.impl.WLD.WldBizImpl import WldBizImpl


class WldCheckBizImpl(WldBizImpl):
    def __init__(self, data=None, encrypt_flag=True, person=False):
        super().__init__(data=data, encrypt_flag=encrypt_flag, person=person)
        self.MysqlBizImpl = MysqlBizImpl()

    def check_credit_apply_status(self, thirdapplyid):
        """
        @param userid: 三方用户ID
        @param credit_apply_no:  授信申请单号
        @return:
        """
        self.log.demsg('接口层授信结果校验...')
        flag = 6
        for n in range(flag):
            res = self.credit_query(thirdApplyId=thirdapplyid)
            try:
                if res['head']['returnCode'] == StatusCodeEnum.SUCCESS.code \
                        and res['head']['returnMessage'] == StatusCodeEnum.SUCCESS.msg:
                    status = res['body']['creditResult']
                    if status == WldApiStatusEnum.QUERY_CREDIT_RESULT_S.value:
                        self.log.demsg('接口层查询：授信成功')
                        return status
                    elif status == WldApiStatusEnum.QUERY_CREDIT_RESULT_F.value:
                        self.log.error('接口层授信失败,状态：{},失败原因{}'.format(status, res['resultMsg']))
                        return status
                    elif status == StatusCodeEnum.TO_DOING.value:
                        self.log.demsg("授信审批状态处理中，请等待....")
                        time.sleep(3)
                        if n == flag - 1:
                            self.log.warning("超过当前系统设置等待时间，请手动查看结果....")
                            return status
                if res['code'] == StatusCodeEnum.NO_HOURLY.code and res['msg'] == StatusCodeEnum.NO_HOURLY.msg:
                    self.log.demsg("请勿频繁请求，请等待....")
                    time.sleep(15)
            except Exception as r:
                self.log.error("系统错误{}".format(r))

    def check_loan_apply_status(self, loanapplyno):
        """
        @param userid: 三方用户ID
        @param loan_apply_no:  授信申请单号
        @return:
        """
        self.log.demsg('接口层支用结果校验...')
        flag = 6
        for n in range(flag):
            res = self.loan_query(thirdApplyId=loanapplyno)
            try:
                if res['head']['returnCode'] == StatusCodeEnum.SUCCESS.code \
                        and res['head']['returnMessage'] == StatusCodeEnum.SUCCESS.msg:
                    status = res['body']['loanResult']
                    if status == WldApiStatusEnum.QUERY_LOAN_RESULT_S.value:
                        self.log.demsg('支用成功')
                        return status
                    elif status == WldApiStatusEnum.QUERY_LOAN_RESULT_F.value:
                        self.log.error('支用失败,状态：{},失败原因{}'.format(status, res['resultMsg']))
                        return status
                    elif status == WldApiStatusEnum.QUERY_LOAN_RESULT_D.value:
                        self.log.demsg("支用审批状态处理中，请等待....")
                        time.sleep(3)
                        if n == flag - 1:
                            self.log.warning("超过当前系统设置等待时间，请手动查看结果....")
                            return status
                if res['code'] == StatusCodeEnum.NO_HOURLY.code and res['msg'] == StatusCodeEnum.NO_HOURLY.msg:
                    self.log.demsg("请勿频繁请求，请等待....")
                    time.sleep(15)
            except Exception as r:
                self.log.error("系统错误{}".format(r))

    def check_repay_status(self, repayapplyserialno):
        """
        @param userid: 三方用户ID
        @param repay_apply_no:  三方还款申请单号
        @return:
        """
        self.log.demsg('接口层还款结果校验...')
        flag = 6
        for n in range(flag):
            res = self.loan_query(repayApplySerialNo=repayapplyserialno)
            try:
                if res['head']['returnCode'] == StatusCodeEnum.SUCCESS.code and res['head']['returnMessage'] == \
                        StatusCodeEnum.SUCCESS.msg:
                    status = res['body']['repayApplyList'][0]['repayStatus']
                    if status == WldApiStatusEnum.QUERY_REPAY_RESULT_S.value:
                        self.log.demsg('还款成功')
                        return status
                    elif status == WldApiStatusEnum.QUERY_REPAY_RESULT_F.value:
                        self.log.error('还款失败,状态：{},失败原因{}'.format(status, res['body']['repayApplyList'][0]['repayStatusDesc']))
                        return status
                    elif status == WldApiStatusEnum.QUERY_REPAY_RESULT_D.value:
                        self.log.demsg("还款审批状态处理中，请等待....")
                        time.sleep(3)
                        if n == flag - 1:
                            self.log.error("超过当前系统设置等待时间，请手动查看结果....")
                            return status
                if res['code'] == StatusCodeEnum.NO_HOURLY.code and res['msg'] == StatusCodeEnum.NO_HOURLY.msg:
                    self.log.demsg("请勿频繁请求，请等待....")
                    time.sleep(15)
            except Exception as r:
                self.log.error("系统错误{}".format(r))

    # def check_bind_status(self, *args, record=0, **kwargs):
    #
    #     self.log.demsg('数据库层绑卡结果校验...')
    #     table = 'credit_bind_card_info'
    #     keys = self.mysql_credit.select_table_column(*args, table_name=table, database=self.credit_database_name)
    #     sql = get_sql_qurey_str(table, *args, db=self.credit_database_name, **kwargs)
    #     values = self.mysql_credit.select(sql)
