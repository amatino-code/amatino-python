"""
Amatino API Python Bindings
Transaction Version List Module
Author: hugh@amatino.io
"""
from amatino import Transaction, Entity
from amatino.internal.api_request import ApiRequest
from amatino.internal.url_parameters import UrlParameters
from amatino.internal.url_target import UrlTarget
from amatino.internal.http_method import HTTPMethod
from amatino.unexpected_response_type import UnexpectedResponseType
from amatino.internal.immutable import Immutable
from amatino.api_error import ApiError
from amatino.missing_key import MissingKey
from typing import TypeVar, Type, List, Any
from collections.abc import Sequence

T = TypeVar('T', bound='TransactionVersionList')


class TransactionVersionList(Sequence):
    """
    Amatino retains a version history of every Transaction. That history
    allows you to step backwards and forwards through changes to the accounting
    information describing an Entity. To view the history of a Transaction, you
    can retrieve a Transaction Version List.
    """
    _PATH = '/transactions/version/list'

    def __init__(
        self,
        entity: Entity,
        transaction_id: int,
        versions: List[Transaction]
    ) -> None:

        assert isinstance(entity, Entity)
        assert isinstance(transaction_id, int)
        assert isinstance(versions, list)
        if len(versions) > 0:
            assert False not in [isinstance(t, Transaction) for t in versions]

        self._entity = entity
        self._transaction_id = transaction_id
        self._versions = versions

        return

    versions = Immutable(lambda s: s._versions)
    entity = Immutable(lambda s: s._entity)
    session = Immutable(lambda s: s._entity.session)

    def __len__(self):
        return len(self.versions)

    def __getitem__(self, key):
        return self.versions[key]

    def __iter__(self):
        return TransactionVersionList.Iterator(self._versions)

    class Iterator:
        """An iterator for iterating through versions"""

        def __init__(self, versions: List[Transaction]) -> None:
            self._index = 0
            self._versions = versions
            return

        def __next__(self) -> Transaction:
            if self._index >= len(self._versions):
                raise StopIteration
            version = self._versions[self._index]
            self._index += 1
            return version

    @classmethod
    def retrieve(
        cls: Type[T],
        entity: Entity,
        transaction: Transaction
    ) -> T:
        """Return a TransactionVersionList for the supplied Transaction"""

        if not isinstance(transaction, Transaction):
            raise TypeError('transaction must be of type Transaction')

        if not isinstance(entity, Entity):
            raise TypeError('entity must be of type Entity')

        targets = [UrlTarget.from_integer('transaction_id', transaction.id_)]
        parameters = UrlParameters(entity_id=entity.id_, targets=targets)
        request = ApiRequest(
            path=cls._PATH,
            method=HTTPMethod.GET,
            credentials=entity.session,
            data=None,
            url_parameters=parameters
        )

        return cls._decode(entity, request.response_data)

    @classmethod
    def _decode(cls: Type[T], entity: Entity, data: Any) -> T:

        if not isinstance(data, list):
            raise UnexpectedResponseType(data, list)

        if len(data) < 1:
            raise ApiError('Response unexpectedly empty')

        tx_list_data = data[0]

        try:

            if tx_list_data['versions'] is None:
                tx_list_data['versions'] = list()

            tx_list = cls(
                entity=entity,
                transaction_id=tx_list_data['transaction_id'],
                versions=Transaction.decode_many(
                    entity,
                    tx_list_data['versions']
                )
            )

        except KeyError as error:
            raise MissingKey(error.args[0])

        return tx_list
