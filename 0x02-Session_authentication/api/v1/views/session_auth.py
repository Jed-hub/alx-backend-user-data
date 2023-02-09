#!/usr/bin/env python3
""" Session auth view
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from os import getenv
from typing import List
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ Login user
    """
    email = request.form.get('email')

    if not email:
        return jsonify({"error": "email missing"}), 400

    pwd = request.form.get('password')

    if not pwd:
        return jsonify({"error": "password missing"}), 400

    try:
        exist_users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not exist_users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in exist_users:
        if not user.is_valid_password(pwd):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    user = exist_users[0]
    session_id = auth.create_session(user.id)

    _my_session_id = getenv('SESSION_NAME')
    response = jsonify(user.to_json())
    response.set_cookie(_my_session_id, session_id)

    return response

@app_views.route('/api/v1/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """ Logout user
    """
    from api.v1.app import auth

    delete = auth.destroy_session(request)

    if not delete:
        abort(404)

    return jsonify({}), 200
