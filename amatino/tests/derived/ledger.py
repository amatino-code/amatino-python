"""
Amatino API Python Bindings
Ledger Test Module
Author: hugh@amatino.io
"""
from amatino.tests.primary.transaction import TransactionTest
from amatino import Ledger
from decimal import Decimal
from amatino import LedgerRow

NAME = 'Retrieve a Ledger'


class LedgerTest(TransactionTest):
    """Test the Ledger object"""

    def __init__(self, name=NAME) -> None:

        super().__init__(name)
        return

    def execute(self) -> None:

        try:
            self.create_transaction(amount=Decimal(42))
            self.create_transaction(amount=Decimal(12))
            self.create_transaction(amount=Decimal(1492))
        except Exception as error:
            self.record_failure(error)
            return

        try:
            ledger = Ledger.retrieve(self.entity, self.asset)
        except Exception as error:
            self.record_failure(error)
            return

        for row in ledger:
            if not isinstance(row, LedgerRow):
                self.record_failure('Unexpected non-LedgerRow type')
                return

        if len(ledger) != 3:
            self.record_failure('Unexpected number of ledger rows')
            return

        ledger_row_1 = ledger[0]
        assert isinstance(ledger_row_1, LedgerRow)

        self.record_success()
