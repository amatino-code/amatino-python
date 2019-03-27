"""
Amatino API Python Bindings
Custom Unit Module
Author: hugh@amatino.io
"""
from amatino.entity import Entity
from amatino.global_unit import GlobalUnit
from amatino.denomination import Denomination
from typing import TypeVar
from typing import Optional
from typing import Type
from typing import List
from typing import Any
from typing import Dict
from amatino.internal.immutable import Immutable
from amatino.internal.constrained_string import ConstrainedString
from amatino.internal.constrained_integer import ConstrainedInteger
from amatino.internal.encodable import Encodable
from amatino.internal.url_target import UrlTarget
from amatino.internal.url_parameters import UrlParameters
from amatino.internal.api_request import ApiRequest
from amatino.internal.http_method import HTTPMethod
from amatino.internal.data_package import DataPackage
from amatino.api_error import ApiError

T = TypeVar('T', bound='CustomUnit')


class CustomUnit(Denomination):
    """
    Custom Units are units of account created by Amatino users. Their scope is
    limited to the Entity in which they are created. They can be used anywhere
    a Global unit would be used, allowing a user to denominate their
    Transactions and Accounts as they please.

    Custom Unit identifiers must be unique with reference to each other, but
    need not be so with reference to Global Units. Therefore, it is possible
    to create a Custom Unit implementation of a Global Unit - For example, a
    USD Custom Unit using a preferred source of foreign exchange rates.
    """
    MAX_DESCRIPTION_LENGTH = 1024
    MIN_CODE_LENGTH = 3
    MAX_CODE_LENGTH = 64
    MAX_NAME_LENGTH = 1024
    MAX_EXPONENT_VALUE = 6
    MIN_EXPONENT_VALUE = 0
    MAX_PRIORITY_VALUE = 10000
    MIN_PRIORITY_VALUE = -10000
    _URL_KEY = 'custom_unit_id'
    _PATH = '/custom_units'

    def __init__(
        self,
        entity: Entity,
        id_: int,
        code: str,
        name: str,
        priority: int,
        description: str,
        exponent: int
    ) -> None:

        self._entity = entity

        super().__init__(code, id_, name, priority, description, exponent)

        return

    session = Immutable(lambda s: s._entity._session)
    entity = Immutable(lambda s: s._entity)

    @classmethod
    def create(
        cls: Type[T],
        entity: Entity,
        name: str,
        code: str,
        exponent: int,
        description: Optional[str] = None,
        priority: Optional[int] = None
    ) -> T:

        arguments = CustomUnit.CreationArguments(
            code,
            name,
            exponent,
            priority,
            description
        )

        parameters = UrlParameters(entity_id=entity.id_)

        request = ApiRequest(
            path=CustomUnit._PATH,
            credentials=entity.session,
            method=HTTPMethod.POST,
            data=DataPackage.from_object(arguments),
            url_parameters=parameters
        )

        return CustomUnit._decode(entity, request.response_data)

    @classmethod
    def retrieve(
        cls: Type[T],
        entity: Entity,
        custom_unit_id: int
    ) -> T:

        target = UrlTarget.from_integer(cls._URL_KEY, custom_unit_id)
        parameters = UrlParameters(entity_id=entity.id_, targets=[target])

        request = ApiRequest(
            path=cls._PATH,
            method=HTTPMethod.GET,
            data=None,
            url_parameters=parameters,
            credentials=entity.session
        )

        return cls._decode(entity, request.response_data)

    @classmethod
    def _retrieve(
        cls: Type[T],
        entity: Entity,
        custom_unit_ids: List[int]
    ) -> T:

        if not isinstance(entity, Entity):
            raise TypeError('entity must be of type `Entity`')

        key = CustomUnit._URL_KEY
        targets = [UrlTarget(key, str(i)) for i in custom_unit_ids]

        url_parameters = UrlParameters(
            entity_id=entity.id_,
            targets=targets
        )

        request = ApiRequest(
            path=CustomUnit._PATH,
            method=HTTPMethod.GET,
            credentials=entity.session,
            data=None,
            url_parameters=url_parameters
        )

        unit = cls._decode(
            entity,
            request.response_data
        )

        return unit

    @classmethod
    def _decode(
        cls: Type[T],
        entity: Entity,
        data: Any
    ) -> T:
        return cls._decodeMany(entity, data)[0]

    @classmethod
    def _decodeMany(
        cls: Type[T],
        entity: Entity,
        data: Any
    ) -> List[T]:

        assert isinstance(entity, Entity)

        if not isinstance(data, list):
            raise ApiError('Unexpected non-list data returned')

        if len(data) < 1:
            raise ApiError('Unexpected empty response data')

        def decode(data: dict) -> T:
            if not isinstance(data, dict):
                raise ApiError('Unexpected non-dict data returned')
            try:
                unit = cls(
                    entity=entity,
                    id_=data['custom_unit_id'],
                    code=data['code'],
                    name=data['name'],
                    priority=data['priority'],
                    description=data['description'],
                    exponent=data['exponent']
                )
            except KeyError as error:
                message = 'Expected key "{key}" missing from response data'
                message.format(key=error.args[0])
                raise ApiError(message)

            return unit

        units = [decode(u) for u in data]

        return units

    def update(
        self,
        name: Optional[str] = None,
        code: Optional[str] = None,
        priority: Optional[int] = None,
        description: Optional[str] = None,
        exponent: Optional[str] = None
    ) -> None:
        """
        Replace existing Custom Unit data with supplied data. Parameters
        not supplied will default to existing values.
        """
        if name is None:
            name = self.name
        if code is None:
            code = self.code
        if priority is None:
            priority = self.priority
        if description is None:
            description = self.description
        if exponent is None:
            exponent = self.exponent

        assert isinstance(code, str)
        assert isinstance(priority, int)
        assert isinstance(description, str)
        assert isinstance(exponent, int)

        arguments = CustomUnit.UpdateArguments(
            self.id_,
            code,
            name,
            exponent,
            priority,
            description
        )

        parameters = UrlParameters(entity_id=self.entity.id_)

        request = ApiRequest(
            path=self._PATH,
            method=HTTPMethod.PUT,
            data=DataPackage.from_object(arguments),
            url_parameters=parameters,
            credentials=self.entity.session
        )

        return CustomUnit._decode(
            self.entity,
            request.response_data
        )

    def delete(
        self,
        custom_unit_replacement: T = None,
        global_unit_replacement: GlobalUnit = None
    ) -> None:
        """
        Irrecoverably delete this Custom Unit. Supply either a Custom Unit
        or Global Unit with which to replace any instances of this
        Custom Unit presently denominating an Account. Even if you are
        certain that this Custom Unit does not presently denominated any
        Account, you must supply a replacement unit.
        """
        raise NotImplementedError

    class CreationArguments(Encodable):
        """
        Used by instances of class CustomUnit to validate arguments provided
        for the creation of a new Custom Unit
        """
        def __init__(
            self,
            code: str,
            name: str,
            exponent: int,
            priority: Optional[int] = None,
            description: Optional[str] = None
        ) -> None:

            super().__init__()

            self._code = CustomUnit._Code(code)
            self._name = CustomUnit._Name(name)
            self._priority = CustomUnit._Priority(priority)
            self._description = CustomUnit._Description(description)
            self._exponent = CustomUnit._Exponent(exponent)

            return

        def serialise(self) -> dict:
            data = {
                'code': self._code.serialise(),
                'name': self._name.serialise(),
                'priority': self._priority.serialise(),
                'description': self._description.serialise(),
                'exponent': self._exponent.serialise()
            }
            return data

    class UpdateArguments(Encodable):
        def __init__(
            self,
            custom_unit_id: int,
            code: str,
            name: str,
            exponent: int,
            priority: Optional[int] = None,
            description: Optional[str] = None
        ) -> None:

            if not isinstance(custom_unit_id, int):
                raise TypeError('custom_unit_id must be of type `int`')

            self._id = custom_unit_id

            self._code = CustomUnit._Code(code)
            self._name = CustomUnit._Name(name)
            self._priority = CustomUnit._Priority(priority)
            self._description = CustomUnit._Description(description)
            self._exponent = CustomUnit._Exponent(exponent)

            return

        def serialise(self) -> Dict[str, Any]:
            data = {
                'custom_unit_id': self._id,
                'code': self._code.serialise(),
                'name': self._name.serialise(),
                'priority': self._priority.serialise(),
                'description': self._description.serialise(),
                'exponent': self._exponent.serialise()
            }
            return data

    class _Priority(Encodable):
        def __init__(self, priority: Optional[int]) -> None:

            self._priority = priority
            if priority is None:
                return

            self._priority = ConstrainedInteger(
                priority,
                'priority',
                CustomUnit.MAX_PRIORITY_VALUE,
                CustomUnit.MIN_PRIORITY_VALUE
            )
            return

        def serialise(self) -> Optional[int]:
            if self._priority is None:
                return None
            assert isinstance(self._priority, ConstrainedInteger)
            return self._priority.serialise()

    class _Code(ConstrainedString):
        def __init__(self, code: str) -> None:
            super().__init__(
                code,
                'code',
                CustomUnit.MAX_CODE_LENGTH,
                CustomUnit.MIN_CODE_LENGTH
            )
            return

    class _Name(ConstrainedString):
        def __init__(self, name: str) -> None:
            super().__init__(
                name,
                'name',
                CustomUnit.MAX_NAME_LENGTH
            )
            return

    class _Description(ConstrainedString):
        def __init__(self, description: Optional[str]) -> None:
            if description is None:
                description = ''
            super().__init__(
                description,
                'description',
                CustomUnit.MAX_DESCRIPTION_LENGTH
            )
            return

    class _Exponent(ConstrainedInteger):
        def __init__(self, exponent: int) -> None:
            super().__init__(
                exponent,
                'exponent',
                CustomUnit.MAX_EXPONENT_VALUE,
                CustomUnit.MIN_EXPONENT_VALUE
            )
            return

    def __repr__(self) -> str:
        rep = '<amatino.CustomUnit at {memory}, id: {id_}, code: {code}, '
        rep += 'name: {name}, priority: {priority}, exponent: {exponent}, '
        rep += 'description: {description}, session: {session_id}, '
        rep += 'entity: {entity_id}>'
        representation = rep.format(
            memory=hex(id(self)),
            id_=str(self.id_),
            code=self.code,
            name=self.name,
            priority=self.priority,
            exponent=self.exponent,
            description=self.description,
            session_id=str(self.entity.session.id_),
            entity_id=self.entity.id_
        )
        return representation
