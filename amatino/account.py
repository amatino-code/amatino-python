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
from amatino.denomination import Denomination
from amatino.color import Color
from typing import TypeVar
from typing import Optional
from typing import Type
from typing import Any
from typing import List
from amatino.internal.immutable import Immutable
from amatino.internal.encodable import Encodable
from amatino.internal.api_request import ApiRequest
from amatino.internal.constrained_string import ConstrainedString
from amatino.internal.data_package import DataPackage
from amatino.internal.http_method import HTTPMethod
from amatino.internal.url_parameters import UrlParameters
from amatino.internal.url_target import UrlTarget
from amatino.api_error import ApiError

T = TypeVar('T', bound='Account')


class Account:
    """
    An Amatino Account is collection of related economic activity. For example,
    an Account might represent a bank account, income from a particular client,
    or company equity. Many Accounts together compose an Entity.
    """
    _PATH = '/accounts'
    MAX_DESCRIPTION_LENGTH = 1024
    MAX_NAME_LENGTH = 1024
    _URL_KEY = 'account_id'

    def __init__(
        self,
        session: Session,
        entity: Entity,
        account_id: int,
        name: str,
        am_type: AMType,
        description: str,
        parent_account_id: int,
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
        self._parent_account_id = parent_account_id
        self._global_unit_id = global_unit_id
        self._custom_unit_id = custom_unit_id
        self._counterparty_id = counterparty_id
        self._color: Color = color

        return

    session = Immutable(lambda s: s._session)
    entity = Immutable(lambda s: s._entity)
    id_ = Immutable(lambda s: s._id)
    name = Immutable(lambda s: s._name)
    am_type = Immutable(lambda s: s._am_type)
    description = Immutable(lambda s: s._description)
    global_unit_id = Immutable(lambda s: s._global_unit_id)
    custom_unit_id = Immutable(lambda s: s._custom_unit_id)
    denomination = Immutable(lambda s: s._denomination())
    counterparty_id = Immutable(lambda s: s._counterparty_id)
    color = Immutable(lambda s: s._color)
    parent_id = Immutable(lambda s: s._parent_account_id)

    @classmethod
    def create(
        cls: Type[T],
        session: Session,
        entity: Entity,
        name: str,
        am_type: AMType,
        denomination: Denomination,
        description: Optional[str],
        parent: Optional[T] = None,
        counter_party: Optional[Entity] = None,
        color: Optional[Color] = None
    ) -> T:

        arguments = Account.CreateArguments(
            name,
            description,
            am_type,
            parent,
            denomination,
            counter_party,
            color
        )

        data = DataPackage.from_object(arguments)

        request = ApiRequest(
            path=Account._PATH,
            method=HTTPMethod.POST,
            credentials=session,
            data=data
        )

        account = cls._decode(session, entity, request.response_data)

        return account

    @classmethod
    def retrieve(
        cls: Type[T],
        session: Session,
        entity: Entity,
        account_id: int
    ) -> T:
        """
        Return an existing Account
        """
        url_parameters = UrlParameters(
            entity_id=entity.id_,
            targets=UrlTarget(key=Account._URL_KEY, value=str(account_id))
        )

        request = ApiRequest(
            path=Account._PATH,
            method=HTTPMethod.GET,
            credentials=session,
            data=None,
            url_parameters=url_parameters
        )

        account = cls._decode(session, entity, request.response_data)

        return account

    def update(
        self: T,
        name: str,
        am_type: AMType,
        parent: Optional[T],
        description: Optional[str],
        denomination: Denomination,
        counterparty: Optional[Entity],
        color: Optional[Color]
    ) -> 'Account':
        """
        Update this Account with new metadata.
        """

        arguments = Account.UpdateArguments(
            self.id_,
            name,
            am_type,
            parent,
            description,
            denomination,
            counterparty,
            color
        )

        data = DataPackage.from_object(arguments)

        request = ApiRequest(
            path=Account._PATH,
            method=HTTPMethod.PUT,
            credentials=self.session,
            data=data
        )

        account = Account._decode(
            self.session,
            self.entity,
            request.response_data
        )

        if account.id_ != self.id_:
            raise ApiError('Returned Account ID does not match request ID')

        return account

    def delete(self):
        raise NotImplementedError

    def _denomination(self) -> Denomination:
        """Return the Denomination of this account"""
        raise NotImplementedError

    class CreateArguments(Encodable):
        def __init__(
            self,
            name: str,
            description: Optional[str],
            am_type: AMType,
            parent: Optional[T],
            denomination: Denomination,
            counter_party: Optional[Entity],
            color: Optional[Color]
        ) -> None:

            self._name = Account._Name(name)
            self._description = Account._Description(description)

            if not isinstance(am_type, AMType):
                raise TypeError('am_type must be of type `AMType`')

            self._type: AMType = am_type
            self._parent = Account._Parent(parent)
            self._global_unit = Account._GlobalUnit(denomination)
            self._custom_unit = Account._CustomUnit(denomination)

            if counter_party and not isinstance(counter_party, Entity):
                raise TypeError('counter_party must be of type `Entity`')

            self._counterparty = counter_party

            if color and not isinstance(color, Color):
                raise TypeError('color must be of type `Color`')

            self._color = color

            return

        def serialise(self) -> Any:

            counterparty_id = None
            if self._counterparty:
                counterparty_id = self._counterparty.id_

            color_code = None
            if self._color:
                color_code = str(self._color)

            data = {
                'name': self._name.serialise(),
                'type': self._type.beep,
                'description': self._description.serialise(),
                'parent_account_id': self._parent.serialise(),
                'counterparty_entity_id': counterparty_id,
                'global_unit_id': self._global_unit.serialise(),
                'custom_unit_id': self._custom_unit.serialise(),
                'color': color_code
            }
            return data

    @classmethod
    def _decode(
        cls: Type[T],
        session: Session,
        entity: Entity,
        data: List[dict]
    ) -> T:

        return cls._decode_many(session, entity, data)[0]

    @classmethod
    def _decode_many(
        cls: Type[T],
        session: Session,
        entity: Entity,
        data: List[dict]
    ) -> List[T]:

        if not isinstance(data, list):
            raise ApiError('Unexpected non-list data returned')

        if len(data) < 1:
            raise ApiError('Unexpected empty response data')

        def decode(data: dict) -> T:
            if not isinstance(data, dict):
                raise ApiError('Unexpected non-dict data returned')
            try:
                account = cls(
                    session=session,
                    entity=entity,
                    account_id=data['account_id'],
                    name=data['name'],
                    am_type=AMType(data['type']),
                    description=data['description'],
                    parent_account_id=data['parent_account_id'],
                    global_unit_id=data['global_unit_id'],
                    custom_unit_id=data['custom_unit_id'],
                    counterparty_id=data['counterparty_entity_id'],
                    color=Color.from_hex_string(data['color'])
                )
            except KeyError as error:
                message = 'Expected key "{key}" missing from response data'
                message.format(key=error.args[0])
                raise ApiError(message)

            return account

        accounts = [decode(a) for a in data]

        return accounts

    class UpdateArguments(Encodable):
        def __init__(
            self,
            account_id: int,
            name: str,
            am_type: AMType,
            parent: Optional[T],
            description: Optional[str],
            denomination: Denomination,
            counterparty: Optional[Entity],
            color: Optional[Color]
        ) -> None:

            if not isinstance(account_id, int):
                raise TypeError('account_id must be of type `int`')

            self._account_id = account_id

            self._name = Account._Name(name)
            self._description = Account._Description(description)
            self._parent = Account._Parent(parent)

            if not isinstance(am_type, AMType):
                raise TypeError('am_type must be of type `AMType`')

            self._type = am_type
            self._global_unit = Account._GlobalUnit(denomination)
            self._custom_unit = Account._CustomUnit(denomination)

            if (
                    counterparty is not None
                    and not isinstance(counterparty, Entity)
            ):
                raise TypeError('counterparty must be of type `Entity`')

            self._counterparty = counterparty

            if color is not None and not isinstance(color, Color):
                raise TypeError('color must be of type `Color`')

            self._color = color

            return

        def serialise(self) -> Any:

            data = {
                'name': self._name.serialise(),
                'account_id': self._account_id,
                'description': self._description.serialise(),
                'type': self._type.value,
                'parent': self._parent.serialise()
            }
            return data

    class _Name(Encodable):
        def __init__(self, string: str) -> None:
            if not isinstance(string, str):
                raise TypeError('name must be of type `str`')
            self._name = ConstrainedString(
                string,
                'name',
                Account.MAX_NAME_LENGTH
            )
            return

        def serialise(self) -> str:
            return str(self._name)

    class _Description(Encodable):
        def __init__(self, string: Optional[str]) -> None:
            if string is not None and not isinstance(string, str):
                raise TypeError('description must be of type `str` or None')
            self._description = ConstrainedString(
                string,
                'description',
                Account.MAX_DESCRIPTION_LENGTH
            )
            return

        def serialise(self) -> str:
            return str(self._description)

    class _Parent(Encodable):
        def __init__(self, parent: Optional[T]) -> None:
            if parent is not None and not isinstance(parent, Account):
                raise TypeError('parent must be of type `Account`')
            self._parent_id = None
            if parent is not None:
                self._parent_id = parent.id_
            return

        def serialise(self) -> Optional[int]:
            return self._parent_id

    class _CustomUnit(Encodable):
        def __init__(self, denomination: Denomination) -> None:

            if not isinstance(denomination, Denomination):
                raise TypeError('denomination must be of type `Denomination`')

            self._custom_unit_id: Optional[int] = None

            if isinstance(denomination, CustomUnit):
                self._custom_unit_id = denomination.id_

            return

        def serialise(self) -> Optional[int]:
            return self._custom_unit_id

    class _GlobalUnit(Encodable):
        def __init__(self, denomination: Denomination) -> None:

            if not isinstance(denomination, Denomination):
                raise TypeError('denomination must be of type `Denomination`')

            self._global_unit_id: Optional[int] = None

            if isinstance(denomination, GlobalUnit):
                self._global_unit_id = denomination.id_

            return

        def serialise(self) -> Optional[int]:
            return self._global_unit_id
