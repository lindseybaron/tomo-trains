from datetime import datetime

from flask import Flask, Response, jsonify, request

from db import Database

app = Flask(__name__)
db = Database()

MAX_TIME = 2359
MIN_TIME = 0


@app.route('/')
def init():
    return "OK"


@app.route('/trains', methods=['POST'])
def add_train():
    """Add a new train line."""
    train_data = request.json
    errors = validate_train_data(train_data)
    if errors:
        return jsonify(errors), 422

    schedule = train_data['schedule']
    schedule.sort()

    db.set(key=train_data['id'], val=train_data['schedule'])

    return jsonify(train_data['schedule']), 200


@app.route('/trains/<string:train_id>')
def get_schedule(train_id):
    """Return the schedule for a given train line."""
    train = db.get(key=train_id)

    return jsonify(train), 200


@app.route('/trains/next', methods=['GET'])
def get_next():
    """Return the next time multiple trains are in the station."""
    now = datetime.now()
    now_number = int(f"{now.hour}{now.minute}")

    # get a sorted list of all the times
    all_trains = db.keys()
    all_times = []
    for train in all_trains:
        all_times.extend(db.get(train))
    all_times.sort()

    # Get the first time later than now.
    times_after_now = list(filter(lambda t: t > now_number, all_times))
    first_duplicate_time = find_first_duplicate_in_sorted_list(times_after_now)
    if not first_duplicate_time:
        first_duplicate_time = find_first_duplicate_in_sorted_list(all_times[:all_times.index(times_after_now[0])])

    return jsonify(first_duplicate_time), 200


def find_first_duplicate_in_sorted_list(values):
    value_set = set()
    for value in values:
        if value in value_set:
            return value
        value_set.add(value)


def validate_train_data(train_data):
    errors = []

    if not (
            train_data.get('id') and
            isinstance(train_data.get('id'), str) and
            len(train_data['id']) <= 8
    ):
        errors.append({"id": "train id is required and must be a string between 1 and 8 characters."})

    if not (
            train_data.get('schedule') is not None and
            isinstance(train_data.get('schedule'), list) and
            all(isinstance(s, int) for s in train_data['schedule']) and
            all(t >= MIN_TIME for t in train_data['schedule']) and
            all(t <= MAX_TIME for t in train_data['schedule'])
    ):
        errors.append({"schedule": "schedule is required and must be a list of integers between 0 and 2359."})

    return errors


if __name__ == '__main__':
    app.run()
