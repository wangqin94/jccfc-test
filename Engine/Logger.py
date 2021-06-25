# -*- coding: utf-8 -*-
# # -----------------------------------------
# # - Common log tools
# # -----------------------------------------

import os
import re
import sys
import time
import json
import logging
import paramiko
from pprint import pprint
from functools import wraps
from inspect import getcallargs
from datetime import date, timedelta
import requests
import pymysql


_project_path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]   # 项目根目录
__all__ = ['Logs', 'os', 're', 'time', 'paramiko',
           'json', 'wraps', 'getcallargs', 'requests',
           'date', 'timedelta', 'pymysql', 'pprint',
           ]

# # -----------------------------------------
# # - Font color style
# # -----------------------------------------

# color number
COLOR_RESET = 0
BLACK = 30
RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
PURPLE = 35
DARK_GREEN = 36
WHITE = 37

# Background color number
BGD_RESET = 0
BGD_BLACK = 40
BGD_CRIMSON = 41
BGD_GREEN = 42
BGD_YELLOW = 43
BGD_BLUE = 44
BGD_PURPLE = 45
BGD_DARK_GREEN = 46
BGD_WHITE = 47

# other style
Underline = 4           # 下划线
thickUnderline = 21     # 粗下划线
strikethrough = 9       # 中划线
ForeWhite = 7           # 前背景白色
BrightLight = 1         # 明亮色


class Logs(object):

    __INSTANCE = None
    __slots__ = ('__logger',)
    __STREAM_H = logging.StreamHandler()
    __STREAM_H.setLevel(logging.DEBUG)

    # # TODO: Limit to instance amount only one
    def __new__(cls, *args, **kwargs):
        if not cls.__INSTANCE:
            cls.__INSTANCE = super().__new__(cls, *args, **kwargs)
        return cls.__INSTANCE

    def __init__(self):
        logger = logging.getLogger()
        if not logger.handlers:
            """ # Logger object init level """
            logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%F %T")

            """ # File handler init """
            dir_name, log_file = os.path.split(os.path.realpath(sys.argv[0]))
            if re.search(r'Scripts$', dir_name):
                strings = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
                _log_file = _project_path + '/LogFile/' + os.path.splitext(log_file)[0] + '_' + strings + '.log'
                if not os.path.exists(_project_path + '/LogFile/'):
                    os.makedirs(_project_path + '/LogFile/')
                file_hdr = logging.FileHandler(_log_file, encoding='utf-8')
                file_hdr.setFormatter(formatter)
                logger.addHandler(file_hdr)
            self.__logger = logger

    def __log_style(self, color=37, bgd=1):
        """ # # console log display sample
        :param color:   recv a number of color
        :param bgd:     recv a number of background
        :return:        stream handler of updated formatter
        """

        fmt = '[%(asctime)s] [%(levelname)s] \033[{};{}m%(message)s\033[0m'.format(bgd, color)
        formatter = logging.Formatter(fmt, '%F %T')
        self.__STREAM_H.setFormatter(formatter)
        self.__logger.addHandler(self.__STREAM_H)

    def _log_style_reset(self):
        fmt = "[%(asctime)s] [%(levelname)s] %(message)s"
        formatter = logging.Formatter(fmt, '%F %T')
        self.__STREAM_H.setFormatter(formatter)
        self.__logger.addHandler(self.__STREAM_H)

    """ # The functions of log level """
    def debug(self, msg, *args, **kwargs):
        self.__log_style(color=WHITE, bgd=BGD_RESET)
        self.__logger.debug(msg, *args, **kwargs)
        self._log_style_reset()

    def info(self, msg, *args, **kwargs):
        self.__log_style(color=1)
        self.__logger.info(msg, *args, **kwargs)
        self._log_style_reset()

    def demsg(self, msg, *args, **kwargs):
        self.__log_style(color=DARK_GREEN, bgd=1)
        self.__logger.info(msg, *args, **kwargs)
        self._log_style_reset()

    def warning(self, msg, *args, **kwargs):
        self.__log_style(color=YELLOW)
        self.__logger.warning(msg, *args, **kwargs)
        self._log_style_reset()

    def error(self, msg, *args, **kwargs):
        self.__log_style(color=RED, bgd=Underline)
        self.__logger.error(msg, *args, **kwargs)
        self._log_style_reset()

    def fatal(self, msg, *args, **kwargs):
        self.__log_style(color=RED, bgd=strikethrough)
        self.__logger.critical(msg, *args, **kwargs)
        self._log_style_reset()


if __name__ == "__main__":
    t = Logs()
    print(id(t))
    print(id(Logs()))
    t.debug('debug msg')
    t.info('info msg')
    t.warning('warning msg')
    t.error('error msg')
    t.fatal('fatal')
    t.demsg('demsg')
