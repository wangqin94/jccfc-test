import logging
from typing import List

import pytest

from src.impl.common.CheckBizImpl import *
from utils.JobCenter import *
from utils.Redis import *


def pytest_collection_modifyitems(
        session: "Session", config: "Config", items: List["Item"]
) -> None:
    print(items)
    # items.reverse()
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')


def pytest_addoption(parser):
    parser.addoption(
        "--log", action="store", default="WARNING", help="set logging level"
    )


@pytest.fixture(scope="class")
def checkBizImpl():
    checkBizImpl = CheckBizImpl()
    return checkBizImpl


@pytest.fixture
def logger():
    loglevel = pytest.config.getoption("--log")
    logger = logging.getLogger(__name__)

    numeric_level = getattr(
        logging,
        loglevel.upper(),
        None
    )
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    logger.setLevel(numeric_level)
    return logger


@pytest.fixture(scope="class")
def mysqlBizImpl():
    mysqlBizImpl = MysqlBizImpl()
    return mysqlBizImpl


@pytest.fixture(scope="class")
def job():
    job = JOB()
    return job


@pytest.fixture(scope="class")
def redis():
    redis = Redis()
    return redis
