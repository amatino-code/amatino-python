"""
Amatino API Python Bindings
Test Module
Author: hugh@amatino.io

Base class for tests or, when executed as __main__, the entrypoint for the test
sequence.
"""

class Test:
    """
    Abstract class offering base-level functionality to tests.
    """
    def __init__(self, test_name: str):
        
        if not isinstance(test_name, str):
            raise TypeError('test_name must be of type `str`')

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

    def record_failure(self, note: str = None) -> None:
        """
        Assert that the test has finished and its conditions were not met
        """
        self._record_result(False, note)
        return

    def _record_result(self, result: bool, note: str) -> None:
        """
        Record an assertion of pass or failure
        """
        assert isinstance(result, bool)

        if self._passed is not None:
            raise RuntimeError('Attempt to pass/fail a completed test')
        self._passed = result

        if note is not None and not isinstance(note, str):
            raise TypeError('If passed, note must be of type `str`')

        self._note = note
        
        return

    def report(self) -> str:
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
            report += '\n       ' + self._note

        return report
