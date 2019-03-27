"""
Amatino API Python Bindings
Performance class Test Module
Author: hugh@blinkybeach.com
"""
from amatino.tests.primary.account import AccountTest
from amatino import Account
from amatino import Transaction
from amatino import Performance
from amatino import AMType
from amatino import Side
from amatino import Entry
from amatino import GlobalUnit
from amatino import TreeNode
from amatino import Entity
from datetime import datetime
from datetime import timedelta
from decimal import Decimal

NAME = 'Retrieve a Performance'


class PerformanceTest(AccountTest):
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

            Transaction.create(
                self.entity,
                datetime.utcnow(),
                [
                    Entry(Side.credit, Decimal('400'), income),
                    Entry(Side.debit, Decimal('400'), expense)
                ],
                self.usd,
                'Test transaction 1'
            )

            Transaction.create(
                self.entity,
                datetime.utcnow(),
                [
                    Entry(Side.credit, Decimal('250'), income_child),
                    Entry(Side.credit, Decimal('250'), income),
                    Entry(Side.debit, Decimal('500'), expense)
                ],
                self.usd,
                'Test transaction 2'
            )

            Transaction.create(
                self.entity,
                datetime.utcnow() - timedelta(days=4),
                [
                    Entry(Side.credit, Decimal('1'), income),
                    Entry(Side.debit, Decimal('1'), expense)
                ],
                self.usd,
                'Test transaction 3'
            )

            Transaction.create(
                self.entity,
                datetime.utcnow() + timedelta(days=4),
                [
                    Entry(Side.debit, Decimal('50'), income),
                    Entry(Side.credit, Decimal('50'), expense)
                ],
                self.usd,
                'Test transaction 4'
            )

            performance = Performance.retrieve(
                entity=self.entity,
                start_time=datetime.utcnow() - timedelta(days=2),
                end_time=datetime.utcnow() + timedelta(days=2),
                denomination=self.usd
            )

            assert isinstance(performance, Performance)
            assert performance.has_income
            assert performance.has_expenses
            assert performance.global_unit_id == self.usd.id_
            assert performance.custom_unit_id is None
            assert isinstance(performance.denomination, GlobalUnit)
            assert isinstance(performance.start_time, datetime)
            assert isinstance(performance.end_time, datetime)
            assert isinstance(performance.generated_time, datetime)
            assert isinstance(performance.entity, Entity)

            income_root = performance.income[0]
            expense_root = performance.expenses[0]

            assert isinstance(income_root, TreeNode)
            assert isinstance(expense_root, TreeNode)
            assert income_root.has_children
            assert not expense_root.has_children
            assert isinstance(income_root.children[0], TreeNode)

            assert income_root.recursive_balance == Decimal('900')
            assert income_root.account_balance == Decimal('650')
            assert income_root.children[0].account_balance == Decimal('250')
            assert expense_root.account_balance == Decimal('900')
            assert expense_root.recursive_balance == Decimal('900')

            assert performance.total_income == Decimal('900')
            assert performance.total_expenses == Decimal('900')

        except Exception as error:
            self.record_failure(error)
            return

        self.record_success()
