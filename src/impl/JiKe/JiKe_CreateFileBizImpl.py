# -*- coding: utf-8 -*-
"""
    Function: 理赔/回购文件生成
"""
from engine.EnvInit import EnvInit
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils.KS3 import KS3
from utils.Logger import Logs
from src.enums.EnumsCommon import *
from src.impl.common.CommonBizImpl import *

_log = Logs()
_ProjectPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # 项目根目录
_FilePath = os.path.join(_ProjectPath, 'FilePath', ProductEnum.JIKE.value, TEST_ENV_INFO)  # 文件存放目录
if not os.path.exists(_FilePath):
    os.makedirs(_FilePath)


def write_repay_file(filename, **repay_temple):
    """
    @param repay_temple: 更新字段key（定义表字段）
    @param filename: 写入文件名
    @return:
    """
    # 写入单期还款文件
    val_list = map(str, [value for key, value in repay_temple.items()])
    strs = '|'.join(val_list)
    with open(filename, 'a+', encoding='utf-8') as f:
        f.write(strs)
        f.write('\n')


class JiKeRepayFile(EnvInit):
    def __init__(self, userData, loanInvoiceId=None, repayTermNo='1', repayDate="2021-08-06"):
        """
        eg: 账单日还款
        @param userData:           用户四要素   必填参数
        @param loanInvoiceId:     借据号
        @param repayTermNo:       还款期次    必填参数
        """
        super().__init__()
        self.log.demsg('当前测试环境 %s', self.env)
        # 初始化ks3连接
        self.ks3 = KS3()
        self.MysqlBizImpl = MysqlBizImpl()
        self.loanInvoiceId = loanInvoiceId
        self.userData = userData
        self.repayTermNo = repayTermNo
        self.repayDate = repayDate

        # 理赔文件 键值对字典数据模板
        self.bankClaimTemple = {
            'loan_no': '',  # 借据号
            'name': self.userData['name'],  # 姓名
            'cer_no': self.userData['cer_no'],  # 身份证号
            'current_period': self.repayTermNo,  # 期次
            'repay_amt': '',  # 代偿总额
            'repay_date': '',  # 代偿日期
            'business_no': str(int(round(time.time() * 1000))) + str(random.randint(0, 9999)),  # 流水号
            'product_id': 'G22E021',  # 商户号
            'type_flag': '1',  # 类型标志
            'loan_amt': '',  # 贷款总金额
            'loan_period': '',  # 贷款总期次
            'loan_date': '',  # 放款时间
            'paid_prin_amt': '',  # 本金
            'paid_int_amt': '',  # 利息
            'left_repay_amt': ''  # 在贷余额
        }

        # bank_repay_loan 键值对字典数据模板
        self.bankBuyBackTemple = {
            'loan_no': '',  # 借据号
            'name': self.userData['name'],  # 姓名
            'cer_no': self.userData['cer_no'],  # 身份证号
            'current_period': self.repayTermNo,  # 期次
            'repay_amt': '',  # 代偿总额
            'repay_date': '',  # 代偿日期
            'business_no': str(int(round(time.time() * 1000))) + str(random.randint(0, 9999)),  # 流水号
            'product_id': 'G22E021',  # 商户号
            'type_flag': '2',  # 类型标志
            'loan_amt': '',  # 贷款总金额
            'loan_period': '',  # 贷款总期次
            'loan_date': '',  # 放款时间
            'paid_prin_amt': '',  # 本金
            'paid_int_amt': '',  # 利息
            'left_repay_amt': ''  # 在贷余额
        }

        # # 执行文件生成上传SFTP服务器
        # self.start()

    def uploadFile(self, fileType):
        """
        @param fileType: 文件类型 0:理赔文件 1:回购文件
        @return:
        """
        # 遍历需要上传的文件
        filePath = "claimPath" if fileType == 0 else "bayBackPath"
        loaclPath = self.get_filename(self.repayDate)[filePath]
        remote = os.path.join(ks3_asset_path['jike'][filePath], self.repayDate.split('-')[0],
                              self.repayDate.split('-')[1], self.repayDate.split('-')[2])

        fileList = []
        remoteList = []
        for root, dirs, files in os.walk(loaclPath):
            for file in files:
                fileList.append(os.path.join(loaclPath, file))
                remoteList.append(format_path(remote) + "/" + file)
        for local, remote in zip(fileList, remoteList):
            self.ks3.upload_file(local, remote)

    # 获取文件存放路径
    def get_filename(self, repayDate):
        # 初始化文件存放路径，(用户_身份证号)
        data_save_path = '%s_%s' % (
            self.userData['name'], self.userData['cer_no'])
        data_save_path = os.path.join(_FilePath, data_save_path, repayDate.replace('-', ''))
        if not os.path.exists(data_save_path):
            os.makedirs(data_save_path)
        # 理赔文件
        claimPath = os.path.join(data_save_path, "claim")
        if not os.path.exists(claimPath):
            os.makedirs(claimPath)
        # 回购文件
        bayBackPath = os.path.join(data_save_path, "bayBack")
        if not os.path.exists(bayBackPath):
            os.makedirs(bayBackPath)
        # 理赔文件名
        claimFileName = os.path.join(claimPath, '%s-claim.txt' % repayDate.replace('-', ''))
        # 回购文件名
        buyBackFileName = os.path.join(bayBackPath, '%s-buyback.txt' % (repayDate.replace('-', '')))
        info = dict()
        info['data_save_path'] = data_save_path
        info['claimPath'] = claimPath
        info['bayBackPath'] = bayBackPath
        info['claimFileName'] = claimFileName
        info['buyBackFileName'] = buyBackFileName
        return info

    def getInvoiceInfo(self):
        """
        return: credit_loan_invoice表信息
        """
        # self.loan_invoice_id 为none 按照用户名取第一条借据信息，否则取当条借据信息
        if self.loanInvoiceId:
            loan_invoice_id = self.loanInvoiceId
            key1 = "loan_invoice_id = '{}'".format(loan_invoice_id)
            sqlCreditLoanInvoice = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key1)
        else:
            key2 = "user_name = '{}'".format(self.userData['name'])
            sqlCreditLoanInvoice = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key2)
        return sqlCreditLoanInvoice

    # 理赔文件生成
    def creditClaimFile(self):
        """
        @return:
        """
        temple = {}
        # 初始化理赔文件
        claimFileName = self.get_filename(self.repayDate)['claimFileName']
        if os.path.exists(claimFileName):
            os.remove(claimFileName)
        # 获取用户借据信息
        creditLoanInvoiceInfo = self.getInvoiceInfo()
        loanInvoiceId = creditLoanInvoiceInfo['loan_invoice_id']

        # 根据借据Id和期次获取资产侧还款计划
        key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loanInvoiceId, self.repayTermNo)
        asset_repay_plan = self.MysqlBizImpl.get_asset_data_info(table="asset_repay_plan", key=key3)

        temple['repay_date'] = self.repayDate.replace('-', '')
        temple['loan_no'] = loanInvoiceId
        temple['loan_period'] = creditLoanInvoiceInfo['installment_num']
        temple['loan_amt'] = creditLoanInvoiceInfo['loan_amount']
        temple['loan_date'] = str(creditLoanInvoiceInfo['loan_pay_time']).split()[0].replace('-', '')
        temple['paid_prin_amt'] = str(asset_repay_plan["pre_repay_principal"])  # 本金
        temple['paid_int_amt'] = str(asset_repay_plan["pre_repay_interest"])  # 利息
        temple['left_repay_amt'] = str(asset_repay_plan["before_calc_principal"])  # 在贷余额
        temple['repay_amt'] = str(asset_repay_plan["pre_repay_principal"] + asset_repay_plan["pre_repay_interest"])  # 总金额

        # 文件赋值
        self.bankClaimTemple.update(temple)

        # 开始写入文件内容
        write_repay_file(claimFileName, **self.bankClaimTemple)

        # 开始上传文件到ks3
        self.uploadFile(fileType=0)

    # 理赔文件生成
    def creditBuyBackFile(self):
        """
        @return:
        """
        temple = {}
        # 初始化文件
        buyBackFileName = self.get_filename(self.repayDate)['buyBackFileName']
        if os.path.exists(buyBackFileName):
            os.remove(buyBackFileName)
        # 获取用户借据信息
        creditLoanInvoiceInfo = self.getInvoiceInfo()
        loanInvoiceId = creditLoanInvoiceInfo['loan_invoice_id']

        # 根据借据Id和期次获取资产侧还款计划
        key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loanInvoiceId, self.repayTermNo)
        asset_repay_plan = self.MysqlBizImpl.get_asset_data_info(table="asset_repay_plan", key=key3)
        totalTerm = creditLoanInvoiceInfo['installment_num']
        temple['repay_date'] = self.repayDate.replace('-', '')
        temple['loan_no'] = loanInvoiceId
        temple['loan_period'] = totalTerm
        temple['loan_amt'] = creditLoanInvoiceInfo['loan_amount']
        temple['loan_date'] = str(creditLoanInvoiceInfo['loan_pay_time']).split()[0].replace('-', '')
        termNo = int(self.repayTermNo)
        while int(totalTerm) >= termNo:
            # 根据借据Id和期次获取资产侧还款计划
            key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loanInvoiceId, str(termNo))
            asset_repay_plan = self.MysqlBizImpl.get_asset_data_info(table="asset_repay_plan", key=key3)
            temple['repay_amt'] = str(asset_repay_plan["pre_repay_principal"])  # 总金额
            temple['paid_prin_amt'] = str(asset_repay_plan["pre_repay_principal"])  # 本金
            temple['paid_int_amt'] = '0'  # 利息
            temple['left_repay_amt'] = str(asset_repay_plan["before_calc_principal"])  # 在贷余额
            temple['business_no'] = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))  # 流水号
            temple['current_period'] = str(termNo)  # 期次

            # 文件赋值
            self.bankBuyBackTemple.update(temple)
            # 开始写入文件内容
            write_repay_file(buyBackFileName, **self.bankBuyBackTemple)
            termNo += 1

        # 开始上传文件到ks3
        self.uploadFile(fileType=1)


if __name__ == '__main__':
    # 美团按期还款、提前结清，按日收息
    data1 = {'name': '汲半芹', 'cer_no': '430224199608242714', 'telephone': '17157209368',
             'bankid': '6215591662020086765'}  # hqas
    t = JiKeRepayFile(data1, repayTermNo='5', repayDate='2022-05-24')
    # t.creditClaimFile()
    t.creditBuyBackFile()
    # t.bill_day_repay_file(repay_term_no='2')
    # t.pre_repay_file(repay_date="2022-04-01", repay_term_no='2')
    # t = MeiTuanLoanFile(data1, apply_date='2022-03-07')
