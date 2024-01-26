# -*- coding: utf-8 -*-
# ------------------------------------------
# 基于项目级业务层公共方法
# ------------------------------------------
from config.globalConfig import *
from engine.EnvInit import EnvInit
from src.enums.EnumsCommon import ProductIdEnum
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from src.test_data.module_data.common import *
from utils.Models import *

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
    _log.info("payload数据: {}".format(json.dumps(payload, ensure_ascii=False)))

    if encrypt_flag:
        encrypt_payload = encrypt(encrypt_url, headers, payload)
        _log.info("请求地址: {}".format(url))
        response = requests.post(url=url, headers=headers, json=encrypt_payload)
        _log.info("响应密文: {}".format(response.json()))
        response = decrypt(decrypt_url, headers, response.json())
    else:
        response = requests.post(url=url, headers=headers, json=payload)
        # _log.info("响应报文: {}".format(payload))
        response = response.json()
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


# 根据输入产品编号获取对应产品年利率
def getInterestRate(productId):
    """
    @param productId: 产品ID
    @return: 产品年利率：interest_fixed_rate
    """

    try:
        if productId == ProductIdEnum.HAIR_DISCOUNT.value:
            product_product_param = MysqlBizImpl().get_base_database_info('product_product_param',
                                                                          product_id=productId,
                                                                          param_key='discount_interest_rate')
        else:
            product_product_param = MysqlBizImpl().get_base_database_info('product_product_param',
                                                                          product_id=productId,
                                                                          param_key='interest_fixed_rate')
        if product_product_param:
            interestRate = product_product_param['param_value']
            return float(interestRate)
        else:
            raise AssertionError("产品配置表年利率参数为空")
    except Exception as err:
        raise err


# 计算当月计提利息
def getDailyAccrueInterest(productId, days, leftAmt):
    """
    @param leftAmt: 当期剩余应还本金
    @param days: 计提天数
    @param productId: 产品ID
    @return: 当月计提利息
    """
    try:
        # 年基准天数
        product_product_param = MysqlBizImpl().get_base_database_info('product_product_param',
                                                                      product_id=productId,
                                                                      param_key='days_per_year')

        if product_product_param:
            yearRate = product_product_param['param_value']  # 产品配置年基准天数
            daysRate = getInterestRate(productId) / float(yearRate) / 100  # 日利率
            if days < 0:
                raise AssertionError("计息天数{}<0，请核对测试数据".format(days))
            dailyAccrueInterest = round(float(leftAmt) * daysRate * days, 6)
            return round(dailyAccrueInterest, 2)
        else:
            raise AssertionError("产品配置表年基准天数参数为空")
    except Exception as err:
        raise err


class ComBizImpl(EnvInit):
    def __init__(self):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()

    # 初始化渠道在贷余额
    def initChannelLoanAmountInfo(self, productId, businessDate=None):
        """
        @param businessDate: 业务时间 默认昨日
        @param productId: 产品编号
        @return:初始化渠道在贷余额
        """
        _log.info('channel_loan_amount表初始化放款金额，不存则新增一条记录...')
        date = businessDate if businessDate else str(get_before_day(1)).replace('-', '')
        data = self.MysqlBizImpl.get_op_channel_database_info('channel_loan_amount', product_id=productId,
                                                              business_date=date)
        if data:
            _log.info('存在 business_date={} 放款金额初始化记录，无需新增'.format(date))
        else:
            self.MysqlBizImpl.insert_channel_database_info("channel_loan_amount", product_id=productId,
                                                           first_balance='10000.0000', total_balance='500000.0000',
                                                           business_date=date)


if __name__ == '__main__':
    print(getDailyAccrueInterest(ProductIdEnum.HAIR_DISCOUNT.value, 1, 7500))
