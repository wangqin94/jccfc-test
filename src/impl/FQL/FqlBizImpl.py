# -*- coding: utf-8 -*-
# ------------------------------------------
# 分期乐接口数据封装类
# ------------------------------------------

from engine.EnvInit import EnvInit
from utils import GlobalVar as gl
from src.impl.common.CommonBizImpl import *
from src.enums.EnumsCommon import *
from src.enums.EnumFql import *
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils.Models import *
from src.test_data.module_data import fql
from utils.FileHandle import *


class FqlBizImpl(EnvInit):
    def __init__(self, *, data=None, encrypt_flag=True, person=True):
        super().__init__()

        # 解析项目特性配置
        self.cfg = fql.fql
        # self.MysqlBizImpl = MysqlBizImpl()
        self.Files = Files()
        self.data = self.get_user_info(data=data, person=person)

        # 设置全局变量
        gl._init()
        # self.log.info('用户四要素信息-全局变量: {}'.format(gl))
        gl.set_value('personData', self.data)
        # print ('\n'.join(['%s:%s' % item for item in gl.__dict__.items()]))

        self.encrypt_flag = encrypt_flag
        self.strings = str(int(round(time.time() * 1000)))
        self.times = time.strftime('%Y-%m-%d', time.localtime())

        self.sourceCode = '000UC010000006268'
        self.encrypt_url = API['request_host_api'].format(self.env) + FqlPathEnum.fqlEncryptPath.value
        self.decrypt_url = API['request_host_api'].format(self.env) + FqlPathEnum.fqlDecryptPath.value

        # 初始化payload变量
        self.active_payload = {}

    def get_user_info(self, data=None, person=True):
        # 获取四要素信息
        if data:
            base_data = data
        else:
            if person:
                base_data = data if data else get_base_data(str(self.env) + ' -> ' + str(ProductEnum.FQL.value), 'applyId')
            else:
                base_data = get_base_data_temp('applyId')
        return base_data

    def set_active_payload(self, payload):
        self.active_payload = payload

    @staticmethod
    def url_encoded_to_json(response):
        data = dict()
        data["content"] = response.split('content=')[1].split('&sign=')[0]
        data["sign"] = response.split('&sign=')[1]
        return data

    # 授信申请payload
    def credit(self, **kwargs):
        credit_data = dict()

        # head
        credit_data['requestSerialNo'] = 'SerialNo' + self.strings + "1"
        credit_data['requestTime'] = self.strings
        credit_data['empNo'] = 'empNo' + self.strings
        credit_data['merchantId'] = self.sourceCode
        credit_data['managerId'] = self.sourceCode
        # body
        credit_data['applyId'] = self.data['applyId']
        credit_data['sourceCode'] = self.sourceCode
        credit_data['firstOrderDate'] = time.strftime('%Y-%m-%d', time.localtime())

        credit_data['idNo'] = self.data['cer_no']
        credit_data['userBankCardNo'] = self.data['bankid']
        credit_data['name'] = self.data['name']
        credit_data['mobileNo'] = self.data['telephone']

        # 更新 payload 字段值
        credit_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit']['payload'], **credit_data)
        self.active_payload = parser.parser

        gl.set_value('creditRequestData', self.active_payload)
        self.log.info('授信请求信息-全局变量: {}'.format(gl))
        print('\n'.join(['%s:%s' % item for item in gl.__dict__.items()]))

        # 校验用户是否在系统中已存在
        # self.MysqlBizImpl.check_user_available(self.data)

        self.log.demsg('开始授信申请...')
        url = self.host_api + self.cfg['credit']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        response['applyId'] = self.data['applyId']
        return response

    # 授信查询payload
    def credit_query(self, **kwargs):
        credit_data = dict()
        # header
        credit_data['requestSerialNo'] = 'SerialNo' + self.strings + "2"

        # body
        credit_data['applyId'] = self.data['applyId']
        credit_data['sourceCode'] = self.sourceCode

        # 更新 payload 字段值
        credit_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit_query']['payload'], **credit_data)
        self.active_payload = parser.parser

        self.log.demsg('开始授信查询...')
        url = self.host_api + self.cfg['credit_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 支用申请payload
    def loan(self, loanTerm='3', **kwargs):
        """ # 支用申请payload字段装填
        注意：键名必须与接口原始数据的键名一致
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: response 接口响应参数 数据类型：json response 接口响应参数 数据类型：json
        """
        loan_data = dict()
        # head
        loan_data['requestSerialNo'] = 'SerialNo' + self.strings + '3'
        loan_data['requestTime'] = self.strings
        loan_data['empNo'] = 'empNo' + self.strings
        loan_data['merchantId'] = self.sourceCode
        loan_data['managerId'] = self.sourceCode

        # body
        loan_data['applyId'] = self.data['applyId']
        loan_data['sourceCode'] = self.sourceCode
        loan_data['name'] = self.data['name']
        loan_data['mobileNo'] = self.data['telephone']
        loan_data['debitAccountNo'] = self.data['bankid']
        loan_data['loanTerm'] = loanTerm

        date = self.times.split()[0]
        firstRepayDate, day = loan_and_period_date_parser(date_str=date, period=int(loanTerm), flag=False,
                                                          max_bill=28)
        loan_data['firstRepayDate'] = firstRepayDate[0]
        loan_data['fixedRepayDay'] = day
        loan_data['mobileNo'] = self.data['telephone']

        # 更新 payload 字段值
        loan_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan']['payload'], **loan_data)
        self.active_payload = parser.parser

        gl.set_value('loanRequestData', self.active_payload)
        self.log.info('支用请求信息-全局变量: {}'.format(gl))
        print('\n'.join(['%s:%s' % item for item in gl.__dict__.items()]))

        self.log.demsg('开始支用申请...')
        url = self.host_api + self.cfg['loan']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        response['applyId'] = self.data['applyId']
        return response

    # 支用查询
    def loan_query(self, **kwargs):
        loan_data = dict()
        # header
        loan_data['requestSerialNo'] = 'SerialNo' + self.strings + "2"

        # body
        loan_data['applyId'] = self.data['applyId']
        loan_data['sourceCode'] = self.sourceCode

        # 更新 payload 字段值
        loan_data.update(kwargs)
        parser = DataUpdate(self.cfg['loan_query']['payload'], **loan_data)
        self.active_payload = parser.parser

        self.log.demsg('开始支用查询...')
        url = self.host_api + self.cfg['loan_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 支用查询payload
    def loan_repay_notice(self, **kwargs):
        loan_data = dict()
        # head
        loan_data['requestSerialNo'] = 'SerialNo' + self.strings + "2"

        # body
        loan_data['applyId'] = self.data['applyId']
        loan_data['sourceCode'] = self.sourceCode

        # 更新 payload 字段值
        loan_data.update(kwargs)
        parser = DataUpdate(self.cfg['credit_query']['payload'], **loan_data)
        self.active_payload = parser.parser
        url = self.host + self.cfg['loan_repay_notice']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def fql_file_upload(self, remote, local):
        """
        分期乐渠道上传文件
        :param remote: 渠道上传路径，不包含根目录（/xdgl/fql），例如/pl
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
        parser = DataUpdate(self.cfg['fql_file_upload']['payload'], **upload_data)
        self.active_payload = parser.parser

        self.log.demsg('分期乐开始上传文件...')
        url = self.host_api + self.cfg['fql_file_upload']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def fql_file_download(self, remote, local):
        """
        分期乐渠道下载文件
        :param remote: 需要下载的文件服务器目录+文件名，不包含根目录（/xdgl/fql），例如/pl/aaa.jpg
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
        parser = DataUpdate(self.cfg['fql_file_download']['payload'], **download_data)
        self.active_payload = parser.parser

        self.log.demsg('分期乐开始下载文件...')
        url = self.host_api + self.cfg['fql_file_download']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        content = response['content']
        self.Files.base64_to_file(content, local)
        return response

    def fql_file_upload_result(self, seqNo):
        """
        分期乐渠道上传文件结果查询
        :param seqNo: 渠道上传文件的seqNo
        :return:
        """
        result_data = dict()
        # header
        result_data['requestSerialNo'] = 'SerialNo' + self.strings + "2"

        # body
        result_data['seqNo'] = seqNo

        # 更新 payload 字段值
        parser = DataUpdate(self.cfg['fql_file_upload_result']['payload'], **result_data)
        self.active_payload = parser.parser

        self.log.demsg('分期乐查询上传结果...')
        url = self.host_api + self.cfg['fql_file_upload_result']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 还款试算
    def repay_trial(self, loanno, loanterm, repaytype, rpyDate, **kwargs):
        repay_trial_data = dict()
        # head
        # repay_trial_data['requestTime'] = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        repay_trial_data['requestSerialNo'] = self.strings + "4"

        # body
        repay_trial_data['capitalLoanNo'] = loanno
        # repay_trial_data['repayDate'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        repay_trial_data['loanTerm'] = loanterm
        repay_trial_data['repayType'] = repaytype
        repay_trial_data['rpyDate'] = rpyDate

        # 更新 payload 字段值
        repay_trial_data.update(kwargs)
        parser = DataUpdate(self.cfg['repay_trial']['payload'], **repay_trial_data)
        self.active_payload = parser.parser
        url = self.host_api + self.cfg['repay_trial']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 代扣申请
    def payment(self, withholdAmt, signNum, capitalLoanNo, rpyTerm, rpyPrincipal, rpyFeeAmt, rpyMuclt, rpyType,
                rpyDate, **kwargs):
        payment_data = dict()

        # Head
        payment_data['requestTime'] = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        payment_data['requestSerialNo'] = self.strings + "4"

        # body
        payment_data['withholdSerialNo'] = "wsn" + self.strings
        payment_data['withholdAmt'] = withholdAmt

        # bindardinfo
        payment_data['userName'] = self.data['name']
        payment_data['phoneNo'] = self.data['telephone']
        payment_data['cardNo'] = self.data['bankid']
        payment_data['idNo'] = self.data['cer_no']

        payment_data['signNum'] = signNum
        payment_data['assetId'] = self.data['applyId']
        payment_data['capitalLoanNo'] = capitalLoanNo

        payment_data['rpyTerm'] = rpyTerm

        # sepOutInfo
        payment_data['amt'] = withholdAmt
        payment_data['rpyTotalAmt'] = withholdAmt
        payment_data['rpyAmt'] = withholdAmt

        payment_data['account'] = self.data['bankid']
        #
        payment_data['rpyPrincipal'] = rpyPrincipal
        payment_data['rpyFeeAmt'] = rpyFeeAmt
        payment_data['rpyMuclt'] = rpyMuclt
        payment_data['rpyType'] = rpyType
        payment_data['rpyDate'] = rpyDate
        # payment_data['rpyDate'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))

        # 更新 payload 字段值
        payment_data.update(kwargs)
        parser = DataUpdate(self.cfg['payment']['payload'], **payment_data)
        self.active_payload = parser.parser
        url = self.host_api + self.cfg['payment']['interface']
        print(url)
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 代扣查询
    def payment_query(self, withholadSerialNo, **kwargs):
        payment_query = dict()
        # head
        payment_query['requestSerialNo'] = 'SerialNo' + self.strings + "2"
        payment_query['withholdSerialNo'] = withholadSerialNo

        # 更新 payload 字段值
        payment_query.update(kwargs)
        parser = DataUpdate(self.cfg['payment_query']['payload'], **payment_query)
        self.active_payload = parser.parser
        url = self.host_api + self.cfg['payment_query']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    # 还款计划查询
    def repay_play_query(self, capitalLoanNo, **kwargs):
        repay_play_query = dict()
        # head
        repay_play_query['requestTime'] = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        repay_play_query['requestSerialNo'] = self.strings + "3"

        # body
        repay_play_query['capitalLoanNo'] = capitalLoanNo

        # 更新 payload 字段值
        repay_play_query.update(kwargs)
        parser = DataUpdate(self.cfg['repay_play_query']['payload'], **repay_play_query)
        self.active_payload = parser.parser
        url = self.host_api + self.cfg['repay_play_query']['interface']
        print(url)
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response


if __name__ == '__main__':
    info = FqlBizImpl()
