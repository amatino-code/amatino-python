"""
Amatino API Python Bindings
Test Module
Author: hugh@amatino.io

Base class for tests or, when executed as __main__, the entrypoint for the test
sequence.
"""
from urllib.error import HTTPError
from typing import Optional
from typing import Any
from os import environ
import traceback


ENVIRONMENT_HELP_MESSAGE = """
Amatino's test suite requires a few environment variables to run. It looks like
you are missing one or more of them. The required variables are:

AMATINO_TEST_USER_ID - Integer user id
AMATINO_TEST_EMAIL - String user email
AMATINO_TEST_SECRET - String user passphrase (take care not to save on disk!)

These three variable must be associated with a valid Amatino user account, with
active billing.

You can add the variables to your environment using the `export` command. For
example:

$ export AMATINO_TEST_EMAIL=some.cool@email.org

Once you've added the required variables, try running the test suite again.
"""


class Test:
    """
    Abstract class offering base-level functionality to tests.
    """
    def __init__(self, test_name: str) -> None:

        if not isinstance(test_name, str):
            raise TypeError('test_name must be of type `str`')

        try:
            raw_user_id = environ['AMATINO_TEST_USER_ID']
            email = environ['AMATINO_TEST_EMAIL']
            secret = environ['AMATINO_TEST_SECRET']
        except KeyError as error:
            print(ENVIRONMENT_HELP_MESSAGE)
            quit()

        if raw_user_id is None:
            raise RuntimeError('AMATINO_TEST_USER_ID env variable required')

        try:
            user_id = int(raw_user_id)
        except Exception as error:
            raise RuntimeError('AMATINO_TEST_USER_ID string must hold integer')

        if email is None:
            raise RuntimeError('AMATINO_TEST_EMAIL env variable required')

        if secret is None:
            raise RuntimeError('AMATINO_TEST_SECRET env variable required')

        self.user_id = user_id
        self.email = email
        self.secret = secret

        self._name = test_name
        self._note = None
        self._passed = None

        return

    def execute(self) -> None:
        """
        Run this test, recording a fail() or pass() for all possible execution
        paths such that pass or fail result is recorded at test conclusion.
        """
        raise NotImplementedError

    def record_success(self, note: str = None) -> None:
        """
        Assert that the test has finished and its conditions were met
        """
        self._record_result(True, note)
        return

    def record_failure(self, note: Optional[Any] = None) -> None:
        """
        Assert that the test has finished and its conditions were not met
        """
        self._record_result(False, note)
        return

    def _record_result(self, result: bool, note: Optional[str]) -> None:
        """
        Record an assertion of pass or failure
        """
        assert isinstance(result, bool)

        if self._passed is not None:
            raise RuntimeError('Attempt to pass/fail a completed test')
        self._passed = result

        if isinstance(note, HTTPError):
            self._note = 'An HTTP error occured: ' + str(note.code)
            try:
                self._note += '. The API returned the following:\n'
                self._note += '       ' + note.read().decode('utf-8')
                self._note += '\n Traceback follows:'
                self._note += '\n ' + traceback.format_exc()
            except Exception:
                pass
            return

        if isinstance(note, Exception):
            self._note = traceback.format_exc()
            return

        self._note = note

        return

    def report(self, index: Optional[int] = None) -> str:
        """
        Return a string describing the outcome of this test.
        """
        if self._passed is None:
            raise RuntimeError('Cannot report on incomplete test')

        report = '[FAIL] '
        if self._passed:
            report = '[PASS] '
        report += self._name

        if self._note is not None:
            report += '\n       ' + str(self._note)

        if index is not None:
            number = str(index)
            while len(number) < 2:
                number = ' ' + number

            report = '[' + number + '] ' + report

        return report
