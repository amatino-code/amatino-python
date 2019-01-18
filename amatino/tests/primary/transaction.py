"""
Amatino API Python Bindings
Account Test Module
Author: hugh@amatino.io
"""
from datetime import datetime
from amatino import Transaction
from amatino import Side
from amatino import Entry
from decimal import Decimal
from amatino.tests.primary.account import AccountTest
from amatino import AMType
from urllib.error import HTTPError
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
            self.session,
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

        try:
            transaction = self.create_transaction()
        except Exception as error:
            self.record_failure(error)
            return

        assert isinstance(transaction, Transaction)

        try:
            transaction = Transaction.retrieve(
                self.session,
                self.entity,
                transaction.id_,
                self.asset.denomination
            )
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
                self.session,
                self.entity,
                transaction.id_,
                self.asset.denomination
            )
        except Exception as error:
            if isinstance(error, HTTPError) and error.code == 404:
                self.record_success()
                return
            self.record_failure(error)

        return
