"""
Amatino API Python Bindings
Constrained Integer Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly by public classes, and
should not be used directly.

"""
from typing import Optional
from amatino.constraint_error import ConstraintError
from amatino.internal.encodable import Encodable


class ConstrainedInteger(Encodable):
    """
    An integer whose maximum, and optionally minimum, magnitude is restricted.
    """
    MAX_ERR = '{name} above maximum value of {}'
    MIN_ERR = '{name} below minimum value of {min_value}'

    def __init__(
        self,
        integer: int,
        name: str,
        max_value: int,
        min_value: Optional[int] = None
    ) -> None:

        assert isinstance(name, str)
        assert isinstance(max_value, int)
        if min_value is not None:
            assert isinstance(min_value, int)

        if not isinstance(integer, int):
            raise TypeError(name + ' must be of type `int`')

        if integer > max_value:
            error = self.MAX_ERR.format(name=name, max_value=str(max_value))
            raise ConstraintError(error)

        self._integer = integer

        if min_value is None:
            return

        if integer < min_value:
            error = self.MIN_ERR.format(name=name, min_value=str(min_value))
            raise ConstraintError(error)

        return

    def serialise(self) -> int:
        return self._integer
