"""
Amatino API Python Bindings
Amatino Alpha Module
Author: hugh@amatino.io

This module provides an interim capability designed to allow use of the
Amatino API from Python while the full-featured Amatino Python library is built
up around it. It is a very thin wrapper around HTTP requests to the Amatino API.

While the broader Python library is not ready for use, the AmatinoAlpha object
abstracts away much of the raw HTTP request wrangling that would be required to
interact with the Amatino API from Python.

"""
import json
from amatino import Session
from amatino._internal._api_request import _ApiRequest
from amatino._internal._url_parameters import _UrlParameters
from amatino._internal._data_package import _DataPackage

class AmatinoAlpha:
    """
    An instance of AmatinoAlpha can make arbitrary requests to the Amatino API.
    It is intended as an interim capability to allow use of the Amatino API from
    Python while the full-featured Amatino Python library is being built.

    Initialise the AmatinoAlpha object in one of three ways:

       1) Email / secret: Provide the email and secret you use to log in to
          https://amatino.io.

       2) User_id / secret: Provide your Amatino user id and secret passphrase.

       3) Saved_session_filepath: Provide the path to a file that contains
          existing session information, created by previously calling the
          save_session_to_disk() method on another AmatinoAlpha instance.

    To make requests, call the request() method. Provide parameters to the
    request() method has defined by the Amatino API HTTP documentation available
    at https://amatino.io/documentation.
    """
    _INVALID_INIT_1 = """User ID and saved session filepath must be None when 
    initialising with email and secret"""
    _INVALID_INIT_2 = """Email and session filepath must be none when
    initialising with user_id and secret"""
    _INVALID_INIT_3 = """Email, user_id, and secret must be none when
    initialising with saved_session_filepath"""
    _INVALID_FILE_DATA = """The data in the file you specified appears to be
    invalidly formatted. Please try creating a new session by initalising
    AmatinoAlpha with email/secret or user_id/secret arguments.
    """
    _NOT_SERIALISABLE = """provided body object does not appear to be json
    serialisable"""

    def __init__(
        self,
        email: str = None,
        secret: str = None,
        user_id: int = None,
        saved_session_filepath: str = None
    ):
        _ = self._validate_initialisation(
            email,
            secret,
            user_id,
            saved_session_filepath
        )

        if saved_session_filepath is not None:
            self._session = self._load_saved_session(
                saved_session_filepath
            )
        else:
            self._session = Session(
                secret=secret,
                email=email,
                user_id=user_id
            )
    
        return

    def _validate_initialisation(
        self,
        email,
        secret,
        user_id,
        saved_session_filepath
    ) -> None:
        """
        Raises exceptions in cases of invalid initialisation
        """

        if email is not None and secret is not None:
            if user_id is not None or saved_session_filepath is not None:
                raise ValueError(self._INVALID_INIT_1)
            return

        if secret is not None and user_id is not None:
            if email is not None or saved_session_filepath is not None:
                raise ValueError(self._INVALID_INIT_2)

        if saved_session_filepath is not None:
            if False in [(a is None) for a in (user_id, secret, email)]:
                raise ValueError(self._INVALID_INIT_3)

        return

    def _load_saved_session(self, saved_session_filepath: str) -> Session:
        """
        Open a specified file and return a Session based on the credentials
        found within.
        """

        if not isinstance(saved_session_filepath, str):
            raise TypeError('saved_session_filepath must be of type str')
        
        with open(saved_session_filepath, 'r') as session_file:
            saved_session = session_file.read()

        try:
            session_json = json.loads(saved_session)
        except json.decoder.JSONDecodeError:
            raise RuntimeError(self._INVALID_FILE_DATA)

        if (
                len(session_json) != 3
                or 'session_id' not in session_json
                or 'user_id' not in session_json
                or 'api_key' not in session_json
                or not isinstance(session_json['session_id'], int)
                or not isinstance(session_json['user_id'], int)
                or not isinstance(session_json['api_key'], str)
        ):
            raise RuntimeError(self._INVALID_FILE_DATA)

        session = Session(
            session_id=session_json['session_id'],
            api_key=session_json['api_key'],
            user_id=session_json['user_id']
        )

        return session

    def request(
        self,
        path: str,
        method: str,
        query_string: str = None,
        body: list = None
    ) -> [dict]:
        """
        Make a request to the Amatino API. Supply parameters as per the
        requirements described for resources in the Amatino API documentation
        at https://amatino.io/documentation
        """
        if body is not None and not isinstance(body, list):
            TypeError('If supplied, body must be of type list')

        if not isinstance(path, str):
            raise TypeError('path must be of type str')

        if query_string is not None and not isinstance(query_string, str):
            raise TypeError('If supplied, query_string must be of type str')

        if not isinstance(method, str):
            raise TypeError('method must be of type str')

        data_package = None
        if body is not None:
            _ = json.dumps(body) # Provoke encoding failure early
            data_package = _DataPackage(raw_list_data=body)

        request = _ApiRequest(
            path,
            method,
            session_credentials=self._session._credentials(),
            data=data_package,
            url_parameters=_UrlParameters(raw_query_string=query_string)
        )

        return request.load(None, load_raw=True)

    def save_session_to_disk(self, filepath: str) -> None:
        """
        Save the current session to the path specified. Doing so allows you
        to load a session from disk later on by initialising the AmatinoAlpha
        object with the saved_session_filepath parameter.
        """
        if not isinstance(filepath, str):
            raise TypeError('filepath must be of type str')
        data_to_write = json.dumps(self._session.in_serialisable_form())
        with open(filepath, 'w') as file_to_write:
            file_to_write.write(data_to_write)
        return
