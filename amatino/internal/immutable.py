"""
Amatino API Python Bindings
Immutable Module
Author: hugh@amatino.io
"""
from amatino.amatino_error import AmatinoError


class Immutable(property):
    """
    An extension of the inbuit `property` class, which enforces immutability
    upon object properties.
    """
    _MESSAGE = """
    Amatino object instances may not be mutated via properties. Use the
    .update() method to make changes.
    """

    def __init__(self, fget) -> None:

        super().__init__(
            fget,
            self._set_error,
            self._del_error,
            None
        )

    def _set_error(self, _1, _2) -> None:
        raise AmatinoError(self._MESSAGE)

    def _del_error(self, _) -> None:
        raise AmatinoError(self._MESSAGE)
