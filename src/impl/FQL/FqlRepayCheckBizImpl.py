from decimal import Decimal

from engine.EnvInit import EnvInit
from src.impl.common.MysqlBizImpl import MysqlBizImpl
from utils import GlobalVar as gl


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
        assert fileRepayInfo['repay_flag'] == gl.get_value('repay_plan')['repay_mode'], "还款标志"
        assert str(fileRepayInfo['repay_num']) == gl.get_value('repay_plan')['term_no']
        assert fileRepayInfo['repay_date'] == gl.get_value('repay_plan')['repay_date']
        assert str(Decimal(fileRepayInfo['repay_principal']).quantize(Decimal("0.00"))) == gl.get_value('repay_plan')['repay_amt']
        assert str(Decimal(fileRepayInfo['repay_interest']).quantize(Decimal("0.00"))) == gl.get_value('repay_plan')['paid_prin_amt']
        assert str(Decimal(fileRepayInfo['repay_penalty_interest']).quantize(Decimal("0.00"))) == gl.get_value('repay_plan')['paid_int_amt']
        assert fileRepayInfo['transfer_status'] == '1', "文件传输状态：1已处理"


    def credit_repay_order1(self,**kwargs):
        repayOrderDetail = self.MysqlBizImpl.get_credit_database_info('credit_repay_order_detail', **kwargs)
        self.log.demsg(f"还款credit_repay_order_detail数据库信息校验----：{repayOrderDetail}")
        assert repayOrderDetail['user_name'] == gl.get_value('personData')['name'], "客户姓名"
        assert repayOrderDetail['repay_status'] == '1', "还款状态"
        if gl.get_value('repay_plan')['repay_mode'] == '3':
           assert repayOrderDetail['repay_type'] == '2'
        else:
           assert repayOrderDetail['repay_type'] == '1'

        self.log.info("左边:{}".format(Decimal(repayOrderDetail['repay_amount']).quantize(Decimal("0.00"))))
        self.log.info("右边:{}".format(Decimal((float(gl.get_value('repay_plan')['repay_amt']) +float(gl.get_value('repay_plan')['paid_prin_amt']) + float(gl.get_value('repay_plan')['paid_int_amt']))).quantize(Decimal("0.00"))))

        assert Decimal(repayOrderDetail['repay_amount']).quantize(Decimal("0.00")) == Decimal((float(gl.get_value('repay_plan')['repay_amt']) +float(gl.get_value('repay_plan')['paid_prin_amt']) + float(gl.get_value('repay_plan')['paid_int_amt']))).quantize(Decimal("0.00"))
        assert str(Decimal(repayOrderDetail['repay_principal']).quantize(Decimal("0.00"))) == gl.get_value('repay_plan')['repay_amt']
        assert str(Decimal(repayOrderDetail['repay_interest']).quantize(Decimal("0.00"))) == gl.get_value('repay_plan')['paid_prin_amt']
        assert str(Decimal(repayOrderDetail['repay_penalty_interest']).quantize(Decimal("0.00"))) == gl.get_value('repay_plan')['paid_int_amt']
        assert str(Decimal(repayOrderDetail['repay_fee']).quantize(Decimal("0.00"))) == '0.00'

        assert Decimal(repayOrderDetail['actual_repay_amount']) .quantize(Decimal("0.00")) == Decimal((float(gl.get_value('repay_plan')['repay_amt']) + float(gl.get_value('repay_plan')['paid_prin_amt']) + float(gl.get_value('repay_plan')['paid_int_amt']))).quantize(Decimal("0.00"))
        assert str(Decimal(repayOrderDetail['actual_repay_principal']).quantize(Decimal("0.00"))) == gl.get_value('repay_plan')['repay_amt']
        assert str(Decimal(repayOrderDetail['actual_repay_interest']).quantize(Decimal("0.00"))) == gl.get_value('repay_plan')['paid_prin_amt']
        assert str(Decimal(repayOrderDetail['actual_repay_fee']).quantize(Decimal("0.00"))) == gl.get_value('repay_plan')['paid_int_amt']
        assert str(Decimal(repayOrderDetail['actual_repay_penalty_interest']).quantize(Decimal("0.00"))) == '0.00'

        assert str(repayOrderDetail['repay_term']) == gl.get_value('repay_plan')['term_no']

        repayOrderInfo = self.MysqlBizImpl.get_credit_database_info('credit_repay_order', repay_apply_id=repayOrderDetail['repay_apply_id'])
        self.log.demsg(f"还款credit_repay_order数据库信息校验----：{repayOrderInfo}")
        assert repayOrderInfo['user_name'] == gl.get_value('personData')['name'], "客户姓名"
        assert repayOrderInfo['user_phone'] == gl.get_value('personData')['telephone']
        assert repayOrderInfo['certificate_type'] == '0', "证件类型"
        assert repayOrderInfo['certificate_no'] == gl.get_value('personData')['cer_no']
        assert repayOrderInfo['repay_status'] == '1'
        if gl.get_value('repay_plan')['repay_mode'] == '3':
            assert repayOrderInfo['repay_type'] == '2'
        else:
            assert repayOrderInfo['repay_type'] == '1'
        assert repayOrderInfo['repay_amount'] == repayOrderDetail['repay_amount']
        assert repayOrderInfo['repay_principal'] == repayOrderDetail['repay_principal']
        assert Decimal(repayOrderInfo['repay_fee_amount']).quantize(Decimal("0.00")) == Decimal((float(repayOrderDetail['repay_interest']) + float(repayOrderDetail['repay_penalty_interest']))).quantize(Decimal("0.00"))
        assert repayOrderInfo['trial_amount'] == repayOrderDetail['repay_amount']

