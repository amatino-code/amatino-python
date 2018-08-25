"""
Amatino API Python Bindings
Session Test Module
Author: hugh@amatino.io
"""
from amatino.tests.test import Test
from amatino.session import Session
from typing import Optional
from typing import Any
from amatino.amatino_error import AmatinoError


class SessionTest(Test):
    """
    Test the Session ancillary object
    """
    TEST_ALL_SESSION_METHODS = True

    def __init__(self, name='Create a session') -> None:

        super().__init__(name)

        self.session: Optional[Session] = None

        return

    def create_session(self) -> Optional[Any]:
        try:
            session = Session.create_with_email(
                self.email,
                self.secret
            )
        except Exception as error:
            return error

        did_fail_to_set = False
        try:
            session.api_key = 0
        except AmatinoError:
            did_fail_to_set = True
            pass

        if did_fail_to_set is not True:
            return 'Property set did not raise exception'

        self.session = session

        if self.TEST_ALL_SESSION_METHODS is False:
            return None

        try:
            session = Session.create_with_user_id(
                self.user_id,
                self.secret
            )
        except Exception as error:
            return error

        return None

    def execute(self) -> None:

        result = self.create_session()

        if result is not None:
            self.record_failure(result)
            return

        self.record_success()
        return
