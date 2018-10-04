"""
Amatino API Python Bindings
Permissions Graph Module
Author: hugh@amatino.io
"""
from amatino.internal.encodable import Encodable
from typing import Optional


class PermissionsGraph(Encodable):
    def __init__(self, raw_graph: Optional[dict]) -> None:
        if raw_graph is None:
            raw_graph = dict()
        self._raw_graph = raw_graph
        return

    def serialise(self) -> dict:
        return self._raw_graph
