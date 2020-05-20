"""
Amatino API Python Bindings
Account Test Module
Author: hugh@amatino.io
"""
from datetime import datetime
from amatino import Side, Entry, Transaction
from decimal import Decimal
from amatino.tests.primary.account import AccountTest
from amatino import AMType, ResourceNotFound
from typing import Optional

NAME = 'Create, retrieve, update, delete a Transaction'


class TransactionTest(AccountTest):
    """Test the Transaction object"""

    def __init__(self, name=NAME) -> None:

        super().__init__(name)
        self.asset = self.create_account(AMType.asset, 'Test Asset')
        self.liability = self.create_account(AMType.liability, 'Test Liability')
        return

    def create_transaction(
        self,
        time: Optional[datetime] = None,
        amount: Optional[Decimal] = None
    ) -> Transaction:

        if time is None:
            time = datetime.utcnow()
        if amount is None:
            amount = Decimal(10)

        transaction = Transaction.create(
            self.entity,
            datetime.utcnow(),
            [
                Entry(Side.debit, amount, self.asset),
                Entry(Side.credit, amount, self.liability)
            ],
            self.usd,
            'Test transaction'
        )

        return transaction

    def execute(self) -> None:

        amount = Decimal(10)

        try:
            transaction = self.create_transaction(amount=amount)
        except Exception as error:
            self.record_failure(error)
            return

        assert isinstance(transaction, Transaction)

        try:
            transaction = Transaction.retrieve(
                self.entity,
                transaction.id_,
                self.asset.denomination
            )
            assert isinstance(transaction, Transaction)
            assert isinstance(transaction.time, datetime)
            assert isinstance(transaction.version_time, datetime)
            assert isinstance(transaction.entries, list)
            assert transaction.magnitude == Decimal(10)
            assert len(transaction) > 1
            for entry in transaction:
                assert isinstance(entry, Entry)

        except Exception as error:
            self.record_failure(error)
            return

        updated_description = 'Updated test description goodness'

        try:
            transaction = transaction.update(description=updated_description)
        except Exception as error:
            self.record_failure(error)
            return

        if not transaction.description == updated_description:
            self.record_failure('Transaction description not updated')
            return

        try:
            transaction.delete()
        except Exception as error:
            self.record_failure(error)
            return

        try:
            Transaction.retrieve(
                self.entity,
                transaction.id_,
                self.asset.denomination
            )
        except Exception as error:
            if not isinstance(error, ResourceNotFound):
                self.record_failure(error)
                return

        self.record_success()
        return
