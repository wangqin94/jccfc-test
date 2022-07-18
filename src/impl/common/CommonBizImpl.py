# -*- coding: utf-8 -*-
# ------------------------------------------
# 基于项目级业务层公共方法
# ------------------------------------------
from urllib import parse

from utils.Models import *
from config.globalConfig import *
from src.test_data.module_data.common import *

_log = MyLog.get_log()


def post_with_encrypt(url, payload, encrypt_url='encrypt_url', decrypt_url='decrypt_url', encrypt_flag=True):
    """

    @param url: 接口请求地址
    @param payload: 接口请求内容主体
    @param encrypt_url: 加密接口请求地址
    @param decrypt_url: 解密接口请求地址
    @param encrypt_flag: 加密标识默认true
    @return: response 接口响应参数 数据类型：json 
    """

    # data1 = json.dumps(payload)
    _log.info("payload数据: {}".format(payload))

    if encrypt_flag:
        encrypt_payload = encrypt(encrypt_url, headers, payload)
        response = requests.post(url=url, headers=headers, json=encrypt_payload)
        _log.info("请求地址: {}".format(url))
        response = decrypt(decrypt_url, headers, response.json())
    else:
        response = requests.post(url=url, headers=headers, json=payload)
        _log.info(f"响应报文类型：{type(response)}")
        response = response.json()
        _log.info(f"响应报文类型：{type(response)}")
        # response = str(response).replace("'", '''"''').replace(" ", "")
        # _log.info(res1)

        _log.info(f"响应报文：{response}")
    return response


def post_with_encrypt_baidu(url, payload, encrypt_url='encrypt_url', decrypt_url='decrypt_url', encrypt_flag=True):
    """

    @param url: 接口请求地址
    @param payload: 接口请求内容主体
    @param encrypt_url: 加密接口请求地址
    @param decrypt_url: 解密接口请求地址
    @param encrypt_flag: 加密标识默认true
    @return: response 接口响应参数 数据类型：json
    """
    data1 = json.dumps(payload)
    _log.info("payload数据: {}".format(data1))

    if encrypt_flag:
        encrypt_payload = encrypt(encrypt_url, headers, payload)
        response = requests.post(url=url, headers=headers_en, data=encrypt_payload)
        response = decrypt(decrypt_url, headers, response.json())
    else:
        response = requests.post(url=url, headers=headers, json=payload)
        response = response.json()
        _log.info(f"响应报文：{response}")
    return response


# 用户额度失效payload
def limit_invalid(self, productId, data):
    limit_invalid_data = dict()
    limit_invalid_data['certificateNo'] = data['cer_no']
    limit_invalid_data['userName'] = data['name']
    limit_invalid_data['productId'] = productId
    limit_invalid_data['reason'] = '11'
    limit_invalid_data['remark'] = ''
    limit_invalid_data['limitId'] = ''
    limit_invalid_data['voucherUrl'] = ''

    self.log.demsg('美团支用查询...')
    url = common.get('limit')['interface']
    response = post_with_encrypt(url, self.active_payload, encrypt_flag=False)
    return response


if __name__ == '__main__':
    print(common.get('limit')['interface'])
