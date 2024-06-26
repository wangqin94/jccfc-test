# -*- coding: utf-8 -*-
"""
test case script
"""
import os
import time
from src.impl.WLD.WldBizImpl import WldBizImpl
if not os.path.exists('person.py'):
    open('person.py', 'w')
from person import *
from utils.Logger import MyLog


class TestCase(object):
    def __init__(self):
        self.process()

    def preprocess(self):
        """ 预置条件处理 """
        pass

    # # [0: 绑卡, 3: 授信, 5: 支用, 6: 还款, 7: 绑卡&授信&支用]
    def process(self, flag=5):
        """ 测试步骤 """
        # 绑卡
        if flag == 0:
            wld = WldBizImpl(data=None)
            wld.bind_card()
            wld.confirm_bind_card()
            wld.credit(loanTerm=6, applyAmount=10000)

        # 绑卡查询
        elif flag == 1:
            wld = WldBizImpl(data=data)
            wld.query_bind_card()

        # 换卡
        elif flag == 2:
            wld = WldBizImpl()
            wld.update_card(loanInvoiceId='000LI5669354082158501976569', idNo='320723198806148818', repaymentAccountNo='6217220211797716769')

        # 授信
        elif flag == 3:
            wld = WldBizImpl(data=data)
            wld.credit(loanTerm=3, applyAmount=1000)

        # 授信查询
        elif flag == 4:
            wld = WldBizImpl(data=data)
            wld.credit_query()

        # 放款
        elif flag == 5:
            wld = WldBizImpl(data=data)
            wld.loan()

        # 支用查询
        elif flag == 5:
            wld = WldBizImpl(data=data)
            wld.loan_query()

        # 还款  repay_term_no还款期次   repay_type还款类型：1-按期还款，2-提前结清，4-逾期还款
        elif flag == 6:
            wld = WldBizImpl(data=data)
            wld.repay(repay_term_no="1", repay_type="1", loan_invoice_id="000LI0002137107007488200014",repay_date='2022-05-07')
            # wld.repay(repayAmount=685.90, repayPrincipal=685.90, repayInterest=0)

        # 上传文件
        elif flag == 8:
            wld = WldBizImpl(data=None)
            resp = wld.wld_file_upload('/credit/test', 'C:\\Users\\jccfc\\Desktop\\aaa.jpg')
            wld.wld_file_upload_result(resp['body']['seqNo'])

        # 下载文件
        elif flag == 9:
            wld = WldBizImpl(data=None)
            resp = wld.wld_file_download('/credit/test/idz-1.jpg', 'C:\\Users\\jccfc\\Desktop\\idz-1.jpg')
            wld.wld_file_upload_result(resp['body']['seqNo'])

        # 批量造数
        elif flag == 7:
            for i in range(1):
                wld = WldBizImpl(data=None)
                user_data = wld.bind_card()['data']
                wld.confirm_bind_card()
                wld.credit(loanTerm=6, applyAmount=1000)
                for n in range(10):
                    time.sleep(3)
                    status = wld.MysqlBizImpl.credit_apply_query(user_data)
                    if status == '03':
                        wld.loan()
                        wld.log.demsg('授信成功')
                        break
                    elif status == '04':
                        wld.log.error('授信失败,状态：{}'.format(status))
                        break
                    elif status == '02':
                        time.sleep(5)
                        wld.log.demsg("授信审批状态处理中，请等待....")
        return self

    def postprocess(self):
        """ 后置条件处理 """
        pass


if __name__ == '__main__':
    start_time = time.time()
    start = TestCase()
    total = time.time() - start_time
    log = MyLog().get_log()
    log.info('程序运行时间：{}'.format(round(total)))
