"""
Amatino API Python Bindings
API Encodable Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""
import json

class _ApiEncodable:
    """
    Private - Not intended to be used directly.

    Abstract class providing request encoding 
    """

    def __init__(self):
        self._data = None
        return

    def in_serialisable_form(self) -> object:
        """
        Return a json-serialisable representation of this
        object - Either a list or a dict.
        """

        assert self._data is not None

        if (
                not isinstance(self._data, list)
                and not isinstance(self._data, dict)
        ):
            raise TypeError('API encodable data of unexpected form')

        return self._data
