"""
Amatino API Python Bindings
API Request Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""
from amatino.entity import Entity
from amatino._internal._url_target import _UrlTarget

class _UrlParameters:
    """    
    Private - Not intended to be used directly.

    An instance of url parameters to be included in a request
    to the Amatino Api
    """
    def __init__(
        self,
        entity: Entity = None,
        targets: [_UrlTarget] = None
        ):

        if entity is not None and not isinstance(entity, Entity):
            raise AssertionError("Entity must be of type Entity")

        if (
                targets is not None
                and (
                    not isinstance(targets, list)
                    or False in [isinstance(t, _UrlTarget) for t in targets]
                )
        ):
            raise AssertionError('Targets must be of type [UrlTarget]')

        self._parameter_string = ''

        if entity is None and targets is None:
            return

        if entity is not None:
            self._parameter_string = '?entity_id=' + entity.id
        
        remaining_targets = targets[:]

        if entity is None:
            self._parameter_string = '?' + str(targets[0])
            remaining_targets = targets[1:]
        
        for target in remaining_targets:
            self._parameter_string += '&' + str(target)

        return

    def __str__(self):
        return self._parameter_string


    def parameter_string(self) -> str:
        """
        Return a string of url parameters suitable for inclusion
        in a request to the Amatino API.
        """
        return self._parameter_string
