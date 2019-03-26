"""
Amatino API Python Bindings
User List Test Module
Author: hugh@amatino.io
"""
from amatino.tests.test import Test
from amatino import UserList
from amatino import User
from amatino import State


class UserListTest(Test):
    """Test the retrieval of a UserList"""
    _NAME = 'Retrieve a UserList'

    def __init__(self) -> None:
        super().__init__(self._NAME)
        return

    def execute(self) -> None:

        try:
            user_list = UserList.retrieve(
                self.session,
                state=State.ALL
            )
            assert isinstance(user_list, UserList)
            for user in UserList:
                assert isinstance(user, User)
        except Exception as error:
            self.record_failure(error)
            return

        self.record_success()
        return
