"""
Amatino API Python Bindings
New Transaction Arguments Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly by public classes, and
should not be used directly.
"""

from amatino.internal.encodable import Encodable


class NewSessionArguments(Encodable):
    """
    Private - Not intended to be used directly.

    An instance of arguments for the creation of a new Session. Performs
    validation of input parameters. May raise various exceptions during
    validation.
    """
    _INVALID_INIT_ID = """Supply either email or user_id, but not both"""

    def __init__(
        self,
        secret: str = None,
        email: str = None,
        user_id: int = None
    ) -> None:

        if email is not None and user_id is not None:
            raise ValueError(self._INVALID_INIT_ID)

        if not isinstance(secret, str):
            raise TypeError('secret must be of type str')

        if email is not None and not isinstance(email, str):
            raise TypeError('email must be of type str')

        if user_id is not None and not isinstance(user_id, int):
            raise TypeError('user_id must be of type int')

        self._secret = secret
        self._email = email
        self._user_id = user_id

        self._data = {
            'secret': self._secret,
            'account_email': self._email,
            'user_id': self._user_id
        }

        return

    def serialise(self) -> dict:
        return self._data
