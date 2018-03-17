"""
Amatino API Python Bindings
Global Unit Module
Author: hugh@amatino.io
"""
from amatino.session import Session

class GlobalUnit:
    """
    Global Units are standardised units of account available across
    all Amatino Entities. For example, many major currencies are available
    as Global Units.

    Global Units cannot be modified by Amatino users.
    """
    def __init__(self, unit_code: str, session: Session):

        if not isinstance(unit_code, str):
            raise TypeError('unit_code must be of type str')

        self._unit_code = unit_code
        self._session = session

        return

    def _retrieve(self) -> None:
        raise NotImplementedError
