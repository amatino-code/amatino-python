"""
Amatino API Python Bindings
Entity Update Arguments
Author: hugh@amatino.io
"""
from amatino.internal.encodable import Encodable
from amatino.internal.entity_create_arguments import NewEntityArguments
from amatino.internal.constrained_string import ConstrainedString
from typing import Optional


class EntityUpdateArguments(Encodable):
    """
    A set of arguments suitable for provision to the Amatino API for the
    purpose of updating an existing Entity
    """
    def __init__(
        self,
        entity_id: str,
        name: str,
        description: str,
        owner_id: int,
        permissions_graph: Optional[dict]
    ) -> None:

        assert isinstance(entity_id, str)

        self._entity_id = entity_id

        self._name = ConstrainedString(
            name,
            'name',
            NewEntityArguments.MAX_NAME_LENGTH
        )

        self._description = ConstrainedString(
            description,
            'description',
            NewEntityArguments.MAX_DESCRIPTION_LENGTH
        )

        if not isinstance(owner_id, int):
            raise TypeError('owner_id must be of type `int`')

        self._owner_id = owner_id

        self._permissions_graph = permissions_graph

        if permissions_graph is None:
            return

        if not isinstance(permissions_graph, dict):
            raise TypeError('permissions_graph must be of type `dict`')

        if False in [isinstance(k, str) for k in permissions_graph]:
            raise TypeError('permissions_graph keys must be of type `str`')

        upg = permissions_graph
        if False in [isinstance(upg[k], dict) for k in upg]:
            raise TypeError('permissions_graph values must be of type `dict`')

        return

    def serialise(self):
        data = {
            'entity_id': self._entity_id,
            'name': str(self._name),
            'description': str(self._description),
            'owner_id': self._owner_id,
            'permissions_graph': self._permissions_graph
        }
        return data
