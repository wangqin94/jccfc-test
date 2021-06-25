# -*- coding: utf-8 -*-
"""
数据库类，连接，查询等方法
"""
import pymysql


class Mysql(object):
    def __init__(self, general_database, credit_database):
        # 获取mysql总数据库，credit信贷数据库配置
        self.general_database = general_database
        self.credit_database = credit_database
        self.__mysql_cursor, self.__mysql = self.create_mysql_conn()
        self.__cursor, self.__db = self.create_credit_conn()
        self.cursor_list = [self.__cursor, self.__mysql_cursor]
        self.cursor = self.__cursor

    def __del__(self):
        self.__cursor.close()
        self.__db.close()
        self.__mysql_cursor.close()
        self.__mysql.close()

    def switch_cusor(self, obj=1):
        self.cursor = self.cursor_list[obj]

    def create_mysql_conn(self):
        # # -------开始创建数据库全局对象--------
        conn = pymysql.connect(host=self.general_database['host'],
                               user=self.general_database['username'],
                               password=self.general_database['password'],
                               port=self.general_database['port'],
                               charset='utf8')
        cursor = conn.cursor()
        # self.cursor_list.append(cursor)
        return cursor, conn

    def create_credit_conn(self):
        # # -------初始化连接credit数据库-------
        db = pymysql.connect(host=self.credit_database['host'],
                             user=self.credit_database['username'],
                             port=self.credit_database['port'],
                             password=self.credit_database['password'],
                             database=self.credit_database['databaseName'],
                             charset='utf8'
                             )
        cursor = db.cursor()
        return cursor, db

    def select_table_column(self, table_name='credit_apply', database='hsit_credit'):
        column_key = []
        sql_column = "select COLUMN_NAME from information_schema.COLUMNS where table_name='{}' and table_schema='{}';".format(table_name, database)
        try:
            self.cursor.execute(sql_column)
        except Exception as e:
            print(e)
        res_column = self.cursor.fetchall()
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


if __name__ == '__main__':
    t = Mysql()

