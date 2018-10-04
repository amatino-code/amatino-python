"""
Amatino API Python Bindings
Credentials Module
Author: hugh@amatino.io
"""


class Credentials:
    """
    Abstract class defining an interface for classes that may be used as
    credentials when authenticating and authorising requests to the Amatino
    API.
    """
    api_key = NotImplemented
    session_id = NotImplemented
