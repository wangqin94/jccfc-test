# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：ZhiXinBizImpl.py
@Author  ：jccfc
@Date    ：2022/1/13 9:51 
"""
from src.impl.MeiTuan.MeiTuanBizImpl import MeiTuanBizImpl
from src.impl.MeiTuan.MeiTuanCheckBizImpl import MeiTuanCheckBizImpl
from src.impl.MeiTuan.MeiTuan_CreateFileBizImpl import MeiTuanLoanFile
from utils.Apollo import *
from src.impl.common.CheckBizImpl import CheckBizImpl
from utils.GlobalVar import GlobalMap
from utils.JobCenter import JOB
from utils.Models import *


class MeiTuanSynBizImpl(MeiTuanBizImpl):
    def __init__(self, data=None, encrypt_flag=True, person=False):
        super().__init__(data=data, encrypt_flag=encrypt_flag, person=person)
        self.job = JOB()
        self.apollo = Apollo()
        self.globalMap = GlobalMap()
        self.CheckBizImpl = CheckBizImpl()
        self.meiTuanCheckBizImpl = MeiTuanCheckBizImpl(self.data)

    # 准备借款数据
    def pre_meituan_Loan(self, loan_date=None, **kwargs):
        """
        多层接口业务组装关键字：放款
        @param loan_date: 放款时间 格式："2021-12-12"
        @param kwargs: 放款字段，键值对
        @return:
        """
        APP_NO = self.credit(APPLY_AMT=1000000)['app_no']
        # 数据库层校验授信结果是否符合预期
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=APP_NO)
        # 接口层校验授信结果是否符合预期
        self.meiTuanCheckBizImpl.check_credit_apply_status(APP_NO)

        # 设置apollo放款mock时间 默认当前时间
        loan_date = loan_date if loan_date else time.strftime('%Y-%m-%d', time.localtime())
        apollo_data = dict()
        apollo_data['credit.loan.trade.date.mock'] = "true"
        apollo_data['credit.loan.date.mock'] = loan_date
        self.apollo.update_config(appId='loan2.1-public', namespace='JCXF.system', **apollo_data)

        # 发起支用申请
        res = self.loan(**kwargs)
        loanNo = res["body"]["APP_NO"]

        # 支用三方申请号loanNo写入全局变量
        self.globalMap.set_map('meituan_loanNo', loanNo)

        # 数据库层校验支用结果是否符合预期
        self.CheckBizImpl.check_file_loan_apply_status(thirdpart_apply_id=loanNo)
        # 接口层校验支用结果是否符合预期
        self.meiTuanCheckBizImpl.check_loan_apply_status(loanNo)

        # 构造放款对账文件
        MeiTuanLoanFile(self.data, apply_date=loan_date)

        # 清除分片流水
        self.MysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
        self.MysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
        self.MysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')

        # 执行任务流下载放款对账文件入库
        self.job.update_job('美团放款对账文件处理任务流', executeBizDateType='CUSTOMER', executeBizDate=loan_date.replace('-', ''))
        self.job.trigger_job('美团放款对账文件处理任务流')
        self.CheckBizImpl.check_third_wait_loan_status(thirdpart_apply_id=loanNo)

        # 执行任务流放款
        self.job.update_job('线下自动放款', executeBizDateType='CUSTOMER', executeBizDate=loan_date.replace('-', ''))
        self.job.trigger_job('线下自动放款')

        # 数据库层校验支用状态-使用中
        self.CheckBizImpl.check_loan_apply_status(thirdpart_apply_id=loanNo)

        # 更新资产asset_loan_invoice_info放款时间,apply_loan_date=loan_date:
        loan_apply_info = self.MysqlBizImpl.get_loan_apply_info(thirdpart_apply_id=loanNo)
        credit_loan_invoice = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice',
                                                                         loan_apply_id=loan_apply_info['loan_apply_id'])
        # 借据号invoiceNo写入全局变量
        self.globalMap.set_map('meituan_loan_invoice_id', credit_loan_invoice['loan_invoice_id'])

        loan_date_temp = str(loan_date).replace("-", '')
        self.MysqlBizImpl.update_asset_database_info('asset_loan_invoice_info', attr="loan_invoice_id='{}'".format(
            credit_loan_invoice['loan_invoice_id']), apply_loan_date=loan_date_temp)

        data = dict()
        data['loan_date'] = loan_date
        data['loan_invoice_id'] = credit_loan_invoice['loan_invoice_id']
        print(self.globalMap.map)

        return data


if __name__ == "__main__":
    MeiTuanBizImpl = MeiTuanSynBizImpl()
    MeiTuanBizImpl.pre_meituan_Loan()
