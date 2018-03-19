"""
Amatino API Python Bindings
API Request Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""
from json import loads
from urllib.request import Request
from urllib.request import urlopen
from urllib.request import HTTPError
from amatino._internal._data_package import _DataPackage
from amatino._internal._url_parameters import _UrlParameters
from amatino._internal._request_headers import _RequestHeaders
from amatino.session import Session

class _ApiRequest:
    """    
    Private - Not intended to be used directly.

    An instance of an http request to the Amatino API.
    """

    _ENDPOINT = 'https://api.amatino.io'
    _DEBUG_ENDPOINT = 'http://127.0.0.1:5000'
    _TIMEOUT = 5
    _VALID_METHODS = ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')

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
            request_data = data.as_json_bytes()
        else:
            request_data = None

        if url_parameters is not None:
            assert isinstance(url_parameters, _UrlParameters)

        assert isinstance(path, str)
        assert isinstance(method, str)
        assert isinstance(debug, bool)
        assert method in self._VALID_METHODS

        if debug is False:
            url = self._ENDPOINT
        else:
            url = self._DEBUG_ENDPOINT

        if url_parameters is not None:
            url += url_parameters.parameter_string()

        headers = _RequestHeaders(path, session, data)

        request = Request(
            url=url,
            data=request_data,
            headers=headers.dictionary(),
            method=method,
        )
        try:
            self._response = urlopen(request, timeout=self._TIMEOUT)
        except HTTPError as error:
            print(error)
            raise NotImplementedError('Insert Amatino error handling here')

        self._raw_data = loads(self._response.read().decode('utf-8'))

        return

    def load(self, index: int = None) -> dict:
        """
        
        """
