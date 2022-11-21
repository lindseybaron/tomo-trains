from threading import Thread

from faker import Faker

from db import Database

fake = Faker()


def add_items(db, start_value, num_values):
    for i in range(start_value, start_value + num_values):
        db.set(key=str(i), val=i)


def test_storage():
    """Asserts that a value can be stored and retrieved from the database."""
    db = Database()
    key, value = "A", "1"
    db.set(key, value)
    assert value == db.get(key)


def test_keys():
    """Asserts that a keys() call to the database returns a key set."""
    db = Database()
    data = {"A": "1",
            "B": object,
            "C": 3}

    for key, value in data.items():
        db.set(key, value)
    assert data.keys() == db.keys()


def test_multi_thread_set():
    db = Database()
    target_num = 1000000

    threads = list()
    for i in range(0, target_num, 1000):
        thread = Thread(target=add_items, args=(db, i, 1000))
        threads.append(thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(db.keys()) == target_num
