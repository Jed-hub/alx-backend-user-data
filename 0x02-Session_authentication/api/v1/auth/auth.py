#!/usr/bin/env python3
"""Auth module
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Auth class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth method
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path[-1] is not '/':
            path += '/'

        for paths in excluded_paths:
            if paths.endswith('*'):
                if path.startswith(paths[:-1]):
                    return False
            elif path == paths:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """authorization header method
        """
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user method
        """
        return None

    def session_cookie(self, request=None):
        """ Return a cookie value from a request
        """
        if request is None:
            return None

        _my_session_id = getenv("SESSION_NAME")

        session_id = request.cookies.get(_my_session_id)

        return session_id
