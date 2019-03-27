"""
Amatino API Python Bindings
Recursive Balance Test Module
Author: hugh@amatino.io
"""
from amatino.tests.primary.transaction import TransactionTest
from amatino import RecursiveBalance
from decimal import Decimal
from amatino import Account
from amatino import Transaction
from amatino import Entry
from amatino import Side
from datetime import datetime

NAME = 'Retrieve a Recursive Balance'


class RecursiveBalanceTest(TransactionTest):
    """Test the Recursive Balance object"""

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

            self.create_transaction(amount=Decimal(42))
            self.create_transaction(amount=Decimal(18))

            Transaction.create(
                self.entity,
                datetime.utcnow(),
                [
                    Entry(Side.debit, Decimal(5), asset_child),
                    Entry(Side.credit, Decimal(5), self.liability)
                ],
                asset_child.denomination
            )

        except Exception as error:
            self.record_failure(error)
            return

        try:
            balance = RecursiveBalance.retrieve(self.entity, self.asset)
        except Exception as error:
            self.record_failure(error)
            return

        if balance.magnitude != Decimal(65):
            message = 'Unexpected magnitude: ' + str(balance.magnitude)
            self.record_failure(message)
            return

        self.record_success()
        return
