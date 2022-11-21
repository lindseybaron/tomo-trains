import json
from copy import deepcopy
from datetime import datetime

import pytest

from app import app
from tests.conftest import trains_data

# You are welcome to use a Flask client fixture or test the running instance, as below
BASE_URL = "http://127.0.0.1:5000/"
client = app.test_client()


def test_startup():
    """Asserts that your service starts and responds"""
    r = client.get("/")
    assert r.status_code == 200
    assert r.data.decode("utf-8") == "OK"


@pytest.mark.freeze_time("2022-11-20T12:34:00")
def test_next_no_next():
    """Assert /trains/next returns empty list if there's no time in the next 24 hours with multiple trains."""
    r = client.get("trains/next")

    assert r.status_code == 200
    assert json.loads(r.data) == []


@pytest.mark.freeze_time("2022-11-20T23:59:00")
def test_next_tomorrow(seed_test_data):
    """Assert /trains/next returns next time multiple trains in station not until next day."""
    r = client.get("trains/next")

    assert r.status_code == 200
    assert json.loads(r.data) == 201


@pytest.mark.freeze_time("2022-11-20T12:34:00")
def test_next(seed_test_data):
    """Assert /trains/next returns the next time multiple trains are in the station."""
    now = datetime.now()
    now_number = int(f"{now.hour}{now.minute}")
    r = client.get("trains/next")

    assert r.status_code == 200
    assert json.loads(r.data) == 1245
    assert json.loads(r.data) >= now_number


@pytest.mark.parametrize("train_data", trains_data)
def test_get(seed_test_data, train_data):
    """Asserts that the schedule is returned for the expected train."""
    train, schedule = train_data

    r = client.get(f"trains/{train}")

    assert r.status_code == 200
    assert json.loads(r.data) == schedule


@pytest.mark.parametrize("train", [
    {"id": "A", "schedule": [180, 640, 1440]},
    {"id": "C", "schedule": [440, 640]},
    {"id": "E", "schedule": [100, 220, 300]},
    {"id": "1", "schedule": [100, 220, 2359]},
    {"id": "2", "schedule": [0]},
    {"id": "TOMO", "schedule": []},  # Names up to 4 characters and empty schedule lists should be allowed.
])
def test_add(train):
    """Asserts that schedules are added and returned as expected."""
    r = client.post(f"trains", json=train)

    assert r.status_code == 200

    response_json = json.loads(r.data.decode("utf-8"))
    assert response_json == train["schedule"]


@pytest.mark.parametrize("train_id", [None, 1, "", "floccinaucinihilipilification", "ABRASIONS", "a+b"])
def test_add_invalid_train_id(train_id):
    """Asserts an error is returned if train id is not provided."""
    json_data = {"schedule": [100, 220, 2359]}
    if train_id is not None:
        json_data["id"] = train_id

    r = client.post(f"trains", json=json_data)

    assert r.status_code == 422
    assert json.loads(r.data) == [{"id": "train id is required and must be a string from 1 to 4 characters."}]


@pytest.mark.parametrize("schedule", [None, [None], ["asdf"], [9999], [123, 9999], [234, "asdf"]])
def test_add_schedule_required(schedule):
    """Asserts an error is returned if train schedule is not provided as a list of ints between 0 and 2359.

        Note: An empty list is allowed.
    """
    json_data = {"id": "TEST"}
    if schedule is not None:
        json_data["schedule"] = schedule

    r = client.post(f"trains", json=json_data)

    assert r.status_code == 422
    assert json.loads(r.data) == [
        {"schedule": "schedule is required and must be a list of integers between 0 and 2359."}
    ]


def test_add_duplicate_train_id():
    """Asserts that schedules are added and returned as expected."""
    train = {"id": "DUPE", "schedule": [1234, 2345]}

    # Add it once, then try to add it again.
    client.post(f"trains", json=train)
    r = client.post(f"trains", json=train)

    assert r.status_code == 422
    assert json.loads(r.data) == [{"id": "train id already exists."}]


def test_add_train_with_duplicate_times():
    """Asserts that schedules do not return duplicate times."""
    expected_train = {"id": "EPUD", "schedule": [1234, 2345]}

    # Post data with duplicate train time.
    train = deepcopy(expected_train)
    train["schedule"].append(1234)

    r = client.post(f"trains", json=train)

    assert r.status_code == 200
    assert json.loads(r.data) == expected_train["schedule"]
