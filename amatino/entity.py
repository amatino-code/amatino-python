"""
Amatino API Python Bindings
Entity Module
Author: hugh@amatino.io
"""
from amatino import Session
from amatino.region import Region
from amatino.internal.entity_create_arguments import NewEntityArguments
from amatino.internal.entity_update_arguments import EntityUpdateArguments
from amatino.internal.api_request import ApiRequest
from amatino.internal.data_package import DataPackage
from amatino.internal.http_method import HTTPMethod
from amatino.internal.url_parameters import UrlParameters
from amatino.amatino_error import AmatinoError
from typing import TypeVar
from typing import Optional
from typing import Type
from amatino.internal.immutable import Immutable

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
        permissions_graph: dict
    ) -> None:

        self._session = session
        self._entity_id = entity_id
        self._name = name
        self._description = description
        self._region_id = region_id
        self._owner_id = owner_id
        self._active = active
        self._permissions_graph = permissions_graph

        return

    session: Session = Immutable(lambda s: s._session)
    id_: str = Immutable(lambda s: s._entity_id)
    name: str = Immutable(lambda s: s._name)
    description: str = Immutable(lambda s: s._description)
    region_id: int = Immutable(lambda s: s._region_id)
    owner_id: int = Immutable(lambda s: s.owner_id)
    active: bool = Immutable(lambda s: s._active)
    permissions_graph: dict = Immutable(lambda s: s._permissions_graph)

    @classmethod
    def create(
        cls: Type[T],
        session: Session,
        name: str,
        description: Optional[str],
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

        created_entity = cls._decode(request.response_data, session)

        return created_entity

    @classmethod
    def _decode(cls: Type[T], data: list, session: Session) -> T:
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
            entity = cls(
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
        cls: Type[T],
        session: Session,
        entity_id: str
    ) -> T:
        if not isinstance(session, Session):
            raise TypeError('session must be of type `Session`')

        if not isinstance(entity_id, str):
            raise TypeError('entity_id must be of type `str`')

        url_parameters = UrlParameters(entity_id=entity_id)

        request = ApiRequest(
            path=Entity.PATH,
            method=HTTPMethod.GET,
            session_credentials=session._credentials(),
            data=None,
            url_parameters=url_parameters,
            debug=False
        )

        entity = cls._decode(request.response_data, session)

        return entity

    def _create(self) -> None:
        raise NotImplementedError

    def _retrieve(self) -> None:
        raise NotImplementedError

    def update(
        self,
        name: str,
        description: str,
        owner_id: int,
        permissions_graph: dict
    ) -> None:
        """
        Modify data describing this Entity. Returns this Entity, the Entity
        instance is updated-in-place.
        """

        update_arguments = EntityUpdateArguments(
            entity_id=self._entity_id,
            name=name,
            description=description,
            owner_id=owner_id,
            permissions_graph=permissions_graph
        )

        request = ApiRequest(
            path=Entity.PATH,
            method=HTTPMethod.PUT,
            session_credentials=self._session._credentials(),
            data=update_arguments,
            url_parameters=None
        )

        updated_entity = Entity._decode(request.response_data, self.session)

        assert self._entity_id == updated_entity.id_
        self._name = updated_entity.name
        self._description = updated_entity.description
        self._region_id = updated_entity.region_id
        self._owner_id = updated_entity.region_id
        self._active = updated_entity.active
        self._permissions_graph = updated_entity.permissions_graph

        del updated_entity

        return None

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
