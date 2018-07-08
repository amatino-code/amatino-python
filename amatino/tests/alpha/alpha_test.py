"""
Amatino API Python Bindings
AlphaTest Module
Author: hugh@amatino.io
"""

from amatino.tests.test import Test
from amatino.amatino_alpha import AmatinoAlpha
import os

class AlphaTest(Test):
    """
    Abstract class offering functions useful for the testing of the AmatinoAlpha
    object.
    """
    _EMAIL_KEY = 'AMATINO_TEST_EMAIL'
    _SECRET_KEY = 'AMATINO_TEST_SECRET'

    def __init__(self, test_name: str):

        super().__init__(test_name)

        self._email = self._load_email()
        self._secret = self._load_secret()

        return

    def create_amatino_alpha(self) -> AmatinoAlpha:
        """
        Return an AmatinoAlpha instance generated using test credentials
        """
        alpha = AmatinoAlpha(
            email=self._email,
            secret=self._secret
        )
        return alpha

    def create_entity(self, alpha: AmatinoAlpha) -> {str: object}:
        """
        Return a dictionary representation of an Entity created with the
        supplied AmatinoAlpha instance.
        """
        if not isinstance(alpha, AmatinoAlpha):
            raise TypeError('alpha must be of type `AmatinoAlpha`')

        entity = alpha.request(
            path='/entities',
            method='POST',
            query_string=None,
            body=[{
                "name": "My First Entity",
                "description": None,
                "region_id": None,
            }]
        )[0]

        return entity

    def _load_email(self) -> str:
        """
        Return a string Amatino account email address from the environment.
        """
        return self._load_variable(self._EMAIL_KEY)

    def _load_secret(self) -> str:
        """
        Return a string Amatino account secret from the environment
        """
        return self._load_variable(self._SECRET_KEY)

    def _load_variable(self, variable_name: str):
        """
        Return a string containing the value of a specified environment
        variable.
        """
        assert isinstance(variable_name, str)
        return os.environ[variable_name]
