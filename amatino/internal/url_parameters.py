"""
Amatino API Python Bindings
API Request Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""
from amatino.internal.url_target import UrlTarget
from typing import Optional
from typing import List
from typing import Type
from typing import TypeVar

T = TypeVar('T', bound='UrlParameters')


class UrlParameters:
    """
    Private - Not intended to be used directly.

    An instance of url parameters to be included in a request
    to the Amatino Api
    """
    def __init__(
        self,
        entity_id: Optional[str] = None,
        targets: Optional[List[UrlTarget]] = None,
        raw_query_string: Optional[str] = None
    ) -> None:

        if raw_query_string is not None:
            if not isinstance(raw_query_string, str):
                raise TypeError('raw_query_string must be of type str')
            self._parameter_string = raw_query_string
            return

        if entity_id is not None and not isinstance(entity_id, str):
            raise TypeError("Entity must be of type str")

        if (
                targets is not None
                and (
                    not isinstance(targets, list)
                    or False in [isinstance(t, UrlTarget) for t in targets]
                )
        ):
            raise TypeError('Targets must be of type List[UrlTarget]')

        self._parameter_string = ''

        if entity_id is None and targets is None:
            return

        if entity_id is not None:
            self._parameter_string = '?entity_id=' + entity_id

        if targets is None:
            return

        remaining_targets = targets[:]

        if entity_id is None:
            self._parameter_string = '?' + str(targets[0])
            remaining_targets = targets[1:]

        for target in remaining_targets:
            self._parameter_string += '&' + str(target)

        return

    @classmethod
    def from_targets(cls: Type[T], targets: List[UrlTarget]) -> T:
        """Initialise UrlParameters with a set of UrlTargets only"""
        return cls(targets=targets)

    @classmethod
    def from_single_target(cls: Type[T], target: UrlTarget) -> T:
        """Initialise UrlParameters with a single UrlTarget"""
        return cls(targets=[target])

    def __str__(self):
        return self._parameter_string

    def parameter_string(self) -> str:
        """
        Return a string of url parameters suitable for inclusion
        in a request to the Amatino API.
        """
        return self._parameter_string
