"""
Amatino API Python Bindings
Test Sequence Module
Author: hugh@amatino.io

Provides a constant manifest of tests to execute
"""
import amatino.tests.primary as primary
import amatino.tests.ancillary as ancillary
import amatino.tests.derived as derived
from amatino.tests.ancillary.custom_unit import CustomUnitTest
from amatino.tests.ancillary.tx_version_list import TxVersionListTest

SEQUENCE = [
    ancillary.SessionTest,
    ancillary.GlobalUnitTest,
    CustomUnitTest,
    ancillary.UserTest,
    primary.EntityTest,
    primary.AccountTest,
    primary.TransactionTest,
    derived.LedgerTest,
    derived.RecursiveLedgerTest,
    derived.BalanceTest,
    derived.RecursiveBalanceTest,
    derived.PositionTest,
    derived.PerformanceTest,
    derived.TreeTest,
    ancillary.UserListTest,
    TxVersionListTest
]
