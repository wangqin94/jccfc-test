# -*- coding: utf-8 -*-
# -----------------------------------------------------
# SFTP工具类
# -----------------------------------------------------
import time

import paramiko

from config.TestEnvInfo import TEST_ENV_INFO
from utils.Logger import *

_log = MyLog.get_log()
__all__ = ['SFTP']
_readconfig = Config()


class SFTP(object):
    def __init__(self):
        self.env = TEST_ENV_INFO
        self.sftp_host = _readconfig.get_sftp(self.env)['host']
        self.sftp_user = _readconfig.get_sftp(self.env)['name']
        self.sftp_passwd = _readconfig.get_sftp(self.env)['password']
        self.sftp_port = _readconfig.get_sftp(self.env)['port']
        self.sftp = self.__login_sftp()

    def __del__(self):
        try:
            self.sftp_close()
        except Exception as err:
            _log.error(err)

    def __login_sftp(self):
        sf = paramiko.Transport(*(self.sftp_host, self.sftp_port))
        sf.connect(username=self.sftp_user, password=self.sftp_passwd)
        return paramiko.SFTPClient.from_transport(sf)

    def sftp_close(self):
        self.sftp.close()

    def upload_file(self, local, remote, clean=True):
        """ # upload local file named ``local`` to server directory of ``remote``
        @param local:       local file
        @param remote:      remote server directory
        @param clean:       only save local file for remote directory true:备份上传， false：强制覆盖上传
        :return:            the result messages of upload file
        """
        self._check_remote_dir_exist(remote, clean=clean)
        if remote[-1] != '/':
            remote += '/'
        if os.path.isdir(local):
            _log.warning('Local src is not files type, please call function upload_dir')
            return
        try:
            filename = os.path.basename(local)
            self.sftp.put(local, os.path.join(remote + filename))
            _log.info('upload %s to server directory of %s success! ', local, remote)
        except Exception as err:
            _log.error('Upload file failed! %s', err)

    def upload_dir(self, local_dir, remote_dir, clean=False):
        """ 覆盖上传 # upload directory named ``local_dir`` to server directory of ``remote_dir``
        @param local_dir:       local directory
        @param remote_dir:      remote server directory for save local directory
        @param clean:           true:备份上传， false：强制覆盖上传
        :return:                the result messages of upload directory
        """
        all_files = self._get_all_files_in_local_dir(local_dir)
        for file in all_files:
            remote_filepath = os.path.join(remote_dir, file)
            remote_filepath = remote_filepath.replace('\\', '/').replace('\\\\', '/').replace('..', '.').replace('/./', '/')
            loacl_filepath = os.path.join(local_dir, file)
            self._check_remote_dir_exist(remote, clean=clean)
            # 开始上传文件
            try:
                self.sftp.put(loacl_filepath, remote_filepath)
                _log.info('upload %s to server directory of %s success! ', loacl_filepath, remote_filepath)
            except Exception as err:
                _log.error('upload file %s failed! %s', remote_filepath, err)

    def download_file(self, local, remote):
        """ # download file named ``remote`` from server to save as ``local``
        @param local:       file's name after downloaded
        @param remote:      file's name in server
        :return:            the result messages of download file
        """
        if os.path.isdir(local):
            _log.warning('Local src must be a file!')
            return
        if os.path.isdir(remote):
            _log.warning('Remote src must be a files type!')
            return
        try:
            self.sftp.get(remote, local)  # 开始下载服务上的文件
            _log.info('download %s save as %s success! ', remote, local)
        except Exception as err:
            _log.error('download failed! %s', err)

    def download_dir(self):
        pass

    def _check_remote_dir_exist(self, remote_dir, clean=False):
        """
        # Check is a directory or not
        @param remote_dir: 远端目录
        @param clean: true:备份上传， false：强制覆盖上传
        @return:
        """
        try:
            is_empty = self.sftp.listdir(remote_dir)
        except IOError as err:
            _log.warning('the directory of %s is not exist; %s!', remote_dir, err)
            _log.info('start to make dir for server...')
            self.sftp.mkdir(remote_dir)
        else:
            if is_empty and clean:
                backup = remote_dir + '_bak' + time.strftime('%Y%m%d%H%M%S')
                _log.warning('the directory of %s is not empty; to bakup the old files!', remote_dir)
                self.sftp.rename(remote_dir, backup)
                self.sftp.mkdir(remote_dir)

    @staticmethod
    def _get_all_files_in_local_dir(local_dir):
        """
        获取本地文件夹路径，遍历所有文件并返回本地文件名
        @param local_dir:
        @return: 返回文件名
        """
        for root, dirs, files in os.walk(local_dir, topdown=True):
            return files

    def recs_mkdir(self, dirs):
        res_dir = '/' if dirs[0] == '/' else './'
        path_list = dirs.split('/')
        for path in path_list:
            if path and path != '.':
                res_dir = os.path.join(res_dir, path).replace('\\', '/')
                try:
                    self.sftp.listdir(res_dir)
                except Exception as err:
                    _log.info("dir {} is not exit, {}".format(res_dir, err))
                    self.sftp.mkdir(res_dir)
                    _log.info("mkdir {} success".format(res_dir))

    def sftp_upload(self, local, remote, clean=False):
        """
        upload file or dir to sftp server
        @param local: 本地文件或者文件夹绝对路径
        @param remote: 远端文件或者文件夹绝对路径
        @param clean: true:备份上传， false：强制覆盖上传
        @return:
        """
        try:
            if os.path.isdir(local):  # 判断本地参数是目录还是文件
                self.upload_dir(local, remote)  # 上传目录
            else:
                self.upload_file(local, remote, clean=False)  # 上传文件
        except Exception as err:
            _log.error('upload exception: %s', err)

    def sftp_download(self, local, remote):
        try:
            if os.path.isdir(local):  # 判断本地参数是目录还是文件
                for f in self.sftp.listdir(remote):  # 遍历远程目录
                    self.sftp.get(os.path.join(remote + f), os.path.join(local + f))  # 下载目录中文件
            else:
                self.sftp.get(remote, local)  # 下载文件
        except Exception as err:
            _log.error('download exception: %s', err)


if __name__ == '__main__':
    remote = "/hj/xdgl/meituan/bank_loan_create/20210102/"
    local = "C:/Users/jccfc/Desktop/身份证/"
    SFTP().sftp_upload(local, remote)

