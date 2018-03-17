"""
Amatino API Python Bindings
Entity Module
Author: hugh@amatino.io
"""
from amatino.session import Session
from amatino.region import Region
from amatino._internal._new_entity_arguments import _NewEntityArguments

class Entity:
    """
    An Amatino entity is a economic unit to be described by accounting
    information. Entities are described by accounts, transactions, and entries.

    An example of an entity might be a legal company, a consolidated group
    of companies, a project, or even a person.

    You may initialise an Entity object in one of two ways:

    1.  Retrieve an existing entity, by supplying a string entity identifier
        to the entity_id parameter.

    2.  Create a new entity, by supplying all parameters.

    """
    def __init__(
            self,
            session: Session,
            entity_id: str,
            name: str = None,
            description: str = None,
            region: Region = None
        ):

        self._session = session
        self._new_entity_arguments = None

        if (
                name is not None
                or description is not None
                or region is not None
        ):
            self._new_entity_arguments = _NewEntityArguments(
                entity_id,
                name,
                description,
                region
            )

            self._create()

            return

        self._entity_id = entity_id
        self._retrieve()

        return

    def _create(self) -> None:
        raise NotImplementedError

    def _retrieve(self) -> None:
        raise NotImplementedError

    def update(self) -> None:
        """
        Modify data describing this Entity. Returns None, the Entity
        Object is updated-in-place.
        """
        raise NotImplementedError

    def delete(self) -> None:
        """
        Destroy this Entity. Deleted entities can be recovered if necessary.
        Returns None, the Entity is updated-in-place.
        """
        raise NotImplementedError

    def restore(self) -> None:
        """
        Restore this Entity from a deleted state. Returns None, the Entity
        is updated-in-place.
        """
        raise NotImplementedError
