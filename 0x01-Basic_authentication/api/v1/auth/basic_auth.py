#!/usr/bin/env python3
""" Basic auth module """
from api.v1.auth.auth import Auth
from base64 import b64decode, binascii


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
