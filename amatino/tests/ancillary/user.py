"""
Amatino API Python Bindings
User Test Module
Author: hugh@amatino.io
"""
from amatino import User, ResourceNotFound
from amatino.tests.ancillary.session import SessionTest


class UserTest(SessionTest):
    """Test the User ancillary object"""

    def __init__(self, name='Create, retrieve, delete Users') -> None:

        super().__init__(name)
        self.create_session()
        return

    def execute(self) -> None:

        try:
            user = User.retrieve(self.session, self.user_id)
            assert isinstance(user, User), 'retrieved is User'

            new_user = User.create(
                session=self.session,
                secret='what a great passphrase',
                handle='Dick Cheney'
            )
            assert isinstance(new_user, User), 'new user is User'

            new_user.delete()

            was_deleted = False
            try:
                User.retrieve(self.session, new_user.id_)
            except ResourceNotFound:
                was_deleted = True

        except Exception as error:
            self.record_failure(error)
            return

        if was_deleted is False:
            self.record_failure('New user not deleted')

        self.record_success()
        return
