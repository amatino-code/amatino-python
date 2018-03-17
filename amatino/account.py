"""
Amatino API Python Bindings
Account Module
Author: hugh@amatino.io
"""
from amatino.entity import Entity
from amatino.session import Session
from amatino.am_type import AMType
from amatino.global_unit import GlobalUnit
from amatino.custom_unit import CustomUnit
from amatino.color import Color

class Account:
    """
    An Amatino Account is collection of related economic activity. For example,
    an Account might represent a bank account, income from a particular client,
    or company equity. Many Accounts together compose an Entity.

    You may initialise an Account in one of two ways:

    1.  An existing account, by the account_id, entity, and session parameters.

    2.  A new account, by supplying data describing the account. In this case,
        supply parameters describing the new account, and ommit the account_id
        parameter.

    """

    def __init__(
            self,
            session: Session,
            entity: Entity,
            account_id: int = None,
            name: str = None,
            am_type: AMType = None,
            parent_account: Account = None,
            global_unit: GlobalUnit = None,
            custom_unit: CustomUnit = None,
            counterparty: Entity = None,
            description: str = None,
            color: Color = None
    ):
        raise NotImplementedError
