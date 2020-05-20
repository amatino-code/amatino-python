"""
Amatino API Python Bindings
Global Unit Module
Author: hugh@amatino.io
"""
from amatino.session import Session
from amatino.denomination import Denomination
from amatino.internal.url_target import UrlTarget
from amatino.internal.url_parameters import UrlParameters
from amatino.internal.api_request import ApiRequest
from amatino.internal.immutable import Immutable
from amatino.internal.http_method import HTTPMethod
from amatino.api_error import ApiError
from amatino.unexpected_response_type import UnexpectedResponseType
from typing import TypeVar
from typing import Type
from typing import Any
from typing import List

T = TypeVar('T', bound='GlobalUnit')


class GlobalUnit(Denomination):
    """
    Global Units are standardised units of account available across
    all Amatino Entities. For example, many major currencies are available
    as Global Units.

    Global Units cannot be modified by Amatino users.
    """
    _PATH = '/units'
    _URL_KEY = 'global_unit_id'

    def __init__(
        self,
        code: str,
        id_: int,
        name: str,
        priority: int,
        description: str,
        exponent: int
    ) -> None:

        super().__init__(code, id_, name, priority, description, exponent)

        return

    @classmethod
    def retrieve(cls: Type[T], session: Session, id_: int) -> T:
        """Retrieve a Global Unit"""
        if not isinstance(id_, int):
            raise TypeError('id_ must be of type `int`')
        return GlobalUnit.retrieve_many(session, [id_])[0]

    @classmethod
    def retrieve_many(
        cls: Type[T],
        session: Session,
        ids: List[int]
    ) -> List[T]:
        """Retrieve a set of Global Units"""

        if not isinstance(session, Session):
            raise TypeError('session must be of type `Session`')

        if not isinstance(ids, list):
            raise TypeError('ids must be of type `List[int]`')

        if False in [isinstance(i, int) for i in ids]:
            raise TypeError('ids must be of type `List[int]`')

        targets = UrlTarget.from_many_integers(GlobalUnit._URL_KEY, ids)
        parameters = UrlParameters.from_targets(targets)

        request = ApiRequest(
            path=GlobalUnit._PATH,
            url_parameters=parameters,
            credentials=session,
            method=HTTPMethod.GET
        )

        units = GlobalUnit._decode_many(request.response_data)

        return units

    @classmethod
    def _decode_many(cls: Type[T], data: Any) -> List[T]:
        """Return a list of Global Units decoded from raw API response data"""

        if not isinstance(data, list):
            raise ApiError('Unexpected non-list API data response')

        def decode(unit_data: Any) -> T:
            if not isinstance(unit_data, dict):
                raise UnexpectedResponseType(unit_data, dict)

            try:
                unit = cls(
                    code=unit_data['code'],
                    id_=unit_data['global_unit_id'],
                    name=unit_data['name'],
                    priority=unit_data['priority'],
                    description=unit_data['description'],
                    exponent=unit_data['exponent']
                )
            except KeyError as error:
                message = 'Expected key "{key}" missing from response data'
                message.format(key=error.args[0])
                raise ApiError(message)

            return unit

        units = [decode(u) for u in data]

        return units

    def __eq__(self, other):
        if isinstance(other, GlobalUnit) and other.id_ == self.id_:
            return True
        return False


class GlobalUnitConstants:

    EUR = GlobalUnit('EUR', 2, 'Euro', 1, '', 2)
    USD = GlobalUnit('USD', 5, 'US Dollar', 1, '', 2)
    AUD = GlobalUnit('AUD', 11, 'Australian Dollar', 1, '', 2)
    CAD = GlobalUnit('CAD', 35, 'Canadian Dollar', 1, '', 2)
    CNY = GlobalUnit('CNY', 39, 'Yuan Renminbi', 1, '', 4)
    NZD = GlobalUnit('NZD', 44, 'New Zealand Dollar', 1, '', 2)
    GBP = GlobalUnit('GBP', 66, 'Pound Sterling', 1, '', 2)
    JPY = GlobalUnit('JPY', 80, 'Yen', 1, '', 2)
    CHF = GlobalUnit('CHF', 94, 'Swiss Franc', 1, '', 3)
    SEK = GlobalUnit('SEK', 143, 'Swedish Krona', 1, '', 2)

    PRIORITY_1_UNITS = (EUR, USD, AUD, CAD, CNY, NZD, GBP, JPY, CHF, SEK)
