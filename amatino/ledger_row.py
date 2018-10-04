"""
Amatino API Python Bindings
Ledger Row Module
Author: hugh@amatino.io
"""
from amatino.session import Session
from amatino.entity import Entity
from amatino.account import Account
from amatino.internal.am_time import AmatinoTime
from amatino.transaction import Transaction
from amatino.internal.immutable import Immutable
from decimal import Decimal
from typing import Optional


class LedgerRow:
    """
    A Ledger Row is a specialised view of a Transaction, delivered as part of a
    Ledger or Recursive Ledger. The Ledger Row describes a Tranasction from the
    perspective of the Account targeted by the controlling Ledger or Recursive
    Ledger.

    When consuming the Amatino API, you will never encounter a Ledger Row on its
    own. They are only ever delivered under the ledger_rows key as part of a
    Ledger or Recursive Ledger object.
    """

    def __init__(
        self,
        transaction_id: int,
        transaction_time: AmatinoTime,
        description: str,
        opposing_account_id: Optional[int],
        opposing_account_name: str,
        debit: Decimal,
        credit: Decimal,
        balance: Decimal
    ) -> None:

        self._transaction_id = transaction_id
        self._transaction_time = transaction_time
        self._description = description
        self._opposing_account_id = opposing_account_id
        self._opposing_account_name = opposing_account_name
        self._debit = debit
        self._credit = credit
        self._balance = balance

        return

    transaction_id = Immutable(lambda s: s._transaction_id)
    transaction_time = Immutable(lambda s: s._transaction_time.raw)
    description = Immutable(lambda s: s._description)
    opposing_account_id = Immutable(lambda s: s._opposing_account_id)
    opposing_account_name = Immutable(lambda s: s._opposing_account_name)
    debit = Immutable(lambda s: s._debit)
    credit = Immutable(lambda s: s._credit)
    balance = Immutable(lambda s: s._balance)

    def opposing_account(
        self,
        session: Session,
        entity: Entity
    ) -> Optional[Account]:
        """Return the account opposing this transaction, or, if many, None"""
        if self.opposing_account_id is None:
            return None
        return Account.retrieve(session, entity, self.opposing_account_id)

    def retrieve_transaction(
        self,
        session: Session,
        entity: Entity
    ) -> Transaction:
        """Retrieve the Transaction this LedgerRow describes"""
        return Transaction.retrieve(session, entity, self.transaction_id)
