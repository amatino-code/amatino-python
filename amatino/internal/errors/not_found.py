"""
Amatino Python
Resource Not Found Error
author: hugh@blinkybeach.com
"""
from amatino.amatino_error import AmatinoError


class ResourceNotFound(AmatinoError):
    """
    An error indicating that Amatino API could not find a resource specified in
    an otherwise validly formed request.
    """
    pass
