"""
Amatino API Python Bindings
Region Module
Author: hugh@amatino.io
"""
from amatino.internal.immutable import Immutable


class Region:
    """
    A geographic region in which Amatino can store accounting information.
    """
    def __init__(
        self,
        id_: int,
        region_code: str
    ) -> None:
        self._id = id_
        self._region_code = region_code
        return

    id_ = Immutable(lambda s: s._id)
