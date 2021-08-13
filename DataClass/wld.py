# -*- coding: utf-8 -*-
# ------------------------------------------
# 我来贷接口数据封装类
# ------------------------------------------
import json
import time

from Config.global_config import *
from Engine.Base import INIT
from Component.wld import *
from Config.TestEnvInfo import *
from ComLib.Models import *


class PayloadGenerator(INIT):
    def __init__(self, *, data=None, repay_term_no='1', repay_type="1", loan_invoice_id=""):
        super().__init__()
        self.data = data if data else get_base_data(str(self.env) + ' -> ' + str(self.project), "applyid")
        self.log.info('用户四要素信息 \n%s', self.data)

        self.strings = str(int(round(time.time() * 1000)))
        self.times = time.strftime('%Y-%m-%d', time.localtime())
        self.repay_term_no = repay_term_no
        self.repay_type = repay_type
        self.loan_invoice_id = loan_invoice_id

        self.encrypt_url = self.host + "/api/v1/secret/thirdEncryptData/WLD"
        self.decrypt_url = self.host + "/api/v1/secret/thirdDecryptData/WLD"

        # 初始化payload变量
        self.active_payload = {}


    def set_active_payload(self, payload):
        self.active_payload = payload

    def encrypt(self, encrypt_payload):
        print("\n开始加密")
        response = requests.post(url=self.encrypt_url, headers=headers, json=encrypt_payload)
        print("加密status_code:", response.status_code)
        res = response.json()
        res = str(res).replace("'", '''"''').replace(" ", "")
        print(f"加密响应报文如下：\n{res}")
        return json.loads(res)

    def decrypt(self, decrypt_payload):
        print("\n开始解密")
        decrypt_payload = json.dumps(decrypt_payload)
        response = requests.post(url=self.decrypt_url, headers=headers, data=decrypt_payload)
        print("解密status_code:", response.status_code)
        res = response.json()
        res = str(res).replace("'", '''"''').replace(" ", "")
        print(f"解密响应报文如下：\n{res}")
        return res

    @staticmethod
    def url_encoded_to_json(response):
        data = dict()
        data["content"] = response.split('content=')[1].split('&sign=')[0]
        data["sign"] = response.split('&sign=')[1]
        return data

    # 发起代扣签约payload
    def bind_card_msg(self, **kwargs):
        bind_card_data = dict()
        # head
        bind_card_data['requestSerialNo'] = 'SerialNo' + self.strings + "1"
        bind_card_data['requestTime'] = self.strings
        # body
        bind_card_data['payer'] = self.data['name']
        bind_card_data['payerIdNum'] = self.data['cer_no']
        bind_card_data['payerBankCardNum'] = self.data['bankid']
        bind_card_data['payerPhoneNum'] = self.data['telephone']

        bind_card_data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['bind_card']['payload'], **bind_card_data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 确认代扣签约payload
    def confirm_bind_card_msg(self, **kwargs):
        confirm_bind_card_data = dict()
        # head
        confirm_bind_card_data['requestSerialNo'] = 'SerialNo' + self.strings + "2"
        confirm_bind_card_data['requestTime'] = self.strings
        # body
        key = "id_card_no = '" + self.data['cer_no'] + "' order by create_time desc"
        content = self.get_credit_data_info(table="credit_bind_card_info", key=key)
        confirm_bind_card_data['tradeSerialNo'] = content['trade_serial_no']
        confirm_bind_card_data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['confirm_bind_card']['payload'], **confirm_bind_card_data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 代扣签约查询
    def query_bind_card_msg(self, **kwargs):
        query_bind_card_data = dict()
        # head
        query_bind_card_data['requestSerialNo'] = 'SerialNo' + self.strings + "3"
        query_bind_card_data['requestTime'] = self.strings
        # body
        key = "id_card_no = '" + self.data['cer_no'] + "' order by create_time desc"
        content = self.get_credit_data_info(table="credit_bind_card_info", key=key)
        query_bind_card_data['tradeSerialNo'] = content['trade_serial_no']
        query_bind_card_data['userId'] = content['user_id']
        query_bind_card_data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['query_bind_card']['payload'], **query_bind_card_data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 换卡通知
    def update_card_msg(self, **kwargs):
        update_card_data = dict()
        # head
        update_card_data['requestSerialNo'] = 'SerialNo' + self.strings + "4"
        update_card_data['requestTime'] = self.strings
        # body
        key = "certificate_no = '" + self.data['cer_no'] + "' order by create_time desc"
        content = self.get_credit_data_info(table="credit_loan_invoice", key=key)
        update_card_data['loanInvoiceId'] = content['loan_invoice_id']
        update_card_data['idNo'] = self.data['cer_no']
        res = requests.get('http://10.10.100.153:8081/getTestData')
        update_card_data['repaymentAccountNo'] = eval(res.text)["银行卡号"]
        update_card_data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['update_card']['payload'], **update_card_data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 授信申请
    def credit_msg(self, **kwargs):
        credit_data = dict()
        # head
        credit_data['requestSerialNo'] = 'SerialNo' + self.strings + "5"
        credit_data['requestTime'] = self.strings
        # body
        credit_data['thirdApplyId'] = self.data['applyid']
        credit_data['userBankCardNo'] = self.data['bankid']
        credit_data['reserveMobile'] = self.data['telephone']
        credit_data['name'] = self.data['name']
        credit_data['idNo'] = self.data['cer_no']
        credit_data['mobileNo'] = self.data['telephone']
        credit_data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['credit']['payload'], **credit_data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 授信申请查询
    def creditquery_msg(self, **kwargs):
        creditquery_data = dict()
        # head
        creditquery_data['requestSerialNo'] = 'SerialNo' + self.strings + "6"
        creditquery_data['requestTime'] = self.strings
        # body
        creditquery_data['thirdApplyId'] = self.data['applyid']
        creditquery_data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['credit_query']['payload'], **creditquery_data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 支用申请
    def loan_msg(self, **kwargs):
        loan_data = dict()
        # head
        loan_data['requestSerialNo'] = 'SerialNo' + self.strings + "7"
        loan_data['requestTime'] = self.strings
        # body
        loan_data['thirdApplyId'] = self.data['applyid']
        loan_data['accountNo'] = self.data['bankid']
        loan_data['mobileNo'] = self.data['telephone']
        loan_data['name'] = self.data['name']
        loan_data['idNo'] = self.data['cer_no']
        key = "thirdpart_apply_id = '" + self.data['applyid'] + "'"
        content = self.get_credit_data_info(table="credit_apply", key=key)
        loan_data['loanAmt'] = float(content['apply_amount'])
        loan_data['loanTerm'] = str(content['apply_term'])
        loan_data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['loan']['payload'], **loan_data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 支用查询
    def loanquery_msg(self, **kwargs):
        loanquery_data = dict()
        # head
        loanquery_data['requestSerialNo'] = 'SerialNo' + self.strings + "8"
        loanquery_data['requestTime'] = self.strings
        # body
        loanquery_data['thirdApplyId'] = self.data['applyid']
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['loan_query']['payload'], **loanquery_data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 还款计划查询
    def repay_plan_msg(self, **kwargs):
        repay_plan_data = dict()
        # head
        repay_plan_data['requestSerialNo'] = 'SerialNo' + self.strings + "9"
        repay_plan_data['requestTime'] = self.strings
        # body
        key = "certificate_no = '" + self.data['cer_no'] + "' order by create_time desc"
        content = self.get_credit_data_info(table="credit_loan_invoice", key=key)
        repay_plan_data['loanInvoiceId'] = content['loan_invoice_id']
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['repay_plan_query']['payload'], **repay_plan_data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)

    # 还款
    def repay_msg(self, **kwargs):
        repay_data = dict()
        # head
        repay_data['requestSerialNo'] = 'SerialNo' + self.strings + "10"
        repay_data['requestTime'] = self.strings
        # body
        repay_data['repayApplySerialNo'] = 'repay' + self.strings + "5"
        repay_data['repayType'] = self.repay_type
        repay_data['repayNum'] = self.repay_term_no
        repay_data['loanInvoiceId'] = self.loan_invoice_id
        key = "user_id in (select user_id from credit_loan_invoice where loan_invoice_id = '" \
              + self.loan_invoice_id + "')"
        content = self.get_credit_data_info(table="credit_bind_card_info", key=key)
        repay_data['repaymentAccountNo'] = content['bank_card_no']
        key1 = "loan_invoice_id = '" + self.loan_invoice_id + "' and current_num = '" + self.repay_term_no + "'"
        content1 = self.get_asset_data_info(table="asset_repay_plan", key=key1)
        print(content1)
        if self.repay_type == "1" or self.repay_type == "4":
            repay_data['repayAmount'] = float(content1['pre_repay_amount'])
            repay_data['repayPrincipal'] = float(content1['pre_repay_principal'])
        elif self.repay_type == "2":
            repay_data['repayAmount'] = float(content1['before_calc_principal']) + float(content1['pre_repay_interest'])
            repay_data['repayPrincipal'] = float(content1['before_calc_principal'])
        repay_data['repayInterest'] = float(content1['pre_repay_interest'])
        repay_data['repayFee'] = float(content1['pre_repay_fee'])
        repay_data['repayOverdueFee'] = float(content1['pre_repay_overdue_fee'])
        repay_data['repayCompoundInterest'] = float(content1['pre_repay_compound_interest'])

        repay_data.update(kwargs)
        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['repay']['payload'], **repay_data)
        self.active_payload = parser.parser
        self.log.info("payload数据: %s", self.active_payload)
        self.set_active_payload(self.active_payload)


if __name__ == '__main__':
    info = PayloadGenerator()
