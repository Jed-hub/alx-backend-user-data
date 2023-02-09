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
    """ Return 
    """
    email = request.form.get('email')
    pwd = request.form.get('password')

    if not email:
        return make_response(jsonify({ "error": "email missing" }), 400)
    if not pwd:
        return make_response(jsonify({ "error": "password missing" }), 400)

    exist_user = User.search({"email": email})

    if len(exist_user) == 0:
        return jsonify({ "error": "no user found for this email" }), 404

    from api.v1.app import auth
    for user in exist_user:
        if user.is_valid_password(pwd):
            session_id = auth.create_session(user.id)
            SESSION_NAME = getenv('SESSION_NAME')
            response = make_response(user.to_json)
            response.set_cookie(SESSION_NAME, session_id)
            return response

    return make_response(jsonify({"error": "wrong password"}), 401)
