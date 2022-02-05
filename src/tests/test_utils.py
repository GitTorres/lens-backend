import pytest
from tests.utils.dict_utils import _update
from app.utils.dates import _is_valid_date
from typing import List, Dict


@pytest.fixture(scope="module")
def simple_dict() -> Dict[str, str]:

    return {"key1": "val1", "key2": "val2"}


@pytest.mark.utils
def test_dict_update(simple_dict: Dict):
    assert _update(simple_dict, {"key1": "val3"}) == {
        "key1": "val3",
        "key2": "val2",
    }


@pytest.mark.utils
def test_is_valid_date():
    valid = [
        "2010-01-01T01:30:10.183736+0000",
        "2010-01-01T01:30:10.18373+0000",
        "2010-01-01T01:30:10.1837+0000",
        "2010-01-01T01:30:10.183+0000",
        "2010-01-01T01:30:10.18+0000",
        "2010-01-01T01:30:10.1+0000",
        "2010-01-01T00:00:00.000000+0000",  # irst moment of the day
        "2010-12-31T23:59:59.999999+0000",  # last moment of the day
    ]

    invalid_times = [
        "2010-01-01T24:30:10.183736+0000",  # invalid hour
        "2010-01-01T-1:30:10.183736+0000",  # invalid hour
        "2010-01-01T23:61:10.183736+0000",  # invalid minute
        "2010-01-01T23:-1:10.183736+0000",  # invalid minute
        "2010-01-01T23:30:61.183736+0000",  # invalid second
        "2010-01-01T23:30:-1.183736+0000",  # invalid second
        "2010-01-01T23:30:-1.1000000+0000",  # invalid microsecond
        "2010-01-01T23:30:-1.-194857+0000",  # invalid microsecond
        "2010-01-01T23:30:-1.1000000+0",  # invalid offset
        "2010-01-01T23:30:-1.-194857+00",  # invalid offset
        "2010-01-01T23:30:-1.-194857+000",  # invalid offset
    ]

    invalid_dates = [
        "-2010-01-01T23:30:10.183736+0000",  # invalid year
        "2010-13-01T23:30:10.183736+0000",  # invalid month
        "2010-01-32T23:30:10.183736+0000",  # invalid day
        "2010-01-22 23:30:10.183736+0000",  # missing T
    ]

    invalid = [*invalid_times, *invalid_dates]

    assert all([_is_valid_date(date) for date in valid])
    assert not any([_is_valid_date(date) for date in invalid])

