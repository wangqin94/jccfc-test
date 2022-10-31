# -*- coding: UTF-8 -*-
"""
@Project : PyCharm
@File : FileHandle.py 
@Author : wangpx
@Time : 2022/7/13 11:28 
"""
import base64
import requests
import time
import os
from config.globalConfig import *
from utils.Logger import MyLog
_log = MyLog.get_log()


class Files(object):
    """
    文件处理
    """

    def __init__(self):
        pass

    def file_to_base64(self, filepath):
        """
        文件转base64
        :param filepath: 文件路径
        :return: base64编码
        """
        with open(filepath, 'rb') as file:
            base64_str = base64.b64encode(file.read())
            src = base64_str.decode('utf-8')
        return src

    def base64_to_file(self, base64_str, filename):
        """
        base64转文件
        :param base64_str: base64编码
        :param filename: 路径及文件名+后缀
        :return:
        """
        file_data = base64.b64decode(base64_str)
        with open(filename, 'wb') as f:
            f.write(file_data)

    def gfs_upload_file(self, host, local, remote):
        """
        gfs上传文件
        :param host: globalConfig.py->API->op-channel_host
        :param local: 本地文件路径包含文件名，例如C:\\Users\\jccfc\\Desktop\\test\\idz-1.jpg
        :param remote: 远程文件路径，例如/hj/wld/credit/test（不包含根目录/xdgl）
        :return:
        """
        url = host + '/hsjry/op-channel/v1/file/upload'
        filename = os.path.basename(local)
        content = Files().file_to_base64(local)
        seqNo = str(int(time.time()*1000))
        data = {
            "seqNo": seqNo,
            "channelNo": "01",
            "applyPath": "/",
            "path": remote,
            "fileName": filename,
            "content": content
        }
        _log.info(f"上传文件请求数据：{data}")
        response = requests.post(url=url, headers=headers, json=data)
        response = response.json()
        _log.info(f"响应报文：{response}")
        Files().gfs_upload_result(host, seqNo)
        return seqNo

    def gfs_upload_result(self, host, seqNo):
        url = host + '/hsjry/op-channel/v1/file/upload/result'
        data = {
            "seqNo": seqNo,
            "channelNo": "01"
        }
        _log.info(f"上传文件结果查询请求数据：{data}")
        response = requests.post(url=url, headers=headers, json=data)
        response = response.json()
        _log.info(f"响应报文：{response}")

    def gfs_download_file(self, host, local_file, remote_file):
        url = host + '/hsjry/op-channel/v1/file/download'
        seqNo = str(int(time.time() * 1000))
        data = {
            "seqNo": seqNo,
            "channelNo": "01",
            "applyPath": "/",
            "fullPath": remote_file
        }
        _log.info(f"下载文件结果查询请求数据：{data}")
        response = requests.post(url=url, headers=headers, json=data)
        response = response.json()
        _log.info(f"响应报文：{response}")
        content = response['data']['content']
        Files().base64_to_file(content, local_file)


if __name__ == '__main__':
    a = Files()
    host = "http://op-channel-rts.corp.jccfc.com"
    local = "C:\\Users\\jccfc\\Desktop\\a.jpg"
    remote = "/xdgl/hj/zhixin/2022/08/12/F6629388810741ADA9D4B4FCBDB9AED40B10BFDA202741BBB1379FB41108BBA7.jpg"
    a.gfs_download_file(host, local, remote)
    # a.gfs_upload_file(host, local, remote)