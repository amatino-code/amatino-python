"""
Amatino API Python Bindings
Request Headers Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""
from amatino.internal.data_package import DataPackage
from amatino.internal.signature import Signature
from amatino.internal.credentials import Credentials


class RequestHeaders:
    """
    Private - Not intended to be used directly.

    An instance of HTTP headers for use in an API request.
    """
    _AGENT = 'Amatino Python'

    def __init__(
        self,
        path: str,
        credentials: Credentials = None,
        request_data: DataPackage = None
    ) -> None:

        self._headers = {'User-Agent': self._AGENT}

        if request_data is not None:
            self._headers['content-type'] = 'application/json'

        if credentials is None:
            return

        signature = Signature(
            api_key=credentials.api_key,
            path=path
        )

        self._headers['X-Signature'] = signature.string
        self._headers['X-Session-ID'] = credentials.session_id

        return

    def dictionary(self) -> dict:
        """
        Return request headers as a dict
        """
        assert isinstance(self._headers, dict)
        return self._headers
