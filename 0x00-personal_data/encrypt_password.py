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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate that the provided password matches the hashed password
    """
    valid = bcrypt.checkpw(password.encode(), hashed_password)

    return valid
