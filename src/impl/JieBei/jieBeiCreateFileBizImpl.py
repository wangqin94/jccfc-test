
import os
import time, datetime

from config.TestEnvInfo import TEST_ENV_INFO
from engine.EnvInit import EnvInit
from src.enums.EnumsCommon import ProductEnum
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils.Logger import Logs

_log = Logs()
_ProjectPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # 项目根目录
_FilePath = os.path.join(_ProjectPath, 'FilePath', ProductEnum.JIEBEI.value, TEST_ENV_INFO)  # 文件存放目录


class creditFile(EnvInit):
    def __init__(self,data):
        super(creditFile, self).__init__()

        self.MysqlBizImpl = MysqlBizImpl()
        self.name = data['name']
        self.certNo = data['cer_no']
        self.telephone = data['telephone']
        self.creditNo = data['applyno']
        self.businessDate = time.strftime('%Y%m%d', time.localtime())
        self.applyDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.expireDate = (datetime.datetime.now() + datetime.timedelta(days=31)).strftime('%Y-%m-%d 00:00:00')


    # 银河授信文件
    def start_creditFile(self):

        sql = "INSERT INTO channel_jiebei_credit_apply(apply_no,credit_no,apply_type, source, product_code, biz_mode, loan_mode, name,cert_no, cert_type, mobile_no, apply_date, expiry_date, " \
               " state, result, biz_data,gmt_create, gmt_modified, business_date, deal_status, fail_reason,status,created,create_time,modified,update_time) " \
               "VALUES ('" +self.creditNo + "','" + self.creditNo + "','ADMIT_APPLY','PLATFORM','JB','JB_ADVANCED_BK_DI','DIRECT','"+ self.name+"','"+self.certNo+"','01','"+self.telephone+"','" \
               +self.applyDate+"','"+self.expireDate+"','PASS','{\"approvalResult\":\"Y\",\"approvalResultCode\":\"\",\"approvalResultMsg\":\"\",\"creditAmt\":1200000,\"extInfo\":\"{}\"}'," \
               "'{\"SUGGEST_INFO\":{\"result\":{\"CreditAmt\":12000,\"Adm\":1},\"bizDataInfo\":{\"applyType\":\"ADMIT_APPLY\",\"bankInfo\":\"\",\"suggestAmtExpireTime\":\"\",\"certType\":\"01\",\"suggestTmpAmtMax\":\"\",\"tmpAmtEffectiveTime\":\"\",\"extInfo\":\"{}\",\"certNo\":\"421002199803103832\",\"productCode\":\"JB\",\"suggestTmpAmtMin\":\"\",\"applyNo\":\"2023032419167965659952604486S\",\"suggestAmtMax\":\"1200000\",\"suggestRateMax\":\"\",\"loanMode\":\"DIRECT\",\"suggestAmtMin\":\"1200000\",\"suggestRateMin\":\"\",\"tmpAmtExpireTime\":\"\",\"creditNo\":\"2023032419167965634194604986S\",\"bizMode\":\"JB_ADVANCED_BK_DI\",\"suggestAmtEffectiveTime\":\"\"}}}','" \
               +self.applyDate + "','" + self.expireDate + "','" + self.businessDate + "','00','','0','system','"+self.applyDate+"','system','" +self.applyDate+"');"

        self.log.demsg("sql：{}".format(sql))
        self.MysqlBizImpl.mysql_op_channel.update(sql)

class loanApplyFile(EnvInit):
    def __init__(self,data):
        super(loanApplyFile, self).__init__()
        self.MysqlBizImpl = MysqlBizImpl()

        self.name = data['name']
        self.certNo = data['cer_no']
        self.telephone = data['telephone']
        self.creditNo = data['applyno']
        self.apply_no = "loanNo" + str(int(round(time.time() * 1000)))
        self.businessDate = time.strftime('%Y%m%d', time.localtime())
        self.applyDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def start_loanApplyFile(self):

        sql = "INSERT INTO channel_jiebei_loan_apply (apply_no,credit_no,source,product_code,biz_mode,name,cert_no,cert_type,apply_date,state,`result`,biz_data,gmt_create,gmt_modified,business_date,deal_status,fail_msg,status,created,create_time,modified,update_time) VALUES " \
              "('" + self.apply_no + "','" + self.creditNo + "','USER','JB','JB_ADVANCED_BK_DI','" + self.name + "','" + self.certNo + "','01','" + self.applyDate + "','PASS','{\"PolicyCode\": \"JCJB_LOAN\", \"CashSuccessFlag\": \"0\", \"JC_inner_failCode\": \"900002\", \"JC_inner_failReason\": \"合作方风控拒绝\"}'," \
              "'{\"certNo\": \"330822199306066918\", \"applyNo\": \"loanNo202211070000000000000002\", \"bizMode\": \"JB_ADVANCED_BK_DI\", \"dayRate\": \"0.00060\", \"endDate\": \"20221207\", \"extInfo\": \"{}\", \"loanUse\": \"1\", \"useArea\": \"1\", \"certType\": \"01\", \"creditNo\": \"applyno16678094629536618\", \"currency\": \"CNY\", \"graceDay\": \"0\", \"loanMode\": \"DIRECT\", \"rateType\": \"F\", \"termType\": \"M\", \"userName\": \"郑半安\", \"applyDate\": \"2022-11-07 11:34:00\", \"encashAmt\": \"6000000\", \"repayMode\": \"1\", \"startDate\": \"20221107\", \"extensions\": \"{}\", \"totalTerms\": \"1\", \"productCode\": \"JB\", \"encashAcctNo\": \"6221198412343214\", \"guaranteeType\": \"A\", \"encashAcctType\": \"01\", \"intRepayFrequency\": \"D\", \"prinRepayFrequency\": \"03\"}','" \
              + self.applyDate + "','" + self.applyDate + "','" + self.businessDate + "','00','','0','system','" + self.applyDate + "','system','" + self.applyDate+"');"

        self.log.demsg("sql：{}".format(sql))
        self.MysqlBizImpl.mysql_op_channel.update(sql)

class loandetailFile(EnvInit):
    def __init__(self, data):
        super(loandetailFile, self).__init__()
        self.MysqlBizImpl = MysqlBizImpl()

        self.name = data['name']
        self.certNo = data['cer_no']
        self.telephone = data['telephone']
        self.creditNo = data['applyno']
        self.contract_no = data['applyno'].replace('applyno','contract_no')
        self.apply_no = "loanNo" + str(int(round(time.time() * 100000000000)))
        self.businessDate = time.strftime('%Y%m%d', time.localtime())
        self.endDate = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y%m%d')
        self.repayDate = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        self.applyDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.seqNo = "seqNo" + str(int(round(time.time() * 100000000000)))

    def start_loandetailFile(self):

        sql1 = "INSERT INTO `channel_jiebei_loan_detail` (contract_no,fund_seq_no,prod_code,name,cert_type,cert_no,loan_status,loan_use,use_area,apply_date,encash_date,currency,encash_amt,start_date,end_date,total_terms,repay_mode,grace_day,rate_type,day_rate,prin_repay_frequency,int_repay_frequency,guarantee_type,credit_no,encash_acct_type,encash_acct_no,repay_acct_type,repay_acct_no,apply_no,region_code,bsn_type,business_date,deal_status,fail_msg,status,created,create_time,modified,update_time) VALUES " \
               "('" + self.contract_no + "','fundSeqNo15843498411111090108','J1010100100000000004_2','" + self.name + "','01','" + self.certNo + "','1','3','1','" + self.applyDate + "','" + self.applyDate + "','CNY','300000','" + self.businessDate + "','" + self.endDate + "',1,'2',15,'F',0.000600,'03','03','D','" + self.creditNo + "','02','18627583490','01','8438516620194837','" + self.apply_no + "','630000','0201','" + self.businessDate + "','00','','0','system','" + self.applyDate + "','system','" + self.applyDate+"');"

        self.log.demsg("sql1：{}".format(sql1))
        self.MysqlBizImpl.mysql_op_channel.update(sql1)

        sql2 = "INSERT INTO `channel_jiebei_repay_plan` (contract_no,term_no,start_date,end_date,prin_amt,int_amt,region_code,bsn_type,business_date,status,created,create_time,modified,update_time) VALUES " \
               "('" + self.contract_no + "','1','" + self.businessDate + "','" + self.endDate + "','300000',100.00,'330000','0201','" + self.businessDate + "','0','system','" + self.applyDate + "','system','" + self.applyDate+"');"

        self.log.demsg("sql2：{}".format(sql2))
        self.MysqlBizImpl.mysql_op_channel.update(sql2)


    def start_repayDetailFile(self):

        sql3 = "INSERT INTO channel_jiebei_repay_loan_detail (contract_no,seq_no,fee_no,withdraw_no,repay_type,repay_date,curr_prin_bal,curr_ovd_prin_bal,curr_int_bal,curr_ovd_int_bal,curr_ovd_prin_pnlt_bal,curr_ovd_int_pnlt_bal,repay_amt,paid_prin_amt,paid_ovd_prin_amt,paid_int_amt,paid_ovd_int_amt,paid_ovd_prin_pnlt_amt,paid_ovd_int_pnlt_amt,fee_amt,accrued_status,write_off,region_code,bsn_type,pre_repay_fee_amt,business_date,status,created,create_time,modified,update_time) VALUES " \
               "('" + self.contract_no + "','" + self.seqNo + "','2021010428013000660001100084158319','2021010410112000010000010403000078368270','01','" + self.repayDate + "','300000','0','300','0','0','0','300300','300000','0','300','0','0','0','300','0','N','500000','0302',0.00,'" + self.endDate + "','0','system','" + self.applyDate + "','system','" + self.applyDate+"');"

        self.log.demsg("sql3：{}".format(sql3))
        self.MysqlBizImpl.mysql_op_channel.update(sql3)

        sql4 = "INSERT INTO `channel_jiebei_repay_instmnt_detail` (contract_no,seq_no,term_no,repay_amt_type,repay_date,curr_prin_bal,curr_int_bal,curr_ovd_prin_pnlt_bal,curr_ovd_int_pnlt_bal,repay_amt,paid_prin_amt,paid_int_amt,paid_ovd_prin_pnlt_amt,paid_ovd_int_pnlt_amt,accrued_status,write_off,region_code,bsn_type,business_date,status,created,create_time,modified,update_time) VALUES " \
               "('" + self.contract_no + "','" + self.seqNo + "',1,'01','" + self.endDate + "','300000','300','0','0','300300','300000','300','0','0','0','N','150000','0301','" + self.endDate + "','0','system','" + self.applyDate + "','system','" + self.applyDate+"');"

        self.log.demsg("sql4：{}".format(sql4))
        self.MysqlBizImpl.mysql_op_channel.update(sql4)
