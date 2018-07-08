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

    def create_accounts(
        self,
        alpha: AmatinoAlpha,
        entity: {str: object}
    ) -> [{str: object}]:
        """
        Return a list of dictionaries representing Accounts created with the
        supplied AmatinoAlpha instance, in the supplied entity.
        """
        assert isinstance(alpha, AmatinoAlpha)
        assert 'entity_id' in entity
        
        accounts = alpha.request(
            path='/accounts',
            method='POST',
            query_string='?entity_id=' + entity['entity_id'],
            body=[{
                "name": "Subscription income",
                "type": 4,
                "parent_account_id": None,
                "global_unit_id": 5,
                "custom_unit_id": None,
                "counterparty_entity_id": None,
                "description": "Sweet loot",
                "colour": None
            }, {
                "name": "Cash",
                "type": 1,
                "parent_account_id": None,
                "global_unit_id": 5,
                "custom_unit_id": None,
                "counterparty_entity_id": None,
                "description": "Stacks of Benjamins",
                "colour": None
            }]
        )
        return accounts

    def create_transactions(
        self,
        alpha: AmatinoAlpha,
        entity: {str: object},
        accounts: [{str: object}]
    ) -> [{str: object}]:
        assert isinstance(alpha, AmatinoAlpha)
        assert 'entity_id' in entity
        assert 'account_id' in accounts[0] and 'account_id' in accounts[1]

        transactions = alpha.request(
            path='/transactions',
            method='POST',
            query_string='?entity_id=' + entity['entity_id'],
            body=[{
                "transaction_time": "2018-07-08_07:08:06.784326",
                "description": "Receipt of some dosh",
                "global_unit_denomination": 11,
                "custom_unit_denomination": None,
                "entries": [{
                    "account_id": accounts[0]["account_id"],
                    "description": '',
                    "side": 1,
                    "amount": "42.01"
                    }, {
                    "account_id": accounts[1]["account_id"],
                    "description": '',
                    "side": 0,
                    "amount": "42.01"
                }]
            }]
        )
        return transactions

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
