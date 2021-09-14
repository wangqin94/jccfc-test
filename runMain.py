#!python3
# -*- coding: utf-8 -*-
import os, sys
from datetime import datetime
from utils import ReadConfig, Logger
from utils.Logger import MyLog
from utils.Models import project_dir
import unittest
from package.BeautifulReport import BeautifulReport
from utils.CommonEmail import MyEmail
from tomorrow import threads

logPath = os.path.join(os.path.join(project_dir(), "results"), str(datetime.now().strftime("%Y%m%d%H%M")))
if not os.path.exists(logPath):
    os.mkdir(logPath)
sys.path.append('..')


readconfig = ReadConfig.Config()


class AllTest():
    def __init__(self):
        global log, resultPath, on_off, email_send_model
        self.DeleteLog = Logger.DeleteLog()
        log = MyLog.get_log()
        resultPath = log.get_report_path()
        on_off = readconfig.get_email("on_off")
        email_send_model = readconfig.get_email("email_send_model")
        self.case_path = r'src\test_data\testFile\case'
        self.caseListFile = os.path.join(project_dir(), self.case_path, "caselist.txt")
        self.caseFile = os.path.join(project_dir(), r"src\test_case")
        self.caseList = []
        self.email = MyEmail.get_email()

    def set_case_list(self):
        """
        set case list
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):
                self.caseList.append(data.replace("\n", ""))
        fb.close()

    def set_case_suite(self, case):
        """
        set case suite
        :return:
        """
        # self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module = []
        case_name = case.split("/")[-1]
        log.info("此次执行的测试文件清单" + case_name + ".py")
        discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None)
        suite_module.append(discover)

        if len(suite_module) > 0:
            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        return test_suite

    # @threads(1)
    def run(self, case):
        """
        run test
        :return:
        """
        try:
            suit = self.set_case_suite(case)
            result = BeautifulReport(suit)
            result.report(filename='report.html', description='测试deafult报告', log_path=resultPath)
        except Exception as ex:
            log.error(str(ex))
        finally:
            log.info("*********TEST END*********")
            # send test report by email
            if email_send_model == "Each_time" and on_off == 'on':
                self.email.send_email()
            elif email_send_model == "failure" and on_off == 'on' and self.email.Judge_Report_Failure() == True:
                self.email.send_email()
            elif on_off == 'off':
                log.info("Doesn't send report email to developer.")
        self.DeleteLog.delete_file()


def main():
    obj = AllTest()
    obj.set_case_list()
    cases = obj.caseList
    for i in cases:
        obj.run(i)


if __name__ == '__main__':
    main()
