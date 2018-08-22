"""
Amatino API Python Bindings
HTTP Method Module
Author: hugh@amatino.io
"""
from enum import Enum


class HTTPMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
