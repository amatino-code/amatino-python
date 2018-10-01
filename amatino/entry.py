"""
Amatino API Python Bindings
Entry Module
Author: hugh@amatino.io
"""
from amatino.side import Side
from amatino.account import Account
from amatino.internal.constrained_string import ConstrainedString
from amatino.internal.encodable import Encodable
from amatino.internal.immutable import Immutable
from decimal import Decimal
from typing import Dict
from typing import Any
from typing import TypeVar
from typing import Optional
from typing import Type

T = TypeVar('T', bound='Entry')


class Entry(Encodable):
    """
    Entries compose Transactions. An individual entry allocates some value to
    an Account as either one of the fundamental Sides: a debit or a credit.
    All together, those debits and credits will add up to zero, satisfying the
    fundamental double-entry accounting equality.
    """
    MAX_DESCRIPTION_LENGTH = 1024

    def __init__(
        self,
        side: Side,
        account: Account,
        amount: Decimal,
        description: Optional[str] = None
    ) -> None:

        if not isinstance(side, Side):
            raise TypeError('side must be of type `Side`')

        if not isinstance(account, Account):
            raise TypeError('account must be of type `Account`')

        if not isinstance(amount, Decimal):
            raise TypeError('amount must be of type `Decimal`')

        self._side = side
        self._account = account
        self._amount = amount
        self._description = Entry._Description(description)

        return

    side = Immutable(lambda s: s._side)
    account = Immutable(lambda s: s._account)
    amount = Immutable(lambda s: s._amount)
    description = Immutable(lambda s: s._description)

    def serialise(self) -> Dict[str, Any]:
        data = {
            'account_id': self._account.id_,
            'amount': str(self._amount),
            'description': self._description.serialise(),
            'side': self._side.value
        }
        return data

    class _Description(Encodable):
        def __init__(self, string: Optional[str]) -> None:
            if string is not None and not isinstance(string, str):
                raise TypeError('description must be of type `str` or None')
            if string is None:
                string = ''
            self._description = ConstrainedString(
                string,
                'description',
                Entry.MAX_DESCRIPTION_LENGTH
            )
            return

        def serialise(self) -> str:
            return str(self._description)

    @classmethod
    def decode(cls: Type[T], data: dict) -> T:
        """Decode an Entry from serialised API response data"""
        raise NotImplementedError
