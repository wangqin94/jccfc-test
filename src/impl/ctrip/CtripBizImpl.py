# ------------------------------------------
# 携程接口数据封装类
# ------------------------------------------
from src.impl.common.CommonBizImpl import *
from src.enums.EnumsCommon import *
from engine.EnvInit import EnvInit
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from src.impl.public.RepayPublicBizImpl import *
from utils.Models import *
from src.test_data.module_data import ctrip


class CtripBizImpl(EnvInit):
    def __init__(self, *, data=None, loan_invoice_id=None):
        """
        @param data:  四要素
        @param loan_invoice_id: 借据号为None取用户第一笔借据，否则取自定义值
        """
        super().__init__()
        # 解析项目特性配置
        self.cfg = ctrip.ctrip

        self.data = data if data else get_base_data(str(self.env) + ' -> ' + str(ProductEnum.ctrip.value), 'open_id')

        self.strings = str(int(round(time.time() * 1000)))

        self.credit_amount = 30000  # 授信申请金额, 默认30000  单位元
        self.loan_amount = 1000  # 支用申请金额, 默认1000  单位元
        self.period = 3  # 借款期数, 默认3期
        # self.repay_term_no = repay_term_no
        # self.repay_mode = repay_mode
        self.loan_invoice_id = loan_invoice_id

        # 初始化payload变量
        self.pre_credit_payload = {}
        self.credit_payload = {}
        self.loan_payload = {}
        self.repay_notice_payload = {}
        self.active_payload = {}
        self.repayPublicBizImpl = RepayPublicBizImpl()
        self.apollo = Apollo()

        # 初始数据库变量
        self.credit_database_name = '%s_credit' % TEST_ENV_INFO.lower()
        self.asset_database_name = '%s_asset' % TEST_ENV_INFO.lower()

        # 初始化查询数据库类
        self.MysqlBizImpl = MysqlBizImpl()

    def set_active_payload(self, payload):
        self.active_payload = payload

    # 预授信申请payload
    def pre_credit(self, **kwargs):
        pre_credit_data = dict()

        # 四要素
        pre_credit_data['id_no'] = self.data['cer_no']
        pre_credit_data['card_no'] = self.data['bankid']
        pre_credit_data['user_name'] = self.data['name']
        pre_credit_data['bank_bind_mobile'] = self.data['telephone']

        pre_credit_data['open_id'] = self.data["open_id"]
        pre_credit_data['request_no'] = 'request_no' + self.strings + "1"
        pre_credit_data['advice_amount'] = self.credit_amount
        pre_credit_data['advice_rate_type'] = "Y"

        pre_credit_data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['pre_credit']['payload'], **pre_credit_data)
        self.active_payload = parser.parser
        self.active_payload['user_data']['Platform']['id_no'] = self.data['cer_no']
        self.active_payload['user_data']['Platform']['user_name'] = self.data['name']
        self.active_payload['user_data']['Platform']['mobile'] = self.data['telephone']

        self.log.demsg('预授信申请...')
        url = self.host + self.cfg['pre_credit']['interface']
        response = post_with_encrypt(url, self.active_payload, encrypt_flag=False)
        return response

    # 授信payload
    def credit(self, **kwargs):
        credit_data = dict()
        # 四要素
        credit_data['id_no'] = self.data['cer_no']
        credit_data['card_no'] = self.data['bankid']
        credit_data['user_name'] = self.data['name']
        credit_data['bank_bind_mobile'] = self.data['telephone']

        credit_data['open_id'] = self.data["open_id"]
        credit_data['request_no'] = 'request_no' + self.strings + "2"
        credit_data['advice_amount'] = self.credit_amount
        credit_data['id_no'] = self.data['cer_no']
        credit_data['user_name'] = self.data['name']
        credit_data['mobile'] = self.data['telephone']
        credit_data['advice_rate_type'] = "Y"

        credit_data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['credit']['payload'], **credit_data)
        self.credit_payload = parser.parser
        self.credit_payload['user_data']['Platform']['id_no'] = self.data['cer_no']
        self.credit_payload['user_data']['Platform']['user_name'] = self.data['name']
        self.credit_payload['user_data']['Platform']['mobile'] = self.data['telephone']

        self.log.demsg('授信申请...')
        url = self.host + self.cfg['credit']['interface']
        response = post_with_encrypt(url, self.credit_payload, encrypt_flag=False)
        return response

    def update_apollo_amount(self):
        # 配置风控mock返回建议额度与授信额度一致
        apollo_data = dict()
        result = self.MysqlBizImpl.get_credit_database_info("credit_apply", thirdpart_user_id=self.data['open_id'])
        i = 1
        while result is None:
            time.sleep(5)
            result = self.MysqlBizImpl.get_credit_database_info("credit_apply", thirdpart_user_id=self.data['open_id'])
            i += 1
            if i == 5:
                break
        try:
            apollo_data['hj.channel.risk.credit.line.amt.mock'] = float(result['apply_amount'])
            self.apollo.update_config(appId='loan2.1-jcxf-credit', **apollo_data)
        except:
            pass

    # 授信查询
    def credit_query(self, **kwargs):
        credit_query_data = dict()
        key = self.MysqlBizImpl.get_credit_apply_info(thirdpart_user_id=self.data['open_id'])
        credit_query_data['request_no'] = key['credit_apply_serial_id']
        credit_query_data['open_id'] = key['thirdpart_user_id']
        # credit_query_data['request_no'] = 'request_no16599436045272'
        # credit_query_data['open_id'] = 'open_id16599435145773753'
        # 更新 payload 字段值
        credit_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit_query']['payload'], **credit_query_data)
        self.active_payload = parser.parser

        self.log.demsg('授信查询...')
        url = self.host + self.cfg['credit_query']['interface']
        response = post_with_encrypt(url, self.active_payload, encrypt_flag=False)
        return response

    # 支用申请payload
    def loan(self, loan_date=None, **kwargs):
        """ # 支用申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json response 接口响应参数 数据类型：json
        """
        loan_data = dict()
        # 四要素
        loan_data['id_no'] = self.data['cer_no']
        loan_data['card_no'] = self.data['bankid']
        loan_data['user_name'] = self.data['name']
        loan_data['bank_bind_mobile'] = self.data['telephone']

        loan_data['open_id'] = self.data["open_id"]
        loan_data['loan_no'] = 'loan_no' + self.strings
        loan_data['loan_amount'] = self.loan_amount
        loan_data['request_no'] = 'request_no' + self.strings + "3"
        loan_data['first_repay_date'] = datetime.now().strftime('%Y%m%d%H%M%S')

        loan_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan']['payload'], **loan_data)
        self.active_payload = parser.parser
        # 设置apollo放款mock时间 默认当前时间
        loan_date = loan_date if loan_date else time.strftime('%Y-%m-%d', time.localtime())
        apollo_data = dict()
        apollo_data['credit.loan.trade.date.mock'] = True
        apollo_data['credit.loan.date.mock'] = loan_date
        self.apollo.update_config(appId='loan2.1-public', namespace='JCXF.system', **apollo_data)

        self.log.demsg('支用申请...')
        url = self.host + self.cfg['loan']['interface']
        response = post_with_encrypt(url, self.active_payload, encrypt_flag=False)
        return response

    # 支用查询
    def loan_query(self, **kwargs):
        loan_query_data = dict()
        # key = self.MysqlBizImpl.get_loan_apply_info(thirdpart_user_id=self.data['open_id'])
        # loan_query_data['loan_request_no'] = key['loan_apply_serial_id']
        # loan_query_data['partner_loan_no'] = key['certificate_no']
        # 更新 payload 字段值
        loan_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan_query']['payload'], **loan_query_data)
        self.active_payload = parser.parser

        self.log.demsg('支用查询...')
        url = self.host + self.cfg['loan_query']['interface']
        response = post_with_encrypt(url, self.active_payload, encrypt_flag=False)
        return response

    # 还款通知payload
    def repay_notice(self, repay_term_no="1", repay_mode="2", repay_date=None, **kwargs):
        """ # 还款通知payload字段装填
        注意：键名必须与接口原始数据的键名一致
        @param repay_term_no:   还款期次
        @param repay_mode:      还款类型:1 按期还款；2 提前结清；3逾期还款
        @param repay_date:      实际还款时间'2021-08-09'
        @param kwargs:          需要临时装填的字段以及值 eg: key=value
        @return: response       接口响应参数 数据类型：json response 接口响应参数 数据类型：json
        """
        # 还款前置任务
        self.repayPublicBizImpl.pre_repay_config(repayDate=repay_date)
        time.sleep(10)
        strings = str(int(round(time.time() * 1000)))
        repay_notice = dict()
        # 根据openId查询支用信息
        key1 = "thirdpart_user_id = '{}'".format(self.data['open_id'])
        credit_loan_apply = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_apply", key=key1)

        # 根据支用申请单号查询借据信息
        if self.loan_invoice_id:
            loan_invoice_id = self.loan_invoice_id
            key2 = "loan_invoice_id = '{}'".format(loan_invoice_id)
            credit_loan_invoice = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key2)
            loan_apply_id = credit_loan_invoice["loan_apply_id"]
            key21 = "loan_apply_id = '{}'".format(loan_apply_id)
            credit_loan_apply = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_apply", key=key21)
        else:
            loan_apply_id = credit_loan_apply["loan_apply_id"]
            key2 = "loan_apply_id = '{}'".format(loan_apply_id)
            credit_loan_invoice = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key2)
            loan_invoice_id = credit_loan_invoice["loan_invoice_id"]

        # 取资产执行利率
        asset_loan_invoice_info = self.MysqlBizImpl.get_asset_database_info(table="asset_loan_invoice_info",
                                                                            loan_invoice_id=loan_invoice_id)
        execute_rate = asset_loan_invoice_info["execute_rate"]
        if repay_term_no:
            asset_repay_plan = self.MysqlBizImpl.get_asset_database_info('asset_repay_plan',
                                                                         loan_invoice_id=loan_invoice_id,
                                                                         current_num=repay_term_no)
        else:
            key = "loan_invoice_id = '{}' and repay_plan_status in ('1','2','4','5') ORDER BY 'current_num'".format(
                loan_invoice_id)
            asset_repay_plan = self.MysqlBizImpl.get_asset_data_info('asset_repay_plan', key, record=0)
        min_term = int(asset_repay_plan['current_num'])
        self.log.demsg('当期最早未还期次: {}'.format(min_term))
        # 根据借据Id和期次获取还款计划
        key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loan_invoice_id, min_term)
        asset_repay_plan = self.MysqlBizImpl.get_asset_data_info(table="asset_repay_plan", key=key3)

        # 通知payload
        repay_notice['open_id'] = self.data['open_id']
        repay_notice['loan_no'] = credit_loan_apply['third_loan_invoice_id']
        repay_notice['repay_no'] = 'repay_no' + strings + "10"
        repay_notice['repay_type'] = "1"
        repay_notice['repay_term_no'] = repay_term_no
        # repay_notice['repay_term_no'] = ""
        repay_notice['finish_time'] = time.strftime('%Y%m%d%H%M%S', time.localtime())

        repay_notice["actual_repay_amount"] = float(asset_repay_plan['pre_repay_amount'])  # 总金额
        repay_notice["repay_principal"] = float(asset_repay_plan['pre_repay_principal'])  # 本金
        repay_notice["repay_interest"] = float(asset_repay_plan['pre_repay_interest'])  # 利息
        repay_notice["repay_penalty_amount"] = float(asset_repay_plan['pre_repay_overdue_fee'])  # 逾期罚息
        repay_notice["repay_fee"] = float(asset_repay_plan['pre_repay_fee'])  # 手续费

        # 按期还款
        if repay_mode == "1":
            repay_notice['repay_type'] = repay_mode
            repay_notice['finish_time'] = str(asset_repay_plan["pre_repay_date"]).replace("-", "") + "112233"

        # 提前当期还款
        if repay_mode == "4":
            repay_notice['repay_type'] = '1'
            repay_notice['finish_time'] = str(repay_date.replace("-", "")) + "112233"

        # 逾期还款
        elif repay_mode == "3":
            repay_notice['repay_type'] = repay_mode
            finish_time = asset_repay_plan["calc_overdue_fee_date"] - relativedelta(days=-int(1))
            repay_notice['finish_time'] = str(finish_time).replace("-", "") + "112233"

        # 提前结清
        elif repay_mode == "2":
            repay_notice['repay_type'] = repay_mode
            repay_notice['finish_time'] = str(repay_date.replace("-", "")) + "112233"
            repay_notice["repay_principal"] = float('{:.2f}'.format(asset_repay_plan['before_calc_principal']))  # 本金

            pre_repay_date = str(asset_repay_plan["start_date"])
            pre_repay_date = datetime.strptime(pre_repay_date, "%Y-%m-%d").date()
            repay_date = datetime.strptime(repay_date, "%Y-%m-%d").date()
            if pre_repay_date > repay_date:
                repay_notice["repay_interest"] = 0  # 如果还款时间小于账单日，利息应该为0
            else:
                # 计算提前结清利息:剩余还款本金*（实际还款时间-本期开始时间）*日利率
                days = get_day(asset_repay_plan["start_date"], repay_date)
                paid_prin_amt = asset_repay_plan["before_calc_principal"] * days * execute_rate / (100 * 360)
                repay_notice["repay_interest"] = float('{:.2f}'.format(paid_prin_amt))  # 利息
                print(repay_notice["repay_interest"])

            repay_notice["repay_penalty_amount"] = 0
            repay_notice["repay_fee"] = 0
            repay_notice["actual_repay_amount"] = float('{:.2f}'.format(repay_notice["repay_principal"] + repay_notice[
                "repay_interest"]))  # 总金额
            print("总金额：{}，本金：{}，利息{}".format(repay_notice["actual_repay_amount"], repay_notice["repay_principal"],
                                             repay_notice["repay_interest"]))

        repay_notice.update(kwargs)
        parser = DataUpdate(self.cfg['loan_repay_notice']['payload'], **repay_notice)
        self.active_payload = parser.parser

        self.log.demsg('还款通知...')
        url = self.host + self.cfg['loan_repay_notice']['interface']
        response = post_with_encrypt(url, self.active_payload, encrypt_flag=False)
        return response


if __name__ == '__main__':
    info = CtripBizImpl()