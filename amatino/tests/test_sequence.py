"""
Amatino API Python Bindings
Test Sequence Module
Author: hugh@amatino.io

Provides a constant manifest of tests to execute
"""

import amatino.tests.alpha as alpha

SEQUENCE = [
    alpha.AlphaCreateTest,
    alpha.AlphaCreateEntityTest,
    alpha.AlphaCreateAccountTest,
    alpha.AlphaCreateTransactionsTest
]
