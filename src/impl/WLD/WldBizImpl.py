# -*- coding: utf-8 -*-
# ------------------------------------------
# 我来贷接口数据封装类
# ------------------------------------------
from engine.EnvInit import EnvInit
from src.impl.common.CommonBizImpl import *
from src.impl.public.RepayPublicBizImpl import *
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils.Models import *
from src.enums.EnumsCommon import *
from src.enums.EnumWld import *
from src.test_data.module_data import wld
from utils.FileHandle import *


class WldBizImpl(EnvInit):
    def __init__(self, data=None, person=True, encrypt_flag=True, **kwargs):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()
        self.Files = Files()
        # 解析项目特性配置
        self.cfg = wld.wld
        # self.log.demsg('当前测试环境 {}'.format(TEST_ENV_INFO))

        # 获取四要素
        if data:
            self.data = data
            # self.log.info('用户四要素信息 {}'.format(self.data))

        else:
            if person:
                self.data = get_base_data(str(self.env) + ' -> ' + str(ProductEnum.WLD.value), 'applyid')
            else:
                self.data = get_base_data_temp('applyid')

        self.encrypt_flag = encrypt_flag
        self.strings = str(int(round(time.time() * 1000)))
        self.times = time.strftime('%Y%m%d%H%M%S', time.localtime())
        # self.repay_term_no = repay_term_no
        # self.repay_type = repay_type
        # self.loan_invoice_id = loan_invoice_id

        self.encrypt_url = self.host + WldPathEnum.wldEncryptPath.value
        self.decrypt_url = self.host + WldPathEnum.wldDecryptPath.value

        # 初始化payload变量
        self.active_payload = {}
        self.repayPublicBizImpl = RepayPublicBizImpl()
        self.apollo = Apollo()

    @staticmethod
    def url_encoded_to_json(response):
        data = dict()
        data["content"] = response.split('content=')[1].split('&sign=')[0]
        data["sign"] = response.split('&sign=')[1]
        return data

    # 发起代扣签约payload
    def bind_card(self, **kwargs):
        bind_card_data = dict()
        # head
        bind_card_data['requestSerialNo'] = 'SerialNo' + self.strings + "1"
        bind_card_data['requestTime'] = self.times
        # body
        bind_card_data['payer'] = self.data['name']
        bind_card_data['payerIdNum'] = self.data['cer_no']
        bind_card_data['payerBankCardNum'] = self.data['bankid']
        bind_card_data['payerPhoneNum'] = self.data['telephone']
        bind_card_data['payerBankCode'] = self.data['bankcode']

        # 更新 payload 字段值
        bind_card_data.update(kwargs)
        parser = DataUpdate(self.cfg['bind_card']['payload'], **bind_card_data)
        self.active_payload = parser.parser

        # 校验用户是否在系统中已存在
        self.MysqlBizImpl.check_user_available(self.data)

        self.log.demsg('发起代扣签约...')
        url = self.host + self.cfg['bind_card']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)

        bind_card_info = dict()
        bind_card_info['data'] = self.data
        bind_card_info['response'] = response
        return bind_card_info

    # 确认代扣签约payload
    def confirm_bind_card(self, **kwargs):
        confirm_bind_card_data = dict()
        # head
        confirm_bind_card_data['requestSerialNo'] = 'SerialNo' + self.strings + "2"
        confirm_bind_card_data['requestTime'] = self.times
        # body
        key = "id_card_no = '" + self.data['cer_no'] + "' order by create_time desc"
        content = self.MysqlBizImpl.get_credit_data_info(table="credit_bind_card_info", key=key)
        confirm_bind_card_data['tradeSerialNo'] = content['trade_serial_no']

        # 更新 payload 字段值
        confirm_bind_card_data.update(kwargs)
        parser = DataUpdate(self.cfg['confirm_bind_card']['payload'], **confirm_bind_card_data)
        self.active_payload = parser.parser

        self.log.demsg('确认代扣签约...')
        url = self.host + self.cfg['confirm_bind_card']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 代扣签约查询
    def query_bind_card(self, **kwargs):
        query_bind_card_data = dict()
        # head
        query_bind_card_data['requestSerialNo'] = 'SerialNo' + self.strings + "3"
        query_bind_card_data['requestTime'] = self.times
        # body
        key = "id_card_no = '" + self.data['cer_no'] + "' order by create_time desc"
        content = self.MysqlBizImpl.get_credit_data_info(table="credit_bind_card_info", key=key)
        query_bind_card_data['tradeSerialNo'] = content['trade_serial_no']
        query_bind_card_data['userId'] = content['user_id']

        # 更新 payload 字段值
        query_bind_card_data.update(kwargs)
        parser = DataUpdate(self.cfg['query_bind_card']['payload'], **query_bind_card_data)
        self.active_payload = parser.parser

        self.log.demsg('代扣签约查询...')
        url = self.host + self.cfg['query_bind_card']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 换卡通知
    def update_card(self, **kwargs):
        update_card_data = dict()
        # head
        update_card_data['requestSerialNo'] = 'SerialNo' + self.strings + "4"
        update_card_data['requestTime'] = self.times
        # body
        key = "certificate_no = '" + self.data['cer_no'] + "' order by create_time desc"
        content = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key)
        update_card_data['loanInvoiceId'] = content['loan_invoice_id']
        update_card_data['idNo'] = self.data['cer_no']
        update_card_data['repaymentAccountNo'] = BankNo().get_bank_card()

        # 更新 payload 字段值
        update_card_data.update(kwargs)
        parser = DataUpdate(self.cfg['update_card']['payload'], **update_card_data)
        self.active_payload = parser.parser

        self.log.demsg('换卡通知...')
        url = self.host + self.cfg['update_card']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 授信申请
    def credit(self, **kwargs):
        credit_data = dict()
        # head
        credit_data['requestSerialNo'] = 'SerialNo' + self.strings + "5"
        credit_data['requestTime'] = self.times
        # body
        credit_data['thirdApplyId'] = self.data['applyid']
        credit_data['userBankCardNo'] = self.data['bankid']
        credit_data['reserveMobile'] = self.data['telephone']
        credit_data['name'] = self.data['name']
        credit_data['idNo'] = self.data['cer_no']
        credit_data['mobileNo'] = self.data['telephone']

        # 更新 payload 字段值
        credit_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit']['payload'], **credit_data)
        self.active_payload = parser.parser

        self.log.demsg('授信申请...')
        url = self.host + self.cfg['credit']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 授信申请查询
    def credit_query(self, **kwargs):
        credit_query_data = dict()
        # head
        credit_query_data['requestSerialNo'] = 'SerialNo' + self.strings + "6"
        credit_query_data['requestTime'] = self.times
        # body
        credit_query_data['thirdApplyId'] = self.data['applyid']

        # 更新 payload 字段值
        credit_query_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit_query']['payload'], **credit_query_data)
        self.active_payload = parser.parser

        self.log.demsg('授信申请查询...')
        url = self.host + self.cfg['credit_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 支用申请
    def loan(self, loan_date=None, **kwargs):
        loan_data = dict()
        # head
        loan_data['requestSerialNo'] = 'SerialNo' + self.strings + "7"
        loan_data['requestTime'] = self.times
        # body
        loan_data['thirdApplyId'] = self.data['applyid']
        loan_data['accountNo'] = self.data['bankid']
        loan_data['mobileNo'] = self.data['telephone']
        loan_data['name'] = self.data['name']
        loan_data['idNo'] = self.data['cer_no']
        key = "thirdpart_apply_id = '" + self.data['applyid'] + "'"
        content = self.MysqlBizImpl.get_credit_data_info(table="credit_apply", key=key)
        loan_data['loanAmt'] = float(content['apply_amount'])
        loan_data['loanTerm'] = str(content['apply_term'])

        # 更新 payload 字段值
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
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 支用查询
    def loan_query(self, **kwargs):
        loan_query_data = dict()
        # head
        loan_query_data['requestSerialNo'] = 'SerialNo' + self.strings + "8"
        loan_query_data['requestTime'] = self.times
        # body
        loan_query_data['thirdApplyId'] = self.data['applyid']

        # 更新 payload 字段值
        loan_query_data.update(**kwargs)
        parser = DataUpdate(self.cfg['loan_query']['payload'], **loan_query_data)
        self.active_payload = parser.parser

        self.log.demsg('支用查询...')
        url = self.host + self.cfg['loan_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 还款计划查询
    def repay_plan(self, **kwargs):
        repay_plan_data = dict()
        # head
        repay_plan_data['requestSerialNo'] = 'SerialNo' + self.strings + "9"
        repay_plan_data['requestTime'] = self.times
        # body
        key = "certificate_no = '" + self.data['cer_no'] + "' order by create_time desc"
        content = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key)
        repay_plan_data['loanInvoiceId'] = content['loan_invoice_id']

        # 更新 payload 字段值
        repay_plan_data.update(kwargs)
        parser = DataUpdate(self.cfg['repay_plan_query']['payload'], **repay_plan_data)
        self.active_payload = parser.parser

        self.log.demsg('还款计划查询...')
        url = self.host + self.cfg['repay_plan_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 还款
    def repay(self, repay_date=None, repay_term_no='1', repay_type="1", loan_invoice_id='', **kwargs):
        # 还款  repay_term_no还款期次   repay_type还款类型：1-按期还款，2-提前结清，4-逾期还款
        # 还款前置任务
        self.repayPublicBizImpl.pre_repay_config(repayDate=repay_date)
        repay_data = dict()
        strings = str(int(round(time.time() * 1000)))
        times = time.strftime('%Y%m%d%H%M%S', time.localtime())
        # head
        repay_data['requestSerialNo'] = 'SerialNo' + strings + "10"
        repay_data['requestTime'] = times
        # body

        repay_data['repayApplySerialNo'] = 'repay' + strings + "5"
        repay_data['repayType'] = repay_type
        repay_data['repayNum'] = repay_term_no
        repay_data['loanInvoiceId'] = loan_invoice_id
        key = "user_id in (select user_id from credit_loan_invoice where loan_invoice_id = '" \
              + loan_invoice_id + "')"

        content = self.MysqlBizImpl.get_credit_data_info(table="credit_bind_card_info", key=key)
        repay_data['repaymentAccountNo'] = content['bank_card_no']
        key1 = "loan_invoice_id = '" + loan_invoice_id + "' and current_num = '" + repay_term_no + "'"
        content1 = self.MysqlBizImpl.get_asset_data_info(table="asset_repay_plan", key=key1)
        self.log.info(content1)
        repay_data['repayInterest'] = float(content1['pre_repay_interest'])
        repay_data['repayFee'] = float(content1['pre_repay_fee'])
        repay_data['repayOverdueFee'] = float(content1['pre_repay_overdue_fee'])
        repay_data['repayCompoundInterest'] = float(content1['pre_repay_compound_interest'])
        # 按期还款/逾期还款
        if repay_type == "1" or repay_type == "4":
            repay_data['repayAmount'] = float(content1['pre_repay_amount'])
            repay_data['repayPrincipal'] = float(content1['pre_repay_principal'])

        # 提前结清
        elif repay_type == "2":
            pre_repay_date = str(content1["start_date"])
            pre_repay_date = datetime.strptime(pre_repay_date, "%Y-%m-%d").date()
            repay_date = datetime.strptime(repay_date, "%Y-%m-%d").date()
            if pre_repay_date > repay_date:
                repay_data["repay_interest"] = 0  # 如果还款时间小于账单日，利息应该为0
            else:
                # 计算提前结清利息:按期收利息
                repay_data['repayInterest'] = float(content1['pre_repay_interest'])
                repay_data['repayPrincipal'] = float(content1['before_calc_principal'])  # 还款总本金
                repay_data['repayAmount'] = repay_data['repayPrincipal'] + repay_data["repayInterest"]  # 总金额

        # 更新 payload 字段值
        repay_data.update(**kwargs)
        parser = DataUpdate(self.cfg['repay']['payload'], **repay_data)
        self.active_payload = parser.parser

        self.log.demsg('发起还款申请...')
        url = self.host + self.cfg['repay']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def wld_file_upload(self, remote, local):
        """
        我来贷渠道上传文件
        :param remote: 渠道上传路径，不包含根目录（/xdgl/hj/wld），例如/credit
        :param local: 本地文件路径+文件名，例如C:\\Users\\jccfc\\Desktop\\aaa.jpg
        :return:
        """
        upload_data = dict()
        filename = os.path.basename(local)
        content = self.Files.file_to_base64(local)
        # header
        upload_data['requestSerialNo'] = 'SerialNo' + self.strings + "2"

        # body
        upload_data['seqNo'] = self.strings
        upload_data['path'] = remote
        upload_data['fileName'] = filename
        upload_data['content'] = content

        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['wld_file_upload']['payload'], **upload_data)
        self.active_payload = parser.parser

        self.log.demsg('我来贷开始上传文件...')
        url = self.host + self.cfg['wld_file_upload']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def wld_file_download(self, remote, local):
        """
        我来贷渠道下载文件
        :param remote: 需要下载的文件服务器目录+文件名，不包含根目录（/xdgl/hj/wld），例如/credit/aaa.jpg
        :param local: 下载到本地文件路径+文件名，例如C:\\Users\\jccfc\\Desktop\\aaa.jpg
        :return:
        """
        download_data = dict()
        # header
        download_data['requestSerialNo'] = 'SerialNo' + self.strings + "2"

        # body
        download_data['seqNo'] = self.strings
        download_data['path'] = remote

        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['wld_file_download']['payload'], **download_data)
        self.active_payload = parser.parser

        self.log.demsg('我来贷开始下载文件...')
        url = self.host + self.cfg['wld_file_download']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        content = response['body']['content']
        self.Files.base64_to_file(content, local)
        return response

    def wld_file_upload_result(self, seqNo):
        """
        我来贷渠道上传文件结果查询
        :param seqNo: 渠道上传文件的seqNo
        :return:
        """
        result_data = dict()
        # header
        result_data['requestSerialNo'] = 'SerialNo' + self.strings + "2"

        # body
        result_data['seqNo'] = seqNo

        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['wld_file_upload_result']['payload'], **result_data)
        self.active_payload = parser.parser

        self.log.demsg('我来贷查询上传结果...')
        url = self.host + self.cfg['wld_file_upload_result']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response


if __name__ == '__main__':
    info = WldBizImpl()
