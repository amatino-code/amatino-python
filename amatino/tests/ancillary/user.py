"""
Amatino API Python Bindings
User Test Module
Author: hugh@amatino.io
"""
from amatino import User
from amatino.tests.ancillary.session import SessionTest


class UserTest(SessionTest):
    """Test the User ancillary object"""

    def __init__(self, name='Retrieve a User') -> None:

        super().__init__(name)
        self.create_session()
        return

    def execute(self) -> None:

        try:
            user = User.retrieve(self.session, self.user_id)
        except Exception as error:
            self.record_failure(error)
            return

        if not isinstance(user, User):
            return_type = str(type(user))
            self.record_failure('Unexpected return type: ' + return_type)
            return

        if not isinstance(user.id_, int):
            id_type = str(type(user.id_))
            self.record_failure('Unexpected user ID type: ' + id_type)
            return

        self.record_success()
        return
