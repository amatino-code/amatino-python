"""
Amatino API Python Bindings
AM Type Module
Author: hugh@amatino.io
"""

class AMType:
    """
    Amatino Types are the five fundamental account type: Asset,
    liability, income, expense, and equity. You won't ever
    need to create an AMType object yourself - Instead, simply
    import required constants from this module: ASSET, LIABILITY,
    INCOME, EXPENSE, EQUITY.
    """
    _VALID = [
        'liability',
        'asset',
        'equity',
        'income',
        'expense'
    ]

    def __init__(self, name: str):
        
        if not isinstance(name, str):
            raise TypeError('AMType name must be of type str')

        if not name in self._VALID:
            raise ValueError('Invalid name. Supply asset, liability, equity, income, or expense')

        self._name = name

        return

ASSET = AMType('asset')
LIABILITY = AMType('liability')
EQUITY = AMType('equity')
INCOME = AMType('income')
EXPENSE = AMType('expense')
