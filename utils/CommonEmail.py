# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import threading
import zipfile
import glob
from utils.Models import *
from requests_html import HTMLSession
from requests_file import FileAdapter

# 配置文件初始化
from utils.ReadConfig import Config

_config = Config()


class Email:
    def __init__(self):
        global host, user, password, port, sender, title

        # 初始化邮件配置参数
        host = _config.get_email("mail_host")
        user = _config.get_email("mail_user")
        password = _config.get_email("mail_pass")
        port = _config.get_email("mail_port")
        sender = _config.get_email("sender")
        title = _config.get_email("subject")
        self.value = _config.get_email("receiver")
        self.receiver = []
        self.session = HTMLSession()

        # 初始化日志引擎模块
        self.log = MyLog.get_log()

        for n in str(self.value).split(","):
            self.receiver.append(n)

        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.subject = date + " " + title

        self.msg = MIMEMultipart('related')
        self.report_path = os.path.join(self.log.get_result_path(), "report.html")

    def config_header(self):
        """
        defined emial header include subject, sender and receiver
        :return:
        """
        self.msg['subject'] = self.subject
        self.msg['from'] = sender
        self.msg['to'] = ";".join(self.receiver)

    def config_content(self):
        """
        write the content of email 自定义HTML文件内容
        :return:
        """
        f = open(os.path.join(project_dir(), r'test_case_data\\config\\emailStyle.txt'))
        content = f.read()
        f.close()
        content_plain = MIMEText(content, 'html', 'UTF-8')
        self.msg.attach(content_plain)
        self.config_image()

    def config_image(self):
        """
        config image that be used by content #构造图片附件
        :return:
        """
        # defined image path(个人头像)
        image1_path = os.path.join(project_dir(), r'test_case_data\\config\\title.jpg')
        fp1 = open(image1_path, 'rb')
        msgImage1 = MIMEImage(fp1.read())
        fp1.close()
        # defined image id
        msgImage1.add_header('Content-ID', '<image1>')
        self.msg.attach(msgImage1)

        # defined image path（公司logo标签）
        image2_path = os.path.join(project_dir(), r'test_case_data\\config\\logo.jpg')
        fp2 = open(image2_path, 'rb')
        msgImage2 = MIMEImage(fp2.read())
        fp2.close()
        # defined image id
        msgImage2.add_header('Content-ID', '<image2>')
        self.msg.attach(msgImage2)

    def config_file(self):
        """
        config email file #构造文件附件链接
        :return:
        """
        # if the file content is not null, then config the email file
        if self.check_file():
            print("文件存在，打印压缩包")
            report_path = self.log.get_result_path()
            zip_path = os.path.join(self.log.get_result_path(), "接口测试报告附件.zip")
            # zip file
            files = glob.glob(report_path + '\*')
            f = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
            for file in files:
                # 修改压缩文件的目录结果
                f.write(file, '/report/' + os.path.basename(file))
            f.close()

            report_file = open(zip_path, 'rb').read()
            file_html = MIMEText(str(report_file), 'base64', 'utf-8')
            file_html['Content-Type'] = 'application/octet-stream'
            file_html['Content-Disposition'] = 'attachment; filename="log_report.zip"'
            self.msg.attach(file_html)
        else:
            self.log.error("report日志文件不存在或为空，异常返回结果")

    def check_file(self):
        """
        check test report
        :return:
        """
        report_path = os.path.join(self.log.get_report_path(), "report.html")
        if os.path.isfile(report_path) and not os.stat(report_path) == 0:
            return True
        else:
            return False

    def send_email(self):
        """
        send email
        :return:
        """
        self.config_header()
        self.config_content()
        self.config_file()
        try:
            smtp = smtplib.SMTP()
            smtp.connect(host)
            smtp.login(user, password)
            smtp.sendmail(sender, self.receiver, self.msg.as_string())
            smtp.quit()
            self.log.info("The test report has send to developer by email.")
        except Exception as ex:
            self.log.error(str(ex))

    def send_mail_text(self):
        '''正文形式发送邮件'''
        self.config_header()
        self.config_file()
        try:
            with open(self.report_path, "r", encoding="utf-8") as fp:
                f = fp.read()
            fp.close()
            content_plain = MIMEText(f, _subtype='html', _charset='utf-8')
            self.msg.attach(content_plain)
            smtp = smtplib.SMTP()
            smtp.connect(host)
            smtp.login(user, password)
            smtp.sendmail(sender, self.receiver, self.msg.as_string())
            smtp.quit()
            self.log.info("测试报告已发送")
        except Exception as ex:
            self.log.error(str(ex))

    def Judge_Report_Failure(self):
        """
        判定测试报告是否包含失败的用例，如果有返回TRUE，没有返回FALSE
        :return:
        """
        try:
            self.session.mount("file://", FileAdapter())
            pwd = self.report_path.replace("\\", "/")
            path = "file:///" + pwd
        except:
            print("测试报告内容读取异常")
        from selenium import webdriver
        webdriver = webdriver.Chrome()
        webdriver.get(path)
        # time.sleep(5)
        text = webdriver.find_element_by_id("testFail").text
        webdriver.close()
        if int(text) > 0:
            return True
        else:
            return False


class MyEmail:
    email = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_email():
        if MyEmail.email is None:
            MyEmail.mutex.acquire()
            MyEmail.email = Email()
            MyEmail.mutex.release()
        return MyEmail.email


if __name__ == "__main__":
    email = MyEmail.get_email()
    email.send_email()
