#!/usr/bin/env python3
""" Authentication module """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> str:
    """ Returns Bytes(salted hash of the input password)
    hashed with bcrypt.hashpw
    """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    return hashed


def _generate_uuid() -> str:
    """Returns a string representation of a new UUID
    """
    UUID = uuid4()
    return str(UUID)


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

    def valid_login(self, email: str, password: str) -> bool:
        """Returns True if email exists and password checked
        with bcrypt.checkpw and False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_pwd = user.hashed_password
        encoded_pwd = password.encode()

        if bcrypt.checkpw(encoded_pwd, user_pwd):
            return True

        return False

    def create_session(self, email: str) -> str:
        """ Returns a session id
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        return session_id