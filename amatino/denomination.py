"""
Amatino API Python Bindings
Denomination Module
Author: hugh@amatino.io
"""
from amatino.internal.immutable import Immutable


class Denomination:
    """
    Abstract class defining an interface for units of account. Adopted by
    Custom Units and Global Units.
    """
    def __init__(
        self,
        code: str,
        id_: int,
        name: str,
        priority: int,
        description: str,
        exponent: int
    ) -> None:

        self._code = code
        self._id = id_
        self._name = name
        self._priority = priority
        self._description = description
        self._exponent = exponent
        return

    code = Immutable(lambda s: s._code)
    id_ = Immutable(lambda s: s._id)
    name = Immutable(lambda s: s._name)
    priority = Immutable(lambda s: s._priority)
    description = Immutable(lambda s: s._description)
    exponent = Immutable(lambda s: s._exponent)
