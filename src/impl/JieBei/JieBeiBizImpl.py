from engine.EnvInit import EnvInit
from src.enums.EnumJieBei import JieBeiEnum
from src.enums.EnumsCommon import *
from src.impl.common.CommonBizImpl import post_with_encrypt
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from src.test_data.module_data import jiebei
from utils.Models import *


class JieBeiBizImpl(EnvInit):
    def __init__(self, *, data=None, encrypt_flag=False, person=True):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()
        # 解析项目特性配置
        self.cfg = jiebei.jiebei

        self.data = self.get_user_info(data=data, person=person)
        self.encrypt_flag = encrypt_flag
        self.strings = str(int(round(time.time() * 1000)))

        self.encrypt_url = self.host + JieBeiEnum.JieBeiEncryptPath.value
        self.decrypt_url = self.host + JieBeiEnum.JieBeiDecryptPath.value

        # 初始化payload变量
        self.active_payload = {}

    def get_user_info(self, data=None, person=True):
        # 获取四要素信息
        if data:
            base_data = data
        else:
            if person:
                base_data = get_base_data(str(self.env) + ' -> ' + str(ProductEnum.JIEBEI.value), "applyno")
            else:
                base_data = get_base_data_temp()
        return base_data

    def feature(self, bizActionType, **kwargs):
        feature_data = dict()

        if bizActionType == 'LOAN_DECISION':
            feature_data['userName'] = self.data['name']
            feature_data['certNo'] = self.data['cer_no']
            feature_data['bizActionType'] = 'LOAN_DECISION'
            feature_data['creditNo'] = self.data['applyno']
            feature_data['applyNo'] = "loanNo" + str(int(round(time.time() * 1000)))
        else:
            feature_data['applyNo'] = self.data['applyno']

        # 更新 payload 字段值
        feature_data.update(kwargs)
        parser = DataUpdate(self.cfg['feature']['payload'], **feature_data)
        self.active_payload = parser.parser

        self.log.demsg('特征取数接口...')
        url = self.host + self.cfg['feature']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def datapreCs(self, **kwargs):
        datapreCs_data = dict()

        datapreCs_data['name'] = self.data['name']
        datapreCs_data['certNo'] = self.data['cer_no']
        datapreCs_data['mobileNo'] = self.data['telephone']
        datapreCs_data['applyNo'] = self.data['applyno']

        # 更新 payload 字段值
        datapreCs_data.update(kwargs)
        parser = DataUpdate(self.cfg['datapreCs']['payload'], **datapreCs_data)
        self.active_payload = parser.parser

        self.log.demsg('初审接口...')
        url = self.host + self.cfg['datapreCs']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def datapreFs(self, applyType, creditAmt='2000000', creditRate='0.00060', applyNo=None, **kwargs):
        datapreFs_data = dict()
        #
        datapreFs_data['name'] = self.data['name']
        datapreFs_data['certNo'] = self.data['cer_no']
        datapreFs_data['mobileNo'] = self.data['telephone']
        datapreFs_data['cardNo'] = self.data['bankid']
        datapreFs_data['applyType'] = applyType
        datapreFs_data['suggestAmtMax'] = creditAmt
        datapreFs_data['suggestAmtMin'] = creditAmt
        datapreFs_data['suggestRateMax'] = creditRate
        datapreFs_data['suggestRateMax'] = creditRate

        if applyType == 'ADJUST_AMT_APPLY' or applyType == 'DECREASE_AMT_APPLY':
            datapreFs_data['applyNo'] = applyNo if applyNo else "amtNo" + str(int(round(time.time() * 1000)))
        else:
            datapreFs_data['applyNo'] = self.data['applyno']

        datapreFs_data['creditNo'] = self.data['applyno']

        # 更新 payload 字段值
        datapreFs_data.update(kwargs)
        parser = DataUpdate(self.cfg['datapreFs']['payload'], **datapreFs_data)
        self.active_payload = parser.parser

        self.log.demsg('复审接口...')
        url = self.host + self.cfg['datapreFs']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def creditNotice(self, bizType, applyNo=None, **kwargs):
        creditNotice_data = dict()

        creditNotice_data['name'] = self.data['name']
        creditNotice_data['certNo'] = self.data['cer_no']
        creditNotice_data['mobile'] = self.data['telephone']
        creditNotice_data['timestamp'] = int(time.time() * 1000)
        creditNotice_data['bizType'] = bizType
        creditNotice_data['applyNo'] = applyNo if applyNo else self.data['applyno']

        # 更新 payload 字段值
        creditNotice_data.update(kwargs)
        parser = DataUpdate(self.cfg['creditNotice']['payload'], **creditNotice_data)
        self.active_payload = parser.parser

        self.log.demsg('授信通知接口...')
        url = self.host + self.cfg['creditNotice']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def pdf_to_base64(self, pdf_path):
        with open(pdf_path, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read()).decode('utf-8')
        return encoded_string

