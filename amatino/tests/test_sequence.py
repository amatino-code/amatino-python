"""
Amatino API Python Bindings
Test Sequence Module
Author: hugh@amatino.io

Provides a constant manifest of tests to execute
"""
import amatino.tests.primary as primary
import amatino.tests.ancillary as ancillary
import amatino.tests.derived as derived

SEQUENCE = [
    ancillary.SessionTest,
    primary.EntityTest,
    primary.AccountTest,
    primary.TransactionTest,
    derived.LedgerTest
]
