"""
Amatino API Python Bindings
Session Credentials Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly by public classes, and
should not be used directly.
"""


class SessionCredentials:
    """
    A structure for passing session credentials between objects that can't
    directly import Session because of Python circular import funtimes. This is
    smelly code and should be refactored out.
    """
    def __init__(self, api_key: str, session_id: int) -> None:
        self.api_key = api_key
        self.session_id = session_id
        return
