# -*- coding: utf-8 -*-
"""
自动安装Python接口自动化厕所框架所需要的库
"""
import os

if __name__ == '__main__':
    installFile = os.path.join(os.path.dirname(__file__), 'package')
    os.system('pip install -r ' + installFile)
