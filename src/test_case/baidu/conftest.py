import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
from src.impl.baidu.BaiDuBizImpl import BaiDuBizImpl


# scope = "session"表示在整个目录中只执行一次
# scope = "moudle"表示每一个模块也就是每个.py文件执行一次
# scope = "class"表示每一个类执行一次
# scope = "function"默认范围，每一个函数或方法都会调用，不填写时便是它
# session > module > class > function
# @pytest.fixture(autouse=True)  想让每一个测试用例都运行公共的方法

@pytest.fixture(scope="class")
def baiduBizImpl(get_base_data):
    data = get_base_data
    baiduBizImpl = BaiDuBizImpl(data=data)
    return baiduBizImpl

