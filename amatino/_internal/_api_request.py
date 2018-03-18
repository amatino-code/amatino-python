"""
Amatino API Python Bindings
API Request Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""
from urllib.request import Request
from urllib.request import urlopen
from amatino._internal._data_package import _DataPackage
from amatino._internal._url_parameters import _UrlParameters
from amatino.session import Session

class _ApiRequest:
    """    
    Private - Not intended to be used directly.

    An instance of an http request to the Amatino API.
    """

    ENDPOINT = 'https://api.amatino.io'
    DEBUG_ENDPOINT = 'http://127.0.0.1:5000'
    TIMEOUT = 5

    def __init__(
        self,
        path: str,
        method: str,
        session: Session = None,
        data: _DataPackage = None,
        url_parameters: _UrlParameters = None,
        debug: bool = False
        ):

        if session is not None:
            assert isinstance(session, Session)

        if data is not None:
            assert isinstance(data, _DataPackage)

        if url_parameters is not None:
            assert isinstance(url_parameters, _UrlParameters)

        assert isinstance(path, str)
        assert isinstance(method, str)
        assert isinstance(debug, bool)

