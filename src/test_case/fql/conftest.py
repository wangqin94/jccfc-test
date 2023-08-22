import pytest
from src.impl.FQL.FqlBizImpl import FqlBizImpl
from src.impl.FQL.FqlCreditCheckBizImpl import FqlCreditCheckBizImpl
from src.impl.FQL.FqlLoanCheckBizImpl import FqlLoanCheckBizImpl
from src.impl.FQL.FqlRepayCheckBizImpl import FqlRepayCheckBizImpl
from utils.Models import get_base_data_temp


@pytest.fixture(scope="class")
def get_base_data_fql():
    data = get_base_data_temp("applyId")
    return data


@pytest.fixture(scope="class", autouse=True)
def fqlBizImpl(get_base_data_fql):
    data = get_base_data_fql
    fqlBizImpl = FqlBizImpl(data=data)
    return fqlBizImpl


@pytest.fixture(scope="class", autouse=True)
def fqlCreditCheckBizImpl():
    fqlCreditCheckBizImpl = FqlCreditCheckBizImpl()
    return fqlCreditCheckBizImpl


@pytest.fixture(scope="class", autouse=True)
def fqlLoanCheckBizImpl():
    fqlLoanCheckBizImpl = FqlLoanCheckBizImpl()
    return fqlLoanCheckBizImpl


@pytest.fixture(scope="class", autouse=True)
def fqlRepayCheckBizImpl():
    fqlRepayCheckBizImpl = FqlRepayCheckBizImpl()
    return fqlRepayCheckBizImpl
