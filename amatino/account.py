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
from amatino.missing_key import MissingKey
from amatino.denominated import Denominated

T = TypeVar('T', bound='Account')


class Account(Denominated):
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

        self._entity = entity
        self._id = account_id
        self._name = name
        self._am_type = am_type
        self._description = description
        self._parent_account_id = parent_account_id
        self._global_unit_id = global_unit_id
        self._custom_unit_id = custom_unit_id
        self._counterparty_id = counterparty_id
        self._color = color

        self._cached_denomination = None

        return

    session = Immutable(lambda s: s._entity.session)
    entity = Immutable(lambda s: s._entity)
    id_ = Immutable(lambda s: s._id)
    name = Immutable(lambda s: s._name)
    am_type = Immutable(lambda s: s._am_type)
    description = Immutable(lambda s: s._description)
    global_unit_id = Immutable(lambda s: s._global_unit_id)
    custom_unit_id = Immutable(lambda s: s._custom_unit_id)
    counterparty_id = Immutable(lambda s: s._counterparty_id)
    color = Immutable(lambda s: s._color)
    parent_id = Immutable(lambda s: s._parent_account_id)
    parent = Immutable(lambda s: s._parent())

    @classmethod
    def create(
        cls: Type[T],
        entity: Entity,
        name: str,
        am_type: AMType,
        denomination: Denomination,
        description: Optional[str] = None,
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
        parameters = UrlParameters(entity_id=entity.id_)

        request = ApiRequest(
            path=Account._PATH,
            method=HTTPMethod.POST,
            credentials=entity.session,
            data=data,
            url_parameters=parameters
        )

        account = cls._decode(entity, request.response_data)

        return account

    @classmethod
    def retrieve(
        cls: Type[T],
        entity: Entity,
        account_id: int
    ) -> T:
        """
        Return an existing Account
        """
        target = UrlTarget.from_integer(key=Account._URL_KEY, value=account_id)
        url_parameters = UrlParameters(entity_id=entity.id_, targets=[target])

        request = ApiRequest(
            path=Account._PATH,
            method=HTTPMethod.GET,
            credentials=entity.session,
            data=None,
            url_parameters=url_parameters
        )

        account = cls._decode(entity, request.response_data)

        return account

    def update(
        self: T,
        name: Optional[str] = None,
        am_type: Optional[AMType] = None,
        parent: Optional[T] = None,
        description: Optional[str] = None,
        denomination: Optional[Denomination] = None,
        counterparty: Optional[Entity] = None,
        color: Optional[Color] = None
    ) -> 'Account':
        """
        Update this Account with new metadata.
        """

        arguments = Account.UpdateArguments(
            self,
            name,
            am_type,
            parent,
            description,
            denomination,
            counterparty,
            color
        )

        data = DataPackage.from_object(arguments)
        parameters = UrlParameters(entity_id=self.entity.id_)

        request = ApiRequest(
            path=Account._PATH,
            method=HTTPMethod.PUT,
            credentials=self.entity.session,
            data=data,
            url_parameters=parameters
        )

        account = Account._decode(
            self.entity,
            request.response_data
        )

        if account.id_ != self.id_:
            raise ApiError('Returned Account ID does not match request ID')

        return account

    def delete(self):
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
            if description is None:
                description = ''
            self._description = Account._Description(description)

            if not isinstance(am_type, AMType):
                raise TypeError('am_type must be of type `AMType`')

            self._type = am_type
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
                'type': self._type.value,
                'description': self._description.serialise(),
                'parent_account_id': self._parent.serialise(),
                'counterparty_entity_id': counterparty_id,
                'global_unit_id': self._global_unit.serialise(),
                'custom_unit_id': self._custom_unit.serialise(),
                'colour': color_code
            }
            return data

    @classmethod
    def _decode(
        cls: Type[T],
        entity: Entity,
        data: List[dict]
    ) -> T:

        return cls._decode_many(entity, data)[0]

    @classmethod
    def _decode_many(
        cls: Type[T],
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
                    entity=entity,
                    account_id=data['account_id'],
                    name=data['name'],
                    am_type=AMType(data['type']),
                    description=data['description'],
                    parent_account_id=data['parent_account_id'],
                    global_unit_id=data['global_unit_id'],
                    custom_unit_id=data['custom_unit_id'],
                    counterparty_id=data['counterparty_entity_id'],
                    color=Color.from_hex_string(data['colour'])
                )
            except KeyError as error:
                raise MissingKey(error.args[0])

            return account

        accounts = [decode(a) for a in data]

        return accounts

    def _parent(self) -> Optional['Account']:
        """Return this Account's parent, if it has one"""
        if self.parent_id is None:
            return None
        assert isinstance(self.parent_id, int)
        return Account.retrieve(self.entity, self.parent_id)

    class UpdateArguments(Encodable):
        def __init__(
            self,
            account: T,
            name: Optional[str],
            am_type: Optional[AMType],
            parent: Optional[T],
            description: Optional[str],
            denomination: Optional[Denomination],
            counterparty: Optional[Entity],
            color: Optional[Color]
        ) -> None:

            if not isinstance(account, Account):
                raise TypeError('account must be of type `Account`')

            self._account_id = account.id_

            if not name:
                name = account.name
            assert isinstance(name, str)
            self._name = Account._Name(name)

            if am_type:
                if not isinstance(am_type, AMType):
                    raise TypeError('am_type must be of type `AMType`')
            else:
                am_type = account.am_type

            self._type = am_type

            if not description:
                description = account.description
            self._description = Account._Description(description)

            if not parent:
                self._parent_id = account.parent_id
            else:
                self._parent_id = Account._Parent(parent).serialise()

            if denomination:
                self._global_unit_id = Account._GlobalUnit(
                    denomination
                ).serialise()
                self._custom_unit_id = Account._CustomUnit(
                    denomination
                ).serialise()
            else:
                self._global_unit_id = account.global_unit_id
                self._custom_unit_id = account.custom_unit_id

            if counterparty:
                if not isinstance(counterparty, Entity):
                    raise TypeError('counterparty must be of type `Entity`')
                self._counterparty_id = counterparty.id_
            else:
                self._counterparty_id = account.counterparty_id

            if color:
                if not isinstance(color, Color):
                    raise TypeError('color must be of type `Color`')
                self._color = color
            else:
                self._color = account.color

            return

        def serialise(self) -> Any:

            data = {
                'name': self._name.serialise(),
                'account_id': self._account_id,
                'description': self._description.serialise(),
                'type': self._type.value,
                'parent_account_id': self._parent_id,
                'global_unit_id': self._global_unit_id,
                'custom_unit_id': self._custom_unit_id,
                'colour': self._color.serialise(),
                'counterparty_entity_id': self._counterparty_id
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

            self._custom_unit_id = None

            if isinstance(denomination, CustomUnit):
                self._custom_unit_id = denomination.id_

            return

        def serialise(self) -> Optional[int]:
            return self._custom_unit_id

    class _GlobalUnit(Encodable):
        def __init__(self, denomination: Denomination) -> None:

            if not isinstance(denomination, Denomination):
                raise TypeError('denomination must be of type `Denomination`')

            self._global_unit_id = None

            if isinstance(denomination, GlobalUnit):
                self._global_unit_id = denomination.id_

            return

        def serialise(self) -> Optional[int]:
            return self._global_unit_id
