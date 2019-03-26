"""
Amatino API Python Bindings
Tree Module
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
from amatino.am_type import AMType
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

T = TypeVar('T', bound='Tree')
K = TypeVar('K', bound='Tree.RetrieveArguments')


class Tree(Decodable, Denominated):
    """
    Trees present the entire chart of Accounts of an Entity in a single
    hierarchical object.

    Each Account is nested under its parent, and in turn lists all its
    children, all providing Balances and Recursive Balances.

    Trees are trimmed for permissions. If the user requesting the tree only
    has read access to a subset of Accounts, they will only receive a tree
    containing those accounts, with placeholder objects filling the place
    of Accounts they are not permitted to read.

    Each Account in the Tree is presented as a Tree Node.
    """
    _PATH = '/trees'

    def __init__(
        self,
        entity: Entity,
        balance_time: AmatinoTime,
        generated_time: AmatinoTime,
        global_unit_denomination: Optional[int],
        custom_unit_denomination: Optional[int],
        tree: List[TreeNode]
    ) -> None:

        assert isinstance(entity, Entity)
        assert isinstance(balance_time, AmatinoTime)
        assert isinstance(generated_time, AmatinoTime)
        if global_unit_denomination is not None:
            assert isinstance(global_unit_denomination, int)
        if custom_unit_denomination is not None:
            assert isinstance(custom_unit_denomination, int)
        assert isinstance(tree, list)
        assert False not in [isinstance(t, TreeNode) for t in tree]

        self._entity = entity
        self._balance_time = balance_time
        self._generated_time = generated_time
        self._global_unit_id = global_unit_denomination
        self._custom_unit_id = custom_unit_denomination
        self._tree = tree

        return

    entity = Immutable(lambda s: s._entity)
    session = Immutable(lambda s: s._entity.session)
    balance_time = Immutable(lambda s: s._balance_time.raw)
    generated_time = Immutable(lambda s: s._generated_time.raw)
    custom_unit_id = Immutable(lambda s: s._custom_unit_id)
    global_unit_id = Immutable(lambda s: s._global_unit_id)
    nodes = Immutable(lambda s: s._tree)

    has_accounts = Immutable(lambda s: len(s._tree) > 0)

    income = Immutable(lambda s: s.nodes_of_type(AMType.income))
    expenses = Immutable(lambda s: s.nodes_of_type(AMType.expense))
    assets = Immutable(lambda s: s.nodes_of_type(AMType.asset))
    liabilities = Immutable(lambda s: s.nodes_of_type(AMType.liability))
    equities = Immutable(lambda s: s.nodes_of_type(AMType.equity))

    has_assets = Immutable(lambda s: len(s.nodes_of_type(AMType.asset)) > 0)
    has_liabilities = Immutable(lambda s: len(
        s.nodes_of_type(AMType.liability)) > 0
    )
    has_income = Immutable(lambda s: len(s.nodes_of_type(AMType.income)) > 0)
    has_expenses = Immutable(lambda s: len(s.nodes_of_type(AMType.expense)) > 0)
    has_equity = Immutable(lambda s: len(s.nodes_of_type(AMType.equity)) > 0)

    total_assets = Immutable(lambda s: s._total(AMType.asset))
    total_expenses = Immutable(lambda s: s._total(AMType.expense))
    total_liabilities = Immutable(lambda s: s._total(AMType.liability))
    total_income = Immutable(lambda s: s._total(AMType.income))
    total_equity = Immutable(lambda s: s._total(AMType.equity))

    def nodes_of_type(self, am_type: AMType) -> List[TreeNode]:
        """Return top-level TreeNodes of the supplied AMType"""
        if not isinstance(am_type, AMType):
            raise TypeError('am_type must be of type `AMType`')
        if not self.has_accounts:
            return list()
        nodes = [n for n in self._tree if n.am_type == am_type]
        return nodes

    def _total(self, am_type: AMType) -> Decimal:
        """Return total recursive balance for accounts with supplied type"""
        assert isinstance(am_type, AMType)
        accounts = self.nodes_of_type(am_type)
        if len(accounts) < 1:
            return Decimal(0)
        total = sum([a.recursive_balance for a in accounts])
        assert isinstance(total, Decimal)
        return total

    @classmethod
    def decode(cls: Type[T], entity: Entity, data: Any) -> T:

        if not isinstance(data, dict):
            raise UnexpectedResponseType(data, dict)

        try:

            tree = cls(
                entity=entity,
                balance_time=AmatinoTime.decode(data['balance_time']),
                generated_time=AmatinoTime.decode(data['generated_time']),
                global_unit_denomination=data['global_unit_denomination'],
                custom_unit_denomination=data['custom_unit_denomination'],
                tree=TreeNode.decode_many(entity, data['tree'])
            )

        except KeyError as error:
            raise MissingKey(error.args[0])

        return tree

    @classmethod
    def retrieve(
        cls: Type[T],
        entity: Entity,
        balance_time: datetime,
        denomination: Denomination
    ) -> T:

        arguments = cls.RetrieveArguments(
            balance_time=balance_time,
            denomination=denomination
        )

        return cls._retrieve(entity, arguments)

    @classmethod
    def _retrieve(
        cls: Type[T],
        entity: Entity,
        arguments: K
    ) -> T:

        if not isinstance(entity, Entity):
            raise TypeError('entity must be of type Entity')

        assert isinstance(arguments, cls.RetrieveArguments)
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

    class RetrieveArguments(Encodable):
        def __init__(
            self,
            balance_time: datetime,
            denomination: Denomination
        ) -> None:

            if not isinstance(balance_time, datetime):
                raise TypeError('balance_time must be of type `datetime`')

            if not isinstance(denomination, Denomination):
                raise TypeError('denomination must be of type `denomination`')

            self._balance_time = AmatinoTime(balance_time)
            self._denomination = denomination

        def serialise(self) -> Dict[str, Any]:

            global_unit_id = None
            custom_unit_id = None

            if isinstance(self._denomination, GlobalUnit):
                global_unit_id = self._denomination.id_
            else:
                assert isinstance(self._denomination, CustomUnit)
                custom_unit_id = self._denomination.id_

            data = {
                'balance_time': self._balance_time.serialise(),
                'custom_unit_denomination': custom_unit_id,
                'global_unit_denomination': global_unit_id
            }

            return data
