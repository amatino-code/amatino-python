"""
Amatino API Python Bindings
Account Module
Author: hugh@amatino.io
"""
from amatino.entity import Entity
from amatino.session import Session
from amatino.am_type import AMType
from amatino.global_unit import GlobalUnit
from amatino.custom_unit import CustomUnit
from amatino.color import Color
from typing import TypeVar
from typing import Optional
from typing import Type
from amatino.internal.immutable import Immutable

T = TypeVar('T', bound='Account')


class Account:
    """
    An Amatino Account is collection of related economic activity. For example,
    an Account might represent a bank account, income from a particular client,
    or company equity. Many Accounts together compose an Entity.
    """
    PATH = '/accounts'

    def __init__(
        self,
        session: Session,
        entity: Entity,
        account_id: int,
        name: str,
        am_type: AMType,
        description: str,
        global_unit_id: Optional[int],
        custom_unit_id: Optional[int],
        counterparty_id: Optional[str],
        color: Color
    ) -> None:

        self._session = session
        self._entity = entity
        self._id = account_id
        self._name = name
        self._am_type = am_type
        self._description = description
        self._global_unit_id = global_unit_id
        self._custom_unit_id = custom_unit_id
        self._counterparty_id = counterparty_id
        self._color = color

        return

    session: Session = Immutable(lambda s: s._session)
    entity: Entity = Immutable(lambda s: s._entity)
    id_: int = Immutable(lambda s: s._id)
    name: str = Immutable(lambda s: s._name)
    am_type: AMType = Immutable(lambda s: s._am_type)
    description: str = Immutable(lambda s: s._description)
    global_unit_id: Optional[int] = Immutable(lambda s: s._global_unit_id)
    custom_unit_id: Optional[int] = Immutable(lambda s: s._custom_unit_id)
    counterparty_id: Optional[str] = Immutable(lambda s: s._counterparty_id)
    color: Color = Immutable(lambda s: s._color)

    @classmethod
    def create_with_global_unit(cls: Type[T]):
        raise NotImplementedError

    @classmethod
    def create_with_custom_unit(cls: Type[T]):
        raise NotImplementedError

    @classmethod
    def _create(cls: Type[T]):
        raise NotImplementedError

    @classmethod
    def retrieve(cls: Type[T]):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError
