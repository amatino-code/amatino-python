"""
Amatino API Python Bindings
User Module
Author: hugh@amatino.io
"""
from amatino.internal.immutable import Immutable
from amatino.session import Session
from amatino.internal.url_parameters import UrlParameters
from amatino.internal.url_target import UrlTarget
from amatino.internal.api_request import ApiRequest
from amatino.internal.http_method import HTTPMethod
from amatino.unexpected_response_type import UnexpectedResponseType
from typing import TypeVar
from typing import Type
from typing import Optional
from typing import List
from typing import Any

T = TypeVar('T', bound='User')


class User:
    """
    A User is a human producer and consumer of data stored by Amatino. When you
    create an Amatino account on the Amatino website, a User is generated in
    your name. You can create other Users at will to serve the needs of your
    application. For example, you might wish to create an Amatino User to
    associate with each end-user of your application, in order to link financial
    information stored in Amatino with that end-user.

    Users created via the Amatino API cannot login or otherwise interact with
    the amatino.io website in any way. They are not eligbile to receive customer
    support from us directly (though you are most welcome to request customer
    support to assist you with users you create), and don't generate associated
    discussion forum accounts. You have absolute control over their lifecycle.
    They can make requests to the Amatino API on their own behalf.

    Generally, if you are creating User accounts for your fellow developers,
    you will want to do so in your billing dashboard. Doing so will allow them
    to manage their password, post to the discussion forums, and contact us for
    support. If you are creating Users to manage financial data inside your
    application, you will want to do so via the Amatino API.

    Users and Entities are woven together using permission graphs. Any User may
    be granted read and or write access to any Account in any Entity, whether
    they were created in the billing dashboard or via the Amatino API.

    If you are on a Fixed Price plan, each additional user you create in the
    Amatino API will count towards your monthly bill. If you are on a Pay Per
    Use plan, creating additional Users incurs no direct marginal cost. You can
    change your plan at any time.
    """
    _URL_KEY = 'user_id'
    _PATH = '/users'

    def __init__(
        self,
        session: Session,
        id_: int,
        email: str,
        name: str,
        handle: str,
        avatar_url: str
    ) -> None:

        self._id = id_
        self._email = email
        self._name = name
        self._handle = handle
        self._avatar_url = avatar_url

        return

    id_ = Immutable(lambda s: s._id)
    email = Immutable(lambda s: s._email)
    name = Immutable(lambda s: s._name)
    handle = Immutable(lambda s: s._handle)
    avatar_url = Immutable(lambda s: s._avatar_url)

    @classmethod
    def retrieve_authenticated_user(cls: Type[T], session: Session) -> T:
        """Return the User authenticated by the supplied Session"""
        raise NotImplementedError  # Pending bug fix in User retrieval

    @classmethod
    def retrieve(cls: Type[T], session: Session, id_: int) -> T:
        """Return the User with supplied ID"""
        if not isinstance(id_, int):
            raise TypeError('id_ must be of type `int`')
        return cls.retrieve_many(session, [id_])[0]

    @classmethod
    def retrieve_many(
        cls: Type[T],
        session: Session,
        ids: List[int]
    ) -> List[T]:
        """Return a list of Users"""
        if not isinstance(ids, list) or False in [
            isinstance(i, int) for i in ids
        ]:
            raise TypeError('ids must be of type List[int]')
        return cls._retrieve_many(session, ids)

    @classmethod
    def _retrieve_many(
        cls: Type[T],
        session: Session,
        ids: Optional[List[int]] = None
    ) -> List[T]:
        """Return a list of users"""

        parameters = None
        if ids is not None:
            targets = UrlTarget.from_many_integers(cls._URL_KEY, ids)
            parameters = UrlParameters.from_targets(targets)

        request = ApiRequest(
            path=cls._PATH,
            data=None,
            credentials=session,
            method=HTTPMethod.GET,
            url_parameters=parameters
        )

        users = cls._decode_many(session, request.response_data)

        return users

    @classmethod
    def _decode_many(cls: Type[T], session: Session, data: Any) -> List[T]:
        """Return a list of Users decoded from API response data"""

        if not isinstance(data, list):
            raise UnexpectedResponseType(data, list)

        def decode(obj: Any) -> T:
            if not isinstance(obj, dict):
                raise UnexpectedResponseType(obj, dict)

            user = cls(
                session=session,
                id_=obj['user_id'],
                email=obj['email'],
                name=obj['name'],
                handle=obj['handle'],
                avatar_url=obj['avatar_url']
            )

            return user

        return [decode(u) for u in data]
