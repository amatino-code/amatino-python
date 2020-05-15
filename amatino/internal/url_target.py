"""
Amatino API Python Bindings
Url Target Module
Author: hugh@amatino.io
"""
from typing import Type
from typing import TypeVar
from typing import List

T = TypeVar('T', bound='UrlTarget')


class UrlTarget:
    """Internal class handling individual url parameter components"""

    def __init__(self, key: str, value: str) -> None:

        if not isinstance(key, str):
            raise TypeError('Key must be of type `str`')

        value = str(value)

        self.key = key
        self.value = value

        return

    @classmethod
    def from_integer(cls: Type[T], key: str, value: int) -> T:
        """Return a UrlTarget formed of an integer value"""
        return cls(key, str(value))

    @classmethod
    def from_many_integers(
        cls: Type[T],
        key: str,
        values: List[int]
    ) -> List[T]:
        """Return a list of integer targets sharing a key"""
        return [cls(key, str(v)) for v in values]

    def __str__(self):
        return self.key + '=' + str(self.value)

    def __eq__(self, other):
        if (
                other.key == self.key
                and other.value == self.value
        ):
            return True
        return False
