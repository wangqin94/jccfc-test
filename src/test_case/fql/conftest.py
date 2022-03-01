import os
import sys

import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
from src.impl.FQL.FqlBizImpl import FqlBizImpl
from src.impl.FQL.FqlCreditCheckBizImpl import FqlCreditCheckBizImpl
from src.impl.FQL.FqlLoanCheckBizImpl import FqlLoanCheckBizImpl
from src.impl.FQL.FqlRepayCheckBizImpl import FqlRepayCheckBizImpl


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



@pytest.fixture(scope="class", autouse=True)
def fqlRepayCheckBizImpl():
    fqlRepayCheckBizImpl = FqlRepayCheckBizImpl()
    return fqlRepayCheckBizImpl