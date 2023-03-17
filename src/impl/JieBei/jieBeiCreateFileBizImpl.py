import datetime
import os
from datetime import time

from config.TestEnvInfo import TEST_ENV_INFO
from engine.EnvInit import EnvInit
from src.enums.EnumsCommon import ProductEnum
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils.Logger import Logs

_log = Logs()
_ProjectPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # 项目根目录
_FilePath = os.path.join(_ProjectPath, 'FilePath', ProductEnum.JIEBEI.value, TEST_ENV_INFO)  # 文件存放目录


class creditFile(EnvInit):
    def __init__(self):
        super(creditFile, self).__init__()
        self.MysqlBizImpl = MysqlBizImpl()



    # 银河授信文件
    def start_creditFile(self):
        self.name = self.data['name']
        self.certNo = self.data['cer_no']
        self.telephone = self.data['telephone']
        self.creditNo = self.data['applyno']
        self.applyDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.expireDate = (datetime.datetime.now()+datetime.timedelta(days=31)).strftime('%Y-%m-%d 00:00:00')

        sql = "INSERT INTO channel_jiebei_credit_apply(apply_no,credit_no,apply_type, source, product_code, biz_mode, loan_mode, name,cert_no, cert_type, mobile_no, apply_date, expire_date, " \
               " state, result, biz_date, gmt_modified, business_date, deal_status, fail_reason,status,created,create_time,modified,update_time) " \
               "VALUES ('" +self.creditNo + "','" + self.creditNo + "','ADMIT_APPLY','PLATFORM','JB','JB_ADVANCED_BK_DI','DIRECT','"+ self.name+"','"+self.certNo+"','01','"+self.telephone+"','" \
               +self.applyDate+"','"+self.expireDate+"','PASS',''"

        self.MysqlBizImpl.mysql_op_channel.update(sql)

class loanApplyFile(EnvInit):
    def __init__(self):
        super(loanApplyFile, self).__init__()
        self.MysqlBizImpl = MysqlBizImpl()