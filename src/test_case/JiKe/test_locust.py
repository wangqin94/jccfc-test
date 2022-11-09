# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：test_locust.py
@Author  ：jccfc
@Date    ：2022/11/8 19:06 
"""
import time

from locust import HttpUser
from locust import task
import os


# 我们在做接口自动化测试时，使用的是request对接口发起请求，在这里我们用的是locust中的httpuser对接口进行发起请求
from src.impl.FQL.FqlBizImpl import FqlBizImpl
from src.impl.JiKe.JiKeBizImpl import JiKeBizImpl
from src.impl.common.CheckBizImpl import CheckBizImpl
from utils.Models import get_next_month_today


class JiKeLocust(HttpUser):
    def on_start(self):
        print("我是一个用户，我启动了")

    def on_stop(self):
        print("我是一个用户，我退出了")

    # 定义好的接口必须使用task装饰器使其成为一个需要执行的任务，否则的话即使启动了locust也不会将定义好的函数作为一个需要执行的任务
    @task
    def login(self):
        fql = FqlBizImpl(data=None)
        # 发起授信申请
        self.applyId = fql.credit(creditAmount=10000, loanAmount=10000, loanTerm=3, interestRate='23')['applyId']
        # 检查授信状态
        time.sleep(30)
        # 发起支用刚申请
        # orderType: 订单类型 1取现；2赊销
        self.cur_time = str(get_next_month_today(1))
        fql.loan(orderType=1, loanTerm=3, loanAmt=10000, firstRepayDate=self.cur_time, interestRate='23')


if __name__ == '__main__':
    os.system("locust -f test_locust.py --web-host=127.0.0.1")
