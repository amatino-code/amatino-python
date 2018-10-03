"""
Amatino API Python Bindings
Unexpected Response Type Module
Author: hugh@amatino.io
"""
from amatino.api_error import ApiError
from typing import Any


class UnexpectedResponseType(ApiError):
    _PREFIX = 'Unexpected API response data type. Expected {}, received {}'

    def __init__(self, recieved: Any, expected: type) -> None:
        super().__init__(
            self._PREFIX.format(str(expected), str(type(recieved)))
        )
