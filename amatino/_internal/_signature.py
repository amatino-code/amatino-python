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
import json

class _Signature:
    """
    Private - Not intended to be used directly.

    An HMAC signature computation
    """
    def __init__(
        self,
        api_key: str,
        path: str,
        json_data = None
        ):

        assert isinstance(api_key, str)
        assert isinstance(path, str)
        if json_data is not None:
            assert isinstance(json_data, dict) or isinstance(json_data, list)
        
        if json_data is not None:
            json_string = json.dumps(json_data, separators=(',', ':'))
            assert isinstance(json_string, str)
            if json_string == 'null':
                json_string = None
        else:
            json_string = None

        encoded_key = api_key.encode('utf-8')

        timestamp = str(int(time.time()))

        if json_string is not None:
            message = timestamp + path + json_string
        else:
            message = timestamp + path

        encoded_message = message.encode('utf-8')

        digest = hmac.new(encoded_key, encoded_message, sha512).digest()
        self._signature = b64encode(digest).decode()

        return

    def string(self) -> str:
        """
        Return a string signature
        """
        assert isinstance(self._signature, str)
        return self._signature
