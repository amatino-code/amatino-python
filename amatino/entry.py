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
from typing import List

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
        amount: Decimal,
        account: Optional[Account] = None,
        description: Optional[str] = None,
        account_id: Optional[int] = None
    ) -> None:

        if not isinstance(side, Side):
            raise TypeError('side must be of type `Side`')

        if not isinstance(amount, Decimal):
            raise TypeError('amount must be of type `Decimal`')

        self._side = side
        if account_id is not None:
            assert isinstance(account_id, int)
            self._account_id = account_id
        else:
            if not isinstance(account, Account):
                raise TypeError('account must be of type `Account`')
            self._account_id = account.id_
        self._amount = amount
        self._description = Entry._Description(description)

        return

    side = Immutable(lambda s: s._side)
    account_id = Immutable(lambda s: s._account_id)
    amount = Immutable(lambda s: s._amount)
    description = Immutable(lambda s: s._description)

    def serialise(self) -> Dict[str, Any]:
        data = {
            'account_id': self._account_id,
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
    def create(
        cls: Type[T],
        side: Side,
        amount: Decimal,
        account: Account,
        description: Optional[str] = None
    ) -> T:

        return cls(side, amount, account=account, description=description)

    @classmethod
    def create_balanced_pair(
        cls: Type[T],
        debit_account: Account,
        credit_account: Account,
        amount: Decimal,
        description: Optional[str] = None
    ) -> List[T]:

        debit = cls(Side.debit, amount, debit_account, description)
        credit = cls(Side.credit, amount, credit_account, description)

        return [debit, credit]

    @classmethod
    def plug(
        cls: Type[T],
        account: Account,
        entries: List[T],
        description: Optional[str] = None
    ) -> Optional[T]:
        """
        Return an entry plugging the balance gap in a given set of Entries. Or,
        return None if the Entries already balance.
        """

        if False in [isinstance(e, Entry) for e in entries]:
            raise TypeError('Entries must be of type List[Entry]')

        debits = sum([e.amount for e in entries if e.side == Side.debit])
        credits_ = sum([e.amount for e in entries if e.side == Side.credit])

        if debits == credits_:
            return None

        if debits > credits_:
            plug_side = Side.credit
            amount = Decimal(debits - credits_)
        else:
            plug_side = Side.debit
            amount = Decimal(credits_ - debits)

        return cls(plug_side, amount, account, description)
