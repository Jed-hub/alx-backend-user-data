#!/usr/bin/env python3
""" app module"""
from flask import Flask, jsonify, request, abort, redirect
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


@app.route('/sessions', methods=['DELETE'])
def logout():
    """ Destroys a session
    """
    session_id = request.cookies.get("session_id", None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    """ User profile
    """
    session_id = request.cookies.get("session_id", None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """ Generates a token and responds with 200
    """
    try:
        email = request.form['email']
    except KeyError:
        abort(403)

    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": token}), 200


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """ Updates password
    """
    try:
        email = request.form['email']
        reset_token = request.form['reset_token']
        new_pwd = request.form['new_password']
    except KeyError:
        abort(403)

    try:
        AUTH.update_password(reset_token, new_pwd)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
