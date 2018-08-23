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
from amatino.internal.new_transaction_arguments import NewTransactionArguments
from typing import TypeVar
from typing import Optional
from typing import Type
from typing import Any
from typing import List
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
    PATH = '/transactions'

    def __init__(
        self,
        session: Session,
        entity: Entity,
        transaction_id: int,
        transaction_time: datetime,
        description: str,
        entries: List[Entry],
        global_unit_id: Optional[GlobalUnit] = None,
        custom_unit_id: Optional[CustomUnit] = None
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

    session: Session = Immutable(lambda s: s._session)
    entity: Entity = Immutable(lambda s: s._entity)
    id_: int = Immutable(lambda s: s._id)
    time: datetime = Immutable(lambda s: s._time)
    description: str = Immutable(lambda s: s._description)
    entries: List[Entry] = Immutable(lambda s: s._entries)
    global_unit_id: Optional[int] = Immutable(lambda s: s._global_unit_id)
    custom_unit_id: Optional[int] = Immutable(lambda s: s._custom_unit_id)

    @classmethod
    def create_with_global_unit(cls: Type[T]) -> T:
        raise NotImplementedError

    @classmethod
    def create_with_custom_unit(cls: Type[T]) -> T:
        raise NotImplementedError

    def _create(self) -> None:
        raise NotImplementedError

    def _retrieve(self) -> None:
        raise NotImplementedError

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
        """
        Return a list versions of this Transaction
        """
        raise NotImplementedError
