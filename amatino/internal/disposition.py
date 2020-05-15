"""
Amatino Python
Disposition Module
author: hugh@blinkybeach.com
"""
from amatino.internal.decodable import Decodable
from nozomi.ancillary.immutable import Immutable
from typing import TypeVar, Type, Any, Dict

T = TypeVar('T', bound='Disposition')


class Disposition(Decodable):

    def __init__(
        self,
        sequence: int,
        count: int,
        limit: int,
        offset: int
    ) -> None:

        self._sequence = sequence
        self._count = count
        self._limit = limit
        self._offset = offset

        return

    sequence = Immutable(lambda s: s._sequence)
    count = Immutable(lambda s: s._count)
    limit = Immutable(lambda s: s._limit)
    offset = Immutable(lambda s: s._offset)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            sequence=data['sequence'],
            count=data['count'],
            limit=data['limit'],
            offset=data['offset']
        )
