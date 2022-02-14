import sys
import time

from engine.EnvInit import EnvInit
from src.enums import global_var as gl
from src.enums.EnumsCommon import *
from src.impl.common.MysqlBizImpl import MysqlBizImpl


class FqlCreditCheckBizImpl(EnvInit):
    def __init__(self):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()

    def check_credit_apply_status(self, m=10, t=3, **kwargs):
        """
        @param kwargs: 查询条件
        @param t: 每次时间间隔, 默认5S
        @param m: 查询轮训次数 默认10次
        @return: response 接口响应参数 数据类型：json
        """
        self.log.demsg('数据库授信结果校验...')
        flag = 2
        for i in range(flag + 1):
            creditApply = self.MysqlBizImpl.get_credit_apply_info(**kwargs)
            if not creditApply:
                self.log.info("credit_apply未查询到授信记录，启动3次轮训")
                time.sleep(t)
                if i == flag:
                    self.log.error("超过当前系统设置等待时间，授信异常，请手动查看结果....")
                    sys.exit(7)
            else:
                self.log.info("授信记录已入credit_apply表")
                break
        for j in range(m):
            creditApply = self.MysqlBizImpl.get_credit_apply_info(**kwargs)
            status = creditApply['status']
            if (status != EnumCreditStatus.AUDITING.value) & (status != EnumCreditStatus.TO_CREDIT.value):
                self.log.demsg('授信已终态------------')
                return creditApply
            else:
                self.log.demsg("授信审批状态处理中，请等待....")
                time.sleep(t)
                if j == m - 1:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")
                    raise Exception("Invalid level!")


    def checkCreditApply1(self, creditApply):
        self.log.demsg(f"授信credit_apply数据库信息校验----：{creditApply}")
        assert creditApply['status'] == '03', "授信成功"
        assert creditApply['credit_biz_type'] == '1', "业务类型：正式授信"
        assert creditApply['credit_type'] == '0', "是否循环授信：否"
        assert creditApply['user_name'] == gl.get_value('name'), "客户姓名"
        assert creditApply['user_tel'] == gl.get_value('telephone'), "客户手机号"
        assert creditApply['certificate_type'] == '0', "证件类型"
        assert creditApply['certificate_no'] == gl.get_value('cer_no'), "身份证号"
        assert creditApply['user_type'] == '200', "客户类型"
        assert creditApply['apply_term'] == 1, "申请期限"
        assert creditApply['apply_term_unit'] == '1', "申请期限单位"
        assert creditApply['product_id'] == 'F021108', "产品码"
        assert creditApply['product_catalog'] == 'F0210001', "产品种类"

    def checkCreditInfo1(self, **kwargs):
        creditInfo = self.MysqlBizImpl.get_credit_database_info('credit_info', **kwargs)
        self.log.demsg(f"授信credit_info数据库信息校验----：{creditInfo}")
        assert creditInfo['user_name'] == gl.get_value('name'), "客户姓名"
        assert creditInfo['user_tel'] == gl.get_value('telephone'), "客户手机号"
        assert creditInfo['certificate_type'] == '0', "证件类型"
        assert creditInfo['certificate_no'] == gl.get_value('cer_no'), "身份证号"
        assert creditInfo['user_type'] == '200', "客户类型"
        assert creditInfo['product_id'] == 'F021108', "产品码"
        assert creditInfo['product_catalog'] == 'F0210001', "产品种类"
        # assert creditInfo['credit_rate'] == '36.0000', "授信年利率"
        # assert creditInfo['credit_amount'] == '1000', "授信金额"
        assert creditInfo['credit_term'] == 1, "申请期限"
        assert creditInfo['credit_term_unit'] == '1', "申请期限单位"