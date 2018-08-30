"""
Amatino API Python Bindings
Denomination Module
Author: hugh@amatino.io
"""
from amatino.internal.immutable import Immutable


class Denomination:
    """
    Abstract class defining an interface for units of account. Adopted by
    Custom Units and Global Units.]
    """
    def __init__(self, code: str, id_: int, name: str) -> None:
        assert isinstance(code, str)
        assert isinstance(id_, int)
        assert isinstance(name, str)
        self._code = code
        self._id = id_
        self._name = name
        return

    code: str = Immutable(lambda s: s._code)
    id_: int = Immutable(lambda s: s._id)
    name: str = Immutable(lambda s: s._name)
