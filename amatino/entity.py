"""
Amatino API Python Bindings
Entity Module
Author: hugh@amatino.io
"""
from amatino import Session
from amatino.region import Region
from amatino.internal.new_entity_arguments import NewEntityArguments
from amatino.internal.api_request import ApiRequest
from amatino.internal.data_package import DataPackage
from amatino.internal.http_method import HTTPMethod
from amatino.amatino_error import AmatinoError
from typing import TypeVar
from typing import Optional
from typing import Any

T = TypeVar('T', bound='Entity')


class Entity:
    """
    An Amatino entity is a economic unit to be described by accounting
    information. Entities are described by accounts, transactions, and entries.

    An example of an entity might be a legal company, a consolidated group
    of companies, a project, or even a person.
    """
    PATH = '/entities'
    MAX_NAME_LENGTH = NewEntityArguments.MAX_NAME_LENGTH
    MAX_DESCRIPTION_LENGTH = NewEntityArguments.MAX_DESCRIPTION_LENGTH

    def __init__(
        self,
        session: Session,
        entity_id: str,
        name: str,
        description: str,
        region_id: int,
        owner_id: int,
        active: bool,
        permissions_graph: {str: {str: {str: bool}}}
    ) -> None:

        self._session = session
        self._entity_id = entity_id
        self._name = name
        self._description = description
        self._region_id = region_id
        self._owner_id = owner_id
        self._active = active
        self._permissions_graph = permissions_graph

        raise NotImplementedError

    @classmethod
    def create(
        cls: type,
        session: Session,
        name: str,
        description: str,
        region: Optional[Region] = None
    ) -> T:

        new_entity_arguments = NewEntityArguments(
            name,
            description,
            region
        )

        request_data = DataPackage.from_object(new_entity_arguments)

        request = ApiRequest(
            Entity.PATH,
            HTTPMethod.POST,
            session._credentials(),
            request_data,
            None,
            False
        )

        created_entity = Entity._decode(request.response_data, session)

        return created_entity

    @classmethod
    def _decode(cls: type, data: list, session: Session) -> T:
        """
        Return an Entity instance decoded from API response data
        """
        assert isinstance(session, Session)

        if not isinstance(data, list):
            raise AmatinoError('Unexpected response format: ' + str(type(data)))

        if len(data) < 1:
            raise AmatinoError('Response list unexpectedly empty')

        raw_entity = data[0]

        if not isinstance(raw_entity, dict):
            raise AmatinoError('Unexpected response format')
        try:
            entity = Entity(
                session=session,
                entity_id=raw_entity['session_id'],
                name=raw_entity['name'],
                description=raw_entity['description'],
                region_id=raw_entity['storage_region'],
                owner_id=raw_entity['owner'],
                active=raw_entity['active'],
                permissions_graph=raw_entity['permissions_graph']
            )

        except KeyError:
            raise AmatinoError('Unexpected response format, missing a key')
        return entity

    @classmethod
    def retrieve(
        cls,
        session: Session,
        entity_id: str
    ) -> T:

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
