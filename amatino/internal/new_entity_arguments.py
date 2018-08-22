"""
Amatino API Python Bindings
New Entity Arguments Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly by public classes, and
should not be used directly.
"""
from amatino.region import Region
from amatino.internal.constrained_string import ConstrainedString
from typing import Optional
from typing import Any
from amatino.internal.encodable import Encodable

class NewEntityArguments(Encodable):
    """
    Private - Not intended to be used directly.

    Used by instances of class Entity to validate, store, and process arguments
    for the creation of new Entities.
    """
    MAX_NAME_LENGTH = 1024
    MAX_DESCRIPTION_LENGTH = 1024

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        region: Optional[Region] = None
    ):

        self._name = ConstrainedString(
            name,
            'name',
            self.MAX_NAME_LENGTH
        )

        self._description = ConstrainedString(
            description or '',
            'description',
            self.MAX_DESCRIPTION_LENGTH
        )

        if region is not None and not isinstance(region, Region):
            raise TypeError('region must be of type `Region`')

        self._region = region
        
        return

    def serialise(self) -> Any:
        data = {
            'name': str(self._name),
            'description': str(self._description),
            'region_id': self._region.id
        }
        return data
