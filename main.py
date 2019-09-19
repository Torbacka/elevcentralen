from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth

from studentcenter import student_client

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    return student_client.authenticate(username, password)


@app.route('/bookings', methods=['GET'])
@auth.login_required
def get_available_bookings():
    return jsonify(student_client.get_available_bookings())


@app.route('/bookings/me', methods=['GET'])
@auth.login_required
def get_all_bookings():
    return jsonify(student_client.get_all_bookings())


if __name__ == '__main__':
    app.run('127.0.0.1', port=8087, debug=True)
