
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
        result = '''{"approvalResult":"Y","approvalResultCode":"","approvalResultMsg":"","creditAmt":1000000,"creditRate":0.00050,"extInfo":"{}"}'''
        bizData = '''{"SUGGEST_INFO":{"result":{"CreditRate":0.00060,"CreditAmt":10000,"Adm":1},"bizDataInfo":{"applyType":"ADMIT_APPLY","bankInfo":"","suggestAmtExpireTime":"2021-01-25 17:59:59","certType":"01","suggestTmpAmtMax":"1000000","tmpAmtEffectiveTime":"","extInfo":"{}","certNo":"36012119900516518X","productCode":"JB","suggestTmpAmtMin":"10000","applyNo":"applyno1689298702251668","suggestAmtMax":"1000000","suggestRateMax":"0.00050","loanMode":"DIRECT","suggestAmtMin":"1000000","suggestRateMin":"0.00050","tmpAmtExpireTime":"","creditNo":"applyno1689298702251668","bizMode":"JB_ADVANCED_BK_DI","suggestAmtEffectiveTime":"2099-12-31 23:59:59"}},"BASIC_INFO":{"result":{"Adm":1},"bizDataInfo":{"applyType":"ADMIT_APPLY","reason":"","certType":"01","riskInfo":"{\\\\"joinRisk\\\\":1,\\\\"apolloInfo\\\\":{\\\\"have_car_prob_grade\\\\":\\\\"02\\\\",\\\\"have_fang_prob_grade\\\\":\\\\"01\\\\",\\\\"mobile_fixed_grade\\\\":\\\\"01\\\\",\\\\"adr_stability_grade\\\\":\\\\"09\\\\",\\\\"occupation\\\\":\\\\"专业技术人员（模型预测）\\\\",\\\\"tot_pay_amt_6m_grade\\\\":\\\\"04\\\\",\\\\"last_6m_avg_asset_total_grade\\\\":\\\\"06\\\\",\\\\"ovd_order_amt_6m_grade\\\\":\\\\"04\\\\",\\\\"positive_biz_cnt_1y_grade\\\\":\\\\"10\\\\",\\\\"cust_seg\\\\":\\\\"A\\\\",\\\\"dev_stability_grade\\\\":\\\\"A\\\\",\\\\"ovd_order_days_6m_grade\\\\":\\\\"01\\\\",\\\\"first_loan_length_grade\\\\":\\\\"05\\\\",\\\\"repay_amt_6m_grade\\\\":\\\\"07\\\\",\\\\"tot_pay_cnt_6m_grade\\\\":\\\\"01\\\\",\\\\"avg_bal_6m_grade\\\\":\\\\"01\\\\",\\\\"riskrank\\\\":\\\\"05\\\\",\\\\"repayment_ability_rank\\\\":\\\\"A\\\\",\\\\"version\\\\":\\\\"V2.0\\\\"}}","source":"PLATFORM","applyExpiredDate":"2023-03-25 15:45:33","participant":"MYXJ","extInfo":"{}","certNo":"36012119900516518X","productCode":"JB","creditFlag":"Y","applyNo":"applyno1689298702251668","name":"测试","custType":"","loanMode":"DIRECT","header":{"reqTimeZone":"UTC+8","appId":"ALIPAY","function":"ant.credit.platform.basic.info.apply","reserve":"sdk-java-1.0.1.20210826","signType":"RSA","inputCharset":"UTF-8","reqTime":"20210128173704","version":"1.0","reqMsgId":"20210128173704587000000000444876"},"creditNo":"applyno16895636209635700","bizMode":"JB_ADVANCED_BK_DI"}},"ASK":{"result":{"Adm":1},"bizDataInfo":{"applyType":"ADMIT_APPLY","certType":"01","agreement":"[{\\\\"agreementType\\\\":\\\\"JIEBEI_ORG_CREDIT_AUTH\\\\",\\\\"instId\\\\":\\\\"SCJCXFJRYXZRGS\\\\",\\\\"name\\\\":\\\\"借呗机构征信协议\\\\",\\\\"version\\\\":\\\\"2\\\\"},{\\\\"agreementType\\\\":\\\\"JIEBEI_CREDIT_SERVICE_AGREEMENT\\\\",\\\\"instId\\\\":\\\\"SCJCXFJRYXZRGS\\\\",\\\\"name\\\\":\\\\"借呗四川锦程消费金融有限责任公司授信协议\\\\",\\\\"version\\\\":\\\\"1\\\\"},{\\\\"agreementType\\\\":\\\\"JIEBEI_APPLY_INFORMATION_AUTHZ\\\\",\\\\"instId\\\\":\\\\"SCJCXFJRYXZRGS\\\\",\\\\"name\\\\":\\\\"借呗数据授权书四川锦程消费金融有限责任公司定制版\\\\",\\\\"version\\\\":\\\\"1\\\\"}]","certValidEndDate":"20351212","mobileNo":"13903268759","participant":"MYXJ","extInfo":"{}","certNo":"36012119900516518X","productCode":"JB","bankCardInfo":"{\\\\"cardType\\\\":\\\\"DC\\\\",\\\\"bankReservedMobileNo\\\\":\\\\"18800129211\\\\",\\\\"bankName\\\\":\\\\"XX银行\\\\",\\\\"cardNo\\\\":\\\\"6225880118085993\\\\"}","userAddressInfo":"{\\\\"prov\\\\": \\\\"浙江省\\\\",\\\\"provCode\\\\":\\\\"330106\\\\", \\\\"city\\\\": \\\\"杭州市\\\\", \\\\"cityCode\\\\": \\\\"330100\\\\", \\\\"area\\\\": \\\\"西湖区\\\\", \\\\"areaCode\\\\": \\\\"330106\\\\", \\\\"address\\\\": \\\\"5rKz5Y2X55yB6ZW/5Z6j5Y6/5q2m6YKx5Lmh56We5Y+w5bqZ5p2ROOWPtw==\\\\"}","applyNo":"applyno1689298702251668","name":"测试","loanMode":"DIRECT","bizMode":"JB_ADVANCED_BK_DI"}}}'''
        sql = '''INSERT INTO channel_jiebei_credit_apply
        (apply_no, credit_no, apply_type, source, product_code, biz_mode, loan_mode, name, cert_no, cert_type, 
        mobile_no, apply_date, expiry_date, state, result, biz_data, gmt_create, gmt_modified, business_date, 
        deal_status, fail_reason, status, created, create_time, modified, update_time)
        VALUES('{}', '{}', 'ADMIT_APPLY', 'PLATFORM', 'JB', 'JB_ADVANCED_BK_DI', 'DIRECT', '{}', '{}', '01', '{}', 
        '{}', '{}', 'PASS', '{}', '{}','{}', '{}', '{}', '00', '', 0, 'system', now(), 'system', now());''' \
            .format(self.creditNo, self.creditNo, self.name, self.certNo, self.telephone, self.applyDate,
                    self.expireDate, result, bizData, self.applyDate, self.applyDate, self.businessDate)
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
        self.apply_no = data['applyno'].replace('applyno', 'loanNo')
        self.businessDate = time.strftime('%Y%m%d', time.localtime())
        self.applyDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def start_loanApplyFile(self):

        sql = "INSERT INTO channel_jiebei_loan_apply (apply_no,credit_no,source,product_code,biz_mode,name,cert_no,cert_type,apply_date,state,`result`,biz_data,gmt_create,gmt_modified,business_date,deal_status,fail_msg,status,created,create_time,modified,update_time) VALUES " \
              "('" + self.apply_no + "','" + self.creditNo + "','USER','JB','JB_ADVANCED_BK_DI','" + self.name + "','" + self.certNo + "','01','" + self.applyDate + "','PASS','{\"PolicyCode\": \"JCJB_LOAN\", \"CashSuccessFlag\": \"0\", \"JC_inner_failCode\": \"900002\", \"JC_inner_failReason\": \"合作方风控拒绝\"}'," \
              "'{\"certNo\": \"330822199306066918\", \"applyNo\": \"loanNo202211070000000000000002\", \"bizMode\": \"JB_ADVANCED_BK_DI\", \"dayRate\": \"0.00060\", \"endDate\": \"20221207\", \"extInfo\": \"{}\", \"loanUse\": \"1\", \"useArea\": \"1\", \"certType\": \"01\", \"creditNo\": \"applyno16678094629536618\", \"currency\": \"CNY\", \"graceDay\": \"0\", \"loanMode\": \"DIRECT\", \"rateType\": \"F\", \"termType\": \"M\", \"userName\": \"郑半安\", \"applyDate\": \"2022-11-07 11:34:00\", \"encashAmt\": \"300000\", \"repayMode\": \"1\", \"startDate\": \"20221107\", \"extensions\": \"{}\", \"totalTerms\": \"1\", \"productCode\": \"JB\", \"encashAcctNo\": \"6217871691567078163\", \"guaranteeType\": \"A\", \"encashAcctType\": \"01\", \"intRepayFrequency\": \"D\", \"prinRepayFrequency\": \"03\"}','" \
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
        self.contract_no = data['applyno'].replace('applyno', 'contract_no')
        self.apply_no = data['applyno'].replace('applyno', 'loanNo')
        self.businessDate = time.strftime('%Y%m%d', time.localtime())
        self.endDate = datetime.datetime.now().strftime('%Y%m%d')
        self.repayDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.applyDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.seqNo = "seqNo" + str(int(round(time.time() * 100000000000)))

    def start_loandetailFile(self):

        sql1 = "INSERT INTO `channel_jiebei_loan_detail` (contract_no,fund_seq_no,prod_code,name,cert_type,cert_no,loan_status,loan_use,use_area,apply_date,encash_date,currency,encash_amt,start_date,end_date,total_terms,repay_mode,grace_day,rate_type,day_rate,prin_repay_frequency,int_repay_frequency,guarantee_type,credit_no,encash_acct_type,encash_acct_no,repay_acct_type,repay_acct_no,apply_no,region_code,bsn_type,business_date,deal_status,fail_msg,status,created,create_time,modified,update_time) VALUES " \
               "('" + self.contract_no + "','loanNo15843498411111090127','J1010100100000000004_2','" + self.name + "','01','" + self.certNo + "','1','3','1','" + self.applyDate + "','" + self.applyDate + "','CNY','300000','" + self.businessDate + "','" + self.endDate + "',1,'2',15,'F',0.000600,'03','03','D','" + self.creditNo + "','02','18627583490','01','8438516620194837','" + self.apply_no + "','630000','0201','" + self.businessDate + "','00','','0','system','" + self.applyDate + "','system','" + self.applyDate+"');"

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

        sql5 = "INSERT INTO `channel_jiebei_instmnt_daily` (contract_no, settle_date, term_no, start_date, end_date, instmnt_status, clear_date, prin_ovd_date, int_ovd_date, prin_ovd_days, int_ovd_days, prin_bal, int_bal, ovd_prin_pnlt_bal, ovd_int_pnlt_bal, accrued_status, write_off, region_code, bsn_type, business_date, status, created, create_time, modified, update_time) VALUES " \
               "('" + self.contract_no + "','" + self.endDate + "',1,'" + self.endDate + "','" + self.endDate + "','CLEAR','','','','0','0','0','0','0','0','0','N','350000','02013000','" + self.endDate + "','0','system','" + self.applyDate + "','system','" + self.applyDate + "');"

        self.log.demsg("sql5：{}".format(sql5))
        self.MysqlBizImpl.mysql_op_channel.update(sql5)
