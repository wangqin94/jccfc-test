# -*- coding: utf-8 -*-
"""
数据库类，连接，查询等方法
"""
import pymysql
from utils.Logger import MyLog

_log = MyLog.get_log()


class Mysql(object):
    def __init__(self, general_database):
        # 获取mysql总数据库，credit信贷数据库配置
        self.general_database = general_database
        self.__mysql_cursor, self.__mysql = self.create_mysql_conn()
        self.cursor_list = [self.__mysql_cursor]
        self.cursor = self.__mysql_cursor

    def __del__(self):
        self.__mysql_cursor.close()
        self.__mysql.close()

    def switch_cusor(self, obj=0):
        self.cursor = self.cursor_list[obj]

    # def create_mysql_conn(self):
    #     # # -------开始创建数据库全局对象--------
    #     conn = pymysql.connect(host=self.general_database['host'],
    #                            user=self.general_database['username'],
    #                            password=self.general_database['password'],
    #                            port=self.general_database['port'],
    #                            charset='utf8')
    #     cursor = conn.cursor()
    #     # self.cursor_list.append(cursor)
    #     return cursor, conn

    def create_mysql_conn(self):
        # # -------初始化连接credit数据库-------
        db = pymysql.connect(host=self.general_database['host'],
                             user=self.general_database['username'],
                             port=self.general_database['port'],
                             password=self.general_database['password'],
                             database=self.general_database['databaseName'],
                             charset='utf8'
                             )
        cursor = db.cursor()
        return cursor, db

    def select_table_column(self, *args, table_name='credit_apply', database='hsit_credit'):
        column_key = []
        sql_column = "select COLUMN_NAME from information_schema.COLUMNS where table_name='{}' and table_schema='{}';".format(table_name, database)
        try:
            self.cursor.execute(sql_column)
        except Exception as e:
            print(e)
        res_column = self.cursor.fetchall()
        if args:
            column_key = args
        else:
            if res_column:
                column_key = [item[0] for item in res_column]
            # print(column_key)
        return column_key

    def select(self, sql):
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
        res_values = self.cursor.fetchall()
        return res_values

    def update(self, sql):
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.__mysql.commit()
        except Exception as e:
            _log.error("数据更新出错：case%s" % e)
            # 发生错误是回滚
            self.__mysql.rollback()
            raise e

    def insert(self, table, **kwargs):
        try:
            # 执行SQL语句
            keys = ', '.join(kwargs.keys())
            values = ', '.join(['%s'] * len(kwargs))
            sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
            self.cursor.execute(sql, tuple(kwargs.values()))
            _log.demsg("成功插入数据[{}]".format(sql))
            # 提交到数据库执行
            self.__mysql.commit()
        except Exception as e:
            _log.error("插入数据出错：case%s" % e)
            # 发生错误是回滚
            self.__mysql.rollback()
            raise e

    def delete(self, sql):
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.__mysql.commit()
        except Exception as e:
            _log.error("数据删除出错：case%s" % e)
            # 发生错误是回滚
            self.__mysql.rollback()


if __name__ == '__main__':
    t = Mysql().select_table_column()

