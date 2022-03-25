import pytest

from src.impl.ctrip.CtripBizImpl import CtripBizImpl
from src.impl.ctrip.CtripCreditCheckBizlmpl import CtripCreditCheckBizImpl
from src.impl.ctrip.CtripLoanCheckBizImpl import *
from utils.Models import *

@pytest.fixture(scope="class")
def get_base_data_ctrip():
    data = get_base_data_temp('userId')
    return data

@pytest.fixture(scope="class", autouse=True)
def ctripBizImpl():
    ctripBizImpl = CtripBizImpl()
    return ctripBizImpl

@pytest.fixture(scope="class", autouse=True)
def ctripCreditCheckBizImpl():
    ctripCreditCheckBizImpl = CtripCreditCheckBizImpl()
    return ctripCreditCheckBizImpl

@pytest.fixture(scope="class", autouse=True)
def get_zhixin_bill_day():
    get_zhixin_bill_day = CtripLoanCheckBizImpl()
    return get_zhixin_bill_day

@pytest.fixture(scope="class", autouse=True)
def ctripLoanCheckBizImpl():
    ctripLoanCheckBizImpl = CtripLoanCheckBizImpl()
    return ctripLoanCheckBizImpl

@pytest.fixture(scope="class", autouse=True)
def mysqlBizImpl():
    mysqlBizImpl = MysqlBizImpl()
    return mysqlBizImpl

@pytest.fixture(scope="class", autouse=True)
def get_base_data_ctrip():
    data = get_base_data_temp('userId')
    return data

