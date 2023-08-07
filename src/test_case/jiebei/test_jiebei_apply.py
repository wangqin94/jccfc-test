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
    def test_apply(self):
        jb = JieBeiCheckBizImpl(data=None)
        jb_apply_file = creditFile(data=jb.data)
        # 初审
        jb.datapreCs()
        self.applyNo = jb.data['applyno']
        # 检查初审结果
        jb.jiebei_check_feature_detail('jc_cs_result', self.applyNo)
        # 复审  tc_NoSource_ToPlatformOne Y-新客，N-老客
        jb.datapreFs(applyType='ADMIT_APPLY', tc_NoSource_ToPlatformOne='Y')
        # 检查复审结果
        jb.jiebei_check_feature_detail('jc_fs_result', self.applyNo)
        # 授信通知
        jb.creditNotice(bizType='ADMIT_APPLY', creditAmt=5000000)
        # 创建授信文件
        jb_apply_file.start_creditFile()
        # 处理授信对账文件
        self.job.update_job('借呗授信对账文件处理任务', group=13, job_type='VIRTUAL_JOB', executeBizDateType='TODAY')
        self.job.trigger_job('借呗授信对账文件处理任务', group=13, job_type='VIRTUAL_JOB')

    """ 后置条件处理 """
    def tearDown(self):
        # 检查授信状态
        self.CheckBizImpl.check_credit_apply_status(thirdpart_apply_id=self.applyNo)


if __name__ == '__main__':
    unittest.main()
