# -*- coding: utf-8 -*-
# -----------------------------------------------------
# 百度放款数据准备
# -----------------------------------------------------
import datetime
import time
from src.impl.common.CheckBizImpl import CheckBizImpl
from src.impl.baidu.BaiDuBizImpl import BaiDuBizImpl
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from src.impl.baidu.BaiDuCreditFileBizImpl import BaiduFile
from src.enums.EnumBaiDu import *
from utils.JobCenter import *


class BaiDuSynBizImpl(object):
    def __init__(self, data=None, loanamount=100000, month=6, repay_mode='02', loan_date=None):
        self.loanamount = loanamount
        self.month = month
        self.repay_mode = repay_mode
        self.loan_date = loan_date if loan_date else datetime.datetime.today().strftime('%Y-%m-%d')
        self.BaiDuBizImpl = BaiDuBizImpl(data=data)
        self.CheckBizImpl = CheckBizImpl()
        self.MysqlBizImpl = MysqlBizImpl()
        self.job = JOB()
        self.data = data if data else self.BaiDuBizImpl.data

    def loan_flow(self):
        """
        放款流程数据准备
        """
        # 发起授信
        credit_apply_id = self.BaiDuBizImpl.credit(initialAmount=self.loanamount)['credit_apply_id']
        # 数据库层校验授信结果是否符合预期
        time.sleep(5)
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=credit_apply_id)
        # 接口层校验授信结果是否符合预期
        ris_code = self.BaiDuBizImpl.credit_query(credit_apply_id=credit_apply_id)['message']['expanding']['risCode']
        assert EnumBaiDuRisCode.ACCEPT.value == ris_code, '授信失败'
        # 发起支用申请
        loan_apply_id = self.BaiDuBizImpl.loan(cashAmount=self.loanamount, term=self.month)['loan_apply_id']
        time.sleep(5)
        # 数据库层校验支用状态-待放款
        self.CheckBizImpl.check_file_loan_apply_status(loan_apply_serial_id=loan_apply_id)
        # 接口层校验支用结果-待放款
        l_ris_code = self.BaiDuBizImpl.loan_query(loan_apply_id=loan_apply_id)['message']['expanding']['risCode']
        assert EnumBaiDuRisCode.ACCEPT.value == l_ris_code, '支用失败'
        # 生成放款文件并上传金山云
        bd = BaiduFile(data=self.data, cur_date=self.loan_date)
        bd.start()
        # 清除分片流水
        self.MysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
        self.MysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
        self.MysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')
        # 执行任务流下载文件入库
        self.job.update_job('百度放款对账下载任务流-测试', executeBizDate=self.loan_date.replace('-', ''))
        self.job.trigger_job('百度放款对账下载任务流-测试')
        time.sleep(5)
        # 检查是否入三方待建账信息
        self.CheckBizImpl.check_third_wait_loan_status(certificate_no=self.data['cer_no'])
        # 执行任务流放款
        self.job.update_job('线下自动放款', executeBizDate=datetime.datetime.today().strftime('%Y%m%d'))
        self.job.trigger_job('线下自动放款')
        # 数据库层校验支用状态-使用中
        self.CheckBizImpl.check_loan_apply_status(loan_apply_serial_id=loan_apply_id)
        # 查询借据号
        info = self.MysqlBizImpl.get_credit_database_info('credit_loan_invoice', certificate_no=self.data['cer_no'])
        loan_no = info['loan_invoice_id']
        return loan_no

