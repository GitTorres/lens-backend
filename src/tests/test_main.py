import pytest
import json
from tests.template import *
from tests.utils.dict_utils import _update
from app.main import app
from typing import List, Dict
from datetime import datetime, timezone
from starlette.testclient import TestClient
from requests.models import Response
from fastapi.encoders import jsonable_encoder


@pytest.fixture(scope="module")
def test_app() -> TestClient:
    client = TestClient(app)

    return client  # use yield instead?


@pytest.fixture(scope="module")
def test_dates() -> List:

    return [
        "2022-02-01T01:43:12.306Z",  # string "1900-01-01T01:01:01.000000+00:00"
        # datetime.utcnow(),  # datetime, not timezone aware
        # datetime.now(timezone.utc),  # datetime, timezone aware
    ]


@pytest.fixture(scope="module")
def data_for_date_tests(test_dates) -> List[Dict]:
    body: Dict = model_summary_template.copy()

    return [_update(body, {"created_time": date}) for date in test_dates]


def test_insert_different_date_types(data_for_date_tests, test_app):
    # endpoint
    url = "/modelsummary/regression"

    assert (
        test_app.put(url=url, data=jsonable_encoder(data_for_date_tests[0])).status_code
        == 200
    )

    # # test each date
    # api_responses: List[Response] = [
    #     test_app.put(url=url, data=jsonable_encoder(body))
    #     for body in data_for_date_tests
    # ]

    # # check that we have a valid response with our test data
    # assert all([result.status_code == 200 for result in api_responses])
