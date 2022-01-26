import pytest
import logging

from typing import List


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