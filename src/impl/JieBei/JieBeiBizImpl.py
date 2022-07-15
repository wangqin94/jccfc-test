from engine.EnvInit import EnvInit
from src.enums.EnumJieBei import JieBeiEnum
from src.impl.common.CommonBizImpl import post_with_encrypt
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from src.test_data.module_data import jiebei
from utils.Models import *
from src.enums.EnumsCommon import *


class JieBeiBizImpl(EnvInit):
    def __init__(self, *, data=None, encrypt_flag=False):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()
        # 解析项目特性配置
        self.cfg = jiebei.jiebei

        self.data = data if data else get_base_data(str(self.env) + ' -> ' + str(ProductEnum.JIEBEI.value), "applyid")

        self.encrypt_flag = encrypt_flag
        self.strings = str(int(round(time.time() * 1000)))

        self.encrypt_url = self.encrypt_url = self.host + JieBeiEnum.JieBeiEncryptPath.value
        self.decrypt_url = self.host + JieBeiEnum.JieBeiDecryptPath.value

        # 初始化payload变量
        self.active_payload = {}

    def feature(self, **kwargs):
        feature_data = dict()
        # 更新 payload 字段值
        feature_data.update(kwargs)
        self.log.demsg('当前测试环境11111: {}'.format(feature_data))
        parser = DataUpdate(self.cfg['feature']['payload'], **feature_data)
        self.active_payload = parser.parser

        self.log.demsg('特征取数接口...')
        url = self.host + self.cfg['feature']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def datapreCs(self, **kwargs):
        datapreCs_data = dict()

        # 更新 payload 字段值
        datapreCs_data.update(kwargs)
        parser = DataUpdate(self.cfg['datapreCs']['payload'], **datapreCs_data)
        self.active_payload = parser.parser

        self.log.demsg('初审接口...')
        url = self.host + self.cfg['datapreCs']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def datapreFs(self, **kwargs):
        datapreFs_data = dict()

        # 更新 payload 字段值
        datapreFs_data.update(kwargs)
        parser = DataUpdate(self.cfg['datapreFs']['payload'], **datapreFs_data)
        self.active_payload = parser.parser

        self.log.demsg('复审接口...')
        url = self.host + self.cfg['datapreFs']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response

    def creditNotice(self, **kwargs):
        creditNotice_data = dict()

        # 更新 payload 字段值
        creditNotice_data.update(kwargs)
        parser = DataUpdate(self.cfg['creditNotice']['payload'], **creditNotice_data)
        self.active_payload = parser.parser

        self.log.demsg('授信通知接口...')
        url = self.host + self.cfg['creditNotice']['interface']
        response = post_with_encrypt(url, self.active_payload, self.encrypt_url, self.decrypt_url,
                                     encrypt_flag=self.encrypt_flag)
        return response