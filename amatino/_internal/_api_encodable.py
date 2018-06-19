"""
Amatino API Python Bindings
API Encodable Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly by public classes, and
should not be used directly.
"""

class _ApiEncodable:
    """
    Private - Not intended to be used directly.

    Abstract class providing a data encoding interface
    """
    def in_serialisable_form(self) -> object:
        """
        Return a json-serialisable representation of this object - Either a list
        or a dict.
        """
        raise NotImplementedError

    def as_json(self) -> str:
        """
        Return a json string representation of this object
        """
        raise NotImplementedError
