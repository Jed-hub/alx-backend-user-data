#!/usr/bin/env python3
""" Basic auth module """
from api.v1.auth.auth import Auth


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
