#!/usr/bin/env python3
""" Authentication module """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """ Returns Bytes(salted hash of the input password)
    hashed with bcrypt.hashpw
    """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    return hashed


class Auth:
    """Auth class to interact with the authentication database
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a user in the db
        Returns a User object
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

            return user

        else:
            raise ValueError(f'User {email} already exists')
