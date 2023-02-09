#!/usr/bin/env python3
""" Session auth view
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from os import getenv
from typing import List
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ Login user
    """
    email = request.form.get('email')
    pwd = request.form.get('password')

    if not email:
        return make_response(jsonify({"error": "email missing"}), 400)
    if not pwd:
        return make_response(jsonify({"error": "password missing"}), 400)

    exist_users = User.search({"email": email})

    if len(exist_users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    for user in exist_users:
        if not user.is_valid_password(pwd):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth


    user = exist_users[0]
    session_id = auth.create_session(user.id)

    _my_session_id = getenv('SESSION_NAME')
    response = make_response(user.to_json)
    response.set_cookie(_my_session_id, session_id)

    return response
