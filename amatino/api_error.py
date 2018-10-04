"""
Amatino API Python Bindings
API Error Module
Author: hugh@amatino.io
"""
from amatino.amatino_error import AmatinoError


class ApiError(AmatinoError):
    """
    An error caused by the Amatino API returning data that Amatino Python could
    not parse, or interpreted as being invalid. This error type indicates
    that there is a bug in either the Amatino API or Amatino Python.
    """
    pass
