# -*- coding: utf-8 -*-
"""
    Function: 理赔/回购文件生成
"""
from engine.EnvInit import EnvInit
from src.enums.EnumYinLiu import EnumFileType
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils.KS3 import KS3
from utils.Logger import Logs
from src.enums.EnumsCommon import *
from src.impl.common.CommonBizImpl import *

_log = Logs()
_ProjectPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # 项目根目录
_FilePath = os.path.join(_ProjectPath, 'FilePath', ProductEnum.YINLIU.value, TEST_ENV_INFO)  # 文件存放目录
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


class YinLiuRepayFile(EnvInit):
    def __init__(self, userData, productId, loanInvoiceId=None, repayTermNo='1', repayDate="2021-08-06"):
        """
        eg: 账单日还款
        @param userData:           用户四要素   必填参数
        @param productId:          产品ID
        @param loanInvoiceId:      借据号
        @param repayTermNo:        还款期次    必填参数
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
        self.productId = productId

        # 理赔文件 键值对字典数据模板
        self.bankClaimTemple = {
            'loan_no': '',  # 借据号
            'name': self.userData['name'],  # 姓名
            'cer_no': self.userData['cer_no'],  # 身份证号
            'current_period': self.repayTermNo,  # 期次
            'repay_amt': '',  # 代偿总额
            'repay_date': '',  # 代偿日期
            'business_no': str(int(round(time.time() * 1000))) + str(random.randint(0, 9999)),  # 流水号
            'product_id': productId,  # 产品号
            'type_flag': '1',  # 类型标志
            'loan_amt': '',  # 贷款总金额
            'loan_period': '',  # 贷款总期次
            'loan_date': '',  # 放款时间
            'paid_prin_amt': '',  # 本金
            'paid_int_amt': '',  # 利息
            'left_repay_amt': ''  # 在贷余额
        }

        # 引流回购通用文件 键值对字典数据模板
        self.bankBuyBackTemple = {
            'loan_no': '',  # 借据号
            'name': self.userData['name'],  # 姓名
            'cer_no': self.userData['cer_no'],  # 身份证号
            'current_period': self.repayTermNo,  # 期次
            'repay_amt': '',  # 代偿总额
            'repay_date': '',  # 代偿日期
            'business_no': str(int(round(time.time() * 1000))) + str(random.randint(0, 9999)),  # 流水号
            'product_id': productId,  # 产品号
            'type_flag': '2',  # 类型标志
            'loan_amt': '',  # 贷款总金额
            'loan_period': '',  # 贷款总期次
            'loan_date': '',  # 放款时间
            'paid_prin_amt': '',  # 本金
            'paid_int_amt': '',  # 利息
            'left_repay_amt': ''  # 在贷余额
        }

        # 海尔回购文件 键值对字典数据模板
        self.hairBuyBackTemple = {
            'loan_no': '',  # 借据号
            'name': self.userData['name'],  # 姓名
            'cer_no': self.userData['cer_no'],  # 身份证号
            'current_period': self.repayTermNo,  # 期次
            'repay_amt': '',  # 代偿总额
            'repay_date': '',  # 代偿日期
            'business_no': str(int(round(time.time() * 1000))) + str(random.randint(0, 9999)),  # 流水号
            'product_id': productId,  # 产品代码
            'type_flag': '2',  # 类型标志
            'loan_amt': '',  # 贷款总金额
            'loan_period': '',  # 贷款总期次
            'loan_date': '',  # 放款时间
            'compensationPrincipal': '',  # 本金
            'compensationInterest': '',  # 利息
            'loanBalance': '',  # 在贷余额  用户级
            'compensationOverdueFee': '',  # 代偿罚息
            'compensationFee': '',  # 代偿违约金
            'handler_status': ''  # 是否贴息 0:未贴息 1:已贴息 EnumBool.YES'
        }

        # 海尔贴息文件 键值对字典数据模板
        self.hairDisInterestTemple = {
            'loanNo': '',  # 借据号
            'repayDate': '',  # 代偿日期
            'repayTermNo': self.repayTermNo,  # 期次
            'productId': productId,  # 产品代码
            'subProductId': '',  # 子产品代码
            'merchantId': '',  # 商户号
            'preInterest': '',  # 利息
        }

    def uploadFile(self, fileType, assetFilePath):
        """
        @param fileType: EnumFileType枚举内容
        @param assetFilePath: 资产文件类型存放路径
        @return:
        """
        # 遍历需要上传的文件
        localPath = self.getLocalFilePath(fileType)
        remote = os.path.join(ks3_asset_path[EnumAppName.ASSET.value], assetFilePath, self.repayDate.split('-')[0],
                              self.repayDate.split('-')[1], self.repayDate.split('-')[2])

        fileList = []
        remoteList = []
        for root, dirs, files in os.walk(localPath):
            for file in files:
                fileList.append(os.path.join(localPath, file))
                remoteList.append(format_path(remote) + "/" + file)
        for local, remote in zip(fileList, remoteList):
            self.ks3.upload_file(local, remote)

    # 获取本地文件存放路径
    def getLocalFilePath(self, fileType):
        """
        @param fileType: 文件类型
        @return: 本地文件存放路径
        """
        # 初始化文件存放路径，(用户_身份证号)
        data_save_path = '%s_%s' % (
            self.userData['name'], self.userData['cer_no'])
        data_save_path = os.path.join(_FilePath, data_save_path, self.repayDate.replace('-', ''))
        if not os.path.exists(data_save_path):
            os.makedirs(data_save_path)
        # 文件所属文件夹不存在则创建
        localFilePath = os.path.join(data_save_path, fileType)
        if not os.path.exists(localFilePath):
            os.makedirs(localFilePath)
        return localFilePath

    # 获取本地文件名称
    def getLocalFileName(self, filePath, fileType):
        """
        @param filePath: 本地文件路径
        @param fileType: 文件类型
        @return: 本地文件名称
        """
        localFileName = os.path.join(filePath, '{}-{}.txt'.format(self.repayDate.replace('-', ''), fileType))
        return localFileName

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
            key2 = "user_name = '{}' and certificate_no ='{}'".format(self.userData['name'],self.userData['cer_no'])
            sqlCreditLoanInvoice = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key2)
        return sqlCreditLoanInvoice

    # 理赔文件生成
    def creditClaimFile(self):
        """
        @return:
        """
        temple = {}
        # 初始化理赔文件
        localFilePath = self.getLocalFilePath(EnumFileType.CLAIM_FILE.fileType)
        claimFileName = self.getLocalFileName(localFilePath, EnumFileType.CLAIM_FILE.fileType)
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
        self.uploadFile(fileType=EnumFileType.CLAIM_FILE.fileType, assetFilePath=EnumFileType.CLAIM_FILE.folderName)

    # 回购文件生成
    def creditBuyBackFile(self):
        """
        @return:
        """
        temple = {}
        # 初始化文件
        localFilePath = self.getLocalFilePath(EnumFileType.BUYBACK_FILE.fileType)
        buyBackFileName = self.getLocalFileName(localFilePath, EnumFileType.BUYBACK_FILE.fileType)
        if os.path.exists(buyBackFileName):
            os.remove(buyBackFileName)
        # 获取用户借据信息
        creditLoanInvoiceInfo = self.getInvoiceInfo()
        loanInvoiceId = creditLoanInvoiceInfo['loan_invoice_id']

        # 组装回购内容
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
        self.uploadFile(fileType=EnumFileType.BUYBACK_FILE.fileType, assetFilePath=EnumFileType.BUYBACK_FILE.folderName)

    # 海尔贴息文件生成
    def creditDisInterestFile(self):
        """
        @return:
        """
        temple = {}
        # 初始化理赔文件
        localFilePath = self.getLocalFilePath(EnumFileType.DIS_INTEREST_FILE.fileType)
        disInterestFileName = self.getLocalFileName(localFilePath, EnumFileType.DIS_INTEREST_FILE.fileType)
        if os.path.exists(disInterestFileName):
            os.remove(disInterestFileName)
        # 获取用户借据信息
        creditLoanInvoiceInfo = self.getInvoiceInfo()
        loanInvoiceId = creditLoanInvoiceInfo['loan_invoice_id']

        # 根据借据Id和期次获取资产侧还款计划
        key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loanInvoiceId, self.repayTermNo)
        asset_repay_plan = self.MysqlBizImpl.get_asset_data_info(table="asset_repay_plan", key=key3)

        temple['repayDate'] = self.repayDate.replace('-', '')
        temple['loanNo'] = loanInvoiceId
        temple['preInterest'] = str(asset_repay_plan["left_repay_interest"])  # 利息
        temple['subProductId'] = self.productId if self.productId == ProductIdEnum.HAIR_DISCOUNT.value else ProductIdEnum.HAIR.value  # 子产品号
        temple['merchantId'] = EnumMerchantId.HAIR.value  # 商户号

        # 文件赋值
        self.hairDisInterestTemple.update(temple)

        # 开始写入文件内容
        write_repay_file(disInterestFileName, **self.hairDisInterestTemple)

        # 开始上传文件到ks3
        self.uploadFile(fileType=EnumFileType.DIS_INTEREST_FILE.fileType, assetFilePath=EnumFileType.DIS_INTEREST_FILE.folderName)

    # 海尔回购文件生成
    def creditHairDisBuyBackFile(self):
        """
        @return:
        """
        # 初始化文件
        localFilePath = self.getLocalFilePath(EnumFileType.DIS_BUYBACK_FILE.fileType)
        buyBackFileName = self.getLocalFileName(localFilePath, EnumFileType.DIS_BUYBACK_FILE.fileType)
        if os.path.exists(buyBackFileName):
            os.remove(buyBackFileName)
        # 获取借据总期数
        totalTerm = self.getInvoiceInfo()['installment_num']
        # 依次写入回购所有期次还款数据
        termNo = int(self.repayTermNo)
        while int(totalTerm) >= termNo:
            # 文件赋值
            self.hairBuyBackTemple.update(self.creditHairBuyBackData(termNo))
            # 开始写入文件内容
            write_repay_file(buyBackFileName, **self.hairBuyBackTemple)
            termNo += 1

        # 开始上传文件到ks3
        self.uploadFile(fileType=EnumFileType.DIS_BUYBACK_FILE.fileType, assetFilePath=EnumFileType.DIS_BUYBACK_FILE.folderName)

    # 海尔预回购文件生成
    def creditHairDisPreBuyBackFile(self):
        """
        @return:
        """
        # 初始化文件
        localFilePath = self.getLocalFilePath(EnumFileType.DIS_PRE_BUYBACK_FILE.fileType)
        buyBackFileName = self.getLocalFileName(localFilePath, EnumFileType.DIS_PRE_BUYBACK_FILE.fileType)
        if os.path.exists(buyBackFileName):
            os.remove(buyBackFileName)
        # 获取借据总期数
        totalTerm = self.getInvoiceInfo()['installment_num']
        # 依次写入回购所有期次还款数据
        termNo = int(self.repayTermNo)
        while int(totalTerm) >= termNo:
            # 文件赋值
            self.hairBuyBackTemple.update(self.creditHairBuyBackData(termNo))
            # 开始写入文件内容
            write_repay_file(buyBackFileName, **self.hairBuyBackTemple)
            termNo += 1

        # 开始上传文件到ks3
        self.uploadFile(fileType=EnumFileType.DIS_BUYBACK_FILE.fileType, assetFilePath=EnumFileType.DIS_BUYBACK_FILE.folderName)

    # 海尔回购文件生成
    def creditHairBuyBackData(self, termNo):
        """
        productId: G23E041:disPreBuyBack预回购文件； G23E042:disBuyBack回购文件
        @return:
        """
        temple = {}
        # 获取用户借据信息
        creditLoanInvoiceInfo = self.getInvoiceInfo()
        loanInvoiceId = creditLoanInvoiceInfo['loan_invoice_id']

        # 组装回购内容
        totalTerm = creditLoanInvoiceInfo['installment_num']
        temple['repay_date'] = self.repayDate.replace('-', '')
        temple['loan_no'] = loanInvoiceId
        temple['loan_period'] = totalTerm
        temple['loan_amt'] = creditLoanInvoiceInfo['loan_amount']
        temple['loan_date'] = str(creditLoanInvoiceInfo['loan_pay_time']).split()[0].replace('-', '')
        # 根据借据Id和期次获取资产侧还款计划
        key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loanInvoiceId, str(termNo))
        asset_repay_plan = self.MysqlBizImpl.get_asset_data_info(table="asset_repay_plan", key=key3)
        temple['repay_amt'] = str(asset_repay_plan["left_repay_principal"])  # 总金额
        temple['compensationPrincipal'] = str(asset_repay_plan["left_repay_principal"])  # 本金
        temple['compensationInterest'] = str(asset_repay_plan["left_repay_interest"])  # 利息
        temple['loanBalance'] = str(asset_repay_plan["before_calc_principal"])  # 在贷余额
        temple['compensationOverdueFee'] = str(asset_repay_plan["left_repay_overdue_fee"])  # 罚息
        temple['compensationFee'] = str(asset_repay_plan["left_repay_fee"])  # 费用
        temple['business_no'] = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))  # 流水号
        temple['current_period'] = str(termNo)  # 期次
        temple['handler_status'] = "1" if self.productId == ProductIdEnum.HAIR_DISCOUNT.value else "0"  # 是否贴息
        return temple


if __name__ == '__main__':
    # 美团按期还款、提前结清，按日收息
    data1 = {'name': '汲半芹', 'cer_no': '430224199608242714', 'telephone': '17157209368',
             'bankid': '6215591662020086765'}  # hqas
    t = YinLiuRepayFile(data1, "G23E011", repayTermNo='5', repayDate='2022-05-24')
    # t.creditClaimFile()
    t.creditBuyBackFile()
    # t.bill_day_repay_file(repay_term_no='2')
    # t.pre_repay_file(repay_date="2022-04-01", repay_term_no='2')
    # t = MeiTuanLoanFile(data1, apply_date='2022-03-07')
