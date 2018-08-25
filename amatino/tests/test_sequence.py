"""
Amatino API Python Bindings
Test Sequence Module
Author: hugh@amatino.io

Provides a constant manifest of tests to execute
"""
import amatino.tests.alpha as alpha
import amatino.tests.primary as primary
import amatino.tests.ancillary as ancillary

SEQUENCE = [
    ancillary.SessionTest,
    primary.EntityTest
    #alpha.AlphaCreateTest,
    #alpha.AlphaCreateEntityTest,
    #alpha.AlphaCreateAccountTest,
    #alpha.AlphaCreateTransactionsTest
]
