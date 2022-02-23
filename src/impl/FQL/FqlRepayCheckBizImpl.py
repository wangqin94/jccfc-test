from engine.EnvInit import EnvInit
from src.impl.common.MysqlBizImpl import MysqlBizImpl


class FqlRepayCheckBizImpl(EnvInit):
    def __init__(self):
        super().__init__()
        self.MysqlBizImpl = MysqlBizImpl()


    def updateBigacct(self, table, attr, **kwargs):
        self.MysqlBizImpl.update_bigacct_database_info(table, attr, **kwargs)

    def updateAssetDatabase(self, table, attr, **kwargs):
        self.MysqlBizImpl.update_asset_database_info(table, attr, **kwargs)

    def deleteSlice(self):
        self.MysqlBizImpl.delete_credit_database_info('credit_slice_batch_serial')
        self.MysqlBizImpl.delete_credit_database_info('credit_slice_batch_log')
        self.MysqlBizImpl.delete_asset_database_info('asset_slice_batch_serial')

    def queryAssetLoanInvoiceInfo(self, table, attr, **kwargs):
        loanInvoiceInfo = self.MysqlBizImpl.get_asset_database_info(table, **kwargs)
        return loanInvoiceInfo

    def check_credit_file_repay1(self,**kwargs):
        fileRepayInfo = self.MysqlBizImpl.get_credit_database_info('credit_file_repay', **kwargs)
        self.log.demsg(f"还款credit_file_repay数据库信息校验----：{fileRepayInfo}")
        assert fileRepayInfo['repay_flag'] == '1', "还款标志"
        assert fileRepayInfo['transfer_status'] == '1', "文件传输状态：1已处理"