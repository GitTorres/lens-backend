import pytest
import json
from tests.template import *
from tests.utils.dict_utils import _update
from app.main import app
from typing import List, Dict, Union
from datetime import datetime, timezone
from starlette.testclient import TestClient
from requests.models import Response
from fastapi.encoders import jsonable_encoder


@pytest.fixture(scope="module")
def test_app() -> TestClient:
    client = TestClient(app)

    return client  # use yield instead?


@pytest.fixture(scope="module")
def valid_dates() -> List:

    return [
        "2022-02-01T01:43:12.306Z",  # string "1900-01-01T01:01:01.000000+00:00"
        datetime.utcnow(),  # datetime, not timezone aware
        datetime.now(timezone.utc),  # datetime, timezone aware
    ]


@pytest.fixture(scope="module")
def valid_numbers() -> List[Union[int, float]]:
    return [100, 99.0, -100, -99.0, 0]


@pytest.fixture(scope="module")
def test_body_valid_dates(valid_dates) -> List[Dict]:
    body: Dict = model_summary_template.copy()

    return [_update(body, {"created_time": date}) for date in valid_dates]


@pytest.fixture(scope="module")
def test_body_invalid_dates(valid_numbers) -> List[Dict]:
    body: Dict = model_summary_template.copy()

    return [_update(body, {"created_time": num}) for num in valid_numbers]


@pytest.mark.put
def test_insert_different_date_types(
    test_body_valid_dates, test_body_invalid_dates, test_app
):
    # endpoint
    url = "/modelsummary/regression"

    # expect ok response for valid dates
    valid_api_responses: List[Response] = [
        test_app.put(url=url, json=jsonable_encoder(body))
        for body in test_body_valid_dates
    ]

    # expect bad response for invalid dates
    invalid_api_responses: List[Response] = [
        test_app.put(url=url, json=jsonable_encoder(body))
        for body in test_body_invalid_dates
    ]

    # check that we have a valid response with our test data
    assert all([result.status_code == 200 for result in valid_api_responses])
