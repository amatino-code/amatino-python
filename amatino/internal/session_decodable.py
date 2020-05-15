"""
Amatino Python
Session Decodable Module
author: hugh@blinkybeach.com
"""
from typing import Any, Optional, TypeVar, Type, List
from amatino.session import Session

T = TypeVar('T', bound='SessionDecodable')


class SessionDecodable:
    """Abstract protocol defining an interface for decodable classes"""

    @classmethod
    def decode(self, data: Any, session: Session) -> T:
        """Return a JSON-serialisable form of the object"""
        raise NotImplementedError

    @classmethod
    def optionally_decode(
        cls: Type[T],
        data: Optional[Any],
        session: Session
    ) -> Optional[T]:
        """Optionally return a decoded object from serialised data"""
        if data is None:
            return None
        return cls.decode(data, session)

    @classmethod
    def decode_many(cls: Type[T], data: Any, session: Session) -> List[T]:
        """Return list of decoded instances of an object"""
        return [cls.decode(d, session) for d in data]

    @classmethod
    def optionally_decode_many(
        cls: Type[T],
        data: Optional[Any],
        session: Session,
        default_to_empty_list: bool = False
    ) -> Optional[List[T]]:
        """Optionally return a list of decoded objects"""
        if data is None and default_to_empty_list is True:
            return list()
        if data is None:
            return None
        return cls.decode_many(data, session)
