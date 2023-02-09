#!/usr/bin/env python3
"""Session auth module
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import Dict
from uuid import uuid4, UUID


class SessionAuth(Auth):
    """Sessions Authentication class
    """
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session ID for a user_id
        """
        if user_id is None or type(user_id) != str:
            return None

        session_id: str = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns User ID based on a session ID
        """
        if session_id is None or type(session_id) != str:
            return None

        user_id = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None):
        """ Returns a User instance based
        on a cookie value
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Deletes the user session/logout
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)

        if session_id is None:
            return False

        user_id = self.user_id_by_session_id(session_id)

        if not user_id:
            return False

        try:
            del self.user_id_by_session_id[session_id]
        except Exception:
            pass

        return True
