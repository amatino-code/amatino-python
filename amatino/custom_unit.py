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
from amatino.internal.immutable import Immutable
from amatino.internal.constrained_string import ConstrainedString
from amatino.internal.constrained_integer import ConstrainedInteger
from amatino.internal.encodable import Encodable

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

        self._priority = priority
        self._description = description
        self._exponent = exponent

        super().__init__(code, id_, name)

        return

    session: Session = Immutable(lambda s: s._session)
    entity: Entity = Immutable(lambda s: s._entity)
    priority: int = Immutable(lambda s: s._priority)
    description: str = Immutable(lambda s: s._description)

    def _create(self) -> None:
        raise NotImplementedError

    def _retrieve(self) -> None:
        raise NotImplementedError

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
        Private - Not intended to be used directly.

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
