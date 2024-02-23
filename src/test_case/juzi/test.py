import requests
url = 'https://ecpouter-uat.corp.jccfc.com/channelQuery/guaranteeLoanBalance'
headers = {"Content-Type": "application/json;charset=utf-8"}
data = {"requestNo": "1707118512213", "guaranteeCode": "H24E02YNBC", "channelFlag": "JUZI"}
res = requests.post(url=url, headers=headers, data=data).json()
print(res)
