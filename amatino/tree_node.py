"""
Amatino API Python Bindings
Tree Node Module
Author: hugh@amatino.io
"""
from typing import TypeVar
from typing import Type
from typing import Any
from typing import List
from typing import Optional
from amatino.decodable import Decodable
from amatino.missing_key import MissingKey
from amatino.am_type import AMType
from amatino.entity import Entity
from amatino.internal.immutable import Immutable
from amatino.unexpected_response_type import UnexpectedResponseType
from amatino.account import Account
from amatino.internal.am_amount import AmatinoAmount
from decimal import Decimal

T = TypeVar('T', bound='TreeNode')


class TreeNode(Decodable):
    """
    A Tree Node is a specialised view of an Account. It provides a recursive
    and individual balance for an Account. You will never interact with Tree
    Nodes' directly, instead you will receive lists of Tree Nodes as components
    of requests for Trees, Positions, and Performances.

    Tree Nodes are recursive objects that may contain other Tree Nodes,
    depending on whether the Account in question has any children.

    Trees, Positions, and Performances describe entire Entities. The User from
    whose perspective you retrieve a Tree, Position, or Performance may not
    have read access to every Account in the Entity. In such cases, Tree Nodes
    describing Accounts to which a User does not have read access will be
    returned with null in their balance fields, and a generic Type in place of
    the actual Account name.
    """

    def __init__(
        self,
        entity: Entity,
        account_id: int,
        depth: int,
        account_balance: Decimal,
        recursive_balance: Decimal,
        name: str,
        am_type: AMType,
        children: Optional[List[T]]
    ) -> None:

        assert isinstance(entity, Entity)
        assert isinstance(account_id, int)
        assert isinstance(depth, int)
        assert isinstance(account_balance, Decimal)
        assert isinstance(recursive_balance, Decimal)
        assert isinstance(name, str)
        assert isinstance(am_type, AMType)
        if children is not None:
            assert isinstance(children, list)
            assert False not in [isinstance(c, TreeNode) for c in children]

        self._entity = entity
        self._account_id = account_id
        self._depth = depth
        self._account_balance = account_balance
        self._recursive_balance = recursive_balance
        self._name = name
        self._am_type = am_type
        self._children = children

        return

    session = Immutable(lambda s: s._entity.session)
    entity = Immutable(lambda s: s._entity)
    account_id = Immutable(lambda s: s._account_id)
    depth = Immutable(lambda s: s._depth)
    account_balance = Immutable(lambda s: s._account_balance)
    recursive_balance = Immutable(lambda s: s._recursive_balance)
    name = Immutable(lambda s: s._name)
    am_type = Immutable(lambda s: s._am_type)
    children = Immutable(lambda s: s._children)

    has_children = Immutable(
        lambda s: s._children is not None and len(s._children) > 0
    )
    account = Immutable(lambda s: s._account())

    _node_cached_account = None

    def _account(self) -> Account:
        """
        Return the Account this TreeNode describes. Cache it for repeated
        requests.
        """
        if isinstance(self._node_cached_account, Account):
            return self._node_cached_account
        account = Account.retrieve(
            session=self.entity.session,
            entity=self.entity,
            account_id=self.account_id
        )
        self._node_cached_account = account
        return account

    @classmethod
    def decode(cls: Type[T], entity: Entity, data: Any) -> T:

        if not isinstance(data, dict):
            raise UnexpectedResponseType(data, dict)

        try:
            children = None
            if data['children'] is not None:
                children = [cls.decode(entity, d) for d in data['children']]
            node = cls(
                entity=entity,
                account_id=data['account_id'],
                depth=data['depth'],
                account_balance=AmatinoAmount.decode(
                    data['account_balance']
                ),
                recursive_balance=AmatinoAmount.decode(
                    data['recursive_balance']
                ),
                name=data['name'],
                am_type=AMType(data['type']),
                children=children
            )
        except KeyError as error:
            raise MissingKey(error.args[0])

        return node
