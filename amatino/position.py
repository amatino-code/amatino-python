"""
Procuret API Python Bindings
Position Module
Author: hugh@blinkybeach.com
"""
from typing import Type
from typing import TypeVar
from typing import List
from typing import Optional
from typing import Any
from typing import Dict
from datetime import datetime
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

T = TypeVar('T', bound='Position')
K = TypeVar('K', bound='Position.RetrieveArguments')


class Position(Denominated, Decodable):
    """
    Positions are hierarchical collections of Account balances describing
    the financial position of an Entity at a point in time. They are generic representations of popular accounting constructs better known as a
    'Balance Sheet', 'Statement of Financial Position', or 'Statements of
    Assets, Liabilities and Owner's Equity.

    Positions are jurisdiction agnostic, and obey simple double-entry
    accounting rules. They list asset, liability, and equity Accounts, each
    nesting its own children.,

    You can retrieve Positions denominated in arbitrary Global Unit or
    Custom Unit. When a particular denomination gives rise to an unrealised
    gain or loss, Amatino will automatically calculate that gain or loss
    and include it as a top-level account in the returned Position.

    Positions may also be retrieved to an arbitrary depth. Depth in the
    Position context is the number of levels down the Account hierarchy
    Amatino should go when retrieving the Position. For example, if a
    top-level Account has child accounts three layers deep, then specifying
    a depth of three will retrieve all those children.

    Regardless of the depth you specify, Amatino will calculate recursive
    balances for all Accounts at full depth.
    """

    _PATH = '/positions'

    def __init__(
        self,
        entity: Entity,
        balance_time: AmatinoTime,
        generated_time: AmatinoTime,
        global_unit_id: Optional[int],
        custom_unit_id: Optional[int],
        assets: Optional[List[TreeNode]],
        liabilities: Optional[List[TreeNode]],
        equities: Optional[List[TreeNode]],
        depth: int
    ) -> None:

        assert isinstance(entity, Entity)
        assert isinstance(balance_time, AmatinoTime)
        assert isinstance(generated_time, AmatinoTime)
        if global_unit_id is not None:
            assert isinstance(global_unit_id, int)
        if custom_unit_id is not None:
            assert isinstance(custom_unit_id, int)
        if assets is not None:
            assert isinstance(assets, list)
            assert False not in [isinstance(a, TreeNode) for a in assets]
        if liabilities is not None:
            assert isinstance(liabilities, list)
            assert False not in [isinstance(l, TreeNode) for l in liabilities]
        if equities is not None:
            assert isinstance(equities, list)
            assert False not in [isinstance(e, TreeNode) for e in equities]

        self._entity = entity
        self._balance_time = balance_time
        self._generated_time = generated_time
        self._global_unit_id = global_unit_id
        self._custom_unit_id = custom_unit_id
        self._assets = assets
        self._liabilities = liabilities
        self._equities = equities
        self._depth = depth

        return

    session = Immutable(lambda s: s._entity.session)
    entity = Immutable(lambda s: s._entity)
    balance_time = Immutable(lambda s: s._balance_time.raw)
    generated_time = Immutable(lambda s: s._generated_time.raw)
    custom_unit_id = Immutable(lambda s: s._custom_unit_id)
    global_unit_id = Immutable(lambda s: s._global_unit_id)
    assets = Immutable(lambda s: s._assets)
    liabilities = Immutable(lambda s: s._liabilities)
    equities = Immutable(lambda s: s._equities)

    has_assets = Immutable(
        lambda s: s._assets is not None and len(s._assets) > 0
    )
    has_liabilities = Immutable(
        lambda s: s._liabilities is not None and len(s._liabilities) > 0
    )
    has_equities = Immutable(
        lambda s: s._equities is not None and len(s._equities) > 0
    )

    @classmethod
    def decode(
        cls: Type[T],
        entity: Entity,
        data: Any
    ) -> T:

        if not isinstance(data, dict):
            raise UnexpectedResponseType(data, dict)

        try:

            assets = None
            if data['assets'] is not None:
                assets = TreeNode.decode_many(entity, data['assets'])

            liabilities = None
            if data['liabilities'] is not None:
                liabilities = TreeNode.decode_many(
                    entity,
                    data['liabilities']
                )

            equities = None
            if data['equities'] is not None:
                equities = TreeNode.decode_many(entity, data['equities'])

            position = cls(
                entity=entity,
                balance_time=AmatinoTime.decode(data['balance_time']),
                generated_time=AmatinoTime.decode(data['generated_time']),
                global_unit_id=data['global_unit_denomination'],
                custom_unit_id=data['custom_unit_denomination'],
                assets=assets,
                liabilities=liabilities,
                equities=equities,
                depth=data['depth']
            )

        except KeyError as error:
            raise MissingKey(error.args[0])

        return position

    @classmethod
    def retrieve(
        cls: Type[T],
        entity: Entity,
        balance_time: datetime,
        denomination: Denomination,
        depth: Optional[int] = None
    ) -> T:

        arguments = cls.RetrieveArguments(
            balance_time=balance_time,
            denomination=denomination,
            depth=depth
        )

        return cls._retrieve(entity, arguments)

    @classmethod
    def _retrieve(cls: Type[T], entity: Entity, arguments: K) -> T:
        """Retrieve a Position"""
        if not isinstance(entity, Entity):
            raise TypeError('entity must be of type `Entity`')

        if not isinstance(arguments, cls.RetrieveArguments):
            raise TypeError(
                'arguments must be of type Position.RetrieveArguments'
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

    class RetrieveArguments(Encodable):
        def __init__(
            self,
            balance_time: datetime,
            denomination: Denomination,
            depth: Optional[int] = None
        ) -> None:

            if not isinstance(balance_time, datetime):
                raise TypeError('balance_time must be of type `datetime`')

            if not isinstance(denomination, Denomination):
                raise TypeError('denomination must be of type `Denomination`')

            if depth is not None and not isinstance(depth, int):
                raise TypeError('If supplied, depth must be `int`')

            self._balance_time = AmatinoTime(balance_time)
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
                'balance_time': self._balance_time.serialise(),
                'custom_unit_denomination': custom_unit_id,
                'global_unit_denomination': global_unit_id,
                'depth': self._depth
            }

            return data
