#!/usr/bin/env python3
""" app module"""
from flask import Flask, jsonify, request, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello() -> str:
    """ Return a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"})

@app.route('/sessions', methods=['POST'])
def login():
    """ Creates a session for the user and stores it the sessionID
    as a cookie with key "session_id" on the response and returns a JSON
    payload of the form
    """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(401)

    if (AUTH.valid_login(email, password)):
        session_id = AUTH.create_session(email)
        if session_id is not None:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response

    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")