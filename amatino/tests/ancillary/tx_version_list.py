"""
Amatino API Python Bindings
Transaction Version List Test Module
Author: hugh@blinkybeach.com
"""
from amatino.tests.primary.account import AccountTest
from amatino import TransactionVersionList
from amatino import Account
from amatino import Transaction
from amatino import AMType
from amatino import Side
from amatino import Entry
from datetime import datetime
from datetime import timedelta
from decimal import Decimal

NAME = 'Retrieve a TransactionVersionList'


class TxVersionListTest(AccountTest):
    """Test the Performance object"""

    def __init__(self, name=NAME) -> None:
        super().__init__(name)
        return

    def execute(self) -> None:

        try:

            income = self.create_account(
                amt=AMType.income,
                name='Test Income'
            )

            income_child = Account.create(
                self.entity,
                'Test income child',
                income.am_type,
                income.denomination,
                parent=income
            )

            expense = self.create_account(
                amt=AMType.expense,
                name='Test Expense'
            )

            transaction = Transaction.create(
                self.entity,
                datetime.utcnow(),
                [
                    Entry(Side.credit, Decimal('400'), income),
                    Entry(Side.debit, Decimal('400'), expense)
                ],
                self.usd,
                'Test transaction 1'
            )

            transaction.update(
                time=datetime.utcnow(),
                entries=[
                    Entry(Side.credit, Decimal('250'), income_child),
                    Entry(Side.credit, Decimal('250'), income),
                    Entry(Side.debit, Decimal('500'), expense)
                ],
                denomination=self.usd,
                description='Test transaction v2'
            )

            transaction.update(
                time=datetime.utcnow() - timedelta(days=4),
                entries=[
                    Entry(Side.credit, Decimal('1'), income),
                    Entry(Side.debit, Decimal('1'), expense)
                ],
                denomination=self.usd,
                description='Test transaction v3'
            )

            tx_version_list = TransactionVersionList.retrieve(
                entity=self.entity,
                transaction=transaction
            )

            assert len(tx_version_list) == 3, 'list length 3'
            for version in tx_version_list:
                assert isinstance(version, Transaction), 'full of Transactions'

        except Exception as error:
            self.record_failure(error)
            return

        self.record_success()
