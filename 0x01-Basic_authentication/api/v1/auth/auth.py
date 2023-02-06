#!/usr/bin/env python3
"""Auth module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class """
    def __init__(self):
        """Constructor
        """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth method
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path[-1] is not '/':
            path += '/'

        for paths in excluded_paths:
            if path == paths:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """authorization header method
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user method
        """
        return None
