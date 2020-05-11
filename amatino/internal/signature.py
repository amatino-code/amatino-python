"""
Amatino API Python Bindings
Signature Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly by public classes, and
should not be used directly.
"""
from hashlib import sha512
from base64 import b64encode
import hmac
import time


class Signature:
    """An HMAC signature computation"""

    def __init__(
        self,
        api_key: str,
        path: str,
    ) -> None:

        assert isinstance(api_key, str)
        assert isinstance(path, str)

        encoded_key = api_key.encode('utf-8')

        timestamp = str(int(time.time()))

        message = timestamp + path

        encoded_message = message.encode('utf-8')

        digest = hmac.new(encoded_key, encoded_message, sha512).digest()
        self._signature = b64encode(digest).decode()

        return

    string = property(lambda s: s._signature)
