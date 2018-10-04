"""
Amatino API Python Bindings
Session Module
Author: hugh@amatino.io
"""
from amatino.internal.session_create_arguments import NewSessionArguments
from amatino.internal.data_package import DataPackage
from amatino.internal.api_request import ApiRequest
from amatino.api_error import ApiError
from typing import TypeVar
from typing import Type
from typing import Any
from typing import Optional
from amatino.internal.immutable import Immutable
from amatino.internal.http_method import HTTPMethod
from amatino.internal.credentials import Credentials

T = TypeVar('T', bound='Session')


class Session(Credentials):
    """
    Sessions are the keys to the Amatino kingdom. All requests to the Amatino
    API, except those requests to create Sessions themselves, must include two
    HTTP headers: An integer session identifier, and a Hashed Message
    Authentication Code (HMAC) signed with a Session API Key. The Session object
    handles said header construction and HMAC signing for you behind the scenes.

    Creating a new Session is analogous to 'logging in', and deleting a Session
    with the delete() method is analogous to 'logging out'. Your application
    might wish to create multiple Sessions for a User. For example, one per
    device.
    """

    _PATH = '/session'

    def __init__(
        self,
        user_id: int = None,
        session_id: int = None,
        api_key: str = None
    ) -> None:

        self._api_key = api_key
        self._session_id = session_id
        self._user_id = user_id

        return

    api_key = Immutable(lambda s: s._api_key)
    session_id = Immutable(lambda s: s._session_id)
    user_id = Immutable(lambda s: s._user_id)
    id_ = Immutable(lambda s: s.session_id)

    @classmethod
    def create_with_email(cls: Type[T], email: str, secret: str) -> T:
        """
        Create a new session using an email / secret pair.
        """
        if not isinstance(email, str):
            raise TypeError('email must be of type `str`')

        if not isinstance(secret, str):
            raise TypeError('secret must be of type `str')

        return cls._create(None, email, secret)

    @classmethod
    def create_with_user_id(cls: Type[T], user_id: int, secret: str) -> T:
        """
        Create a new session using a user_id / secret pair
        """
        if not isinstance(user_id, int):
            raise TypeError('user_id must be of type `int`')

        if not isinstance(secret, str):
            raise TypeError('secret must be of type `str`')

        return cls._create(user_id, None, secret)

    @classmethod
    def _create(
        cls: Type[T],
        user_id: Optional[int],
        email: Optional[str],
        secret: str
    ) -> T:

        new_arguments = NewSessionArguments(secret, email, user_id)

        request_data = DataPackage(
            object_data=new_arguments,
            override_listing=True
        )

        request = ApiRequest(
            path=cls._PATH,
            method=HTTPMethod.POST,
            data=request_data
        )

        entity = cls._decode(request.response_data)

        return entity

    @classmethod
    def _decode(cls: Type[T], response_data: Any):

        if not isinstance(response_data, dict):
            raise ApiError('Unexpected non-dict type when decoding Session')

        try:
            api_key = response_data['api_key']
            session_id = response_data['session_id']
            user_id = response_data['user_id']
        except KeyError as error:
            message = 'Expected key "{key}" missing from response data'
            message.format(key=error.args[0])
            raise ApiError(message)

        entity = cls(user_id, session_id, api_key)

        return entity

    def delete(self):
        """
        Destroy this Session, such that its id and api_key are no
        longer valid for authenticating Amatino API requests. Analagous
        to 'logging out' the underlying User.
        """
        raise NotImplementedError
