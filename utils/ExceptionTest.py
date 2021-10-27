# -*- coding: utf-8 -*-
"""

"""
import requests

__all__ = ['asset_delete', 'asset_put', 'payconvert', 'user_put', 'exception_service']


def asset_delete(instance):
    url = 'https://eureka-hsit.corp.jccfc.com/eureka/apps/LOANV2-ASSET/' + instance
    print("url:{}".format(url))
    res = requests.delete(url=url)
    print(res.status_code)
    print("res.text:{}".format(res.text))


def asset_put(instance):
    # 使asset服务宕机
    # url = 'https://eureka-hsit.corp.jccfc.com/eureka/apps/LOANV2-ASSET/' + instance + '/status?value=OUT_OF_SERVICE'
    # 启动asset服务
    url = 'https://eureka-hsit.corp.jccfc.com/eureka/apps/LOANV2-ASSET/' + instance + '/status?value=UP'
    print("url:{}".format(url))
    res = requests.put(url=url)
    print(res.status_code)
    print("res.text:{}".format(res.text))


def user_put(instance):
    # 使user服务宕机
    # url = 'https://eureka-hsit.corp.jccfc.com/eureka/apps/LOANV2-USER/' + instance + '/status?value=OUT_OF_SERVICE'
    # 启动asset服务
    url = 'https://eureka-hsit.corp.jccfc.com/eureka/apps/LOANV2-USER/' + instance + '/status?value=UP'
    print("url:{}".format(url))
    res = requests.put(url=url)
    print(res.status_code)
    print("res.text:{}".format(res.text))


def payconvert(instance):
    # 使user服务宕机
    # url = 'https://eureka-hsit.corp.jccfc.com/eureka/apps/LOANV2-PAYCONVERT/'
    # + instance + '/status?value=OUT_OF_SERVICE'
    # url = 'https://eureka-qas.corp.jccfc.com/eureka/apps/LOANV2-PAYCONVERT/' + instance + '/status?value=OUT_OF_SERVICE'
    # url = 'https://eureka-hqas.corp.jccfc.com/eureka/apps/LOANV2-PAYCONVERT/' + instance + '/status?value=OUT_OF_SERVICE'
    # 启动asset服务
    url = 'https://eureka-hqas.corp.jccfc.com/eureka/apps/LOANV2-PAYCONVERT/' + instance + '/status?value=UP'
    # url = 'https://eureka-qas.corp.jccfc.com/eureka/apps/LOANV2-PAYCONVERT/' + instance + '/status?value=UP'
    print("url:{}".format(url))
    res = requests.put(url=url)
    print(res.status_code)
    print("res.text:{}".format(res.text))


def exception_service(api, instance):
    # 使服务宕机
    url = 'https://eureka-hsit.corp.jccfc.com/eureka/apps/' + api + instance + '/status?value=OUT_OF_SERVICE'
    # 启动服务
    url = 'https://eureka-hsit.corp.jccfc.com/eureka/apps/' + api + instance + '/status?value=UP'
    print("url:{}".format(url))
    res = requests.put(url=url)
    print(res.status_code)
    print("res.text:{}".format(res.text))


def cc_service(api, instance):
    # 使服务宕机
    # url = 'https://eureka-hqas.corp.jccfc.com/eureka/apps/' + api + instance + '/status?value=OUT_OF_SERVICE'
    # 启动服务
    url = 'https://eureka-hqas.corp.jccfc.com/eureka/apps/' + api + instance + '/status?value=UP'
    print("url:{}".format(url))
    res = requests.put(url=url)
    print(res.status_code)
    print("res.text:{}".format(res.text))


if __name__ == '__main__':
    # asset_put('10.233.68.181:8080:loanV2-asset:asset-869b5c84bb-vgc4m')
    # user_put('10.233.73.151:8080:loanV2-user:user-69c899cdc-tlljg')
    # payconvert('10.233.76.223:8080:loanV2-payConvert:convert-6975dd9c8f-tdq62')
    payconvert('10.233.78.185:8080:loanV2-payConvert:convert-77db7445fb-kr9c2')
