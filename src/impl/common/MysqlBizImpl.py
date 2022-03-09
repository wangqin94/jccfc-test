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
        # 获取表属性字段名
        keys = self.mysql_credit.select_table_column(table_name=table, database=self.credit_database_name)
        # 获取查询内容
        values = self.mysql_credit.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            if record == 999:
                data = [dict(zip(keys, item)) for item in values]
                self.log.info("执行sql查询：{} {}: query {} ".format(sql, data, len(data)))
            else:
                data = [dict(zip(keys, item)) for item in values][record]
                self.log.info("执行sql查询：{} {}: query 1 ".format(sql, data))
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
            if record == 999:
                data = [dict(zip(keys, item)) for item in values]
                self.log.info("执行sql查询：{} {}: query {} ".format(sql, data, len(data)))
            else:
                data = [dict(zip(keys, item)) for item in values][record]
                self.log.info("执行sql查询：{} {}: query 1 ".format(sql, data))
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

    def get_loan_apply_info(self, *args, record=0, **kwargs):
        """
        @param record: 查询记录,非必填
        @param args: 查询表子项
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        table = 'credit_loan_apply'
        keys = self.mysql_credit.select_table_column(*args, table_name=table, database=self.credit_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, *args, db=self.credit_database_name, **kwargs)
        values = self.mysql_credit.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            if record == 999:
                data = [dict(zip(keys, item)) for item in values]
                self.log.info("执行sql查询：{} {}: query {} ".format(sql, data, len(data)))
            else:
                data = [dict(zip(keys, item)) for item in values][record]
                self.log.info("执行sql查询：{} {}: query 1 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def get_credit_apply_info(self, *args, record=0, **kwargs):
        """
        @param record: 查询记录，非必填
        @param args: 查询表子项
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        table = 'credit_apply'
        keys = self.mysql_credit.select_table_column(*args, table_name=table, database=self.credit_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, *args, db=self.credit_database_name, **kwargs)
        values = self.mysql_credit.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            if record == 999:
                data = [dict(zip(keys, item)) for item in values]
                self.log.info("执行sql查询：{} {}: query {} ".format(sql, data, len(data)))
            else:
                data = [dict(zip(keys, item)) for item in values][record]
                self.log.info("执行sql查询：{} {}: query 1 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def get_credit_database_info(self, table, *args, record=0, **kwargs):
        """
        @param table:
        @param args: 查询表子项 tuple
        @param record: 查询记录，非必填
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        keys = self.mysql_credit.select_table_column(*args, table_name=table, database=self.credit_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, *args, db=self.credit_database_name, **kwargs)
        values = self.mysql_credit.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            if record == 999:
                data = [dict(zip(keys, item)) for item in values]
                self.log.info("执行sql查询：{} {}: query {} ".format(sql, data, len(data)))
            else:
                data = [dict(zip(keys, item)) for item in values][record]
                self.log.info("执行sql查询：{} {}: query 1 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def get_asset_database_info(self, table, *args, record=0, **kwargs):
        """
        @param table:
        @param args: 查询表子项 tuple
        @param record: 查询记录，非必填  record == 999: 查询所有记录
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        keys = self.mysql_asset.select_table_column(*args, table_name=table, database=self.asset_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, *args, db=self.asset_database_name, **kwargs)
        values = self.mysql_asset.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            if record == 999:
                data = [dict(zip(keys, item)) for item in values]
                self.log.info("执行sql查询：{} {}: query {} ".format(sql, data, len(data)))
            else:
                data = [dict(zip(keys, item)) for item in values][record]
                self.log.info("执行sql查询：{} {}: query 1 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def get_user_database_info(self, table, *args, record=0, **kwargs):
        """
        @param table:
        @param args: 查询表子项 tuple
        @param record: 查询记录，非必填
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        keys = self.mysql_user.select_table_column(*args, table_name=table, database=self.user_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, *args, db=self.user_database_name, **kwargs)
        values = self.mysql_user.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            if record == 999:
                data = [dict(zip(keys, item)) for item in values]
                self.log.info("执行sql查询：{} {}: query {} ".format(sql, data, len(data)))
            else:
                data = [dict(zip(keys, item)) for item in values][record]
                self.log.info("执行sql查询：{} {}: query 1 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def get_base_database_info(self, table, *args, record=0, **kwargs):
        """
        过去base数据库结构
        @param args: 查询表子项 tuple
        @param table:
        @param record: 查询记录，非必填
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        keys = self.mysql_base.select_table_column(*args, table_name=table, database=self.base_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, *args, db=self.base_database_name, **kwargs)
        values = self.mysql_base.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            if record == 999:
                data = [dict(zip(keys, item)) for item in values]
                self.log.info("执行sql查询：{} {}: query {} ".format(sql, data, len(data)))
            else:
                data = [dict(zip(keys, item)) for item in values][record]
                self.log.info("执行sql查询：{} {}: query 1 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def get_bigacct_database_info(self, table, *args, record=0, **kwargs):
        """
        获取base数据库结构
        @param args: 查询表子项 tuple
        @param table: 查询表
        @param record: 查询记录，非必填
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        keys = self.mysql_bigacct.select_table_column(*args, table_name=table, database=self.bigacct_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, *args, db=self.bigacct_database_name, **kwargs)
        values = self.mysql_bigacct.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            if record == 999:
                data = [dict(zip(keys, item)) for item in values]
                self.log.info("执行sql查询：{} {}: query {} ".format(sql, data, len(data)))
            else:
                data = [dict(zip(keys, item)) for item in values][record]
                self.log.info("执行sql查询：{} {}: query 1 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def get_op_channel_database_info(self, table, *args, record=0, **kwargs):
        """
        获取op_channel数据库结构
        @param args: 查询表子项 tuple
        @param table: 查询表
        @param record: 查询记录，非必填
        @param kwargs: 查询条件，字典类型
        @return: response 接口响应参数 数据类型：json
        """
        keys = self.mysql_op_channel.select_table_column(*args, table_name=table,
                                                         database=self.op_channel_database_name)
        # 获取查询内容
        sql = get_sql_qurey_str(table, *args, db=self.op_channel_database_name, **kwargs)
        values = self.mysql_op_channel.select(sql)
        try:
            # 每条查询到的数据处理 [{表字段:内容值, ...}, {}]
            if record == 999:
                data = [dict(zip(keys, item)) for item in values]
                self.log.info("执行sql查询：{} {}: query {} ".format(sql, data, len(data)))
            else:
                data = [dict(zip(keys, item)) for item in values][record]
                self.log.info("执行sql查询：{} {}: query 1 ".format(sql, data))
            return data
        except Exception as err:
            self.log.warning("SQL查询{} {}: query 0 ".format(sql, err))

    def update_bigacct_database_info(self, table, attr, **kwargs):
        """
        更新bigacct数据库结构
        @param table: 更新表
        @param attr: 更新条件 tuple
        @param kwargs: 更新值，字典类型
        """
        # 获取查询内容
        sql = update_sql_qurey_str(table, self.bigacct_database_name, attr=attr, **kwargs)
        self.mysql_bigacct.update(sql)
        self.log.info("sql：更新成功 [{}]".format(sql))

    def update_asset_database_info(self, table, attr, **kwargs):
        """
        更新asset数据库结构
        @param table: 更新表
        @param attr: 更新条件 tuple
        @param kwargs: 更新值，字典类型
        """
        # 获取查询内容
        sql = update_sql_qurey_str(table, self.asset_database_name, attr=attr, **kwargs)
        self.mysql_asset.update(sql)
        self.log.info("sql：更新成功 [{}]".format(sql))

    def update_credit_database_info(self, table, attr, **kwargs):
        """
        更新credit数据库结构
        @param table: 更新表
        @param attr: 更新条件 tuple
        @param kwargs: 更新值，字典类型
        """
        # 获取查询内容
        sql = update_sql_qurey_str(table, self.credit_database_name, attr=attr, **kwargs)
        self.mysql_credit.update(sql)
        self.log.info("sql：更新成功 [{}]".format(sql))

    def delete_asset_database_info(self, table, **kwargs):
        """
        删除asset数据库结构
        @param table: 更新表
        @param kwargs: 更新值，字典类型
        """
        # 获取查询内容
        sql = delete_sql_qurey_str(table, self.asset_database_name, **kwargs)
        self.mysql_asset.delete(sql)
        self.log.info("sql：删除成功 [{}]".format(sql))

    def delete_credit_database_info(self, table, **kwargs):
        """
        删除credit数据库结构
        @param table: 更新表
        @param kwargs: 更新值，字典类型
        """
        # 获取查询内容
        sql = delete_sql_qurey_str(table, self.credit_database_name, **kwargs)
        self.mysql_credit.delete(sql)
        self.log.info("sql：删除成功 [{}]".format(sql))

    def get_loan_apply_status(self, exp_status, m=6, t=5, **kwargs):
        """
        查询支用状态
        @param t: 每次时间间隔, 默认5S
        @param exp_status: 需要查询的状态
        @param m: 查询轮训次数 默认6次
        @param kwargs: 查询条件
        @return: status 支用单状态
        """
        self.log.demsg('获取支用单的借据状态...')
        for n in range(1, m + 1):
            info = self.get_loan_apply_info(**kwargs)
            status = info['status']
            if status == exp_status:
                self.log.demsg('credit_loan_apply获取支用单状态[status：{}]'.format(status))
                return status
            else:
                if n == m:
                    self.log.error("超过当前系统设置等待时间，请手动查看结果....")
                    sys.exit(7)
                self.log.demsg("credit_loan_apply获取支用单状态不符合预期,启动轮训查询")
                time.sleep(t)

    def get_asset_job_ctl_info(self, job_date, job_type='ASSET_BI_JOB_FINISH'):
        self.log.demsg('检查资产卸数时间，不存则新增一条记录...')
        data = self.get_asset_database_info('asset_job_ctl', job_date=job_date, job_type=job_type)
        if data:
            self.log.info('存在 job_date={} 资产卸数记录，无需新增'.format(job_date))
        else:
            curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.mysql_asset.insert('asset_job_ctl', tenant_id='000', job_date=job_date, job_type=job_type,
                                    job_name='日终结束任务', job_order='999', job_status='1', create_time=curtime,
                                    update_time=curtime)


if __name__ == '__main__':
    # t = MysqlBizImpl().get_bigacct_database_info('acct_sys_info', sys_id='BIGACCT')
    # MysqlBizImpl().update_bigacct_database_info('acct_sys_info', attr="sys_id='BIGACCT'", account_date='20220217')
    # print(common.get('limit')['interface'])
    # MysqlBizImpl().get_loan_apply_info(id=999)
    # MysqlBizImpl().get_credit_apply_info('credit_apply_id', credit_apply_id='000CA2021031500000021')
    # MysqlBizImpl().get_loan_apply_status('01')
    # MysqlBizImpl().get_asset_database_info('asset_repay_plan', 'sum(pre_repay_amount)', record=999, loan_invoice_id='000LI0001287425037156375010', repay_plan_status='4')
    MysqlBizImpl().update_asset_job_ctl_date('20210909')
