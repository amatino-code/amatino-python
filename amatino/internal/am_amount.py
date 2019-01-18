"""
Amatino API Python Bindings
Amatino Amount Module
Author: hugh@amatino.io
"""

from decimal import Decimal
from typing import TypeVar
from typing import Type

T = TypeVar('T', bound='AmatinoAmount')


class AmatinoAmount(Decimal):
    """
    Internal class bridging string amount representations to the Python
    Decimal class.
    """

    @classmethod
    def decode(cls: Type[T], amount: str) -> T:
        """Return a Decimal number decoded from an API response"""
        assert isinstance(amount, str)

        negate = False
        if amount[0] == "(":
            amount = amount[1:-1]
            negate = True

        value = cls(amount.replace(",", ""))

        if negate is True:
            value = value * -1

        return value
