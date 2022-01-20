import os

from config.TestEnvInfo import TEST_ENV_INFO
from engine.EnvInit import EnvInit
from src.enums.EnumsCommon import ProductEnum
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils.Logger import Logs

_log = Logs()
_ProjectPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # 项目根目录
_FilePath = os.path.join(_ProjectPath, 'FilePath', ProductEnum.JieTiao.value, TEST_ENV_INFO)  # 文件存放目录
if not os.path.exists(_FilePath):
    os.makedirs(_FilePath)


class repayPlanFile(EnvInit):
    def __init__(self, data, cur_date=None, loan_record=0, repay_mode='02'):
        super(repayPlanFile, self).__init__()
        self.MysqlBizImpl = MysqlBizImpl()

        self.repay_plan_keys = [
            'cur_date',
            'loan_id',

            ]

        self.repay_plan_template = [
            'cur_date',
            'loan_id',

        ]


        # 还款计划文件生成入口
    def start_repayPlanFile(self):
        # 开始写入还款计划文件
        for amt in self.amount:
            # period_id = strings + "%03d" % syb
            self.get_repay_plan(self.repay_plan_template, amt)

        self.log.demsg("还款计划生成路径：{}".format(_FilePath))


class repayDetailFile(EnvInit):
    def __init__(self, data, cur_date=None, loan_record=0, repay_mode='02'):
        super(repayPlanFile, self).__init__()
        self.MysqlBizImpl = MysqlBizImpl()

    def start_repayDetailFile(self):
        self.log.demsg("还款计划生成路径：{}".format(_FilePath))