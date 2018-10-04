"""
Amatino API Python Bindings
Ledger Order Module
Author: hugh@amatino.io
"""
from enum import Enum


class LedgerOrder(Enum):
    OLDEST_FIRST = True
    YOUNGEST_FIRST = False
