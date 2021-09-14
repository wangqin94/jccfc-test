# -*- coding: utf-8 -*-
import json
import os
import requests
import socket
from utils import ReadConfig
from utils.Logger import MyLog

readConfig = ReadConfig.Config()


class CommonHttp:
    def __init__(self):
        global scheme, host, port, timeout
        scheme = readConfig.get_http("scheme")
        host = readConfig.get_http("host")
        port = readConfig.get_http("port")
        timeout = readConfig.get_http("timeout")
        self.session = requests.session()
        self.logger = MyLog.get_log()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.json = None
        self.url = None
        self.files = {}
        self.state = 0

    def set_url(self, url):
        """
        set url
        :param url:
        :return:
        """
        self.url = scheme + '://' + host + ':' + port + url
        self.logger.info("请求URL:%s" % self.url)

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header
        self.logger.info("请求header:%s" % self.headers)

    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param
        self.logger.info("请求params:%s" % self.params)

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data
        self.logger.info("请求body:%s" % self.data)

    def set_json(self, data):
        """
        set json
        :param data:
        :return:
        """
        self.json = json.dumps(data)
        self.logger.info("请求body:%s" % self.json)

    def set_cookies(self, cookies):
        if cookies:
            self.session.cookies.update(cookies)

    def set_files(self, filename):
        """
        set upload files
        :param filename:
        :return:
        """
        if filename != '':
            project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_dir = os.path.join(project_path, r"src\test_case_data\\img\\testfile")
            file_path = os.path.join(file_dir, filename)
            self.files = {'file': open(file_path, 'rb')}

        if filename == '' or filename is None:
            self.state = 1

    def get(self):
        """
        defined get method
        :return:
        """
        try:
            response = self.session.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))
            self.logger.info("请求类型:GET")
            self.logger.info("返回参数%s" % response.text)
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include get params and post data
    # uninclude upload file
    def post(self):
        """
        defined post method
        :return:
        """
        try:
            response = self.session.post(self.url, headers=self.headers, params=self.params, data=self.data,
                                         json=self.json,
                                         timeout=float(timeout)
                                         )
            # response.raise_for_status()
            self.logger.info("请求类型:POST")
            self.logger.info("返回参数%s" % response.text)
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include upload file
    def postWithFile(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files,
                                     timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # for json
    def postWithJson(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None


class TCPClient(object):
    """用于测试TCP协议的socket请求，对于WebSocket，socket.io需要另外的封装"""

    def __init__(self, domain, port, timeout=30, max_receive=102400):
        self.domain = domain
        self.port = port
        self.connected = 0  # 连接后置为1
        self.max_receive = max_receive
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(timeout)
        self.logger = MyLog.get_log()

    def connect(self):
        """连接指定IP、端口"""
        if not self.connected:
            try:
                self._sock.connect((self.domain, self.port))
            except socket.error as e:
                self.logger.exception(e)
            else:
                self.connected = 1
                self.logger.debug('TCPClient connect to {0}:{1} success.'.format(self.domain, self.port))

    def send(self, data, dtype='str', suffix=''):
        """向服务器端发送send_string，并返回信息，若报错，则返回None"""
        if dtype == 'json':
            send_string = json.dumps(data) + suffix
        else:
            send_string = data + suffix
        self.connect()
        if self.connected:
            try:
                self._sock.send(send_string.encode())
                self.logger.debug('TCPClient Send {0}'.format(send_string))
            except socket.error as e:
                self.logger.exception(e)

            try:
                rec = self._sock.recv(self.max_receive).decode()
                if suffix:
                    rec = rec[:-len(suffix)]
                    self.logger.debug('TCPClient received {0}'.format(rec))
                return rec
            except socket.error as e:
                self.logger.exception(e)

    def close(self):
        """关闭连接"""
        if self.connected:
            self._sock.close()
            self.logger.debug('TCPClient closed.')


class DDT:
    def __init__(self, data):
        self.scheme = readConfig.get_http("scheme")
        self.host = readConfig.get_http("host")  # 从config.ini配置文件内获取host
        self.port = readConfig.get_http("port")
        self.data = data
        self.rowNum = data['rowNum']
        self.case_id = self.data['id']
        self.case_name = self.data['case_name']
        self.describe = self.data['describe']
        self.method = self.data['method']
        self.path = self.data['path']  # 在Excel测试文件内获取接口路径--path
        self.body = self.data['body']
        self.type = self.data['type']
        self.checkfield = self.data['checkfield']
        self.checkpoint = self.data['checkpoint']
        self.verify = False

    def send_requests(self, s):
        '''封装requests请求'''
        url = self.scheme + '://' + self.host + ':' + self.port + self.path
        # 请求头部headers
        try:
            headers = eval(self.data["headers"])
            print("请求头部：%s") % headers
        except:
            headers = None
        print("正在执行用例:******---%s---********" % self.case_id)
        if self.case_name == '':
            print("用例名称:未描述用例")
        else:
            print("用例名称:%s" % self.case_name)
        print("请求方式:%s,请求url:%s" % (self.method, url))
        # url后面的params参数
        try:
            params = eval(self.data["params"])
            print("请求params:%s" % params)
        except:
            params = None
        # post请求body内容
        try:
            bodydata = eval(self.data["body"])
        except:
            bodydata = {}

        # 判断传data数据还是json
        if self.type == "data":
            body = bodydata
        elif self.type == "json":
            body = json.dumps(bodydata)
        else:
            body = bodydata
        if self.method == "post": print("post请求body类型为：%s ,body内容为：%s" % (self.type, body))
        res = {}  # 用于接受返回数据
        try:
            r = s.request(method=self.method,
                          url=url,
                          params=params,
                          headers=headers,
                          data=body,
                          verify=self.verify
                          )
            res['describe'] = self.describe
            res['id'] = self.case_id
            res['rowNum'] = self.rowNum
            res["statuscode"] = str(r.status_code)  # 状态码转成str
            res["text"] = r.text
            res["times"] = str(r.elapsed.total_seconds())  # 接口请求时间转str
            if res["statuscode"] != "200":
                res["error"] = res["text"]
            else:
                res["error"] = r.json().get("Message")
            res["msg"] = ""
            content = ""
            if self.checkfield == '':
                if self.checkpoint in res["text"]:
                    res["result"] = "pass"
                    print("用例测试结果:%s---->%s" % (self.case_id, res["result"]))
                else:
                    res["result"] = "fail"
                    print("用例测试结果:%s---->%s" % (self.case_id, res["result"]))
                return res
            else:
                if self.checkpoint in res[self.checkfield]:
                    res["result"] = "pass"
                    print("用例测试结果:%s---->%s" % (self.case_id, res["result"]))
                else:
                    res["result"] = "fail"
                    print("用例测试结果:%s---->%s" % (self.case_id, res["result"]))
                return res
        except Exception as msg:
            res["msg"] = str(msg)
            return res
