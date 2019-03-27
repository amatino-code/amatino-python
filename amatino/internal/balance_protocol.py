"""
Amatino API Python Bindings
Balance Protocol Module
Author: hugh@blinkybeach.com
"""
from typing import TypeVar
from typing import Type
from typing import List
from typing import Dict
from typing import Any
from typing import Optional
from decimal import Decimal
from datetime import datetime
from amatino.denomination import Denomination
from amatino.entity import Entity
from amatino.account import Account
from amatino.global_unit import GlobalUnit
from amatino.custom_unit import CustomUnit
from amatino.unexpected_response_type import UnexpectedResponseType
from amatino.internal.am_time import AmatinoTime
from amatino.internal.immutable import Immutable
from amatino.internal.encodable import Encodable
from amatino.internal.api_request import ApiRequest
from amatino.internal.http_method import HTTPMethod
from amatino.internal.data_package import DataPackage
from amatino.internal.url_parameters import UrlParameters
from amatino.denominated import Denominated


T = TypeVar('T', bound='BalanceProtocol')
K = TypeVar('K', bound='BalanceProtocol.RetrieveArguments')


class BalanceProtocol(Denominated):
    """
    Abstract class defining a protocol for classes representing balances. In
    practice these are Balance and RecrusiveBalance. This class is intended
    to be private, and internal to the Amatino library. You should not
    use it directly when integrating Amatino Python into your application.
    """

    PATH = NotImplemented

    def __init__(
        self,
        entity: Entity,
        balance_time: AmatinoTime,
        generated_time: AmatinoTime,
        recursive: bool,
        global_unit_id: Optional[int],
        custom_unit_id: Optional[int],
        account_id: int,
        magnitude: Decimal
    ) -> None:

        if self.PATH == NotImplemented:
            raise RuntimeError('Balance classes must implement .PATH property')

        assert isinstance(entity, Entity)
        assert isinstance(balance_time, AmatinoTime)
        assert isinstance(generated_time, AmatinoTime)
        assert isinstance(recursive, bool)
        if global_unit_id is not None:
            assert isinstance(global_unit_id, int)
        if custom_unit_id is not None:
            assert isinstance(custom_unit_id, int)
        assert isinstance(account_id, int)
        assert isinstance(magnitude, Decimal)

        self._entity = entity
        self._balance_time = balance_time
        self._generated_time = generated_time
        self._recursive = recursive
        self._custom_unit_id = custom_unit_id
        self._global_unit_id = global_unit_id
        self._magnitude = magnitude
        self._account_id = account_id

        return

    entity = Immutable(lambda s: s._entity)
    session = Immutable(lambda s: s._entity.session)
    time = Immutable(lambda s: s._balance_time.raw)
    generated_time = Immutable(lambda s: s._generated_time.raw)
    magnitude = Immutable(lambda s: s._magnitude)
    is_recursive = Immutable(lambda s: s._recursive)
    account_id = Immutable(lambda s: s._account_id)
    account = Immutable(
        lambda s: Account.retrieve(s.entity.session, s.entity, s.account_id)
    )
    global_unit_id = Immutable(lambda s: s._global_unit_id)
    custom_unit_id = Immutable(lambda s: s._custom_unit_id)

    @classmethod
    def retrieve_many(
        cls: Type[T],
        entity: Entity,
        arguments: List[K]
    ) -> List[T]:
        """Retrieve several Balances."""
        if not isinstance(entity, Entity):
            raise TypeError('entity must be of type `Entity`')

        if False in [isinstance(a, cls.RetrieveArguments) for a in arguments]:
            raise TypeError(
                'arguments must be of type List[Balance.RetrieveArguments]'
            )

        data = DataPackage(list_data=arguments)
        parameters = UrlParameters(entity_id=entity.id_)

        request = ApiRequest(
            path=cls.PATH,
            method=HTTPMethod.GET,
            credentials=entity.session,
            data=data,
            url_parameters=parameters
        )

        return cls._decode_many(entity, request.response_data)

    @classmethod
    def _decode_many(
        cls: Type[T],
        entity: Entity,
        data: Any
    ) -> List[T]:

        if not isinstance(data, list):
            raise UnexpectedResponseType(data, list)

        for balance in data:
            if not isinstance(balance, dict):
                raise UnexpectedResponseType(balance, dict)

        balances = list()

        for balance in data:
            balances.append(cls(
                entity,
                AmatinoTime.decode(balance['balance_time']),
                AmatinoTime.decode(balance['generated_time']),
                balance['recursive'],
                balance['global_unit_denomination'],
                balance['custom_unit_denomination'],
                balance['account_id'],
                Decimal(balance['balance'])
            ))

        return balances

    @classmethod
    def retrieve(
        cls: Type[T],
        entity: Entity,
        account: Account,
        balance_time: Optional[datetime] = None,
        denomination: Optional[Denomination] = None
    ) -> T:
        """Retrieve a Balance"""
        arguments = cls.RetrieveArguments(
            account,
            balance_time,
            denomination
        )
        return cls.retrieve_many(entity, [arguments])[0]

    class RetrieveArguments(Encodable):
        def __init__(
            self,
            account: Account,
            balance_time: Optional[datetime] = None,
            denomination: Optional[Denomination] = None
        ) -> None:

            if not isinstance(account, Account):
                raise TypeError('account must be of type Account')

            if (
                    balance_time is not None
                    and not isinstance(balance_time, datetime)
            ):
                raise TypeError(
                    'balance_time must be of type `datetime or None'
                )

            if (
                    denomination is not None
                    and not isinstance(denomination, Denomination)
            ):
                raise TypeError(
                    'denomination must conform to `Denomination`'
                )

            if denomination is None:
                denomination = account.denomination

            self._account = account
            self._balance_time = None
            if balance_time:
                self._balance_time = AmatinoTime(balance_time)
            self._denomination = denomination

        def serialise(self) -> Dict[str, Any]:

            global_unit_id = None
            custom_unit_id = None

            if isinstance(self._denomination, GlobalUnit):
                global_unit_id = self._denomination.id_
            else:
                assert isinstance(self._denomination, CustomUnit)
                custom_unit_id = self._denomination.id_

            balance_time = None
            if self._balance_time:
                balance_time = self._balance_time.serialise()

            data = {
                'account_id': self._account.id_,
                'balance_time': balance_time,
                'custom_unit_denomination': custom_unit_id,
                'global_unit_denomination': global_unit_id
            }

            return data
