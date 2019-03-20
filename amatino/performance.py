"""
Amatino API Python Bindings
Performance Module
Author: hugh@amatino.io
"""
from typing import Type
from typing import TypeVar
from typing import List
from typing import Optional
from typing import Any
from typing import Dict
from datetime import datetime
from decimal import Decimal
from amatino.denominated import Denominated
from amatino.denomination import Denomination
from amatino.decodable import Decodable
from amatino.internal.data_package import DataPackage
from amatino.internal.api_request import ApiRequest
from amatino.internal.url_parameters import UrlParameters
from amatino.internal.http_method import HTTPMethod
from amatino.internal.encodable import Encodable
from amatino.missing_key import MissingKey
from amatino.entity import Entity
from amatino.unexpected_response_type import UnexpectedResponseType
from amatino.internal.am_time import AmatinoTime
from amatino.tree_node import TreeNode
from amatino.internal.immutable import Immutable
from amatino.global_unit import GlobalUnit
from amatino.custom_unit import CustomUnit

T = TypeVar('T', bound='Performance')
K = TypeVar('K', bound='Performance.RetrieveArguments')


class Performance(Denominated, Decodable):
    """
    A Performance is a hierarchical collection of Account balances describing
    the financial performance of an Entity over a period of time. They are
    generic representations of popular accounting constructs known as the
    'Income Statement', 'Profit & Loss', or 'Statement of Financial
    Performance'.

    The Peformance object is jurisdiction agnostic, and obeys simple
    double-entry accounting rules. They list income and expense, each nesting
    its own children.

    You can retrieve a Performance denominated in an arbitrary Global Unit or
    Custom Unit. Amatino will automatically calculate the implicit gain or loss
    relative to each Account's underlying denomination and include those gains
    and losses in each Account balance.

    A Performance may be retrieved to an arbitrary depth. Depth in the
    Performance context is the number of levels down the Account hierarchy
    Amatino should go when retrieving the Performance. For example, if a
    top-level Account has child accounts three layers deep, then specifying a
    depth of three will retrieve all those children.

    Regardless of the depth you specify, Amatino will calculate recursive
    balances at full depth.
    """

    _PATH = '/performances'

    def __init__(
        self,
        entity: Entity,
        start_time: AmatinoTime,
        end_time: AmatinoTime,
        generated_time: AmatinoTime,
        global_unit_id: Optional[int],
        custom_unit_id: Optional[int],
        income: List[TreeNode],
        expenses: List[TreeNode],
        depth: int
    ) -> None:

        assert isinstance(entity, Entity)
        assert isinstance(start_time, AmatinoTime)
        assert isinstance(end_time, AmatinoTime)
        assert isinstance(generated_time, AmatinoTime)
        if global_unit_id is not None:
            assert isinstance(global_unit_id, int)
        if custom_unit_id is not None:
            assert isinstance(custom_unit_id, int)
        assert isinstance(income, list)
        assert False not in [isinstance(i, TreeNode) for i in income]
        assert isinstance(expenses, list)
        assert False not in [isinstance(e, TreeNode) for e in expenses]
        assert isinstance(depth, int)

        self._entity = entity
        self._start_time = start_time
        self._end_time = end_time
        self._generated_time = generated_time
        self._global_unit_id = global_unit_id
        self._custom_unit_id = custom_unit_id
        self._income = income
        self._expenses = expenses
        self._depth = depth

        return

    entity = Immutable(lambda s: s._entity)
    session = Immutable(lambda s: s._entity.session)
    start_time = Immutable(lambda s: s._start_time.raw)
    end_time = Immutable(lambda s: s._end_time.raw)
    generated_time = Immutable(lambda s: s._generated_time.raw)
    custom_unit_id = Immutable(lambda s: s._custom_unit_id)
    global_unit_id = Immutable(lambda s: s._global_unit_id)
    income = Immutable(lambda s: s._income)
    expenses = Immutable(lambda s: s._expenses)

    has_income = Immutable(lambda s: len(s._income) > 0)
    has_expenses = Immutable(lambda s: len(s._expenses) > 0)

    total_income = Immutable(lambda s: s._compute_income())
    total_expenses = Immutable(lambda s: s._compute_expenses())

    @classmethod
    def decode(
        cls: Type[T],
        entity: Entity,
        data: Any
    ) -> T:

        if not isinstance(data, dict):
            raise UnexpectedResponseType(data, dict)

        try:

            income = None
            if data['income'] is not None:
                income = TreeNode.decode_many(entity, data['income'])

            expenses = None
            if data['expenses'] is not None:
                expenses = TreeNode.decode_many(entity, data['expenses'])

            performance = cls(
                entity=entity,
                start_time=AmatinoTime.decode(data['start_time']),
                end_time=AmatinoTime.decode(data['end_time']),
                generated_time=AmatinoTime.decode(data['generated_time']),
                custom_unit_id=data['custom_unit_denomination'],
                global_unit_id=data['global_unit_denomination'],
                income=income,
                expenses=expenses,
                depth=data['depth']
            )
        except KeyError as error:
            raise MissingKey(error.args[0])

        return performance

    @classmethod
    def retrieve(
        cls: Type[T],
        entity: Entity,
        start_time: datetime,
        end_time: datetime,
        denomination: Denomination,
        depth: Optional[int] = None
    ) -> T:

        arguments = cls.RetrieveArguments(
            start_time=start_time,
            end_time=end_time,
            denomination=denomination,
            depth=depth
        )

        return cls._retrieve(entity, arguments)

    @classmethod
    def _retrieve(cls: Type[T], entity: Entity, arguments: K) -> T:
        """Retrieve a Performance"""
        if not isinstance(entity, Entity):
            raise TypeError('entity must be of type `Entity`')

        if not isinstance(arguments, cls.RetrieveArguments):
            raise TypeError(
                'arguments must be of type Performance.RetrieveArguments'
            )

        data = DataPackage(object_data=arguments, override_listing=True)
        parameters = UrlParameters(entity_id=entity.id_)

        request = ApiRequest(
            path=cls._PATH,
            method=HTTPMethod.GET,
            credentials=entity.session,
            data=data,
            url_parameters=parameters
        )

        return cls.decode(entity, request.response_data)

    def _compute_income(self) -> Decimal:
        """Return total income"""
        if not self.has_income:
            return Decimal(0)
        income = sum([i.recursive_balance for i in self._income])
        assert isinstance(income, Decimal)
        return income

    def _compute_expenses(self) -> Decimal:
        """Return total expenses"""
        if not self.has_expenses:
            return Decimal(0)
        expenses = sum([e.recursive_balance for e in self._expenses])
        assert isinstance(expenses, Decimal)
        return expenses

    class RetrieveArguments(Encodable):
        def __init__(
            self,
            start_time: datetime,
            end_time: datetime,
            denomination: Denomination,
            depth: Optional[int] = None
        ) -> None:

            if not isinstance(start_time, datetime):
                raise TypeError('start_time must be of type `datetime`')

            if not isinstance(end_time, datetime):
                raise TypeError('end_time must be of type `datetime`')

            if not isinstance(denomination, Denomination):
                raise TypeError('denomination must be of type `Denomination`')

            if depth is not None and not isinstance(depth, int):
                raise TypeError(
                    'If supplied, depth must be of type `int`'
                )

            self._start_time = AmatinoTime(start_time)
            self._end_time = AmatinoTime(end_time)
            self._denomination = denomination
            self._depth = depth

            return

        def serialise(self) -> Dict[str, Any]:

            global_unit_id = None
            custom_unit_id = None

            if isinstance(self._denomination, GlobalUnit):
                global_unit_id = self._denomination.id_
            else:
                assert isinstance(self._denomination, CustomUnit)
                custom_unit_id = self._denomination.id_

            data = {
                'start_time': self._start_time.serialise(),
                'end_time': self._end_time.serialise(),
                'custom_unit_denomination': custom_unit_id,
                'global_unit_denomination': global_unit_id,
                'depth': self._depth
            }

            return data
