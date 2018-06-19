"""
Amatino API Python Bindings
Request Headers Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""
from amatino._internal._session_credentials import _SessionCredentials
from amatino._internal._data_package import _DataPackage
from amatino._internal._signature import _Signature

class _RequestHeaders:
    """
    Private - Not intended to be used directly.

    An instance of HTTP headers for use in an API request.
    """
    _AGENT = 'Amatino Python'

    def __init__(
        self,
        path: str,
        session_credentials: _SessionCredentials = None,
        request_data: _DataPackage = None
        ):

        self._headers = {'User-Agent': self._AGENT}

        if request_data is not None:
            self._headers['content-type'] = 'application/json'

        if session_credentials is None:
            return

        signature = _Signature(
            api_key=session_credentials.api_key,
            path=path,
            json_data=request_data.as_object()
        )

        self._headers['X-Signature'] = signature.string()
        self._headers['X-Session-ID'] = session_credentials.session_id
        
        return

    def dictionary(self) -> dict:
        """
        Return request headers as a dict
        """
        assert isinstance(self._headers, dict)
        return self._headers
