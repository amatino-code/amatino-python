"""
Amatino API Python Bindings
Amatino Alpha creation test module
Author: hugh@amatino.io
"""

from amatino.amatino_alpha import AmatinoAlpha
from amatino.tests.alpha.alpha_test import AlphaTest

class AlphaCreateTest(AlphaTest):
    """
    Assert that it is possible to create an Amatino Alpha instance
    """
    def __init__(self):
        super().__init__('Create an Amatino Alpha instance')

    def execute(self) -> None:
        try:
            _ = self.create_amatino_alpha()
        except Exception as error:
            hint = 'Failed to create AmatinoAlpha instance, error: '
            self.record_failure(hint + str(error))
            return
        self.record_success()
        return
