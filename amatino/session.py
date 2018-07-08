"""
Amatino API Python Bindings
Session Module
Author: hugh@amatino.io
"""
from amatino._internal._new_session_arguments import _NewSessionArguments
from amatino._internal._data_package import _DataPackage
from amatino._internal._api_request import _ApiRequest
from amatino._internal._session_credentials import _SessionCredentials

class Session:
    """
    Sessions are the keys to the Amatino kingdom. All requests to the
    Amatino API, except those requests to create Sessions themselves, 
    must include two HTTP headers: An integer session identifier, and
    a Hashed Message Authentication Code (HMAC) signed with a Session
    API Key. The Session object handles said header construction
    and HMAC signing for you behind the scenes.

    Creating a new Session is analogous to 'logging in', and deleting a
    Session with the delete() method is analogous to 'logging out'. Your
    application might wish to create multiple Sessions for a User. For
    example, one per device.

    You can initialise a Session in one of three ways.

    1.  Create a new Session, by supplying the email and secret parameters. For
        example, you might require a user to input their email and secret
        passphrase when they first start your application. Note: You must never
        store a user's secret passphrase!

    2.  Load an existing Session, by supplying the session_id and api_key
        parameters. For example, perhaps you have securely stored session data
        on the user's device, and wish to load that session data such that the
        user does not have to log in again every time they restart your
        application.

    2.  Create a new Session, by supplying the user_id and secret parameters.
        For example, you might have created a new User using the Amatino API,
        and been provided with a user_id in response. You can then use that
        user_id to login in lieu of an email address.

    """

    _PATH = '/session'
    _OBJECT_STRUCTURE = (
        ('api_key', str),
        ('session_id', int),
        ('user_id', int)
    )

    def __init__(
        self,
        secret: str = None,
        email: str = None,
        user_id: int = None,
        session_id: int = None,
        api_key: str = None
        ):

        if (
                secret is not None
                and (
                    email is not None
                    or user_id is not None
                )
            ):
            new_arguments = _NewSessionArguments(
                secret=secret,
                email=email,
                user_id=user_id
            )
            request_data = _DataPackage(
                object_data=new_arguments,
                override_listing=True
            )
            request = _ApiRequest(
                path=self._PATH,
                method='POST',
                data=request_data
            )
            # Load request response
            raw_object = request.load(self._OBJECT_STRUCTURE)
            self.api_key = raw_object['api_key']
            self.session_id = raw_object['session_id']
            self.user_id = raw_object['user_id']

            return

        if (
            session_id is not None
            and api_key is not None
            and user_id is not None
            ):

            if not isinstance(session_id, int):
                raise TypeError('session_id must be of type int')
            
            if not isinstance(api_key, str):
                raise TypeError('api_key must be of type str')

            if not isinstance(user_id, int):
                raise TypeError('user_id must be of type int')

            self.api_key = api_key
            self.session_id = session_id
            self.user_id = user_id

            return

        error = """
        Supply either email & secret, or api_key & session_id & user_id
        """
        raise TypeError(error)

    def _create(self):
        raise NotImplementedError

    def delete(self):
        """
        Destroy this Session, such that its id and api_key are no
        longer valid for authenticating Amatino API requests. Analagous
        to 'logging out' the underlying User.
        """
        raise NotImplementedError

    def _credentials(self) -> _SessionCredentials:
        """
        Return _SessionCredentials from the attributes of this Session
        """
        return _SessionCredentials(self.api_key, self.session_id)
        

    def in_serialisable_form(self) -> dict:
        """
        Return a dictionary containing the attributes of this session
        """
        data = {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'api_key': self.api_key
        }
        return data