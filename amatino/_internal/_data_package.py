"""
Amatino API Python Bindings
Data Package Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly by public classes, and
should not be used directly.
"""
import json
from amatino._internal._api_encodable import _ApiEncodable

class _DataPackage:
    """
    Private - Not intended to be used directly.

    Abstract class providing JSON data packing capabilities to concrete classes.
    """
    def __init__(self,
        list_data: list = None,
        object_data: dict = None,
        override_listing: bool = False,
        raw_list_data: [dict] = None
        ):
    
        self._data = None

        if raw_list_data is not None:
            assert isinstance(raw_list_data, list)
            self._data = raw_list_data
            return

        assert isinstance(override_listing, bool)
        assert (list_data is None or object_data is None)
        
        if list_data is not None:
            assert isinstance(list_data, list)
            assert False not in [
                isinstance(e, _ApiEncodable) for e in list_data
            ]
            assert override_listing is False
            self._data = [e.in_serialisable_form() for e in list_data]
        
        if object_data is not None:
            assert isinstance(object_data, _ApiEncodable)
            if override_listing is True:
                self._data = object_data.in_serialisable_form()
            else:
                self._data = [object_data.in_serialisable_form()]

        assert self._data is not None
        return

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
