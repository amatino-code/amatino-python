"""
Amatino API Python Bindings
Constrained String Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly by public classes, and
should not be used directly.

"""
from typing import Optional
from amatino.constraint_error import ConstraintError
from amatino.internal.encodable import Encodable


class ConstrainedString(Encodable):
    """
    A string whose maximum, and optionally minimum, length is restricted. Throws
    TypeError if supplied with something other than a `str`, and ConstraintError
    if a constrained is violated.
    """

    MAX_ERR = "{name} exceeds maximum length of {max_char}"
    MIN_ERR = "{name} below minimum length of {min_char}"

    def __init__(
        self,
        string: str,
        name: str,
        max_length: int,
        min_length: Optional[int] = None
    ) -> None:

        assert isinstance(name, str)
        assert isinstance(max_length, int)
        if min_length is not None:
            assert isinstance(min_length, int)

        if not isinstance(string, str):
            raise TypeError(name + ' must be of type `str`')

        if len(string) > max_length:
            error = self.MAX_ERR.format(name=name, max_char=str(max_length))
            raise ConstraintError(error)

        self._string = string
        self._name = name

        if min_length is None:
            return

        if len(string) < min_length:
            error = self.MIN_ERR.format(name=name, min_char=str(min_length))
            raise ConstraintError(error)

        return

    def __str__(self) -> str:
        return self._string

    def serialise(self) -> str:
        return self._string
