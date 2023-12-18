import unittest
from src.impl.common.CheckBizImpl import *
from src.impl.JieBei.JieBeiCheckBizImpl import *
from src.impl.JieBei.JieBeiCreateFileBizImpl import *
from utils.JobCenter import *
from person import *


class MyTestCase(unittest.TestCase):
    """ 预置条件处理 """
    def setUp(self):
        self.CheckBizImpl = CheckBizImpl()
        self.job = JOB()

    """ 测试步骤 """
    def test_apply(self, data=None, applyType='ADMIT_APPLY', creditAmt='5000000',tmpAmtMax=None,tmpAmtMin=None):
        """
        授信或调额流程
        :param applyType: #授信 ADMIT_APPLY；提额 ADJUST_AMT_APPLY；降额 DECREASE_AMT_APPLY;临额TMP_AMT_APPLY
        :param creditAmt: 授信额度，或调整后的额度，单位分
        :return:
        """
        jb = JieBeiCheckBizImpl(data=data)
        if applyType == 'ADMIT_APPLY':
            self.applyNo = jb.data['applyno']
            # 初审
            jb.datapreCs()
            # 检查初审结果
            jb.jiebei_check_feature_detail('jc_cs_result', self.applyNo)
        else:
            if applyType == 'ADJUST_AMT_APPLY' or applyType == 'DECREASE_AMT_APPLY':
                self.applyNo = "amtNo" + str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
            elif applyType == 'TMP_AMT_APPLY':
                self.applyNo = "tmpAmtNo" + str(int(round(time.time() * 1000))) + str(random.randint(0, 9999))
        # 复审  tc_NoSource_ToPlatformOne Y-新客，N-老客  applyNo：调额申请号
        jb.datapreFs(applyType=applyType, creditAmt=creditAmt, tmpAmtMax=tmpAmtMax, tmpAmtMin=tmpAmtMin,applyNo=self.applyNo, tc_NoSource_ToPlatformOne='Y')
        if applyType == 'ADMIT_APPLY':
            # 检查复审结果
            jb.jiebei_check_feature_detail('jc_fs_result', self.applyNo)
        elif applyType == 'ADJUST_AMT_APPLY':
            # 检查升额复审结果
            jb.jiebei_check_feature_detail('jc_limit_up_result', self.applyNo)
        elif applyType == 'DECREASE_AMT_APPLY':
            # 检查降额复审结果
            jb.jiebei_check_feature_detail('jc_limit_down_result', self.applyNo)
        elif applyType == 'TMP_AMT_APPLY':
            # 检查临额复审结果
            jb.jiebei_check_feature_detail('jc_tmp_amt_result', self.applyNo)
        # 授信通知
        jb.creditNotice(bizType=applyType, applyNo=self.applyNo, creditAmt=creditAmt,tmpCreditAmt='')
        # 创建授信文件
        jb_apply_file = creditFile(data=jb.data)
        jb_apply_file.start_creditFile(apply_type=applyType, creditAmt=creditAmt, applyNo=self.applyNo,tmpCreditAmt='')
        # 处理授信对账文件
        self.job.update_job('借呗授信对账文件处理任务', group=13, job_type='VIRTUAL_JOB', executeBizDateType='TODAY')
        self.job.trigger_job('借呗授信对账文件处理任务', group=13, job_type='VIRTUAL_JOB')
        if applyType == 'ADMIT_APPLY':
            # 检查授信状态
            self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.applyNo)

    """ 后置条件处理 """
    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
