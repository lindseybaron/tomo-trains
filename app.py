from flask import Flask, Response, jsonify, request

from db import Database

app = Flask(__name__)
db = Database()


@app.route('/')
def init():
    return "OK"


@app.route('/trains', methods=['POST'])
def add_train():
    """Add a new train line."""
    train_data = request.json

    if not train_data.get('id'):
        raise ValueError("Train id is required.")

    if not isinstance(train_data.get('id'), str):
        raise ValueError("Train id must be a string.")

    if not isinstance(train_data.get('schedule'), list):
        raise ValueError("Schedule must be a list.")

    db.set(key=train_data['id'], val=train_data['schedule'])

    return jsonify(train_data['schedule']), 200


@app.route('/trains/<string:train_id>')
def get_schedule(train_id):
    """ Implement a route that returns the schedule for a given train line """
    train = db.get(key=train_id)

    return jsonify(train), 200


@app.route('/trains/next')
def get_next():
    """ Implement a route that returns the next time multiple trains are in the station """
    raise NotImplementedError


if __name__ == '__main__':
    app.run()
