"""
Amatino API Python Bindings
Recursive Balance Module
Author: hugh@blinkybeach.com
"""
from amatino.internal.immutable import Immutable
from amatino.internal.balance_protocol import BalanceProtocol


class RecursiveBalance(BalanceProtocol):
    """
    A Recursive Balance represents the sum total value of all Entries party to
    an Account, and all of that Account's children.
    """

    PATH = '/accounts/balance/recursive'
