# -*- coding: utf-8 -*-
# ------------------------------------------
# 基于项目级业务层公共方法
# ------------------------------------------


# port http请求
from engine.Base import INIT
from utils.Models import *
from config.globalConfig import *
from src.test_data.module_data.common import *

log = MyLog.get_log()


def post_with_encrypt(url, payload, encrypt_url='encrypt_url', decrypt_url='decrypt_url', encrypt_flag=True):
    """

    @param url: 接口请求地址
    @param payload: 接口请求内容主体
    @param encrypt_url: 加密接口请求地址
    @param decrypt_url: 解密接口请求地址
    @param encrypt_flag: 加密标识默认true
    @return: 
    """
    log.info("payload数据: {}".format(payload))

    if encrypt_flag:
        encrypt_payload = encrypt(encrypt_url, headers, payload)
        response = requests.post(url=url, headers=headers, json=encrypt_payload)
        response = decrypt(decrypt_url, headers, response.json())
    else:
        response = requests.post(url=url, headers=headers, json=payload)
        response = response.json()
        log.info(f"响应报文：{response}")
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


class GetSqlData(INIT):
    def __init__(self):
        super().__init__()

    def get_loan_apply_info(self, record=0, **kwargs):
        """
        @param record: 查询记录,非必填
        @param kwargs: 查询条件，字典类型
        @return:
        """
        table = 'credit_loan_apply'
        keys = self.mysql_credit.select_table_column(table_name=table, database=self.credit_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, self.credit_database_name, attr=None, **kwargs)
        self.log.info("sql查询语句：{}".format(sql))
        values = self.mysql_credit.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            return data
        except (IndexError, Exception):
            self.log.warning("SQL查询结果为空")

    def get_credit_apply_info(self, record=0, **kwargs):
        """
        @param record: 查询记录，非必填
        @param kwargs: 查询条件，字典类型
        @return:
        """
        table = 'credit_apply'
        keys = self.mysql_credit.select_table_column(table_name=table, database=self.credit_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, self.credit_database_name, attr=None, **kwargs)
        self.log.info("sql查询语句：{}".format(sql))
        values = self.mysql_credit.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            return data
        except (IndexError, Exception):
            self.log.warning("SQL查询结果为空")

    def get_credit_database_info(self, table, record=0, **kwargs):
        """
        @param record: 查询记录，非必填
        @param kwargs: 查询条件，字典类型
        @return:
        """
        keys = self.mysql_credit.select_table_column(table_name=table, database=self.credit_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, self.credit_database_name, attr=None, **kwargs)
        self.log.info("sql查询语句：{}".format(sql))
        values = self.mysql_credit.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            return data
        except (IndexError, Exception):
            self.log.warning("SQL查询结果为空")

    def get_user_database_info(self, table, record=0, **kwargs):
        """
        @param record: 查询记录，非必填
        @param kwargs: 查询条件，字典类型
        @return:
        """
        keys = self.mysql_user.select_table_column(table_name=table, database=self.user_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, self.user_database_name, attr=None, **kwargs)
        self.log.info("sql查询语句：{}".format(sql))
        values = self.mysql_user.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            return data
        except (IndexError, Exception):
            self.log.warning("SQL查询结果为空")


if __name__ == '__main__':
    # t = GetSqlData().get_credit_apply_info(a=1, b=2)
    print(common.get('limit')['interface'])
