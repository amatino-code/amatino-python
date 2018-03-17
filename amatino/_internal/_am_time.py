"""
Amatino API Python Bindings
AM Time Package
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""
import json
from datetime import datetime

class _AMTime:
    """
    Private - Not intended to be used directly.

    An Amatino-specific time instance, used to convert
    datetime objects into strings of the format expected
    by the Amatino API
    """
    _FORMAT_STRING = '%Y-%m-%d_%H:%M:%S.%f'

    def __init__(self, date_time: datetime):
        self._raw_time = date_time
        self._time = datetime.strftime(self._raw_time, self._FORMAT_STRING)
        return

    def time(self) -> str:
        """
        Return Amatino API compliant time string
        """
        return self._time
