"""
Amatino API Python Bindings
AM Type Module
Author: hugh@amatino.io
"""
from enum import Enum


class AMType(Enum):
    """
    Double-entry accounting divides accounts into five fundamental types:
    Assets, liabilities, equities, incomes and expenses. Throughout Amatino,
    these five constants are referred to as Types.

    Because 'Type' is such a loaded word in the programming world, Amatino
    Python name-spaces Types as AMType.

    You will most often encounter Types when creating Accounts. Erstwhile, most
    of the work that Types do occurs behind the scenes, and you won't need to
    interact with them directly.

    Under the hood, Types allow Amatino to maintain the Fundamental Double-Entry
    Equality.
    """
    asset = 1
    liability = 2
    equity = 3
    income = 4
    expense = 5
