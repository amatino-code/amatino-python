"""
Amatino API Python Bindings
Recursive Ledger Module
Author: hugh@amatino.io
"""
from amatino.ledger import Ledger


class RecursiveLedger(Ledger):
    """
    A Recursive Ledger is a list of Transactions from the perspective of a
    particular Account, and all the Transactions party to all child Accounts
    of that Account. Recursive Ledgers are ordered by Transaction time, and
    include a running Account Balance for every line.

    If you request a Recursive Ledger in a unit other than the target Account
    native unit, or if child Accounts feature heterogenous units, Amatino will
    compute and return unrealised gains and losses. Find out more in the
    Unrealised Gains and Losses article

    Amatino will return a maximum total of 1,000 Ledger Rows per retrieval
    request. If the Ledger you define spans more than 1,000 rows, it will be
    broken into pages you can retrieve seperately.
    """
    _PATH = '/accounts/ledger/recursive'
