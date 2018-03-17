"""
Amatino API Python Bindings
Entry Module
Author: hugh@amatino.io
"""

class Entry:
    """
    Entries compose Transactions. An individual entry allocates some value to
    an Account as either one of the fundamental Sides: a debit or a credit.
    All together, those debits and credits will add up to zero, satisfying the
    fundamental double-entry accounting equality.
    """

    def __init__(self):
        pass

    def _create(self) -> None:
        raise NotImplementedError

    def _retrieve(self) -> None:
        raise NotImplementedError

    def update(self) -> None:
        raise NotImplementedError

    def restore(self) -> None:
        raise NotImplementedError