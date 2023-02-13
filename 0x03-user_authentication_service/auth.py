#!/usr/bin/env python3
""" Authentication module """
import bcrypt


def _hash_password(password: str) -> str:
    """ Returns Bytes(salted hash of the input password)
    hashed with bcrypt.hashpw
    """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed
