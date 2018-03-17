"""
Amatino API Python Bindings
Data Package Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""
import json

class _DataPackage:
    """
    Private - Not intended to be used directly.

    Abstract class providing JSON data packing capabilities
    to concrete classes.
    """
    def __init__(self,
        list_data: list = None,
        object_data: dict = None,
        override_listing: bool = False
        ):
    
        self._data = None

        assert isinstance(override_listing, bool)
        
        if list_data is not None:
            assert isinstance(list_data, list)
            assert override_listing is False
            self._data = list_data
        
        if object_data is not None:
            assert isinstance(object_data, dict)
            if override_listing is True:
                self._data = object_data
            else:
                self._data = [object_data]

        assert self._data is not None
        return

    def as_json_bytes(self) -> bytes:
        """
        Return package arguments as JSON bytes suitable
        for inclusion in an HTTP request.
        """
        data = json.dumps(self._data).encode('utf-8')
        return data
