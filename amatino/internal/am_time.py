"""
Amatino API Python Bindings
AM Time Package
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""
import datetime
from amatino.internal.immutable import Immutable
from amatino.internal.encodable import Encodable
from amatino.api_error import ApiError
from typing import Type
from typing import TypeVar

T = TypeVar('T', bound='AmatinoTime')


class AmatinoTime(Encodable):
    """
    Private - Not intended to be used directly.

    An Amatino-specific time instance, used to convert datetime objects into
    strings of the format expected by the Amatino API
    """
    _FORMAT_STRING = '%Y-%m-%d_%H:%M:%S.%f'

    def __init__(self, date_time: datetime.datetime) -> None:
        if not isinstance(date_time, datetime.datetime):
            raise TypeError('Unexpected datetime type, `datetime` required')
        self._raw_time = date_time.replace(tzinfo=AmatinoTime.UTC())
        return

    string = Immutable(lambda s: s.serialise())
    raw = Immutable(lambda s: s._raw_time)

    def serialise(self) -> str:
        return datetime.datetime.strftime(self._raw_time, self._FORMAT_STRING)

    class UTC(datetime.tzinfo):
        """UTC timezone."""

        def utcoffset(self, dt):
            return datetime.timedelta(0)

        def tzname(self, dt):
            return 'UTC'

        def dst(self, dt):
            return datetime.timedelta(0)

    @classmethod
    def decode(cls: Type[T], data: str) -> T:
        """Return an AmatinoTime instance decoded from a string"""

        if not isinstance(data, str):
            raise ApiError('Unexepected type when decoding AmatinoTime')

        date_time = datetime.datetime.strptime(data, AmatinoTime._FORMAT_STRING)
        amatino_time = cls(date_time)
        return amatino_time
