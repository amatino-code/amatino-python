"""
Amatino API Python Bindings
Request Headers Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""
from amatino.session import Session
from amatino._internal._data_package import _DataPackage
from amatino._internal._signature import _Signature

class _RequestHeaders:
    """
    Private - Not intended to be used directly.

    An instance of HTTP headers for use in an API
    request.
    """
    _AGENT = 'Amatino Python'

    def __init__(
        self,
        path: str,
        session: Session = None,
        request_data: _DataPackage = None
        ):

        self._headers = {
            'User-Agent': self._AGENT
        }

        if session is None:
            return

        signature = _Signature(
            api_key=session.api_key,
            path=path,
            json_data=request_data.as_object()
        )

        self._headers['X-Signature'] = signature.string()
        self._headers['X-Session-ID'] = session.session_id
        
        return

    def dictionary(self) -> dict:
        """
        Return request headers as a dict
        """
        assert isinstance(self._headers, dict)
        return self._headers
