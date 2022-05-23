# @unique
from enum import Enum


class EnumBaiDuPath(Enum):
    BaiDuEncryptPath = "/api/v1/baidu/demo/encryptData"
    BaiDuDecryptPath = "/api/v1/baidu/demo/decryptData"
    BaiDuFileEncryptPath = "/baidu/demo/file/encrypt"


class EnumBaiDuRisCode(Enum):
    ACCEPT = '10000'  # 成功
    IN_PROCESS = '20000'  # 处理中
    REJECT = '90000'  # 失败
