# -*- coding: utf-8 -*-
# -----------------------------------------------------
# SFTP工具类
# -----------------------------------------------------

from Engine.Logger import *

_log = Logs()
__all__ = ['SFTP']


class SFTP(object):
    def __init__(self, host, username, password, port):
        self.sftp_host = host
        self.sftp_user = username
        self.sftp_passwd = password
        self.sftp_port = port
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
        :param local:       local file
        :param remote:      remote server directory
        :param clean:       only save local file for remote directory
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

    def upload_dir(self, local_dir, remote_dir, clean=True):
        """ # upload directory named ``local_dir`` to server directory of ``remote_dir``
        :param local_dir:       local directory
        :param remote_dir:      remote server directory for save local directory
        :param clean:           None
        :return:                the result messages of upload directory
        """
        all_files = self._get_all_files_in_local_dir(local_dir)
        path_record = []
        for file in all_files:
            remote_filename = os.path.join(remote_dir, file)
            remote_filename = remote_filename.replace('\\', '/').replace('\\\\', '/').replace('..', '.').replace('/./', '/')
            remote_path, filenme = os.path.split(remote_filename)
            # 服务器上创建对应目录
            if remote_path not in path_record:
                path_record.append(remote_path)
                self.recs_mkdir(remote_path)
            # 开始上传文件
            try:
                print(file, '->', remote_filename)
                self.sftp.put(file, remote_filename)
            except Exception as err:
                _log.error('upload file %s failed! %s', file, err)

    def download_file(self, local, remote):
        """ # download file named ``remote`` from server to save as ``local``
        :param local:       file's name after downloaded
        :param remote:      file's name in server
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
        # Check is a directory or not
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
        all_files = list()
        for root, dirs, files in os.walk(local_dir, topdown=True):
            for file in files:
                filename = os.path.join(root, file)
                all_files.append(filename.replace('\\', '/'))
        return all_files

    def recs_mkdir(self, dirs):
        res_dir = '/' if dirs[0] == '/' else './'
        path_list = dirs.split('/')
        for path in path_list:
            if path and path != '.':
                res_dir = os.path.join(res_dir, path).replace('\\', '/')
                try:
                    self.sftp.listdir(res_dir)
                except Exception as err:
                    print(err, ', mkdir %s' % res_dir)
                    self.sftp.mkdir(res_dir)

    def sftp_upload(self, local, remote):
        try:
            if os.path.isdir(local):  # 判断本地参数是目录还是文件
                for f in os.listdir(local):  # 遍历本地目录
                    self.sftp.put(os.path.join(local + f), os.path.join(remote + f))  # 上传目录中的文件
            else:
                self.sftp.put(local, remote)  # 上传文件
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
    pass
