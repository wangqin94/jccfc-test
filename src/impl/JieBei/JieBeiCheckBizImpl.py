# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：JieBeiCheckBizImpl.py
@Author  ：jccfc
@Date    ：2022/07/06 15:55
"""
import time
from src.impl.JieBei.JieBeiBizImpl import JieBeiBizImpl

class JieBeiCheckBizImpl(JieBeiBizImpl):
    def __init__(self, data):
        super().__init__(data=data)

    def jiebei_check_feature_detail(self, feature_key, third_apply_no, m=20, t=3):
        self.log.demsg('开始检查特征取数明细...')
        sql = "select feature_value from channel_jiebei_feature_detail where feature_key = '{}' and apply_no = '{}'".\
            format(feature_key, third_apply_no)
        for i in range(m):
            info = self.MysqlBizImpl.mysql_op_channel.select(sql)
            try:
                feature_value = info[0][0]
                if feature_value == '1':
                    self.log.demsg('特征取数成功')
                    break
                elif feature_value == '0':
                    raise AssertionError('检验不符合期望，特征取数结果为拒绝')
                else:
                    self.log.demsg("处理中，请等待....")
                    time.sleep(t)
            except:
                self.log.demsg('特征取数明细未入库')
                time.sleep(t)










