"""
Amatino API Python Bindings
Recursive Ledger Test Module
Author: hugh@amatino.io
"""
from datetime import datetime
from amatino.tests.primary.transaction import TransactionTest
from amatino import Account
from amatino import Transaction
from amatino import RecursiveLedger
from amatino import Side
from amatino import Entry
from decimal import Decimal

NAME = 'Retrieve a RecursiveLedger'


class RecursiveLedgerTest(TransactionTest):
    """Test the RecursiveLedger object"""

    def __init__(self, name=NAME) -> None:

        super().__init__(name)
        return

    def execute(self) -> None:

        try:
            asset_child = Account.create(
                self.entity,
                'Test Asset Child',
                self.asset.am_type,
                self.asset.denomination,
                parent=self.asset
            )

            Transaction.create(
                self.entity,
                datetime.utcnow(),
                [
                    Entry(Side.debit, Decimal(5), self.asset),
                    Entry(Side.credit, Decimal(5), self.liability)
                ],
                self.asset.denomination
            )

            Transaction.create(
                self.entity,
                datetime.utcnow(),
                [
                    Entry(Side.debit, Decimal(5), asset_child),
                    Entry(Side.credit, Decimal(5), self.liability)
                ],
                asset_child.denomination
            )

            ledger = RecursiveLedger.retrieve(
                self.entity,
                self.asset
            )
        except Exception as error:
            self.record_failure(error)
            return

        if not isinstance(ledger, RecursiveLedger):
            return_type = str(type(ledger))
            self.record_failure('Unexpected return type: ' + return_type)

        if len(ledger) != 2:
            self.record_failure('Ledger length unexpected: ' + str(len(ledger)))
            return

        if ledger.account_id != self.asset.id_:
            self.record_failure('Account IDs do not match')
            return

        self.record_success()

        return
