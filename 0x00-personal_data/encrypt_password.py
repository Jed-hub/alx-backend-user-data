#!/usr/bin/env python3
""" encrypt password module """
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Returns a salted hashed password in byte string
    """
    encoded = password.encode()
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())

    return hashed
