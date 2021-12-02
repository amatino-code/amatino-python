"""
Amatino API Python Bindings
Ledger Module
Author: hugh@amatino.io
"""
from datetime import datetime
from amatino.ledger_order import LedgerOrder
from amatino.internal.am_time import AmatinoTime
from amatino.denomination import Denomination
from amatino.custom_unit import CustomUnit
from amatino.global_unit import GlobalUnit
from amatino.session import Session
from amatino.entity import Entity
from amatino.internal.immutable import Immutable
from amatino.account import Account
from amatino.internal.encodable import Encodable
from amatino.internal.api_request import ApiRequest
from amatino.internal.url_parameters import UrlParameters
from amatino.ledger_row import LedgerRow
from amatino.unexpected_response_type import UnexpectedResponseType
from amatino.missing_key import MissingKey
from amatino.internal.http_method import HTTPMethod
from amatino.internal.data_package import DataPackage
from amatino.internal.am_amount import AmatinoAmount
from typing import Optional
from typing import TypeVar
from typing import Type
from typing import Dict
from typing import Any
from typing import List
from collections.abc import Sequence
from amatino.denominated import Denominated

T = TypeVar('T', bound='Ledger')


class Ledger(Sequence, Denominated):
    """
    A Ledger is a list of Transactions from the perspective of a particular
    Account. Ledgers are ordered by Transaction time, and include a running
    Account Balance for every line.

    You can request Ledgers in arbitrary Global or Custom Units, not just the
    native unit of the target Account. If you request a Ledger in a unit other
    than the target Account native unit, Amatino will compute and return
    unrealised gains and losses.

    Amatino will return a maximum total of 1,000 Ledger Rows per retrieval
    request. If the Ledger you define spans more than 1,000 rows, it will be
    broken into pages you can retrieve seperately.
    """

    _PATH = '/accounts/ledger'

    def __init__(
        self,
        entity: Entity,
        account_id: int,
        start_time: AmatinoTime,
        end_time: AmatinoTime,
        recursive: bool,
        generated_time: AmatinoTime,
        global_unit_id: Optional[int],
        custom_unit_id: Optional[int],
        page: int,
        number_of_pages: int,
        order: LedgerOrder,
        ledger_rows: List[LedgerRow]
    ) -> None:

        self._entity = entity
        self._account_id = account_id
        self._start_time = start_time
        self._end_time = end_time
        self._recursive = recursive
        self._generated_time = generated_time
        self._global_unit_id = global_unit_id
        self._custom_unit_id = custom_unit_id
        self._page = page
        self._number_of_pages = number_of_pages
        self._order = order
        self._rows = ledger_rows

        return

    session = Immutable(lambda s: s._entity.session)
    entity = Immutable(lambda s: s._entity)
    account_id = Immutable(lambda s: s._account_id)
    account = Immutable(
        lambda s: Account.retrieve(s.session, s.entity, s.account_id)
    )
    start_time = Immutable(lambda s: s._start_time.raw)
    end_time = Immutable(lambda s: s._end_time.raw)
    recursive = Immutable(lambda s: s._recursive)
    generated_time = Immutable(lambda s: s._generated_time.raw)
    global_unit_id = Immutable(lambda s: s._global_unit_id)
    custom_unit_id = Immutable(lambda s: s._custom_unit_id)
    page = Immutable(lambda s: s._page)
    number_of_pages = Immutable(lambda s: s._number_of_pages)
    order = Immutable(lambda s: s._order)
    rows = Immutable(lambda s: s._rows)

    @classmethod
    def retrieve(
        cls: Type[T],
        entity: Entity,
        account: Account,
        order: LedgerOrder = LedgerOrder.YOUNGEST_FIRST,
        page: int = 1,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        denomination: Optional[Denomination] = None
    ) -> T:
        """
        Retrieve a Ledger for the supplied account. Optionally specify order,
        page, denomination, start time, and end time.
        """
        if not isinstance(entity, Entity):
            raise TypeError('entity must be of type `Entity`')

        arguments = Ledger.RetrieveArguments(
            account,
            order,
            page,
            start_time,
            end_time,
            denomination
        )
        data = DataPackage(object_data=arguments, override_listing=True)

        parameters = UrlParameters(entity_id=entity.id_)

        request = ApiRequest(
            path=cls._PATH,
            method=HTTPMethod.GET,
            credentials=entity.session,
            data=data,
            url_parameters=parameters
        )

        return cls._decode(entity, request.response_data)

    @classmethod
    def _decode(
        cls: Type[T],
        entity: Entity,
        data: Any
    ) -> T:

        if not isinstance(data, dict):
            raise UnexpectedResponseType(type(data), dict)

        try:
            ledger = cls(
                entity=entity,
                account_id=data['account_id'],
                start_time=AmatinoTime.decode(data['start_time']),
                end_time=AmatinoTime.decode(data['end_time']),
                recursive=data['recursive'],
                generated_time=AmatinoTime.decode(data['generated_time']),
                global_unit_id=data['global_unit_denomination'],
                custom_unit_id=data['custom_unit_denomination'],
                ledger_rows=Ledger._decode_rows(data['ledger_rows']),
                page=data['page'],
                number_of_pages=data['number_of_pages'],
                order=LedgerOrder(data['ordered_oldest_first'])
            )
        except KeyError as error:
            raise MissingKey(error.args[0])

        return ledger

    @classmethod
    def _decode_rows(cls: Type[T], rows: List[Any]) -> List[LedgerRow]:
        """Return LedgerRows decoded from raw API response data"""
        if not isinstance(rows, list):
            raise UnexpectedResponseType(rows, list)

        def decode(data) -> LedgerRow:

            if not isinstance(data, list):
                raise UnexpectedResponseType(data, list)

            row = LedgerRow(
                transaction_id=data[0],
                transaction_time=AmatinoTime.decode(data[1]),
                description=data[2],
                opposing_account_id=data[3],
                opposing_account_name=data[4],
                debit=AmatinoAmount.decode(data[5]),
                credit=AmatinoAmount.decode(data[6]),
                balance=AmatinoAmount.decode(data[7])
            )

            return row

        return [decode(r) for r in rows]

    class RetrieveArguments(Encodable):
        def __init__(
            self,
            account: Account,
            order: LedgerOrder = LedgerOrder.YOUNGEST_FIRST,
            page: int = 1,
            start_time: Optional[datetime] = None,
            end_time: Optional[datetime] = None,
            denomination: Optional[Denomination] = None
        ) -> None:

            if not isinstance(account, Account):
                raise TypeError('account must be of type `Account`')

            if not isinstance(order, LedgerOrder):
                raise TypeError('order must beof type `LedgerOrder`')

            if not isinstance(page, int):
                raise TypeError('page must be of type `int`')

            if start_time and not isinstance(start_time, datetime):
                raise TypeError('start_time must be of type `datetime` or None')

            if end_time and not isinstance(end_time, datetime):
                raise TypeError('end_time must be of type `datetime` or None')

            if denomination and not isinstance(denomination, Denomination):
                raise TypeError(
                    'denomination must be of type `Denomination` or None'
                )

            if denomination is None:
                denomination = account.denomination

            self._account = account
            self._order = order
            self._page = page
            self._start_time = None
            if start_time:
                self._start_time = AmatinoTime(start_time)
            self._end_time = None
            if end_time:
                self._end_time = AmatinoTime(end_time)
            self._denomination = denomination

        def serialise(self) -> Dict[str, Any]:
            global_unit_id = None
            custom_unit_id = None
            if isinstance(self._denomination, GlobalUnit):
                global_unit_id = self._denomination.id_
            else:
                assert isinstance(self._denomination, CustomUnit)
                custom_unit_id = self._denomination.id_

            start_time = None
            if self._start_time:
                start_time = AmatinoTime(self._start_time).serialise()

            end_time = None
            if self._end_time:
                end_time = AmatinoTime(self._end_time).serialise()

            data = {
                'account_id': self._account.id_,
                'start_time': start_time,
                'end_time': end_time,
                'page': self._page,
                'global_unit_denomination': global_unit_id,
                'custom_unit_denomination': custom_unit_id,
                'order_oldest_first': self._order.value
            }

            return data

    def __iter__(self):
        return Ledger.Iterator(self._rows)

    class Iterator:
        """An iterator for iterating through LedgerRows in a Ledger"""

        def __init__(self, rows: List[LedgerRow]) -> None:
            self._index = 0
            self._rows = rows
            return

        def __next__(self) -> LedgerRow:
            if self._index >= len(self._rows):
                raise StopIteration
            row = self._rows[self._index]
            self._index += 1
            return row

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, key):
        return self.rows[key]
