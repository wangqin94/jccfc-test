# -*- coding: utf-8 -*-
"""
    Function: 分期乐还款文件生成
"""
from datetime import datetime

from config.TestEnvInfo import *
from engine.EnvInit import EnvInit
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils.Models import *
from utils.KS3 import *
from src.enums.EnumsCommon import *
from utils import GlobalVar as gl


_ProjectPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # 项目根目录
_FilePath = os.path.join(_ProjectPath, 'FilePath', ProductEnum.FQL.value, TEST_ENV_INFO)  # 文件存放目录
if not os.path.exists(_FilePath):
    os.makedirs(_FilePath)


class fqlRepayFile(EnvInit):
    def __init__(self, data, repay_mode='1', term_no='1', repay_date='2021-08-09'):
        """
        @param data:  四要素
        @param repay_mode:  还款模式，1：按期还款；3：提前结清；5；逾期还款
        @param term_no:     还款期数
        @param repay_date:    还款时间
        """
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()
        self.ks3 = KS3()
        self.applyId = data['applyId']
        self.repay_mode = repay_mode
        self.term_no = term_no
        self.repay_date = repay_date
        self.data_save_path = ''
        self.repay_filename = ""
        self.current_date = time.strftime('%Y-%m-%d', time.localtime())
        self.data = data

        # 还款 字段名列表，(文件生成时字符串拼接使用)
        self.repay_key_temple = [
            'applyId',
            'term_no',
            'repay_date',
            'repay_amt',
            'paid_prin_amt',
            'paid_int_amt',
            'repay_mode',
            'reserve',
        ]

        # 还款 键值对字典数据模板
        self.repay_temple = {
            'applyId': "",  # applyid
            'term_no': "1",  # 还款期次
            'repay_date': "",  # 还款时间
            'repay_amt': "",  # 还款本金
            'paid_prin_amt': "",  # 还款利息
            'paid_int_amt': "",  # 还款罚息
            'repay_mode': "",  # 还款方式
            'reserve': "",  # 备注字段
        }
        # 执行
        self.start()

    # 文件生成入口
    def start(self):
        # 开始写入还款文件
        self.repayment_acct_period(self.repay_temple)
        self.log.demsg("还款文件生成路径：{}".format(_FilePath))

    # 计算还款时间和放款时间差，天为单位
    def get_day(self, time1, time2):
        """
        @param time1: 时间1
        @param time2: 时间2
        :return: 差异天数
        """
        try:
            day_num = 0
            day1 = time.strptime(str(time1), '%Y-%m-%d')
            day2 = time.strptime(str(time2), '%Y-%m-%d')
            if type == 'day':
                day_num = (int(time.mktime(day2)) - int(time.mktime(day1))) / (24 * 60 * 60)
            return abs(int(day_num))
        except Exception as e:
            self.log.error("系统错误:{}".format(e))

    # 获取文件存放路径，还款文件名
    def get_filename(self, repay_date):
        # 初始化文件存放路径，(用户_身份证号)
        data_save_path = '%s_%s' % (
            self.data['name'], self.data['cer_no'])
        data_save_path = os.path.join(_FilePath, data_save_path, repay_date)
        if not os.path.exists(data_save_path):
            os.makedirs(data_save_path)
        # 借据文件名
        repayment_acct = os.path.join(data_save_path,  'JC_repayment_acct_%s.txt' % (repay_date.replace('-', '')))
        return data_save_path, repayment_acct

    # 还款文件生成
    def repayment_acct_period(self, temple):
        """
        @param temple: 还款字段字典模板
        :return:
        """
        temple['applyId'] = self.applyId
        temple['repay_mode'] = self.repay_mode
        temple['term_no'] = self.term_no

        # 根据applyId查询还款计划中的借据号
        key1 = "apply_id = '{}'".format(self.applyId)
        credit_repay_plan = self.MysqlBizImpl.get_credit_data_info(table="credit_repay_plan", key=key1)
        loan_invoice_id = credit_repay_plan["loan_invoice_id"]

        # 根据applyId查询还款计划中的借据号
        key2 = "thirdpart_apply_id = '{}'".format(self.applyId)
        credit_loan_apply = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_apply", key=key2)
        apply_rate = credit_loan_apply["apply_rate"]

        # 根据借据Id和期次获取资产侧还款计划
        key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loan_invoice_id, self.term_no)
        asset_repay_plan = self.MysqlBizImpl.get_asset_data_info(table="asset_repay_plan", key=key3)
        temple['repay_amt'] = str('{:.2f}'.format(asset_repay_plan["pre_repay_principal"]))
        temple['paid_prin_amt'] = str('{:.2f}'.format(asset_repay_plan["pre_repay_interest"]))
        temple['paid_int_amt'] = str('{:.2f}'.format(asset_repay_plan["pre_repay_fee"]))
        # 按期还款
        if self.repay_mode == "1":
            temple['repay_date'] = str(asset_repay_plan["pre_repay_date"]).replace("-", "")
            self.repay_date = asset_repay_plan["pre_repay_date"]
            # 获取文件名及存放路径
            self.repay_filename = self.get_filename(str(self.repay_date))[1]

        # 逾期还款
        elif self.repay_mode == "5":
            temple['repay_date'] = str(self.repay_date).replace("-", "")
            # self.repay_date = asset_repay_plan["calc_overdue_fee_date"]
            self.repay_filename = self.get_filename(str(self.repay_date))[1]

        # 提前结清
        elif self.repay_mode == "3":
            temple['repay_date'] = self.repay_date.replace("-", "")
            self.repay_filename = self.get_filename(str(self.repay_date))[1]
            temple['repay_amt'] = str("{:.2f}".format(asset_repay_plan["before_calc_principal"]))  # 剩余应还本金
            temple['paid_int_amt'] = 0

            pre_repay_date = str(asset_repay_plan["start_date"])
            pre_repay_date = datetime.strptime(pre_repay_date, "%Y-%m-%d").date()
            repay_date = datetime.strptime(self.repay_date, "%Y-%m-%d").date()
            if pre_repay_date > repay_date:
                temple["paid_prin_amt"] = 0  # 如果还款时间小于账单日，利息应该为0
            else:
                # 计算提前结清利息:剩余还款本金*（实际还款时间-本期开始时间）*日利率
                days = get_day(asset_repay_plan["start_date"], self.repay_date)
                # 利息
                paid_prin_amt = asset_repay_plan["left_principal"] * days * apply_rate / (100 * 360)
                temple['paid_prin_amt'] = str('{:.2f}'.format(paid_prin_amt))

        repay_plan={}
        repay_plan['term_no'] = temple['term_no']
        repay_plan['repay_mode'] = temple['repay_mode']
        repay_plan['repay_date'] = temple['repay_date']
        repay_plan['repay_amt'] = temple['repay_amt']
        repay_plan['paid_prin_amt'] = temple['paid_prin_amt']
        repay_plan['paid_int_amt'] = temple['paid_int_amt']
        gl.set_value('repay_plan', repay_plan)
        # 写入单期还款文件
        val_list = map(str, [temple[key] for key in self.repay_temple])
        strs = '|'.join(val_list)
        with open(self.repay_filename, 'w+', encoding='utf-8') as f:
            f.write(strs)
            f.write("|")

        #上传金山云
        self.ks3.upload_file(self.repay_filename, 'xdgl/fql/pl/' + 'JC_repayment_acct_%s.txt' % str(self.repay_date).replace("-", ""))



if __name__ == '__main__':
    # 按期还款，提前结清（按日计息），提前结清
    # repay_mode:  还款模式，1：按期还款；3：提前结清；5；逾期还款
    from src.test_case.fql.person import data
    t = fqlRepayFile(data, repay_date='2021-09-16', term_no="1", repay_mode='1')
