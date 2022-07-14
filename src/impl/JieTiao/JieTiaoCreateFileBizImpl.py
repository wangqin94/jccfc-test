import os
import time

from config.TestEnvInfo import TEST_ENV_INFO
from engine.EnvInit import EnvInit
from src.enums.EnumsCommon import ProductEnum
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils.Logger import Logs

_log = Logs()
_ProjectPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # 项目根目录
_FilePath = os.path.join(_ProjectPath, 'FilePath', ProductEnum.JieTiao.value, TEST_ENV_INFO)  # 文件存放目录


class repayPlanFile(EnvInit):
    def __init__(self):
        super(repayPlanFile, self).__init__()
        self.MysqlBizImpl = MysqlBizImpl()

        # 获取文件存储名
        data_save_path = '%s' % (time.strftime('%Y%m%d', time.localtime()))
        self.data_save_path = os.path.join(_FilePath, data_save_path)
        if not os.path.exists(self.data_save_path):
            os.makedirs(self.data_save_path)

        self.repay_plan_keys = [
            'loan_req_no',
            'repay_num',
            'current_num',
            'pre_repay_date',
            'pre_repay_amount',
            'pre_repay_principal',
            'pre_repay_interest',
            'pre_repay_overdue_fee',
            'actual_repay_principal',
            'actual_repay_interest',
            'actual_repay_overdue_fee',
            'actual_repay_date',
            'actual_repay_amount'
            ]

        self.repay_plan_template = {
            'loan_req_no': "",
            'repay_num': "",
            'current_num': "",
            'pre_repay_date': "",
            'pre_repay_amount': "",
            'pre_repay_principal': "",
            'pre_repay_interest': "",
            'pre_repay_overdue_fee': "",
            'actual_repay_principal': "0",
            'actual_repay_interest': "0",
            'actual_repay_overdue_fee': "0",
            'actual_repay_date': "",
            'actual_repay_amount': "0"
        }



     # 还款计划文件生成入口
    def start_repayPlanFile(self, loan_invoice_id=''):

        self.loan_invoice_id = loan_invoice_id

        # 查询sql语句:loan_req_no
        sql = "select thirdpart_apply_id from {}.credit_loan_apply cla where  loan_apply_id = (select loan_apply_id from {}.credit_loan_invoice cli where  loan_invoice_id = '{}') ;".format(
            self.MysqlBizImpl.credit_database_name, self.MysqlBizImpl.credit_database_name, self.loan_invoice_id)
        # 获取查询内容
        values = self.MysqlBizImpl.mysql_credit.select(sql)

        self.repay_plan_template['loan_req_no'] = values[0][0]

        self.log.demsg("repay_plan_template：{}".format(self.repay_plan_template))

        # 查询 还款计划
        table = 'asset_repay_plan'
        # 查询sql语句
        sql = "select repay_num,current_num,pre_repay_date,pre_repay_amount,pre_repay_principal,pre_repay_interest,pre_repay_overdue_fee from {}.asset_repay_plan where loan_invoice_id='{}' order by current_num;".format(
            self.MysqlBizImpl.asset_database_name, self.loan_invoice_id)

        # 获取查询内容
        values = self.MysqlBizImpl.mysql_asset.select(sql)
        self.log.demsg("还款计划查询资产：{}".format(values))

        # 开始写入还款计划文件
        for v in values :
            self.log.demsg("循环：{}".format(v))
            self.get_repay_plan(v)


        # 还款计划文件生成
    def get_repay_plan(self, value):
        repayPlanPath = '%s' % (time.strftime('%Y%m%d', time.localtime()))
        repay_plan = os.path.join(self.data_save_path, 'PLAN'+repayPlanPath+'.txt')

        self.repay_plan_template['repay_num'] = value[0]
        self.repay_plan_template['current_num'] = value[1]
        self.repay_plan_template['pre_repay_date'] = value[2]
        self.repay_plan_template['pre_repay_amount'] = value[3]
        self.repay_plan_template['pre_repay_principal'] = value[4]
        self.repay_plan_template['pre_repay_interest'] = value[5]
        self.repay_plan_template['pre_repay_overdue_fee'] = value[6]
        self.repay_plan_template['actual_repay_date'] = value[2]

        val_list = map(str, [self.repay_plan_template[key] for key in self.repay_plan_keys])
        strings = '|'.join(val_list)
        with open(repay_plan, 'a+', encoding='utf-8') as f:
            f.write(strings)
            f.write('\n')

class repayDetailFile(EnvInit):
    def __init__(self):
        super(repayDetailFile, self).__init__()
        self.MysqlBizImpl = MysqlBizImpl()

        # 获取文件存储名
        data_save_path = '%s' % (time.strftime('%Y%m%d', time.localtime()))
        self.data_save_path = os.path.join(_FilePath, data_save_path)
        if not os.path.exists(self.data_save_path):
            os.makedirs(self.data_save_path)

        self.repay_detail_keys = [
            'loanReqNo',
            'sourceCode',
            'rpyType',
            'rpyTerm',
            'rpyReqNo',
            'tranNo',
            'rpyDate',
            'rpyPrinAmt',
            'rpyIntAmt',
            'rpyOintAmt',
            'rpyShareAmt',
            'rpyDeductAmt',
            'rpyRedLineAmt',
            'ifEnough',
            'rpyShareAmtOne',
            'rpyShareAmtTwo',
            'rpyShareAmtThree',
            'rpyShareAmtFour',
            'rpyChannel'
        ]

        self.repay_detail_template = {
            'loanReqNo': "",
            'sourceCode': "",
            'rpyType': "",
            'rpyTerm': "",
            'rpyReqNo': "",
            'tranNo': "",
            'rpyDate': "",
            'rpyPrinAmt': "",
            'rpyIntAmt': "",
            'rpyOintAmt': "",
            'rpyShareAmt': "",
            'rpyDeductAmt': "",
            'rpyRedLineAmt': "",
            'ifEnough': "",
            'rpyShareAmtOne': "",
            'rpyShareAmtTwo': "",
            'rpyShareAmtThree': "",
            'rpyShareAmtFour': "",
            'rpyChannel': ""
        }

    def start_repayDetailFile(self,withhold_id=''):

        # 查询sql语句
        sql = "select   a.third_loan_id , 'QH' ,b.rpy_type ,a.repay_term ,a.third_repay_id ,a.third_withhold_id, DATE_FORMAT(repay_time,'%Y-%m-%d') , repay_principal,repay_interest, " \
              "repay_overdue_fee,refund_amount ,market_amount ,red_line_amount ,settle_status , b.rpy_share_amt_one, b.rpy_share_amt_two, b.rpy_share_amt_three, b.rpy_share_amt_four, withhold_type " \
              "from  {}.channel_repay a  left join {}.channel_jietiao_repay_info b on a.repay_id = b.repay_id  where a.withhold_id ='{}' ;".format(self.MysqlBizImpl.op_channel_database_name,self.MysqlBizImpl.op_channel_database_name,  withhold_id)

        # 获取查询内容
        values = self.MysqlBizImpl.mysql_op_channel.select(sql)
        self.log.demsg("还款明细：{}".format(values))

        # 开始写入还款计划文件
        for v in values:
            self.log.demsg("循环：{}".format(v))
            self.get_repay_detail(v)

    def start(self,check_id=''):

        self.strings = str(int(round(time.time() * 1000)))
        self.log.demsg("checkid：{}".format(check_id))
        sql1 = "INSERT INTO channel_file_check(check_id, channel_no, merchant_id, product_id, user_id, user_name, certificate_type,certificate_no, relation_id, relation_id_type, thirdpart_apply_id, apply_date, deal_status, "\
               " fail_reason, business_date, status, created, create_time, modified, update_time) "\
               "VALUES ('{}', 'JIETIAO', 'F22E01360J', 'F22E011', '000UC02002022062700000013', '彭成瑶', '0', '230307195910188572', '000CA2022100400000004', '1', 'loanReqNo16563812597682', '2022-03-23 00:00:00', '03', '', "\
               " '20220627', 0, 'system', '2022-06-28 09:54:21', 'system', '2022-06-29 14:54:15');".format(check_id)

        self.MysqlBizImpl.mysql_op_channel.update(sql1)

        sql = "INSERT INTO channel_file_check_detail (check_detail_id,check_id,file_type,file_url,deal_status,fail_reason,status,created,create_time,modified,update_time) " \
              "VALUES ('" +self.strings + "DEF1" + "','{}','1','xdgl/hj/jietiao/2022/06/29/7DB8214930C941C987E9CF868E645CE9.jpg','03','',0,'system','2022-06-28 09:54:21','system','2022-06-29 14:55:38'), ".format(check_id) +\
              " ('" +self.strings + "DEF2" + "','{}','2','xdgl/hj/jietiao/2022/06/29/81D8B612F0DB47C786CBD62FFB588978.jpg','03','',0,'system','2022-06-28 09:54:21','system','2022-06-29 14:55:38'), ".format(check_id)+ \
              " ('" +self.strings + "DEF3" + "','{}','20','xdgl/hj/jietiao/2022/06/29/5B3EE12E75BF4F4D8BA5A5363E64FC36.jpg','03','',0,'system','2022-06-28 09:54:21','system','2022-06-29 15:28:12');	".format(check_id)
        self.log.demsg("sql：{}".format(sql))
        self.MysqlBizImpl.mysql_op_channel.update(sql)



# 还款明细文件生成
    def get_repay_detail(self, value):
        repayDetailPath = '%s' % (time.strftime('%Y%m%d', time.localtime()))
        repay_detail = os.path.join(self.data_save_path, 'REPAY'+repayDetailPath+'.txt')
        self.log.demsg("还款明细生成路径：{}".format(repay_detail))

        val_list = map(str, [v for v in value])
        strings = '|'.join(val_list)
        with open(repay_detail, 'a+', encoding='utf-8') as f:
            f.write(strings)
            f.write('\n')