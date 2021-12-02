"""
Amatino API Python Bindings
Transaction Module
Author: hugh@amatino.io
"""
from datetime import datetime
from amatino.entity import Entity
from amatino.global_unit import GlobalUnit
from amatino.custom_unit import CustomUnit
from amatino.entry import Entry
from amatino.side import Side
from amatino.denomination import Denomination
from amatino.internal.encodable import Encodable
from amatino.internal.constrained_string import ConstrainedString
from amatino.internal.am_time import AmatinoTime
from amatino.internal.api_request import ApiRequest
from amatino.internal.data_package import DataPackage
from amatino.internal.http_method import HTTPMethod
from amatino.internal.url_target import UrlTarget
from amatino.internal.url_parameters import UrlParameters
from amatino.api_error import ApiError
from amatino.missing_key import MissingKey
from amatino.internal.am_amount import AmatinoAmount
from decimal import Decimal
from typing import TypeVar, Optional, Type, Any, List, Dict
from amatino.internal.immutable import Immutable
from collections.abc import Sequence

T = TypeVar('T', bound='Transaction')


class Transaction(Sequence):
    """
    A Transaction is an exchange of value between two or more Accounts. For
    example, the raising of an invoice, the incrurring of a liability, or the
    receipt of a payment. Many Transactions together, each touching the same
    Account, form an Account Ledger, and the cumulative sum of the Transactions
    form an Account Balance.

    Transactions are composed of Entries, each of which includes a debit or
    credit (The fundamental Sides). The sum of all debits and credits in all
    the Entries that compose a Transaction must always equal zero.

    Transactions may be retrieved and created in arbitrary units, either a
    Global Units or Custom Units. Amatino will transparently handle all unit
    conversions. For example, a Transaction could be created in Australian
    Dollars, touch an Account denominated in Pounds Sterling, and be retrieved
    in Bitcoin.
    """
    _PATH = '/transactions'
    MAX_DESCRIPTION_LENGTH = 1024
    _URL_KEY = 'transaction_id'

    def __init__(
        self,
        entity: Entity,
        transaction_id: int,
        transaction_time: AmatinoTime,
        version_time: AmatinoTime,
        description: str,
        entries: List[Entry],
        global_unit_id: Optional[int] = None,
        custom_unit_id: Optional[int] = None
    ) -> None:

        self._entity = entity
        self._id = transaction_id
        self._time = transaction_time
        self._version_time = version_time
        self._description = description
        self._entries = entries
        self._global_unit_id = global_unit_id
        self._custom_unit_id = custom_unit_id

        return

    session = Immutable(lambda s: s._entity.session)
    entity = Immutable(lambda s: s._entity)
    id_ = Immutable(lambda s: s._id)
    time = Immutable(lambda s: s._time.raw)
    version_time = Immutable(lambda s: s._version_time.raw)
    description = Immutable(lambda s: s._description)
    entries = Immutable(lambda s: s._entries)
    global_unit_id = Immutable(lambda s: s._global_unit_id)
    custom_unit_id = Immutable(lambda s: s._custom_unit_id)
    denomination = Immutable(lambda s: s._denomination())
    magnitude = Immutable(
        lambda s: sum([e.amount for e in s._entries if e.side == Side.debit])
    )

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, key):
        return self.entries[key]

    @classmethod
    def create(
        cls: Type[T],
        entity: Entity,
        time: datetime,
        entries: List[Entry],
        denomination: Denomination,
        description: Optional[str] = None,
    ) -> T:

        arguments = Transaction.CreateArguments(
            time,
            entries,
            denomination,
            description
        )

        data = DataPackage.from_object(arguments)
        parameters = UrlParameters(entity_id=entity.id_)

        request = ApiRequest(
            path=Transaction._PATH,
            method=HTTPMethod.POST,
            credentials=entity.session,
            data=data,
            url_parameters=parameters
        )

        transaction = cls._decode(entity, request.response_data)

        return transaction

    @classmethod
    def retrieve(
        cls: Type[T],
        entity: Entity,
        id_: int,
        denomination: Denomination
    ) -> T:
        """Return a retrieved Transaction"""
        return cls.retrieve_many(entity, [id_], denomination)[0]

    @classmethod
    def retrieve_many(
        cls: Type[T],
        entity: Entity,
        ids: List[int],
        denomination: Denomination
    ) -> List[T]:
        """Return many retrieved Transactions"""

        if not isinstance(entity, Entity):
            raise TypeError('entity must be of type `Entity`')

        if not isinstance(ids, list):
            raise TypeError('ids must be of type `list`')

        if False in [isinstance(i, int) for i in ids]:
            raise TypeError('ids must be of type `int`')

        parameters = UrlParameters(entity_id=entity.id_)

        data = DataPackage(list_data=[cls.RetrieveArguments(
            i, denomination, None
        ) for i in ids])

        request = ApiRequest(
            path=Transaction._PATH,
            method=HTTPMethod.GET,
            credentials=entity.session,
            data=data,
            url_parameters=parameters
        )

        transactions = cls.decode_many(
            entity,
            request.response_data
        )

        return transactions

    @classmethod
    def _decode(
        cls: Type[T],
        entity: Entity,
        data: List[dict]
    ) -> T:

        return cls.decode_many(entity, data)[0]

    @classmethod
    def decode_many(
        cls: Type[T],
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
                transaction = cls(
                    entity=entity,
                    transaction_id=data['transaction_id'],
                    transaction_time=AmatinoTime.decode(
                        data['transaction_time']
                    ),
                    version_time=AmatinoTime.decode(data['version_time']),
                    description=data['description'],
                    entries=cls._decode_entries(data['entries']),
                    global_unit_id=data['global_unit_denomination'],
                    custom_unit_id=data['custom_unit_denomination']
                )
            except KeyError as error:
                raise MissingKey(error.args[0])

            return transaction

        transactions = [decode(t) for t in data]

        return transactions

    def update(
        self: T,
        time: Optional[datetime] = None,
        entries: Optional[List[Entry]] = None,
        denomination: Optional[Denomination] = None,
        description: Optional[str] = None
    ) -> T:
        """Replace existing transaction data with supplied data."""

        arguments = Transaction.UpdateArguments(
            self,
            time,
            entries,
            denomination,
            description
        )

        data = DataPackage.from_object(arguments)
        parameters = UrlParameters(entity_id=self.entity.id_)

        request = ApiRequest(
            path=Transaction._PATH,
            method=HTTPMethod.PUT,
            credentials=self.entity.session,
            data=data,
            url_parameters=parameters
        )

        transaction = Transaction._decode(
            self.entity,
            request.response_data
        )

        if transaction.id_ != self.id_:
            raise ApiError('Mismatched response Trasaction ID - Fatal')

        return transaction

    def delete(self) -> None:
        """
        Destroy this Transaction, such that it will no longer be included
        in any view of this Entity's accounting information.
        """

        target = UrlTarget(self._URL_KEY, str(self.id_))
        parameters = UrlParameters(entity_id=self.entity.id_, targets=[target])

        ApiRequest(
            path=self._PATH,
            method=HTTPMethod.DELETE,
            credentials=self.entity.session,
            data=None,
            url_parameters=parameters
        )

        return

    def restore(self) -> None:
        """
        Restore this transaction from a deleted state to an active state.
        """
        raise NotImplementedError

    def list_versions(self) -> List[Any]:
        """Return a list of versions of this Transaction"""
        raise NotImplementedError

    def _denomination(self) -> Denomination:
        """Return the Denomination of this Transaction"""
        if self.global_unit_id is not None:
            return GlobalUnit.retrieve(self.entity.session, self.global_unit_id)
        return CustomUnit.retrieve(
            self.entity,
            self.custom_unit_id
        )

    @classmethod
    def _decode_entries(cls: Type[T], data: Any) -> List[Entry]:
        """Return Entries decoded from API response data"""
        if not isinstance(data, list):
            raise ApiError('Unexpected API response type ' + str(type(data)))

        def decode(obj) -> Entry:
            if not isinstance(obj, dict):
                raise ApiError('Unexpected API object type ' + str(type(obj)))

            try:
                entry = Entry(
                    side=Side(obj['side']),
                    amount=AmatinoAmount.decode(obj['amount']),
                    account_id=obj['account_id'],
                    description=obj['description']
                )
            except KeyError as error:
                raise MissingKey(error.args[0])

            return entry

        return [decode(e) for e in data]

    class RetrieveArguments(Encodable):
        def __init__(
            self,
            transaction_id: int,
            denomination: Denomination,
            version: Optional[int]
        ) -> None:

            if not isinstance(transaction_id, int):
                raise TypeError('transaction_id must be of type `int`')

            if not isinstance(denomination, Denomination):
                raise TypeError('denomination must be of type `Denomination`')

            if version and not isinstance(version, int):
                raise TypeError('version must be of type `Optional[int]`')

            self._transaction_id = transaction_id

            if isinstance(denomination, GlobalUnit):
                self._global_unit_id = denomination.id_
                self._custom_unit_id = None
            else:
                self._global_unit_id = None
                self._custom_unit_id = denomination.id_

            self._version = version

            return

        def serialise(self) -> Dict[str, Any]:
            data = {
                'transaction_id': self._transaction_id,
                'global_unit_denomination': self._global_unit_id,
                'custom_unit_denomination': self._custom_unit_id,
                'version': self._version
            }
            return data

    class CreateArguments(Encodable):
        def __init__(
            self,
            time: datetime,
            entries: List[Entry],
            denomination: Denomination,
            description: Optional[str] = None,
        ) -> None:

            if not isinstance(time, datetime):
                raise TypeError('time must be of type `datetime.datetime`')

            if not isinstance(denomination, Denomination):
                raise TypeError('denomination must be of type `Denomination`')

            self._time = AmatinoTime(time)
            self._denomination = denomination
            self._entries = Transaction._Entries(entries)
            self._description = Transaction._Description(description)

            return

        def serialise(self) -> Dict[str, Any]:
            if isinstance(self._denomination, CustomUnit):
                custom_unit_id = self._denomination.id_
                global_unit_id = None
            else:
                custom_unit_id = None
                global_unit_id = self._denomination.id_

            data = {
                'transaction_time': self._time.serialise(),
                'custom_unit_denomination': custom_unit_id,
                'global_unit_denomination': global_unit_id,
                'description': self._description.serialise(),
                'entries': self._entries.serialise()
            }
            return data

    class UpdateArguments(Encodable):
        def __init__(
            self,
            transaction: T,
            time: Optional[datetime] = None,
            entries: Optional[List[Entry]] = None,
            denomination: Optional[Denomination] = None,
            description: Optional[str] = None
        ) -> None:

            if not isinstance(transaction, Transaction):
                raise TypeError('transaction must be of type `Transaction`')

            self._transaction_id = transaction.id_

            if time:
                if not isinstance(time, datetime):
                    raise TypeError('time must be of type `datetime`')
                self._time = AmatinoTime(time)
            else:
                self._time = AmatinoTime(transaction.time)

            if entries:
                self._entries = Transaction._Entries(entries)
            else:
                self._entries = Transaction._Entries(transaction.entries)

            if denomination:
                if not isinstance(denomination, Denomination):
                    raise TypeError(
                        'demomination must be of type `Denomination`'
                    )
                self._denomination = denomination
            else:
                self._denomination = transaction.denomination

            if description:
                self._description = Transaction._Description(description)
            else:
                self._description = Transaction._Description(
                    transaction.description
                )

            return

        def serialise(self) -> Dict[str, Any]:
            if isinstance(self._denomination, CustomUnit):
                custom_unit_id = self._denomination.id_
                global_unit_id = None
            else:
                custom_unit_id = None
                global_unit_id = self._denomination.id_

            data = {
                'transaction_id': self._transaction_id,
                'transaction_time': self._time.serialise(),
                'custom_unit_denomination': custom_unit_id,
                'global_unit_denomination': global_unit_id,
                'description': self._description.serialise(),
                'entries': self._entries.serialise()
            }
            return data

    class _Description(ConstrainedString):
        def __init__(self, string: Optional[str] = None) -> None:
            if string is None:
                string = ''
            super().__init__(
                string,
                'description',
                Transaction.MAX_DESCRIPTION_LENGTH
            )
            return

    class _Entries(Encodable):
        def __init__(self, entries: List[Entry]) -> None:

            if not isinstance(entries, list):
                raise TypeError('entries must be of type List[Entry]')
            if False in [isinstance(e, Entry) for e in entries]:
                raise TypeError('entries must be of type List[Entry]')

            debits = sum([e.amount for e in entries if e.side == Side.debit])
            credits_ = sum([e.amount for e in entries if e.side == Side.credit])

            if debits != credits_:
                raise ValueError('sum of debits must equal sum of credits')

            self._entries = entries
            return

        entries = Immutable(lambda s: s._entries)
        debits = Immutable(
            lambda s: [e for e in s._entries if e.side == Side.debit]
        )
        credits_ = Immutable(
            lambda s: [e for e in s._entries if e.side == Side.credit]
        )

        def serialise(self) -> List[Dict]:
            return [e.serialise() for e in self._entries]
