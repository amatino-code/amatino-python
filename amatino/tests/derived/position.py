"""
Amatino API Python Bindings
Position Test Module
author: hugh@blinkybeach.com
"""
from amatino.tests.primary.account import AccountTest
from amatino import Account
from amatino import Transaction
from amatino import Position
from amatino import Entity
from amatino import GlobalUnit
from amatino import TreeNode
from amatino import AMType
from amatino import Entry
from amatino import Side
from decimal import Decimal
from datetime import datetime
from datetime import timedelta

NAME = 'Retrieve a Position'


class PositionTest(AccountTest):
    """Test the Position object"""

    def __init__(self, name=NAME) -> None:
        super().__init__(name)
        return

    def execute(self) -> None:

        try:

            asset = self.create_account(
                AMType.asset,
                'Test Asset'
            )

            liability = self.create_account(
                AMType.liability,
                'Test Liability'
            )

            liability_child = Account.create(
                entity=self.entity,
                name='Test liability child',
                am_type=AMType.liability,
                denomination=liability.denomination,
                parent=liability
            )

            Transaction.create(
                self.entity,
                datetime.utcnow(),
                [
                    Entry(Side.debit, Decimal('400'), asset),
                    Entry(Side.credit, Decimal('400'), liability)
                ],
                self.usd,
                'Test transaction 1'
            )

            Transaction.create(
                self.entity,
                datetime.utcnow(),
                [
                    Entry(Side.debit, Decimal('700'), asset),
                    Entry(Side.credit, Decimal('200'), liability),
                    Entry(Side.credit, Decimal('500'), liability_child)
                ],
                self.usd,
                'Test transaction 2'
            )

            Transaction.create(
                self.entity,
                datetime.utcnow() + timedelta(days=4),
                [
                    Entry(Side.debit, Decimal('1'), asset),
                    Entry(Side.credit, Decimal('1'), liability)
                ],
                self.usd,
                'Test transaction 3'
            )

            position = Position.retrieve(
                entity=self.entity,
                balance_time=datetime.utcnow(),
                denomination=self.usd
            )

            assert isinstance(position, Position)
            assert position.has_assets
            assert position.has_liabilities
            assert not position.has_equities
            assert isinstance(position.denomination, GlobalUnit)
            assert isinstance(position.balance_time, datetime)
            assert isinstance(position.generated_time, datetime)
            assert isinstance(position.entity, Entity)

            asset_root = position.assets[0]
            liability_root = position.liabilities[0]

            assert isinstance(asset_root, TreeNode)
            assert isinstance(liability_root, TreeNode)
            assert liability_root.has_children
            assert not asset_root.has_children

            liability_depth_1 = liability_root.children[0]

            assert isinstance(liability_depth_1, TreeNode)
            assert not liability_depth_1.has_children

            assert asset_root.recursive_balance == Decimal('1100')
            assert asset_root.account_balance == Decimal('1100')
            assert liability_root.account_balance == Decimal('600')
            assert liability_root.recursive_balance == Decimal('1100')
            assert liability_depth_1.account_balance == Decimal('500')
            assert liability_depth_1.recursive_balance == Decimal('500')

        except Exception as error:
            self.record_failure(error)
            return

        self.record_success()
