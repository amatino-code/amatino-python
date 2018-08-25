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
from typing import Any
from amatino.internal.immutable import Immutable
from amatino.internal.encodable import Encodable
from amatino.internal.api_request import ApiRequest
from amatino.internal.constrained_string import ConstrainedString

T = TypeVar('T', bound='Account')


class Account:
    """
    An Amatino Account is collection of related economic activity. For example,
    an Account might represent a bank account, income from a particular client,
    or company equity. Many Accounts together compose an Entity.
    """
    PATH = '/accounts'
    MAX_DESCRIPTION_LENGTH = 1024
    MAX_NAME_LENGTH = 1024

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
        self._color: Color = color

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
    def _create(
        cls: Type[T],
        name: str,
        description: Optional[str],
        am_type: AMType,
        global_unit: Optional[GlobalUnit],
        custom_unit: Optional[CustomUnit],
        counter_party: Optional[Entity],
        color: Optional[Color]
    ) -> T:

        raise NotImplementedError

    @classmethod
    def retrieve(cls: Type[T]):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    class CreateArguments(Encodable):
        """
        """
        def __init__(
            self,
            name: str,
            description: Optional[str],
            am_type: AMType,
            parent: Optional[T],
            global_unit: Optional[GlobalUnit],
            custom_unit: Optional[CustomUnit],
            counter_party: Optional[Entity],
            color: Optional[Color]
        ) -> None:

            self._name = ConstrainedString(
                name,
                'name',
                Account.MAX_NAME_LENGTH
            )

            self._description = ConstrainedString(
                description,
                'description',
                Account.MAX_DESCRIPTION_LENGTH
            )

            if not isinstance(am_type, AMType):
                raise TypeError('am_type must be of type `AMType`')

            self._type: AMType = am_type

            if parent and not isinstance(parent, Account):
                raise TypeError('parent must be of type `Account`')

            self._parent: Optional[Account] = parent

            if global_unit is not None and custom_unit is not None:
                raise AssertionError('Both global & custom unit supplied')

            if global_unit is None and custom_unit is None:
                raise AssertionError('Neither global nor custom unit supplied')

            if global_unit and not isinstance(global_unit, GlobalUnit):
                raise TypeError('global_unit must be of type `GlobalUnit`')

            if custom_unit and not isinstance(custom_unit, CustomUnit):
                raise TypeError('custom_unit must be of type `CustomUnit')

            self._global_unit: Optional[GlobalUnit] = global_unit
            self._custom_unit: Optional[CustomUnit] = custom_unit

            if counter_party and not isinstance(counter_party, Entity):
                raise TypeError('counter_party must be of type `Entity`')

            self._counterparty = counter_party

            if color and not isinstance(color, Color):
                raise TypeError('color must be of type `Color`')

            self._color = color

            return

        def serialise(self) -> Any:

            parent_id = None
            if self._parent is not None:
                parent_id = self._parent.id_

            global_unit_id = None
            if self._global_unit:
                global_unit_id = self._global_unit.id_

            custom_unit_id = None
            if self._custom_unit:
                custom_unit_id = self._custom_unit.id_

            counterparty_id = None
            if self._counterparty:
                counterparty_id = self._counterparty.id_

            color_code = None
            if self._color:
                color_code = str(self._color)

            data = {
                'name': str(self._name),
                'type': self._type.beep,
                'parent_account_id': parent_id,
                'counterparty_entity_id': counterparty_id,
                'global_unit_id': global_unit_id,
                'custom_unit_id': custom_unit_id,
                'color': color_code
            }
            return data
