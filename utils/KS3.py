# -*- coding: utf-8 -*-
# -----------------------------------------------------
# KS3工具类
# -----------------------------------------------------
import socket

from ks3.connection import Connection
from utils.Logger import *
from utils.ReadConfig import *
from config.TestEnvInfo import TEST_ENV_INFO

_log = MyLog.get_log()
__all__ = ['KS3']
_readconfig = Config()


class KS3(object):
    def __init__(self):
        self.env = TEST_ENV_INFO
        self.ak = _readconfig.get_ks3('ak')
        self.sk = _readconfig.get_ks3('sk')
        self.bucket_name = json.loads(_readconfig.get_ks3('bucket_name'))[self.env]
        self.host = _readconfig.get_ks3('host')

    def __connection(self):
        """
        连接金山云
        :return:
        """
        conn = Connection(self.ak, self.sk, host=self.host)
        self.bucket = conn.get_bucket(self.bucket_name)

    def upload_file(self, local, remote):
        """
        金山云上传文件
        :param local: 本地文件路径
        :param remote: 远程文件路径，相对路径，如xdgl/test/img.png
        :return:
        """
        self.__connection()
        try:
            key = self.bucket.new_key(remote)
            ret = key.set_contents_from_filename(local)
            if ret and ret.status == 200:
                _log.info("上传成功")
            else:
                _log.info(ret)
        except Exception as e:
            print("上传失败, Error: %s  " % e)


if __name__ == '__main__':
    loacl = "D:\\jccfc-test\\utils\\img.png"
    remote = "xdgl/test/img.png"
    m = KS3()
    m.upload_file(loacl, remote)