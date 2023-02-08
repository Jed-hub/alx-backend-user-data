#!/usr/bin/env python3
"""Session auth module
"""
from api.v1.auth.auth import Auth
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
