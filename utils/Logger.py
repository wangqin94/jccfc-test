# -*- coding: utf-8 -*-
# # -----------------------------------------
# # - Common log tools
# # -----------------------------------------

import os
import logging
from logging.handlers import RotatingFileHandler
import threading
from datetime import datetime
import datetime as dt
import shutil

# # -----------------------------------------
# # - Font color style
# # -----------------------------------------

# color number
from utils.ReadConfig import Config

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
Underline = 4  # 下划线
thickUnderline = 21  # 粗下划线
strikethrough = 9  # 中划线
ForeWhite = 7  # 前背景白色
BrightLight = 1  # 明亮色

# 配置文件初始化
_config = Config()

# 初始化根路径
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

resultPath = os.path.join(project_dir, "results")  # 日志目录
log_file_name = _config.get_log('file_name') if _config.get_log('file_name') else 'output.log'  # 日志文件


def get_log_filepath():
    # 初始化日志目录，不存在则创建
    if not os.path.exists(resultPath):
        os.mkdir(resultPath)
    # 设置控制台日志目录
    listdir = [d for d in os.listdir(resultPath)]
    # 如果日志文件目录不存在则创建
    if listdir == []:
        logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M")))
        os.mkdir(logPath)
        listdir = [d for d in os.listdir(resultPath)]

    # 写入最近一次日志目录
    old_log_file_name = listdir[-1]
    new_log_file_name = str(datetime.now().strftime("%Y%m%d%H%M"))
    logPath = os.path.join(resultPath, old_log_file_name)

    # 如果历史日志目录超过过期时间写入新的日志目录
    file_failure = int(_config.get_log('file_failure'))
    if (int(new_log_file_name) - int(old_log_file_name)) > file_failure:
        logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M")))
        os.mkdir(logPath)
    return logPath


class Logs(object):
    # 控制台日志句柄初始化
    __INSTANCE = None
    __slots__ = ('__logger', 'logPath')
    console_handler = logging.StreamHandler()
    console_output_level = _config.get_log('console_level')
    console_handler.setLevel(console_output_level)

    # # TODO: Limit to instance amount only one
    def __new__(cls, *args, **kwargs):
        if not cls.__INSTANCE:
            cls.__INSTANCE = super().__new__(cls, *args, **kwargs)
        return cls.__INSTANCE

    def __init__(self):
        # 初始化
        logger = logging.getLogger()
        # 设置日志级别
        logger.setLevel(_config.get_log('file_level'))
        self.logPath = get_log_filepath()

        if not logger.handlers:  # 避免重复日志
            # 初始文件日志句柄
            # file_handler = logging.FileHandler(os.path.join(self.logPath, log_file_name))
            # 写入文件，如果文件超过100个Bytes，仅保留5个文件。
            file_handler = RotatingFileHandler(os.path.join(self.logPath, log_file_name), maxBytes=100*1024, backupCount=3)
            formatter = logging.Formatter(_config.get_log('pattern'))
            file_handler.setFormatter(formatter)
            # 设置文件日志级别
            file_output_level = _config.get_log('file_level')
            file_handler.setLevel(file_output_level)
            logger.addHandler(file_handler)
            self.__logger = logger

    def build_start_line(self, case_no):
        """
        write start line
        :param case_no:
        :return:
        """
        self.__logger.info("------" + case_no + " API test Start------")

    def build_end_line(self, case_no):
        """
        write end line
        :param case_no:
        :return:
        """
        self.__logger.info("--------" + case_no + " END--------")

    def build_case_line(self, case_name, code, msg):
        """
        write test case line
        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.__logger.info((case_name + " - Code:" + code + " - msg:" + msg))

    def get_report_path(self):
        """
        get report file path
        :return:
        """
        report_path = os.path.join(self.logPath)  # , "report.html")
        return report_path

    def get_result_path(self):
        """
        get test result path
        :return:
        """
        return self.logPath

    def write_result(self, result):
        """
        write result in logfile
        :param result:
        :return:
        """
        result_path = os.path.join(self.logPath, log_file_name)
        fb = open(result_path, "wb")
        try:
            fb.write(result)
        except FileNotFoundError as ex:
            self.__logger.error(str(ex))

    def __log_style(self, color=37, bgd=1):
        """ # # console log display sample
        :param color:   recv a number of color
        :param bgd:     recv a number of background
        :return:        stream handler of updated formatter
        """

        fmt = '[%(asctime)s] [%(levelname)s] \033[{};{}m%(message)s\033[0m'.format(bgd, color)
        formatter = logging.Formatter(fmt, '%F %T')
        self.console_handler.setFormatter(formatter)
        self.__logger.addHandler(self.console_handler)

    def _log_style_reset(self):
        fmt = "[%(asctime)s] [%(levelname)s] %(message)s"
        formatter = logging.Formatter(fmt, '%F %T')
        self.console_handler.setFormatter(formatter)
        self.__logger.addHandler(self.console_handler)

    """ # The functions of log level """

    def debug(self, msg, *args, **kwargs):
        self.__log_style(color=WHITE, bgd=BGD_RESET)
        if len(msg) > 1024:
            msg = "日志长度超过1024，控制台只打印1024字节长度,{}".format(msg[0:1023])
        self.__logger.debug(msg, *args, **kwargs)
        self._log_style_reset()

    def info(self, msg, *args, **kwargs):
        self.__log_style(color=1)
        if len(msg) > 1024:
            msg = "日志长度超过1024，控制台只打印1024字节长度,{}".format(msg[0:1023])
        self.__logger.info(msg, *args, **kwargs)
        self._log_style_reset()

    def demsg(self, msg, *args, **kwargs):
        self.__log_style(color=DARK_GREEN, bgd=1)
        if len(msg) > 1024:
            msg = "日志长度超过1024，控制台只打印1024字节长度,{}".format(msg[0:1023])
        self.__logger.info(msg, *args, **kwargs)
        self._log_style_reset()

    def warning(self, msg, *args, **kwargs):
        self.__log_style(color=YELLOW)
        if len(msg) > 1024:
            msg = "日志长度超过1024，控制台只打印1024字节长度,{}".format(msg[0:1023])
        self.__logger.warning(msg, *args, **kwargs)
        self._log_style_reset()

    def error(self, msg, *args, **kwargs):
        self.__log_style(color=RED, bgd=Underline)
        if len(msg) > 1024:
            msg = "日志长度超过1024，控制台只打印1024字节长度,{}".format(msg[0:1023])
        self.__logger.error(msg, *args, **kwargs)
        self._log_style_reset()

    def fatal(self, msg, *args, **kwargs):
        self.__log_style(color=RED, bgd=strikethrough)
        if len(msg) > 1024:
            msg = "日志长度超过1024，控制台只打印1024字节长度,{}".format(msg[0:1023])
        self.__logger.critical(msg, *args, **kwargs)
        self._log_style_reset()


class DeleteLog:
    def __init__(self):
        self.backup_days = _config.get_log('backup_days')
        self.del_path = os.path.join(project_dir, "results")
        if not os.path.exists(self.del_path):
            os.mkdir(self.del_path)
        self.delList = os.listdir(self.del_path)  # 需要删除目录下所有文件或文件夹列表
        self.logger = MyLog.get_log()

    def compare_file_time(self, file):
        time_of_last_mod = dt.date.fromtimestamp(os.path.getctime(file))
        days_between = (dt.date.today() - time_of_last_mod).days
        if int(days_between) >= int(self.backup_days):
            return True
        return False

    def delete_file(self):
        try:
            if self.delList:
                self.logger.debug("日志文件夹中存在文件或文件夹")
        except Exception as e:
            print('Error:', e)
        else:
            for f in self.delList:  # 遍历该列表

                filePath = os.path.join(self.del_path, f)  # 如果列表项是文件
                if self.compare_file_time(filePath) and (os.path.isfile(filePath)):
                    self.logger.info('日志文件目录中存在时间超过有效期%s天的文件' % self.backup_days)
                    os.remove(filePath)
                    print("天啊，这是文件不是文件夹，删除错了")
                    print(filePath + " was removed!")
                '''   
                elif os.path.isdir(filePath):  # 如果不是文件，肯定是文件夹
                    print("文件夹存在")
                    for i in [os.sep.join([filePath, v]) for v in os.listdir(filePath)]:
                        if self.compare_file_time(i) and (os.path.isfile(i)):
                            shutil.rmtree(filePath, True)  # shutil（高级文件操作）shutil.rmtree() 的方法，不仅是清空，直接连文件夹都一起删掉
                            print("Directory:" + filePath + " was removed")
                '''
                try:
                    if os.path.isdir(filePath) and self.compare_file_time(filePath):  # 删除log目录
                        self.logger.info('日志文件目录中存在时间超过有效期%s天的文件夹' % self.backup_days)
                        for root, dirs, files in os.walk(filePath):  # (root:'目录x'，dirs:[目录x下的目录list]，files:目录x下面的文件)
                            for name in files:
                                # delete the log and test result
                                del_file = os.path.join(root, name)
                                os.remove(del_file)
                                self.logger.info(u'remove file[%s] successfully' % del_file)
                        shutil.rmtree(filePath)
                        self.logger.info(u'remove dir[%s] successfully' % filePath)
                except Exception as e:
                    self.logger.error(str(e))


class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Logs()
            MyLog.mutex.release()

        return MyLog.log


if __name__ == "__main__":
    logger = MyLog.get_log()
    logger.debug("test debug")
    logger.info("test info")
    logger.warning("test warning")
    logger.error("hahahah")
    d = DeleteLog()
    d.delete_file()
