"""
Amatino API Python Bindings
Data Package Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly by public classes, and
should not be used directly.
"""
import json
from amatino.internal.encodable import Encodable
from typing import TypeVar
from typing import Any
from typing import List
from typing import Type

T = TypeVar('T', bound='DataPackage')


class DataPackage:
    """
    Private - Not intended to be used directly.

    Abstract class providing JSON data packing capabilities to concrete classes.
    """
    def __init__(
        self,
        list_data: List[Encodable] = None,
        object_data: Encodable = None,
        override_listing: bool = False,
        raw_data: Any = None
    ) -> None:

        self._data = None

        if raw_data is not None:
            self._data = raw_data
            return

        assert isinstance(override_listing, bool)
        assert (list_data is None or object_data is None)

        if list_data is not None:
            assert isinstance(list_data, list)
            assert False not in [
                isinstance(e, Encodable) for e in list_data
            ]
            assert override_listing is False
            self._data = [e.serialise() for e in list_data]

        if object_data is not None:
            assert isinstance(object_data, Encodable)
            if override_listing is True:
                self._data = object_data.serialise()
            else:
                self._data = [object_data.serialise()]

        assert self._data is not None
        return

    @classmethod
    def from_object(
        cls: Type[T],
        data: Encodable,
        override_listing: bool = False
    ) -> T:
        """
        Return a new instance of DataPackage initialised with a single Encodable
        object
        """
        return cls(object_data=data, override_listing=override_listing)

    def as_json_bytes(self) -> bytes:
        """
        Return package arguments as JSON bytes suitable
        for inclusion in an HTTP request.
        """
        return json.dumps(self._data).encode('utf-8')

    def as_object(self):
        """
        Return the underlying object data, either a list
        or a dictionary.
        """
        return self._data
