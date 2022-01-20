# -*- coding: utf-8 -*-
# ------------------------------------------
# 基于项目级业务层公共方法
# ------------------------------------------
import sys

from engine.MysqlInit import MysqlInit
from utils.Models import *


class MysqlBizImpl(MysqlInit):
    def __init__(self):
        super().__init__()

    def get_credit_data_info(self, table='credit_loan_apply', key="查询条件", record=0):
        """
        :function: 获取credit数据库表中信息
        table : 表名
        key ： 查询关键字
        record ： 根据列表指定序列返回查询数据
        """
        sql = "select * from {}.{} where {};".format(self.credit_database_name, table, key)
        self.log.info(sql)
        # 获取表属性字段名
        keys = self.mysql_credit.select_table_column(table_name=table, database=self.credit_database_name)
        # 获取查询内容
        values = self.mysql_credit.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def get_asset_data_info(self, table='asset_loan_apply', key="查询条件", record=0):
        """
        :function: 获取asset数据库表中信息
        table : 表名
        key ： 查询关键字
        record ： 根据列表指定序列返回查询数据
        """
        sql = "select * from {}.{} where {};".format(self.asset_database_name, table, key)
        # self.log.info(sql)
        # 获取表属性字段名
        keys = self.mysql_asset.select_table_column(table_name=table, database=self.asset_database_name)
        # 获取查询内容
        values = self.mysql_asset.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def credit_apply_query(self, data):
        """ # 接口数据payload解密
            :return:                查询状态
            """
        key = "certificate_no = '{}'".format(data['cer_no'])
        info = self.get_credit_data_info(table="credit_apply", key=key)
        try:
            status = info['status']
            return status
        except (IndexError, Exception):
            self.log.warning("SQL查询query 0 ")

    def check_user_available(self, data):
        sql = "select * from credit_apply where user_tel='{}';".format(data['telephone'])
        res = self.mysql_credit.select(sql)
        if res:
            if data['cer_no'] not in res[0]:
                self.log.error('手机号已被注册, 主程序退出!')
                sys.exit(7)
            else:
                self.log.warning('提示：用户已存在授信信息\n继续流程...')

    def get_loan_apply_info(self, record=0, attr=None, **kwargs):
        """
        @param record: 查询记录,非必填
        @param attr: 查询表子项
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        table = 'credit_loan_apply'
        keys = self.mysql_credit.select_table_column(table_name=table, database=self.credit_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, self.credit_database_name, attr=attr, **kwargs)
        values = self.mysql_credit.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            self.log.info("执行sql查询：{} {}: query 0 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def get_credit_apply_info(self, record=0, attr=None, **kwargs):
        """
        @param record: 查询记录，非必填
        @param attr: 查询表子项
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        table = 'credit_apply'
        keys = self.mysql_credit.select_table_column(table_name=table, database=self.credit_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, self.credit_database_name, attr=attr, **kwargs)
        values = self.mysql_credit.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            self.log.info("执行sql查询：{} {}: query 0 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def get_credit_database_info(self, table, record=0, attr=None, **kwargs):
        """
        @param table:
        @param attr: 查询表子项
        @param record: 查询记录，非必填
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        keys = self.mysql_credit.select_table_column(table_name=table, database=self.credit_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, self.credit_database_name, attr=attr, **kwargs)
        values = self.mysql_credit.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            self.log.info("执行sql查询：{} {}: query 0 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def get_asset_database_info(self, table, record=0, attr=None, **kwargs):
        """
        @param table:
        @param attr: 查询表子项
        @param record: 查询记录，非必填
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        keys = self.mysql_asset.select_table_column(table_name=table, database=self.asset_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, self.asset_database_name, attr=attr, **kwargs)
        values = self.mysql_asset.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            self.log.info("执行sql查询：{} {}: query 0 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def get_user_database_info(self, table, record=0, attr=None, **kwargs):
        """
        @param table:
        @param attr: 查询表子项
        @param record: 查询记录，非必填
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        keys = self.mysql_user.select_table_column(table_name=table, database=self.user_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, self.user_database_name, attr=attr, **kwargs)
        values = self.mysql_user.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            self.log.info("执行sql查询：{} {}: query 0 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def get_base_database_info(self, table, record=0, attr=None, **kwargs):
        """
        过去base数据库结构
        @param attr: 查询表子项
        @param table:
        @param record: 查询记录，非必填
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        keys = self.mysql_base.select_table_column(table_name=table, database=self.base_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, self.base_database_name, attr=attr, **kwargs)
        values = self.mysql_base.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            self.log.info("执行sql查询：{} {}: query 0 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def get_bigacct_database_info(self, table, record=0, attr=None, **kwargs):
        """
        获取base数据库结构
        @param attr: 查询表子项
        @param table: 查询表
        @param record: 查询记录，非必填
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        keys = self.mysql_bigacct.select_table_column(table_name=table, database=self.bigacct_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, self.bigacct_database_name, attr=attr, **kwargs)
        values = self.mysql_bigacct.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            self.log.info("执行sql查询：{} {}: query 0 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def get_op_channel_database_info(self, table, record=0, attr=None, **kwargs):
        """
        获取op_channel数据库结构
        @param attr: 查询表子项
        @param table: 查询表
        @param record: 查询记录，非必填
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        keys = self.mysql_op_channel.select_table_column(table_name=table, database=self.op_channel_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, self.op_channel_database_name, attr=attr, **kwargs)
        values = self.mysql_op_channel.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            data = [dict(zip(keys, item)) for item in values][record]
            self.log.info("执行sql查询：{} {}: query 0 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def update_bigacct_database_info(self, table, attr, **kwargs):
        """
        更新bigacct数据库结构
        @param table: 更新表
        @param attr: 更新条件
        @param kwargs: 更新值，字典类型
        """
        keys = self.mysql_bigacct.select_table_column(table_name=table, database=self.bigacct_database_name)
        # 获取查询内容
        sql = update_sql_qurey_str(table, self.bigacct_database_name, attr=attr, **kwargs)
        self.mysql_bigacct.update(sql)
        self.log.info("sql：更新成功 [{}]".format(sql))

    def update_asset_database_info(self, table, attr, **kwargs):
        """
        更新asset数据库结构
        @param table: 更新表
        @param attr: 更新条件
        @param kwargs: 更新值，字典类型
        """
        keys = self.mysql_asset.select_table_column(table_name=table, database=self.asset_database_name)
        # 获取查询内容
        sql = update_sql_qurey_str(table, self.asset_database_name, attr=attr, **kwargs)
        self.mysql_asset.update(sql)
        self.log.info("sql：更新成功 [{}]".format(sql))


if __name__ == '__main__':
    # t = MysqlBizImpl().get_bigacct_database_info('acct_sys_info', sys_id='BIGACCT')
    # MysqlBizImpl().update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", account_date='20220113')
    # print(common.get('limit')['interface'])
    MysqlBizImpl().get_loan_apply_info(id=999)
