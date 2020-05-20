"""
Amatino API Python Bindings
Entity Module
Author: hugh@amatino.io
"""
from amatino import Session
from amatino.region import Region
from amatino.user import User
from amatino.permissions_graph import PermissionsGraph
from amatino.internal.api_request import ApiRequest
from amatino.internal.data_package import DataPackage
from amatino.internal.http_method import HTTPMethod
from amatino.internal.url_parameters import UrlParameters
from amatino.internal.constrained_string import ConstrainedString
from amatino.internal.encodable import Encodable
from amatino.state import State
from typing import TypeVar, Optional, Type, Dict, Any, List
from amatino.internal.immutable import Immutable
from amatino.internal.session_decodable import SessionDecodable
from amatino.internal.disposition import Disposition
from amatino.internal.url_target import UrlTarget

T = TypeVar('T', bound='Entity')


class Entity(SessionDecodable):
    """
    An Amatino entity is a economic unit to be described by accounting
    information. Entities are described by accounts, transactions, and entries.

    An example of an entity might be a legal company, a consolidated group
    of companies, a project, or even a person.
    """
    PATH = '/entities'
    LIST_PATH = '/entities/list'
    MAX_NAME_LENGTH = 1024
    MAX_DESCRIPTION_LENGTH = 4096
    MAX_NAME_SEARCH_LENGTH = 64
    MIN_NAME_SEARCH_LENGTH = 3

    def __init__(
        self,
        session: Session,
        entity_id: str,
        name: str,
        description: str,
        region_id: int,
        owner_id: int,
        permissions_graph: PermissionsGraph,
        disposition: Disposition
    ) -> None:

        self._session = session
        self._entity_id = entity_id
        self._name = name
        self._description = description
        self._region_id = region_id
        self._owner_id = owner_id
        self._permissions_graph = permissions_graph
        self._disposition = disposition

        return

    session = Immutable(lambda s: s._session)
    id_ = Immutable(lambda s: s._entity_id)
    name = Immutable(lambda s: s._name)
    description = Immutable(lambda s: s._description)
    region_id = Immutable(lambda s: s._region_id)
    owner_id = Immutable(lambda s: s._owner_id)
    permissions_graph = Immutable(lambda s: s._permissions_graph)
    disposition = Immutable(lambda s: s._disposition)

    @classmethod
    def create(
        cls: Type[T],
        session: Session,
        name: str,
        description: Optional[str],
        region: Optional[Region] = None
    ) -> T:

        new_entity_arguments = cls.CreateArguments(
            name,
            description,
            region
        )

        request_data = DataPackage.from_object(new_entity_arguments)

        request = ApiRequest(
            Entity.PATH,
            HTTPMethod.POST,
            session,
            request_data,
            None,
            False
        )

        created_entity = cls.decode(request.response_data, session)

        return created_entity

    @classmethod
    def decode(cls: Type[T], data: Any, session: Session) -> T:
        """
        Return an Entity instance decoded from API response data
        """
        if isinstance(data, list):
            data = data[0]

        assert isinstance(session, Session)

        return cls(
            session=session,
            entity_id=data['entity_id'],
            name=data['name'],
            description=data['description'],
            region_id=data['region_id'],
            owner_id=data['owner'],
            permissions_graph=PermissionsGraph(data['permissions_graph']),
            disposition=Disposition.decode(data['disposition'])
        )

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
            credentials=session,
            data=None,
            url_parameters=url_parameters,
            debug=False
        )

        return cls.decode(request.response_data, session)

    @classmethod
    def retrieve_list(
        cls: Type[T],
        session: Session,
        state: State = State.ALL,
        offset: int = 0,
        limit: int = 10,
        name_fragment: Optional[str] = None
    ) -> List[T]:

        if not isinstance(session, Session):
            raise TypeError('session must be of type `amatino.Session`')

        if not isinstance(offset, int):
            raise TypeError('offset must be of type `int`')

        if not isinstance(limit, int):
            raise TypeError('limit must be of type `int`')

        if not isinstance(state, State):
            raise TypeError('state must be of type `amatino.State`')

        if name_fragment is not None:
            if not isinstance(name_fragment, str):
                raise TypeError('name_fragment must be of type `str`')
            if len(name_fragment) < cls.MIN_NAME_SEARCH_LENGTH:
                raise ValueError(
                    'name_fragment minimum length is {c} char'.format(
                        c=str(cls.MIN_NAME_SEARCH_LENGTH)
                    )
                )
            if len(name_fragment) > cls.MAX_NAME_SEARCH_LENGTH:
                raise ValueError(
                    'name_fragment maximum length is {c} char'.format(
                        c=str(cls.MAX_NAME_SEARCH_LENGTH)
                    )
                )

        url_targets = [
            UrlTarget('limit', limit),
            UrlTarget('offset', offset),
            UrlTarget('state', state.value)
        ]

        if name_fragment is not None:
            url_targets.append(UrlTarget('name', name_fragment))

        url_parameters = UrlParameters(targets=url_targets)

        request = ApiRequest(
            path=Entity.LIST_PATH,
            method=HTTPMethod.GET,
            credentials=session,
            data=None,
            url_parameters=url_parameters
        )

        return cls.optionally_decode_many(
            data=request.response_data,
            session=session,
            default_to_empty_list=True
        )

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        owner: Optional[User] = None,
        permissions_graph: Optional[PermissionsGraph] = None
    ) -> 'Entity':
        """
        Modify data describing this Entity. Returns this Entity, the Entity
        instance is not modified in place.
        """

        owner_id = None
        if owner is not None:
            owner_id = owner.id_

        update_arguments = Entity.UpdateArguments(
            self,
            name=name,
            description=description,
            owner_id=owner_id,
            permissions_graph=permissions_graph
        )

        data_package = DataPackage.from_object(data=update_arguments)

        request = ApiRequest(
            path=Entity.PATH,
            method=HTTPMethod.PUT,
            credentials=self._session,
            data=data_package,
            url_parameters=None
        )

        updated_entity = Entity.decode(request.response_data, self.session)

        return updated_entity

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

    class _Description(ConstrainedString):
        def __init__(self, description: str) -> None:
            super().__init__(
                description,
                'description',
                Entity.MAX_DESCRIPTION_LENGTH
            )
            return

    class _Name(ConstrainedString):
        def __init__(self, name: str) -> None:
            super().__init__(
                name,
                'name',
                Entity.MAX_NAME_LENGTH
            )
            return

    class UpdateArguments(Encodable):
        def __init__(
            self,
            entity: T,
            name: Optional[str] = None,
            description: Optional[str] = None,
            owner_id: Optional[int] = None,
            permissions_graph: Optional[PermissionsGraph] = None
        ) -> None:

            if not isinstance(entity, Entity):
                raise TypeError('entity must be of type `Entity`')

            self._entity = entity

            if name:
                self._name = Entity._Name(name).serialise()
            else:
                self._name = entity.name

            if description:
                self._description = Entity._Description.serialise()
            else:
                self._description = entity._description

            if owner_id:
                if not isinstance(owner_id, int):
                    raise TypeError('owner_id must be of type `int`')
                self._owner_id = owner_id
            else:
                self._owner_id = entity.owner_id

            if permissions_graph:
                if not isinstance(permissions_graph, PermissionsGraph):
                    raise TypeError(
                        'graph must be of type `PermissionsGraph`'
                    )
                self._permissions_graph = permissions_graph
            else:
                self._permissions_graph = entity.permissions_graph

            return

        def serialise(self) -> Dict[str, Any]:
            data = {
                'name': self._name,
                'description': self._description,
                'entity_id': self._entity.id_,
                'owner': self._owner_id,
                'permissions_graph': self._permissions_graph.serialise()
            }
            return data

    class CreateArguments(Encodable):
        def __init__(
            self,
            name: str,
            description: Optional[str],
            region: Optional[Region] = None
        ) -> None:

            self._name = ConstrainedString(
                name,
                'name',
                Entity.MAX_NAME_LENGTH
            )

            self._description = ConstrainedString(
                description or '',
                'description',
                Entity.MAX_DESCRIPTION_LENGTH
            )

            if region is not None and not isinstance(region, Region):
                raise TypeError('region must be of type `Region`')

            self._region = region

            return

        def serialise(self) -> Dict[str, Any]:
            region_id = None
            if isinstance(self._region, Region):
                region_id = self._region.id_

            data = {
                'name': self._name.serialise(),
                'description': self._description.serialise(),
                'region_id': region_id
            }

            return data
