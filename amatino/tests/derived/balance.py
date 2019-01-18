"""
Amatino API Python Bindings
Balance Test Module
Author: hugh@amatino.io
"""
from amatino.tests.primary.transaction import TransactionTest
from amatino import Balance
from decimal import Decimal

NAME = 'Retrieve a Balance'


class BalanceTest(TransactionTest):
    """Test the Balance object"""

    def __init__(self, name=NAME) -> None:

        super().__init__(name)
        return

    def execute(self) -> None:

        try:
            self.create_transaction(amount=Decimal(42))
            self.create_transaction(amount=Decimal(18))
        except Exception as error:
            self.record_failure(error)
            return

        try:
            balance = Balance.retrieve(self.entity, self.asset)
        except Exception as error:
            self.record_failure(error)
            return

        if balance.magnitude != Decimal(60):
            message = 'Unexpected magnitude: ' + str(balance.magnitude)
            self.record_failure(message)
            return

        self.record_success()
        return
