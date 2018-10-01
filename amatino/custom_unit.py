"""
Amatino API Python Bindings
Custom Unit Module
Author: hugh@amatino.io
"""
from amatino.session import Session
from amatino.entity import Entity
from amatino.global_unit import GlobalUnit
from amatino.denomination import Denomination
from typing import TypeVar
from typing import Optional
from typing import Type
from typing import List
from typing import Any
from amatino.internal.immutable import Immutable
from amatino.internal.constrained_string import ConstrainedString
from amatino.internal.constrained_integer import ConstrainedInteger
from amatino.internal.encodable import Encodable
from amatino.internal.url_target import UrlTarget
from amatino.internal.url_parameters import UrlParameters
from amatino.internal.api_request import ApiRequest
from amatino.internal.http_method import HTTPMethod
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
    _URL_KEY = 'custom_unit_id'

    def __init__(
        self,
        session: Session,
        entity: Entity,
        id_: int,
        code: str,
        name: str,
        priority: int,
        description: str,
        exponent: int
    ) -> None:

        self._session = session
        self._entity = entity

        super().__init__(code, id_, name, priority, description, exponent)

        return

    session: Session = Immutable(lambda s: s._session)
    entity: Entity = Immutable(lambda s: s._entity)

    @classmethod
    def _create(self) -> None:
        raise NotImplementedError

    @classmethod
    def retrieve(
        cls: Type[T],
        entity: Entity,
        session: Session,
        custom_unit_id: int
    ) -> T:

        raise NotImplementedError

    @classmethod
    def _retrieve(
        cls: Type[T],
        entity: Entity,
        session: Session,
        custom_unit_ids: List[int]
    ) -> T:

        if not isinstance(entity, Entity):
            raise TypeError('entity must be of type `Entity`')

        if not isinstance(session, Session):
            raise TypeError('session must be of type `Session')

        key = CustomUnit._URL_KEY
        targets = [UrlTarget(key, str(i)) for i in custom_unit_ids]

        url_parameters = UrlParameters(
            entity_id=entity.id_,
            targets=targets
        )

        request = ApiRequest(
            path=CustomUnit._PATH,
            method=HTTPMethod.GET,
            credentials=session,
            data=None,
            url_parameters=url_parameters
        )

        unit = cls._decode(
            session,
            entity,
            request.response_data
        )

        return unit

    @classmethod
    def _decode(
        cls: Type[T],
        session: Session,
        entity: Entity,
        data: Any
    ) -> T:
        return cls._decodeMany(session, entity, data)[0]

    @classmethod
    def _decodeMany(
        cls: Type[T],
        session: Session,
        entity: Entity,
        data: Any
    ) -> List[T]:
        if not isinstance(data, list):
            raise ApiError('Unexpected non-list data returned')

        if len(data) < 1:
            raise ApiError('Unexpected empty response data')

        def decode(data: dict) -> T:
            if not isinstance(data, dict):
                raise ApiError('Unexpected non-dict data returned')
            try:
                unit = cls(
                    session=session,
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
        name: str = None,
        priority: int = None,
        description: str = None,
        exponent: str = None
    ) -> None:
        """
        Replace existing Custom Unit data with supplied data. Parameters
        not supplied will default to existing values.
        """
        raise NotImplementedError

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

            self._code = ConstrainedString(
                code,
                'code',
                CustomUnit.MAX_CODE_LENGTH,
                CustomUnit.MIN_CODE_LENGTH
            )
            self._name = ConstrainedString(
                name,
                'name',
                CustomUnit.MAX_DESCRIPTION_LENGTH
            )
            self._priority = CustomUnit._Priority(priority)
            self._description = ConstrainedString(
                description,
                'description',
                CustomUnit.MAX_DESCRIPTION_LENGTH
            )
            self._exponent = ConstrainedInteger(
                exponent,
                'exponent',
                CustomUnit.MAX_EXPONENT_VALUE,
                CustomUnit.MIN_EXPONENT_VALUE
            )
            self._package = {
                'code': str(self._code),
                'name': str(self._name),
                'priority': self._priority.serialise(),
                'description': str(self._description),
                'exponent': self._exponent.serialise()
            }

            return

        def serialise(self) -> dict:
            return self._package

        class _Priority(Encodable):
            def __init__(self, priority: Optional[int]) -> None:
                if priority is not None and not isinstance(priority, int):
                    raise TypeError('priority must be of type `int`')

                self._priority: Optional[ConstrainedInteger] = priority

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
                return self._priority.serialise()
