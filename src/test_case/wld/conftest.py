import pytest
import sys
import os
from src.impl.WLD.WldBizImpl import WldBizImpl
from src.impl.WLD.WldSynBizImpl import WldSynBizImpl

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
from src.impl.common.CheckBizImpl import *
from src.impl.WLD.WldCheckBizImpl import WldCheckBizImpl


# scope = "session"表示在整个目录中只执行一次
# scope = "moudle"表示每一个模块也就是每个.py文件执行一次
# scope = "class"表示每一个类执行一次
# scope = "function"默认范围，每一个函数或方法都会调用，不填写时便是它
# session > module > class > function
# @pytest.fixture(autouse=True)  想让每一个测试用例都运行公共的方法

@pytest.fixture(scope="class")
def get_base_data_wld():
    data = get_base_data_temp('applyid')
    return data


@pytest.fixture(scope="class")
def wldBizImpl(get_base_data_wld):
    data = get_base_data_wld
    wldBizImpl = WldBizImpl(data=data)
    return wldBizImpl


@pytest.fixture(scope="class")
def checkBizImpl():
    checkBizImpl = CheckBizImpl()
    return checkBizImpl


@pytest.fixture(scope="class")
def wldCheckBizImpl(get_base_data_wld):
    data = get_base_data_wld
    wldCheckBizImpl = WldCheckBizImpl(data)
    return wldCheckBizImpl
#
#
@pytest.fixture(scope="class")
def mysqlBizImpl():
    mysqlBizImpl = MysqlBizImpl()
    return mysqlBizImpl
#

@pytest.fixture(scope="class")
def wldSynBizImpl(get_base_data_wld):
    data = get_base_data_wld
    wld = WldSynBizImpl(data)
    bil_date = wld.preLoanapply()
    data['bill_date']= bil_date
    return data
