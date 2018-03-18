"""
Amatino API Python Bindings
Session Module
Author: hugh@amatino.io
"""
from amatino._internal._new_session_arguments import _NewSessionArguments
from amatino._internal._data_package import _DataPackage
from amatino._internal._api_request import _ApiRequest

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

    You can initialise a Session in one of two ways.

    1.  Create a new Session, by supplying the email and secret
        parameters. For example, you might require a user to input
        their email and secret passphrase when they first start
        your application. Note: You must never store a user's
        secret passphrase.

    2.  Load an existing Session, by supplying the session_id and
        api_key parameters. For example, perhaps you have securely
        stored session data on the user's device, and wish to load
        that session data such that the user does not have to log
        in again every time they restart your application.

    """

    _PATH = '/session'

    def __init__(
        self,
        secret: str = None,
        email: str = None,
        session_id=None,
        api_key=None
        ):

        if (
                secret is not None
                or email is not None
            ):
            new_arguments = _NewSessionArguments(
                secret=secret,
                email=email
            )
            request_data = _DataPackage(object_data=new_arguments)
            request = _ApiRequest(
                path=self._PATH,
                method='POST',
                data=request_data
            )
            # Load request response
            

    def _create(self):
        raise NotImplementedError

    def delete(self):
        """
        Destroy this Session, such that its id and api_key are no
        longer valid for authenticating Amatino API requests. Analagous
        to 'logging out' the underlying User.
        """
        raise NotImplementedError


