"""
Amatino API Python Bindings
AM Side Module
Author: hugh@amatino.io
"""
from enum import Enum


class Side(Enum):
    """
    Side is Amatino's name for the fundamental double-entry bookeeping
    building blocks, the debit and credit. They are constant and unchanging, so
    while you can retrieve them with a GET request, you can also safely
    hard-code them into your application.

    When consuming the Amatino API, Sides primarily pop up when dealing with
    Transactions. Transactions are made up of multiple Entries, each of which
    must include a Side.
    """
    debit = 0
    credit = 1
