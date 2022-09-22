# -*- coding: UTF-8 -*-
"""
@Project : PyCharm
@File : FileHandle.py 
@Author : wangpx
@Time : 2022/7/13 11:28 
"""
import base64


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
        :param filename: 文件名+后缀
        :return:
        """
        file_data = base64.b64decode(base64_str)
        with open(filename, 'wb') as f:
            f.write(file_data)


if __name__ == '__main__':
    f = Files()
    filepath = 'img.png'
    str = f.file_to_base64(filepath)
    print(str)
    f.base64_to_file(str)