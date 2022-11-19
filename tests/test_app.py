import json

import pytest

from app import app

# You are welcome to use a Flask client fixture or test the running instance, as below
BASE_URL = 'http://127.0.0.1:5000/'

client = app.test_client()


def test_startup():
    """Asserts that your service starts and responds"""
    r = client.get("/")
    assert r.status_code == 200
    assert r.data.decode('utf-8') == "OK"


@pytest.mark.parametrize("train", [
    {'id': 'TOMO', 'schedule': [180, 640, 1440]},
    {'id': 'FOMO', 'schedule': [440, 640]},
    {'id': '1', 'schedule': [100, 220, 300]}
])
def test_add(train):
    """Asserts that schedules are added and returned as expected."""

    r = client.post(f'trains', json=train)

    assert r.status_code == 200

    response_json = json.loads(r.data.decode('utf-8'))
    assert response_json == train['schedule']


def test_next():
    """ Implement a test for the /trains/next functionality"""
    raise NotImplementedError


# Implement any other necessary tests
