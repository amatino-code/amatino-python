"""
Amatino API Python Bindings
Decodable Module
Author: hugh@amatino.io
"""
from json import loads
from typing import TypeVar
from typing import Type
from typing import List
from typing import Any
from amatino.unexpected_response_type import UnexpectedResponseType

T = TypeVar('T', bound='Decodable')


class Decodable:
    """
    Abstract class defining an interface for objects that may be decoded from
    serialised data.
    """

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        raise NotImplementedError

    @classmethod
    def decode_many(cls: Type[T], data: Any) -> List[T]:
        if not isinstance(data, list):
            raise UnexpectedResponseType(data, list)
        return [cls.decode(o) for o in data]

    @classmethod
    def deserialise(cls: Type[T], data: str) -> T:
        return cls.decode(loads(data))

    @classmethod
    def deserialise_many(cls: Type[T], data: str) -> List[T]:
        return cls.decode_many(loads(data))
