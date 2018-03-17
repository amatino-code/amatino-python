"""
Amatino API Python Bindings
Custom Unit Module
Author: hugh@amatino.io
"""
from amatino.session import Session
from amatino.entity import Entity
from amatino.global_unit import GlobalUnit
from amatino._internal._new_custom_unit_arguments import _NewCustomUnitArguments

class CustomUnit:
    """
    Custom Units are units of account created by Amatino users. Their scope is
    limited to the Entity in which they are created. They can be used anywhere
    a Global unit would be used, allowing a user to denominate their
    Transactions and Accounts as they please.

    Custom Unit identifiers must be unique with reference to each other, but
    need not be so with reference to Global Units. Therefore, it is possible
    to create a Custom Unit implementation of a Global Unit - For example, a
    USD Custom Unit using a preferred source of foreign exchange rates.

    You may initialise a Custom Unit object in one of two ways:

    1.  Retrieve an existing Custom Unit, by supplying an existing string
        Custom Unit code to the code parameter.

    2.  Create a new Custom new, by supplying all arguments, including
        a new and unique code.

    """
    def __init__(
            self,
            session: Session,
            entity: Entity,
            code: str,
            name: str = None,
            priority: int = None,
            description: str = None,
            exponent: int = None
        ):

        self._new_unit_argumentss = None
        self._code = None
        self._session = session
        self._entity = entity

        if (
                name is not None
                or priority is not None
                or description is not None
                or exponent is not None
        ):
            self._new_unit_arguments = _NewCustomUnitArguments(
                code,
                name,
                priority,
                description,
                exponent
            )

            self._create()
            return

        self._code = code
        self._retrieve()

        return

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
            custom_unit_replacement: CustomUnit = None,
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
