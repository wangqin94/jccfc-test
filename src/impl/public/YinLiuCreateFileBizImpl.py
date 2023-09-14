# -*- coding: utf-8 -*-
"""
    Function: 理赔/回购文件生成
"""
from src.enums.EnumYinLiu import EnumFileType
from src.enums.EnumsCommon import *
from src.impl.common.CommonBizImpl import *
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from src.test_data.module_data import Hair, WeiCai, HaLo, YiXin
from utils.KS3 import KS3
from utils.Logger import Logs

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
            key2 = "user_name = '{}' and certificate_no ='{}'".format(self.userData['name'], self.userData['cer_no'])
            sqlCreditLoanInvoice = self.MysqlBizImpl.get_credit_data_info(table="credit_loan_invoice", key=key2)
        return sqlCreditLoanInvoice

    # 海尔回购文件内容
    def creditHairBuyBackData(self, termNo):
        """
        productId: G23E041:disPreBuyBack预回购文件； G23E042:disBuyBack回购文件
        @return: 融担模式海尔回购对账文件数据
        """
        temple = {}
        # 获取用户借据信息
        creditLoanInvoiceInfo = self.getInvoiceInfo()
        loanInvoiceId = creditLoanInvoiceInfo['loan_invoice_id']

        # 组装回购内容
        totalTerm = creditLoanInvoiceInfo['installment_num']
        temple['repay_date'] = self.repayDate.replace('-', '')
        temple['loan_no'] = loanInvoiceId
        temple['name'] = self.userData['name']
        temple['cer_no'] = self.userData['cer_no']
        temple['product_id'] = ProductIdEnum.HAIR_DISCOUNT.value
        temple['loan_period'] = totalTerm
        temple['loan_amt'] = creditLoanInvoiceInfo['loan_amount']
        temple['loan_date'] = str(creditLoanInvoiceInfo['loan_pay_time']).split()[0].replace('-', '')
        # 根据借据Id和期次获取资产侧还款计划
        key3 = "loan_invoice_id = '{}' and current_num = '{}'".format(loanInvoiceId, str(termNo))
        asset_repay_plan = self.MysqlBizImpl.get_asset_data_info(table="asset_repay_plan", key=key3)
        temple['repay_amt'] = str(asset_repay_plan["left_repay_amount"])  # 总金额
        temple['compensationPrincipal'] = str(asset_repay_plan["left_repay_principal"])  # 本金
        temple['compensationInterest'] = str(asset_repay_plan["left_repay_interest"])  # 利息
        temple['loanBalance'] = str(asset_repay_plan["before_calc_principal"])  # 在贷余额
        temple['compensationOverdueFee'] = str(asset_repay_plan["left_repay_overdue_fee"])  # 罚息
        temple['compensationFee'] = str(asset_repay_plan["left_repay_fee"])  # 费用
        temple['business_no'] = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))  # 流水号
        temple['current_period'] = str(termNo)  # 期次
        temple['handler_status'] = "0"  # 是否贴息
        if self.productId == ProductIdEnum.HAIR_DISCOUNT.value:
            temple['handler_status'] = "1"
            self.log.demsg("贴息产品,利息查asset_repay_plan_merchant_interest表")
            asset_repay_plan = self.MysqlBizImpl.get_asset_database_info('asset_repay_plan_merchant_interest',
                                                                         loan_invoice_id=loanInvoiceId,
                                                                         current_num=termNo)
            temple['compensationInterest'] = str(asset_repay_plan["left_repay_interest"])  # 利息
            temple['repay_amt'] = round(float(temple['repay_amt']) + float(temple['compensationInterest']), 2)
        return temple

    # 理赔文件内容
    def creditClaimData(self):
        """
        @return:融担模式理赔对账文件数据-通用模板
        """
        claimTemple = {}
        # 获取用户借据信息
        creditLoanInvoiceInfo = self.getInvoiceInfo()
        loanInvoiceId = creditLoanInvoiceInfo['loan_invoice_id']
        asset_repay_plan = self.MysqlBizImpl.get_asset_database_info("asset_repay_plan", loan_invoice_id=loanInvoiceId,
                                                                     current_num=self.repayTermNo)
        # 组装理赔文件内容
        claimTemple['name'] = self.userData['name']
        claimTemple['cer_no'] = self.userData['cer_no']
        claimTemple['current_period'] = self.repayTermNo
        claimTemple['business_no'] = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))  # 流水号
        claimTemple['product_id'] = self.productId
        claimTemple['repay_date'] = self.repayDate.replace('-', '')
        claimTemple['loan_no'] = loanInvoiceId
        claimTemple['loan_period'] = creditLoanInvoiceInfo['installment_num']
        claimTemple['loan_amt'] = creditLoanInvoiceInfo['loan_amount']
        claimTemple['loan_date'] = str(creditLoanInvoiceInfo['loan_pay_time']).split()[0].replace('-', '')
        claimTemple['repay_amt'] = str(asset_repay_plan["left_repay_amount"])  # 总金额
        claimTemple['paid_prin_amt'] = str(asset_repay_plan["left_repay_principal"])  # 本金
        claimTemple['paid_int_amt'] = str(asset_repay_plan["left_repay_interest"])  # 利息
        claimTemple['left_repay_amt'] = str(asset_repay_plan["before_calc_principal"])  # 在贷余额
        claimTemple['compensationOverdueFee'] = str(asset_repay_plan["left_repay_overdue_fee"])  # 罚息
        return claimTemple

    # 回购文件内容
    def creditBuyBackData(self, termNo):
        """
        @param termNo: 期次
        @return: 融担模式回购对账文件数据-通用模板
        """
        buyBackTemple = {}
        # 获取用户借据信息
        creditLoanInvoiceInfo = self.getInvoiceInfo()
        loanInvoiceId = creditLoanInvoiceInfo['loan_invoice_id']
        asset_repay_plan = self.MysqlBizImpl.get_asset_database_info("asset_repay_plan", loan_invoice_id=loanInvoiceId,
                                                                     current_num=termNo)
        # 组装理赔文件内容
        buyBackTemple['name'] = self.userData['name']
        buyBackTemple['cer_no'] = self.userData['cer_no']
        buyBackTemple['current_period'] = termNo
        buyBackTemple['business_no'] = str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))  # 流水号
        buyBackTemple['product_id'] = self.productId
        buyBackTemple['repay_date'] = self.repayDate.replace('-', '')
        buyBackTemple['loan_no'] = loanInvoiceId
        buyBackTemple['loan_period'] = creditLoanInvoiceInfo['installment_num']
        buyBackTemple['loan_amt'] = creditLoanInvoiceInfo['loan_amount']
        buyBackTemple['loan_date'] = str(creditLoanInvoiceInfo['loan_pay_time']).split()[0].replace('-', '')
        buyBackTemple['repay_amt'] = str(asset_repay_plan["left_repay_principal"])  # 总金额
        buyBackTemple['paid_prin_amt'] = str(asset_repay_plan["left_repay_principal"])  # 本金
        buyBackTemple['paid_int_amt'] = 0  # 利息
        buyBackTemple['left_repay_amt'] = str(asset_repay_plan["before_calc_principal"])  # 在贷余额
        buyBackTemple['compensationOverdueFee'] = str(asset_repay_plan["left_repay_overdue_fee"])  # 罚息
        return buyBackTemple

    # 贴息文件内容
    def creditDisInterestData(self):
        """
        @return: 融担模式贴息对账文件数据-通用模板
        """
        DisInterestTemple = {}
        # 获取用户借据信息
        creditLoanInvoiceInfo = self.getInvoiceInfo()
        loanInvoiceId = creditLoanInvoiceInfo['loan_invoice_id']
        asset_repay_plan = self.MysqlBizImpl.get_asset_database_info("asset_repay_plan_merchant_interest",
                                                                     loan_invoice_id=loanInvoiceId,
                                                                     current_num=self.repayTermNo)
        # 组装贴息文件内容
        DisInterestTemple['repayDate'] = self.repayDate.replace('-', '')
        DisInterestTemple['loanNo'] = loanInvoiceId
        DisInterestTemple['repayTermNo'] = self.repayTermNo
        DisInterestTemple['preInterest'] = str(asset_repay_plan["left_repay_interest"])  # 利息
        DisInterestTemple['merchantId'] = EnumMerchantId.HAIR.value  # 商户号
        DisInterestTemple['productId'] = self.productId  # 产品号
        return DisInterestTemple

    # 理赔文件生成
    def creditClaimFile(self, **kwargs):
        """
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: 融担模式通用版本-理赔文件
        """
        # 初始化理赔文件
        localFilePath = self.getLocalFilePath(EnumFileType.CLAIM_FILE.fileType)
        claimFileName = self.getLocalFileName(localFilePath, EnumFileType.CLAIM_FILE.fileType)
        if os.path.exists(claimFileName):
            os.remove(claimFileName)
        # 获取理赔对账文件模板参数-哈啰为通用模板标准
        templePath = HaLo.HaLo
        claimTemple = templePath['haloClaimTemple']
        # 文件赋值
        self.creditClaimData().update(**kwargs)
        payload = DataUpdate(claimTemple, **self.creditClaimData()).parser
        self.log.demsg("待写入理赔文件数据：{}".format(payload))
        # 开始写入文件内容
        write_repay_file(claimFileName, **payload)

        # 开始上传文件到ks3
        self.uploadFile(fileType=EnumFileType.CLAIM_FILE.fileType, assetFilePath=EnumFileType.CLAIM_FILE.folderName)

    # 微财理赔文件生成
    def creditWeiCaiClaimFile(self, **kwargs):
        """
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: 融担模式微财理赔对账文件
        """
        # 初始化理赔文件
        localFilePath = self.getLocalFilePath(EnumFileType.CLAIM_FILE.fileType)
        claimFileName = self.getLocalFileName(localFilePath, EnumFileType.CLAIM_FILE.fileType)
        if os.path.exists(claimFileName):
            os.remove(claimFileName)
        # 获取微财理赔对账文件参数
        templePath = WeiCai.WeiCai
        wcClaimTemple = templePath['weiCaiClaimTemple']

        # 文件赋值
        self.creditClaimData().update(**kwargs)
        payload = DataUpdate(wcClaimTemple, **self.creditClaimData()).parser
        self.log.demsg("待写入理赔文件数据：{}".format(payload))
        # 开始写入文件内容
        write_repay_file(claimFileName, **payload)

        # 开始上传文件到ks3
        self.uploadFile(fileType=EnumFileType.CLAIM_FILE.fileType, assetFilePath=EnumFileType.CLAIM_FILE.folderName)

    # 微财理赔文件生成
    def creditYiXinClaimFile(self, **kwargs):
        """
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: 融担模式微财理赔对账文件
        """
        # 初始化理赔文件
        localFilePath = self.getLocalFilePath(EnumFileType.CLAIM_FILE.fileType)
        claimFileName = self.getLocalFileName(localFilePath, EnumFileType.CLAIM_FILE.fileType)
        if os.path.exists(claimFileName):
            os.remove(claimFileName)
        # 获取微财理赔对账文件参数
        templePath = YiXin.YiXin
        wcClaimTemple = templePath['weiCaiClaimTemple']

        # 文件赋值
        self.creditClaimData().update(**kwargs)
        payload = DataUpdate(wcClaimTemple, **self.creditClaimData()).parser
        self.log.demsg("待写入理赔文件数据：{}".format(payload))
        # 开始写入文件内容
        write_repay_file(claimFileName, **payload)

        # 开始上传文件到ks3
        self.uploadFile(fileType=EnumFileType.CLAIM_FILE.fileType, assetFilePath=EnumFileType.CLAIM_FILE.folderName)

    # 微财回购文件生成
    def creditWeiCaiBuyBackFile(self):
        """
        @return: 融担模式微财回购对账文件
        """
        # 初始化文件
        localFilePath = self.getLocalFilePath(EnumFileType.BUYBACK_FILE.fileType)
        buyBackFileName = self.getLocalFileName(localFilePath, EnumFileType.BUYBACK_FILE.fileType)
        if os.path.exists(buyBackFileName):
            os.remove(buyBackFileName)
        # 获取微财理赔对账文件参数
        templePath = WeiCai.WeiCai
        buyBackTemple = templePath['weiCaiBuyBackTemple']
        # 获取借据总期数
        totalTerm = self.getInvoiceInfo()['installment_num']
        creditLoanInvoiceInfo = self.getInvoiceInfo()
        loanInvoiceId = creditLoanInvoiceInfo['loan_invoice_id']
        # 依次写入回购所有期次还款数据
        termNo = int(self.repayTermNo)
        while int(totalTerm) >= termNo:
            # 获取当期还款计划
            creditBuyBackData = self.creditBuyBackData(termNo)
            asset_repay_plan = self.MysqlBizImpl.get_asset_database_info("asset_repay_plan",
                                                                         loan_invoice_id=loanInvoiceId,
                                                                         current_num=termNo)
            # 获取回购当期已计提利息
            if termNo == int(self.repayTermNo):
                days = get_day(asset_repay_plan['start_date'], self.repayDate)
                creditBuyBackData['paid_int_amt'] = getDailyAccrueInterest(self.productId, days, asset_repay_plan['left_principal'])
                creditBuyBackData['repay_amt'] = float(creditBuyBackData['paid_prin_amt']) + creditBuyBackData['paid_int_amt']

            payload = DataUpdate(buyBackTemple, **creditBuyBackData).parser
            # 开始写入文件内容
            write_repay_file(buyBackFileName, **payload)
            termNo += 1

        # 开始上传文件到ks3
        self.uploadFile(fileType=EnumFileType.BUYBACK_FILE.fileType, assetFilePath=EnumFileType.BUYBACK_FILE.folderName)

    # 微财回购文件生成
    def creditYiXinBuyBackFile(self):
        """
        @return: 融担模式微财回购对账文件
        """
        # 初始化文件
        localFilePath = self.getLocalFilePath(EnumFileType.BUYBACK_FILE.fileType)
        buyBackFileName = self.getLocalFileName(localFilePath, EnumFileType.BUYBACK_FILE.fileType)
        if os.path.exists(buyBackFileName):
            os.remove(buyBackFileName)
        # 获取微财理赔对账文件参数
        templePath = YiXin.YiXin
        buyBackTemple = templePath['weiCaiBuyBackTemple']
        # 获取借据总期数
        totalTerm = self.getInvoiceInfo()['installment_num']
        creditLoanInvoiceInfo = self.getInvoiceInfo()
        loanInvoiceId = creditLoanInvoiceInfo['loan_invoice_id']
        # 依次写入回购所有期次还款数据
        termNo = int(self.repayTermNo)
        while int(totalTerm) >= termNo:
            # 获取当期还款计划
            creditBuyBackData = self.creditBuyBackData(termNo)
            asset_repay_plan = self.MysqlBizImpl.get_asset_database_info("asset_repay_plan",
                                                                         loan_invoice_id=loanInvoiceId,
                                                                         current_num=termNo)
            # 获取回购当期已计提利息
            if termNo == int(self.repayTermNo):
                days = get_day(asset_repay_plan['start_date'], self.repayDate)
                creditBuyBackData['paid_int_amt'] = getDailyAccrueInterest(self.productId, days, creditBuyBackData['paid_prin_amt'])
                creditBuyBackData['repay_amt'] = float(creditBuyBackData['paid_prin_amt']) + creditBuyBackData['paid_int_amt']

            payload = DataUpdate(buyBackTemple, **creditBuyBackData).parser
            # 开始写入文件内容
            write_repay_file(buyBackFileName, **payload)
            termNo += 1

        # 开始上传文件到ks3
        self.uploadFile(fileType=EnumFileType.BUYBACK_FILE.fileType, assetFilePath=EnumFileType.BUYBACK_FILE.folderName)

    # 回购文件生成
    def creditBuyBackFile(self, **kwargs):
        """
        @param kwargs: 需要临时装填的字段以及值 eg: key=value
        @return: 融担模式回购对账文件-通用模板
        """

        # 初始化文件
        localFilePath = self.getLocalFilePath(EnumFileType.BUYBACK_FILE.fileType)
        buyBackFileName = self.getLocalFileName(localFilePath, EnumFileType.BUYBACK_FILE.fileType)
        if os.path.exists(buyBackFileName):
            os.remove(buyBackFileName)

        # 获取回购对账文件模板参数-哈啰为通用模板标准
        templePath = HaLo.HaLo
        buyBackTemple = templePath['haloBuyBackTemple']
        totalTerm = self.getInvoiceInfo()['installment_num']  # 获取借据总期数
        # 依次写入回购所有期次还款数据
        termNo = int(self.repayTermNo)
        while int(totalTerm) >= termNo:
            # 文件赋值
            self.creditBuyBackData(termNo).update(**kwargs)
            payload = DataUpdate(buyBackTemple, **self.creditBuyBackData(termNo)).parser
            # 开始写入文件内容
            write_repay_file(buyBackFileName, **payload)
            termNo += 1

        # 开始上传文件到ks3
        self.uploadFile(fileType=EnumFileType.BUYBACK_FILE.fileType, assetFilePath=EnumFileType.BUYBACK_FILE.folderName)

    # 海尔贴息文件生成
    def creditHairDisInterestFile(self, **kwargs):
        """
        @return: 融担模式海尔贴息对账文件
        """
        # 初始化理赔文件
        localFilePath = self.getLocalFilePath(EnumFileType.DIS_INTEREST_FILE.fileType)
        disInterestFileName = self.getLocalFileName(localFilePath, EnumFileType.DIS_INTEREST_FILE.fileType)
        if os.path.exists(disInterestFileName):
            os.remove(disInterestFileName)
        # 获取海尔贴息对账文件参数
        templePath = Hair.Hair
        hairDisInterestTemple = templePath['hairDisInterestTemple']

        hairDisInterestTemple[
            'subProductId'] = self.productId if self.productId == ProductIdEnum.HAIR_DISCOUNT.value else ProductIdEnum.HAIR.value  # 子产品号

        # 文件赋值
        self.creditDisInterestData().update(**kwargs)
        payload = DataUpdate(hairDisInterestTemple, **self.creditDisInterestData()).parser
        self.log.demsg("待写入海尔贴息文件数据：{}".format(payload))
        # 开始写入文件内容
        write_repay_file(disInterestFileName, **hairDisInterestTemple)

        # 开始上传文件到ks3
        self.uploadFile(fileType=EnumFileType.DIS_INTEREST_FILE.fileType,
                        assetFilePath=EnumFileType.DIS_INTEREST_FILE.folderName)

    # 海尔回购文件生成
    def creditHairDisBuyBackFile(self):
        """
        @return: 融担模式海尔回购对账文件
        """
        # 初始化文件
        localFilePath = self.getLocalFilePath(EnumFileType.DIS_BUYBACK_FILE.fileType)
        buyBackFileName = self.getLocalFileName(localFilePath, EnumFileType.DIS_BUYBACK_FILE.fileType)
        if os.path.exists(buyBackFileName):
            os.remove(buyBackFileName)

        # 获取海尔回购对账文件参数
        templePath = Hair.Hair
        hairBuyBackTemple = templePath['hairBuyBackTemple']
        # 获取借据总期数
        totalTerm = self.getInvoiceInfo()['installment_num']
        # 依次写入回购所有期次还款数据
        termNo = int(self.repayTermNo)
        while int(totalTerm) >= termNo:
            # 文件赋值
            hairBuyBackTemple.update(self.creditHairBuyBackData(termNo))
            # 开始写入文件内容
            write_repay_file(buyBackFileName, **hairBuyBackTemple)
            termNo += 1

        # 开始上传文件到ks3
        self.uploadFile(fileType=EnumFileType.DIS_BUYBACK_FILE.fileType,
                        assetFilePath=EnumFileType.DIS_BUYBACK_FILE.folderName)

    # 海尔预回购文件生成
    def creditHairDisPreBuyBackFile(self):
        """
        @return: 融担模式海尔预回购对账文件
        """
        # 初始化文件
        localFilePath = self.getLocalFilePath(EnumFileType.DIS_PRE_BUYBACK_FILE.fileType)
        buyBackFileName = self.getLocalFileName(localFilePath, EnumFileType.DIS_PRE_BUYBACK_FILE.fileType)
        if os.path.exists(buyBackFileName):
            os.remove(buyBackFileName)
        # 获取预海尔回购对账文件参数
        templePath = Hair.Hair
        hairBuyBackTemple = templePath['hairBuyBackTemple']
        # 获取借据总期数
        totalTerm = self.getInvoiceInfo()['installment_num']
        # 依次写入回购所有期次还款数据
        termNo = int(self.repayTermNo)
        while int(totalTerm) >= termNo:
            # 文件赋值
            hairBuyBackTemple.update(self.creditHairBuyBackData(termNo))
            # 开始写入文件内容
            write_repay_file(buyBackFileName, **hairBuyBackTemple)
            termNo += 1

        # 开始上传文件到ks3
        self.uploadFile(fileType=EnumFileType.DIS_PRE_BUYBACK_FILE.fileType,
                        assetFilePath=EnumFileType.DIS_PRE_BUYBACK_FILE.folderName)


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
