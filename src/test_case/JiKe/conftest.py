import pytest

from src.impl.JiKe.JiKeCheckBizImpl import JiKeCheckBizImpl
from src.impl.JiKe.JiKeBizImpl import JiKeBizImpl
from src.impl.JiKe.JiKeSynBizImpl import JiKeSynBizImpl
from utils.GlobalVar import GlobalMap
from utils.Models import *


# scope = "session"表示在整个目录中只执行一次
# scope = "module"表示每一个模块也就是每个.py文件执行一次
# scope = "class"表示每一个类执行一次
# scope = "function"默认范围，每一个函数或方法都会调用，不填写时便是它
# session > module > class > function
# @pytest.fixture(autouse=True)  想让每一个测试用例都运行公共的方法
@pytest.fixture(scope="module", autouse=True)
def get_base_data_jike():
    data = get_base_data_temp()
    GlobalMap().set(jike=data)
    return data


@pytest.fixture(scope="class", autouse=True)
def jikeBizImpl(get_base_data_jike):
    data = get_base_data_jike
    jikeBizImpl = JiKeBizImpl(data=data)
    return jikeBizImpl


@pytest.fixture(scope="class", autouse=True)
def jikeCheckBizImpl(get_base_data_jike):
    data = get_base_data_jike
    jikeCheckBizImpl = JiKeCheckBizImpl(data)
    return jikeCheckBizImpl


@pytest.fixture(scope="class")
def jikeLoanApply(get_base_data_jike):
    data = get_base_data_jike
    jikeSynBizImpl = JiKeSynBizImpl(data)
    # 默认当前系统时间放款，期数12期
    jikeLoanApply = jikeSynBizImpl.preLoanApply()
    return jikeLoanApply
