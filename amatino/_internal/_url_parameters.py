"""
Amatino API Python Bindings
API Request Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""

class _UrlParameters:
    """    
    Private - Not intended to be used directly.

    An instance of url parameters to be included in a request
    to the Amatino Api
    """
    def __init__(self):
        raise NotImplementedError

    def parameter_string(self) -> str:
        """
        Return a string of url parameters suitable for inclusion
        in a request to the Amatino API.
        """
        raise NotImplementedError
