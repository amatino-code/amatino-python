"""
Amatino API Python Bindings
Url Target Module
Author: hugh@amatino.io
"""
from typing import Type
from typing import TypeVar

T = TypeVar('T', bound='UrlTarget')


class UrlTarget:
    """Internal class handling individual url parameter components"""

    def __init__(self, key: str, value: str) -> None:

        if not isinstance(key, str):
            raise TypeError('Key must be of type `str`')

        if not isinstance(value, str):
            raise TypeError('value must be of type `str`')

        self.key = key
        self.value = value

        return

    @classmethod
    def from_integer(
        cls: Type[T],
        key: str,
        value: int,
    ) -> T:

        if not isinstance(value, int):
            raise TypeError('value must be of type `int`')

        return cls(key, str(value))

    def __str__(self):
        return self.key + '=' + str(self.value)

    def __eq__(self, other):
        if (
                other.key == self.key
                and other.value == self.value
        ):
            return True
        return False
