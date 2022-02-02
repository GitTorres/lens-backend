import pytest
from tests.utils.dict_utils import _update
from typing import List, Dict


@pytest.fixture(scope="module")
def simple_dict() -> List:

    return {"key1": "val1", "key2": "val2"}


@pytest.mark.utils
def test_dict_update(simple_dict: Dict):
    assert _update(simple_dict, {"key1": "val3"}) == {
        "key1": "val3",
        "key2": "val2",
    }

