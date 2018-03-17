"""
Amatino API Python Bindings
New Transaction Arguments Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""

class _NewSessionArguments:
    """
    Private - Not intended to be used directly.

    An instance of arguments for the creation of a new Session. Performs
    validation of input parameters. May raise various exceptions during
    said validation.
    """

    _INVALID_TYPE = """
        Secret and email must be of type str
    """

    def __init__(self, secret: str, email: str):
        
        if (
            not isinstance(secret, str)
            or not isinstance(email, str)
        ):
            raise TypeError(self._INVALID_TYPE)

        self._secret = secret
        self._email = email

        return
