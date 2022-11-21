import pytest

from app import db


trains_data = [
    ("N", [201, 401, 801, 2201]),
    ("Q", [130, 1130, 2130]),
    ("R", [645, 945, 1245, 1545, 1945]),
    ("W", [201, 1131, 1245]),
    ("G", [1, 720, 1229, 2359]),
    ("J", [128, 550, 1041, 314]),
    ("Z", [0, 600, 1200, 1800, 2200]),
]


@pytest.fixture
def seed_test_data():

    for train_data in trains_data:
        train, schedule = train_data
        db.set(train, schedule)

    yield
