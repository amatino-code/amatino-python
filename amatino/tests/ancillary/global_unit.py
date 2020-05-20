"""
Amatino API Python Bindings
Global Unit Test Module
Author: hugh@amatino.io
"""
from amatino.tests.ancillary.session import SessionTest
from amatino import GlobalUnit, GlobalUnitConstants

USD_UNIT_ID = 5


class GlobalUnitTest(SessionTest):
    """Test the Global Unit object"""

    def __init__(self, name='Retrieve a Global Unit') -> None:

        super().__init__(name)
        self.create_session()

        return

    def execute(self) -> None:

        try:
            usd = GlobalUnit.retrieve(self.session, USD_UNIT_ID)
        except Exception as error:
            self.record_failure(error)
            return

        if not isinstance(usd.code, str):
            self.record_failure('Unexpected code type ' + str(type(usd.code)))
            return

        if not isinstance(usd.name, str):
            self.record_failure('Unexpected name type ' + str(type(usd.name)))
            return

        assert usd == GlobalUnitConstants.USD

        for unit in GlobalUnitConstants.PRIORITY_1_UNITS:
            assert isinstance(unit.code, str)
            assert len(unit.code) == 3

        self.record_success()
        return
