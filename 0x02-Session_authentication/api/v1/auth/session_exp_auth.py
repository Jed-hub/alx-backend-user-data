#!/usr/bin/env python3
""" Expiration date to session module
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from typing import Dict
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Session Expiration Auth
    """
    def __init__(self):
        """ Initialization
        """
        SESSION_DURATION = getenv('SESSION_DURATION', 0)

        try:
            SESSION_DURATION = int(SESSION_DURATION)
        except Exception:
            SESSION_DURATION = 0

        self.session_duration = SESSION_DURATION

    def create_session(self, user_id=None):
        """ Creates a session
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session_dictionary: Dict = {
                "user_id": user_id,
                "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session__dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Return user id for session
        """
        if session_id is None or\
           session_id not in self.user_id_by_session_id.keys():
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)

        if self.session_duration <= 0 or session_dictionary is None:
            return session_dictionary.get('user_id', None)

        created_by = session_dictionary.get('created_at', None)
        if created_by is None:
            return None

        expired_session = created_by + timedelta(seconds=self.session_duration)

        if expired_session < datetime.now():
            return None

        return session_dictionary.get('user_id', None)
