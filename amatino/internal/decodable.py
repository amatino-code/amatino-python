"""
Amatino Python
Decodable Module
author: hugh@blinkybeach.com
"""
from json import loads
from typing import Any, Optional, TypeVar, Type, List

T = TypeVar('T', bound='Decodable')


class Decodable:
    """Abstract protocol defining an interface for decodable classes"""

    @classmethod
    def decode(self, data: Any) -> T:
        """Return a JSON-serialisable form of the object"""
        raise NotImplementedError

    @classmethod
    def optionally_decode(cls: Type[T], data: Optional[Any]) -> Optional[T]:
        """Optionally return a decoded object from serialised data"""
        if data is None:
            return None
        return cls.decode(data)

    @classmethod
    def deserialise(cls: Type[T], serial: str) -> T:
        """Return a JSON string representation of the object"""
        return cls.decode(loads(serial))

    @classmethod
    def optionally_deserialise(
        cls: Type[T],
        serial: Optional[str]
    ) -> Optional[T]:
        if serial is None:
            return None
        return cls.deserialise(serial)

    @classmethod
    def decode_many(cls: Type[T], data: Any) -> List[T]:
        """Return list of decoded instances of an object"""
        return [cls.decode(d) for d in data]

    @classmethod
    def optionally_decode_many(
        cls: Type[T],
        data: Optional[Any],
        default_to_empty_list: bool = False
    ) -> Optional[List[T]]:
        """Optionally return a list of decoded objects"""
        if data is None and default_to_empty_list is True:
            return list()
        if data is None:
            return None
        return cls.decode_many(data)
