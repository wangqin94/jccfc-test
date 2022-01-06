# -*- coding: utf-8 -*-
import os
import json
import configparser


class Config:
    """配置文件读取方法封装"""

    def __init__(self, config_file="config.ini"):
        # 获取配置文件所在目录
        self.conf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config")
        self.config_file = config_file
        # 生成配置文件完整路径
        self.config_name = os.path.basename(os.path.join(self.conf_path, self.config_file))
        self.conf = configparser.RawConfigParser()
        # 读取配置文件到conf对象(中文乱码问题需要添加encoding="utf-8-sig")
        self.conf.read(os.path.join(self.conf_path, self.config_name), encoding="utf-8-sig")

    def get_http(self, name):
        value = self.conf.get("HTTP", name)
        return json.loads(value)

    def get_email(self, name):
        value = self.conf.get("EMAIL", name)
        return value

    def get_mysql(self, env, name):
        value = self.conf.get(env, name)
        return json.loads(value)

    def get_api(self, env, name):
        value = self.conf.get("API", name)
        return value.format(env)

    def get_vehicle(self, name):
        value = self.conf.get("VEHICLE", name)
        return value

    def get_interface_url(self, name):
        value = self.conf.get("INTERFACE_URL", name)
        return value

    def get_log(self, name):
        value = self.conf.get("LOG", name)
        return value

    def get_path(self, name):
        value = self.conf.get("PATH", name)
        return value

    def get_browser(self, name):
        value = self.conf.get("BROWSER", name)
        return value

    def get_job(self, name):
        value = self.conf.get("JOB", name)
        return value

    def get_redis(self, name):
        value = self.conf.get("REDIS", name)
        return json.loads(value)


if __name__ == '__main__':
    c = Config()
    # print(c.get_mysql("hsit", 'database'))
    # print(c.get_api('hsit','request_host') + '/api/v1/baidu/demo/credit/apply')
    print(c.get_http('headers'))
