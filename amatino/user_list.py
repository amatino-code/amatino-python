"""
Amatino API Python Bindings
User Module
Author: hugh@amatino.io
"""
from amatino.internal.immutable import Immutable
from amatino.internal.am_time import AmatinoTime
from amatino import User, Session, State
from typing import List, Type, TypeVar, Any, Optional
from amatino.internal.api_request import ApiRequest
from amatino.internal.url_parameters import UrlParameters
from amatino.internal.url_target import UrlTarget
from amatino.internal.http_method import HTTPMethod
from amatino.api_error import ApiError
from amatino.missing_key import MissingKey
from collections.abc import Sequence

T = TypeVar('T', bound='UserList')


class UserList(Sequence):
    """
    A User List is a collection of Users for whom the retrieving User has
    billing responsibility, and who were created using the Amatino API.

    The User List excludes Users managed by the billing dashboard.
    """
    _PATH = '/users/list'

    def __init__(
        self,
        page: int,
        number_of_pages: int,
        generated_time: AmatinoTime,
        state: State,
        users: List[User],
        session: Session
    ) -> None:

        assert isinstance(generated_time, AmatinoTime)
        assert isinstance(number_of_pages, int)
        assert isinstance(page, int)
        assert isinstance(users, list)
        assert False not in [isinstance(u, User) for u in users]
        assert isinstance(state, State)
        assert isinstance(session, Session)

        self._generated_time = generated_time
        self._number_of_pages = number_of_pages
        self._page = page
        self._users = users
        self._state = state
        self._session = session

        return

    generated_time = Immutable(lambda s: s._generated_time.raw)
    number_of_pages = Immutable(lambda s: s._number_of_pages)
    page = Immutable(lambda s: s._page)
    users = Immutable(lambda s: s._users)
    state = Immutable(lambda s: s._state)
    has_more_pages = Immutable(lambda s: s._number_of_pages > self._page)

    def __iter__(self):
        return UserList.Iterator(self._users)

    class Iterator:
        """An iterator for iterating through users in a UserList"""

        def __init__(self, users: List[User]) -> None:
            self._index = 0
            self._users = users
            return

        def __next__(self) -> User:
            if self._index >= len(self._users):
                raise StopIteration
            user = self._users[self._index]
            self._index += 1
            return user

    def __len__(self):
        return len(self.users)

    def __getitem__(self, key):
        return self.users[key]

    def next_page(self: T) -> Optional[T]:
        """
        Return the next page available in this Entity List, or None if no more
        pages are available.
        """
        if not self.has_more_pages:
            return None

        return self.retrieve(
            session=self._session,
            state=self._state,
            page=self._page + 1
        )

    @classmethod
    def retrieve(
        cls: Type[T],
        session: Session,
        state: State = State.ALL,
        page: int = 1
    ) -> T:
        """
        Retrieve a UserList from the perspective of the User tied to the
        supplied Session. Optionally specify a State (active, all, deleted) and
        integer page number.
        """
        if not isinstance(session, Session):
            raise TypeError('session must be of type Session')

        if not isinstance(state, State):
            raise TypeError('state must be of type State')

        if not isinstance(page, int):
            raise TypeError('page must be of type int')

        state_target = UrlTarget('state', state.value)
        page_target = UrlTarget('page', str(page))
        parameters = UrlParameters(targets=[state_target, page_target])

        request = ApiRequest(
            path=cls._PATH,
            method=HTTPMethod.GET,
            credentials=session,
            data=None,
            url_parameters=parameters
        )

        return cls.decode(session, request.response_data)

    @classmethod
    def decode(
        cls: Type[T],
        session: Session,
        data: Any
    ) -> T:

        if not isinstance(data, dict):
            raise ApiError('Unexpected data type returned: ' + str(type(data)))

        try:
            user_list = cls(
                page=data['page'],
                number_of_pages=data['number_of_pages'],
                generated_time=AmatinoTime.decode(data['generated_time']),
                state=State(data['state']),
                users=User.decode_many(session, data['users']),
                session=session
            )
        except KeyError as error:
            raise MissingKey(error.args[0])

        return user_list
