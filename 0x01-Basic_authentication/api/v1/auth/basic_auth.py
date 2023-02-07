#!/usr/bin/env python3
""" Basic auth module """
from api.v1.auth.auth import Auth
from base64 import b64decode, binascii
from typing import TypeVar, List
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class
    """
    def extract_base64_authorization_header(
                                            self,
                                            authorization_header: str
                                            ) -> str:
        """Returns the Base64 part of the authorization
        header for Basic Authentication
        """
        if authorization_header is None\
           or type(authorization_header) != str\
           or not authorization_header.startswith('Basic ')\
           and not authorization_header.endswith(' '):

            return None

        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
                                           self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Returns the decoded value of a Base64
        string base64_authorization_header
        """
        if base64_authorization_header is None\
           or type(base64_authorization_header) != str:
            return None

        try:
            decoded = b64decode(base64_authorization_header)
        except binascii.Error as e:
            return None

        return decoded.decode('utf-8')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Returns the user email and password from
        Base64 decoded value
        """
        if decoded_base64_authorization_header is None\
           or type(decoded_base64_authorization_header) != str\
           or ':' not in decoded_base64_authorization_header:

            return (None, None)

        credentials = decoded_base64_authorization_header.split(':', 1)

        return (credentials[0], credentials[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Returns the user instance based on his email and pwd
        """
        if user_email is None or type(user_email) != str\
           or user_pwd is None or type(user_pwd) != str:

            return None

        try:
            exist_user: List[TypeVar('User')]
            exist_user = User.search({"email": user_email})
        except Exception:
            return None

        for user in exist_user:
            if user.is_valid_password(user_pwd):
                return user

        return None
