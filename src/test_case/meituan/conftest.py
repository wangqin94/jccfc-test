import pytest

from src.impl.MeiTuan.MeiTuanBizImpl import MeiTuanBizImpl
from src.impl.MeiTuan.MeiTuanCheckBizImpl import MeiTuanCheckBizImpl
from src.impl.MeiTuan.MeiTuanSynBizImpl import MeiTuanSynBizImpl
from src.impl.common.CheckBizImpl import *



# scope = "session"表示在整个目录中只执行一次
# scope = "module"表示每一个模块也就是每个.py文件执行一次
# scope = "class"表示每一个类执行一次
# scope = "function"默认范围，每一个函数或方法都会调用，不填写时便是它
# session > module > class > function
# @pytest.fixture(autouse=True)  想让每一个测试用例都运行公共的方法

@pytest.fixture(scope="class", autouse=True)
def get_base_data_meituan():
    data = get_base_data_temp('app_no')
    return data


@pytest.fixture(scope="class", autouse=True)
def meiTuanBizImpl(get_base_data_meituan):
    data = get_base_data_meituan
    meiTuanBizImpl = MeiTuanBizImpl(data=data)
    return meiTuanBizImpl


@pytest.fixture(scope="class", autouse=True)
def meiTuanCheckBizImpl(get_base_data_meituan):
    data = get_base_data_meituan
    meiTuanCheckBizImpl = MeiTuanCheckBizImpl(data)
    return meiTuanCheckBizImpl


# @pytest.fixture(scope="class", autouse=True)
# def meiTuanSynBizImpl(get_base_data_meituan):
#     data = get_base_data_meituan
#     meiTuanSynBizImpl = MeiTuanSynBizImpl(data)
#     return meiTuanSynBizImpl
