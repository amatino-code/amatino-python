"""
Amatino API Python Bindings
Missing Key Module
Author: hugh@amatino.io
"""
from amatino.api_error import ApiError


class MissingKey(ApiError):
    _PREFIX = 'Expected key "{}" missing from response data'

    def __init__(self, key: str) -> None:
        super().__init__(self._PREFIX.format(key))
