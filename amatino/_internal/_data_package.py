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
    def __init__(self):
        self._package = None
        return

    def as_json_bytes(self) -> bytes:
        """
        Return package arguments as JSON bytes suitable
        for inclusion in an HTTP request.
        """
        data = json.dumps(self._package).encode('utf-8')
        return data
