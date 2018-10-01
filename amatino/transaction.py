"""
Amatino API Python Bindings
Transaction Module
Author: hugh@amatino.io
"""
from datetime import datetime
from amatino.session import Session
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
from amatino.api_error import ApiError
from typing import TypeVar
from typing import Optional
from typing import Type
from typing import Any
from typing import List
from typing import Dict
from amatino.internal.immutable import Immutable

T = TypeVar('T', bound='Transaction')


class Transaction:
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

    def __init__(
        self,
        session: Session,
        entity: Entity,
        transaction_id: int,
        transaction_time: AmatinoTime,
        description: str,
        entries: List[Entry],
        global_unit_id: Optional[int] = None,
        custom_unit_id: Optional[int] = None
    ) -> None:

        self._session = session
        self._entity = entity
        self._id = transaction_id
        self._time = transaction_time
        self._description = description
        self._entries = entries
        self._global_unit_id = global_unit_id
        self._custom_unit_id = custom_unit_id

        return

    session = Immutable(lambda s: s._session)
    entity = Immutable(lambda s: s._entity)
    id_ = Immutable(lambda s: s._id)
    time = Immutable(lambda s: s._time.raw)
    description = Immutable(lambda s: s._description)
    entries = Immutable(lambda s: s._entries)
    global_unit_id = Immutable(lambda s: s._global_unit_id)
    custom_unit_id = Immutable(lambda s: s._custom_unit_id)
    global_unit = Immutable(lambda s: GlobalUnit.retrieve(s.global_unit_id))

    @classmethod
    def create(
        cls: Type[T],
        session: Session,
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

        request = ApiRequest(
            path=Transaction._PATH,
            method=HTTPMethod.POST,
            credentials=session,
            data=data
        )

        transaction = cls._decode(session, entity, request.response_data)

        return transaction

    def _create(self) -> None:
        raise NotImplementedError

    def _retrieve(self) -> None:
        raise NotImplementedError

    @classmethod
    def _decode(
        cls: Type[T],
        session: Session,
        entity: Entity,
        data: List[dict]
    ) -> T:

        return cls._decode_many(session, entity, data)[0]

    @classmethod
    def _decode_many(
        cls: Type[T],
        session: Session,
        entity: Entity,
        data: List[dict]
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
                    session=session,
                    entity=entity,
                    transaction_id=data['transaction_id'],
                    transaction_time=AmatinoTime.decode(
                        data['transaction_time']
                    ),
                    description=data['description'],
                    entries=[Entry.decode(e) for e in data['entries']],
                    global_unit_id=data['global_unit_denomination'],
                    custom_unit_id=data['custom_unit_denomination']
                )
            except KeyError as error:
                message = 'Expected key "{key}" missing from response data'
                message.format(key=error.args[0])
                raise ApiError(message)

            return transaction

        transactions = [decode(t) for t in data]

        return transactions

    def update(self) -> None:
        """
        Replace existing transaction data with supplied data.
        """
        raise NotImplementedError

    def delete(self) -> None:
        """
        Destroy this Transaction, such that it will no longer be included
        in any view of this Entity's accounting information.
        """
        raise NotImplementedError

    def restore(self) -> None:
        """
        Restore this transaction from a deleted state to an active state.
        """
        raise NotImplementedError

    def list_versions(self) -> List[Any]:
        """Return a list of versions of this Transaction"""
        raise NotImplementedError

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

            if description is None:
                description = ''

            self._time = AmatinoTime(time)
            self._denomination = denomination
            self._entries = Transaction._Entries(entries)
            self._description = ConstrainedString(
                description,
                'description',
                Transaction.MAX_DESCRIPTION_LENGTH
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
                'transaction_time': self._time.serialise(),
                'custom_unit_denomination': custom_unit_id,
                'global_unit_denomination': global_unit_id,
                'description': self._description.serialise(),
                'entries': self._entries.serialise()
            }
            return data

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
