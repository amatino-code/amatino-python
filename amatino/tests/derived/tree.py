"""
Amatino API Python Bindings
Tree Test Module
Author: hugh@blinkybeach.com
"""
from amatino.tests.primary.account import AccountTest
from amatino import Account
from amatino import Transaction
from amatino import Tree
from amatino import AMType
from amatino import Side
from amatino import Entry
from amatino import GlobalUnit
from amatino import TreeNode
from amatino import Entity
from datetime import datetime
from datetime import timedelta
from decimal import Decimal

NAME = 'Retrieve a Tree'


class TreeTest(AccountTest):
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

            asset = self.create_account(
                AMType.asset,
                'Test Asset'
            )

            Transaction.create(
                self.entity,
                datetime.utcnow(),
                [
                    Entry(Side.credit, Decimal('400'), income),
                    Entry(Side.debit, Decimal('400'), asset)
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
                    Entry(Side.debit, Decimal('500'), asset)
                ],
                self.usd,
                'Test transaction 2'
            )

            Transaction.create(
                self.entity,
                datetime.utcnow(),
                [
                    Entry(Side.credit, Decimal('300'), asset),
                    Entry(Side.debit, Decimal('300'), expense)
                ],
                self.usd,
                'Test transaction 3'
            )

            Transaction.create(
                self.entity,
                datetime.utcnow() + timedelta(days=4),
                [
                    Entry(Side.debit, Decimal('50'), expense),
                    Entry(Side.credit, Decimal('50'), asset)
                ],
                self.usd,
                'Test transaction 4'
            )

            tree = Tree.retrieve(
                entity=self.entity,
                balance_time=datetime.utcnow() + timedelta(hours=1),
                denomination=self.usd
            )

            assert isinstance(tree, Tree)
            assert tree.has_income
            assert tree.has_expenses
            assert not tree.has_liabilities
            assert not tree.has_equity
            assert tree.global_unit_id == self.usd.id_
            assert tree.custom_unit_id is None
            assert isinstance(tree.denomination, GlobalUnit)
            assert isinstance(tree.balance_time, datetime)
            assert isinstance(tree.generated_time, datetime)
            assert isinstance(tree.entity, Entity)

            income_root = tree.income[0]
            expense_root = tree.expenses[0]

            assert isinstance(income_root, TreeNode)
            assert isinstance(expense_root, TreeNode)
            assert income_root.has_children
            assert not expense_root.has_children
            assert isinstance(income_root.children[0], TreeNode)

            assert income_root.recursive_balance == Decimal('900')
            assert income_root.account_balance == Decimal('650')
            assert income_root.children[0].account_balance == Decimal('250')
            assert expense_root.account_balance == Decimal('300')
            assert expense_root.recursive_balance == Decimal('300')

            assert tree.total_income == Decimal('900')
            assert tree.total_expenses == Decimal('300')
            assert tree.total_assets == Decimal('600')
            assert tree.total_equity == Decimal('0')
            assert tree.total_liabilities == Decimal('0')

        except Exception as error:
            self.record_failure(error)
            return

        self.record_success()
