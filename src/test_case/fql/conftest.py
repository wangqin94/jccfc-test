import pytest

from src.impl.FQL.FqlBizImpl import FqlBizImpl
from src.impl.FQL.FqlCreditCheckBizImpl import FqlCreditCheckBizImpl
from src.impl.FQL.FqlLoanCheckBizImpl import FqlLoanCheckBizImpl


@pytest.fixture(scope="class", autouse=True)
def fqlBizImpl():
    fqlBizImpl = FqlBizImpl()
    return fqlBizImpl

@pytest.fixture(scope="class", autouse=True)
def fqlCreditCheckBizImpl():
    fqlCreditCheckBizImpl = FqlCreditCheckBizImpl()
    return fqlCreditCheckBizImpl

@pytest.fixture(scope="class", autouse=True)
def fqlLoanCheckBizImpl():
    fqlLoanCheckBizImpl = FqlLoanCheckBizImpl()
    return fqlLoanCheckBizImpl
