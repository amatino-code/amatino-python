"""
Amatino API Python Bindings
Transaction Module
Author: hugh@amatino.io
"""
from datetime import datetime
from amatino.global_unit import GlobalUnit
from amatino.custom_unit import CustomUnit
from amatino.entry import Entry
from amatino._internal._new_transaction_arguments import _NewTransactionArguments

class Transaction:
    """
    A Transaction records an exchange of value between or within
    one ore more Accounts. Initialise a Transaction object in one
    of two ways:

    1. An existing transaction, by supplying an integer transaction id. In
       this case, supply only the transaction_id keyword argument. For
       example, Transaction(transaction_id=93243532)

    2. A new transaction, by supplying data describing the transaction. In
       this case, supply all keyword arguments except for transaction_id.

    """
    _INVALID_EXISTING_MESSAGE = """
        Invalid arguments for the initialisation of an existing Transaction
    """

    def __init__(
            self,
            transaction_id: int = None,
            transaction_time: datetime = None,
            description: str = None,
            global_unit: GlobalUnit = None,
            custom_unit: CustomUnit = None,
            entries: [Entry] = None
    ):

        self._new_arguments = None
        self._existing_attributes = None

        if transaction_id is None:
            self._new_arguments = _NewTransactionArguments(
                transaction_time=transaction_time,
                description=description,
                global_unit=global_unit,
                custom_unit=custom_unit,
                entries=entries
            )

        return

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
        in any view of this Entity's accounting information. Deleted
        Transactions can be restored if necessary.
        """
        raise NotImplementedError

    def restore(self) -> None:
        """
        Restore this transaction from a deleted state to an active state.
        """
        raise NotImplementedError

    def list_versions(self) -> [Transaction]:
        """
        Return a list versions of this Transaction
        """
        raise NotImplementedError
