# -*- coding: utf-8 -*-
# -----------------------------------------------------
# KS3工具类
# -----------------------------------------------------

from ks3.connection import Connection
from utils.ReadConfig import *
from utils.FileHandle import *
from utils.Apollo import *

_log = MyLog.get_log()
__all__ = ['KS3']
_readconfig = Config()


class KS3(object):
    def __init__(self):
        self.env = TEST_ENV_INFO
        self.bucket_name = json.loads(_readconfig.get_ks3('bucket_name'))[self.env]
        self.host = _readconfig.get_ks3('host')
        if 'h' in self.bucket_name:
            self.ak = _readconfig.get_ks3('ak')
            self.sk = _readconfig.get_ks3('sk')
        else:
            self.ak = _readconfig.get_ks3('ak1')
            self.sk = _readconfig.get_ks3('sk1')
        flag = self.gfsflag = Apollo().get_config(key='ks3.gfs.flag', appId='loan2.1-public', namespace='JCXF.system')
        self.gfsflag = flag if flag else "ks3"
        self.file = Files()
        self.host_op_channel = API['op-channel_host'].format(self.env)

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
        try:
            flag = self.gfsflag['value']
        except Exception as e:
            print("ks3.gfs.flag未配置: %s" % e)
            flag = None
        if flag == 'gfs':
            remote1 = remote[4:]
            self.file.gfs_upload_file(self.host_op_channel, local, remote1)
        else:
            self.__connection()
            try:
                key = self.bucket.new_key(remote)
                ret = key.set_contents_from_filename(local)
                if ret and ret.status == 200:
                    _log.demsg("ks3文件上传成功")
                else:
                    _log.info(ret)
            except Exception as e:
                print("上传失败, Error: %s  " % e)


if __name__ == '__main__':
    loacl = "D:\\jccfc-test\\utils\\img.png"
    remote = "xdgl/test/img.png"
    m = KS3()
    m.upload_file(loacl, remote)
