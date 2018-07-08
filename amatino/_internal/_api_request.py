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
from amatino._internal._session_credentials import _SessionCredentials
from amatino._internal._data_package import _DataPackage
from amatino._internal._url_parameters import _UrlParameters
from amatino._internal._request_headers import _RequestHeaders

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
        session_credentials: _SessionCredentials = None,
        data: _DataPackage = None,
        url_parameters: _UrlParameters = None,
        debug: bool = False
    ):

        if session_credentials is not None:
            assert isinstance(session_credentials, _SessionCredentials)

        if data is not None:
            assert isinstance(data, _DataPackage)
            request_data = data.as_json_bytes()
        else:
            request_data = None

        if url_parameters is not None:
            assert isinstance(url_parameters, _UrlParameters)

        if method not in self._VALID_METHODS:
            raise ValueError(
                'Invalid method. Options: ' + str(self._VALID_METHODS)
            )

        if debug is False:
            url = self._ENDPOINT
        else:
            url = self._DEBUG_ENDPOINT

        url += path

        if url_parameters is not None:
            url += url_parameters.parameter_string()

        headers = _RequestHeaders(path, session_credentials, data)
        request = Request(
            url=url,
            data=request_data,
            headers=headers.dictionary(),
            method=method,
        )
        try:
            self._response = urlopen(request, timeout=self._TIMEOUT)
        except HTTPError as error:
            # Insert error handling
            raise error

        self._raw_data = loads(self._response.read().decode('utf-8'))

        return

    def load(
        self,
        structure: tuple,
        index: int = None,
        load_raw: bool = False
    ) -> dict:
        """
        Return a dictionary containing object attributes. Optionally load the
        raw data from the request, why may be of type list.
        """
        if load_raw is True:
            return self._raw_data

        assert isinstance(structure, tuple)

        if index is not None:
            assert isinstance(index, int)

        if isinstance(self._raw_data, list) and index is None:
            raise TypeError('List source loads require an index')

        if index == None:
            raw_object = self._raw_data
        else:
            raw_object = self._raw_data[index]

        for pair in structure:
            if pair[0] not in raw_object:
                raise NotImplementedError('Implement Amatino error here')
            if not isinstance(raw_object[pair[0]], pair[1]):
                raise NotImplementedError('Implement Amatino error here')

        return raw_object
