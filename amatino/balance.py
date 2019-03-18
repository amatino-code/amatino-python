"""
Amatino API Python Bindings
Balance Module
Author: hugh@amatino.io
"""
from amatino.internal.immutable import Immutable
from amatino.internal.balance_protocol import BalanceProtocol


class Balance(BalanceProtocol):
    """
    A Balance represents the sum total value of all Entries party to an Account.
    """

    PATH = '/accounts/balance'
