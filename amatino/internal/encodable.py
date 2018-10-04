"""
Amatino API Python Bindings
Encodable Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly by public classes, and
should not be used directly.
"""
from typing import Any
import json


class Encodable:
    """
    Abstract class defining an interface for types that may be serialised
    to JSON.
    """
    def serialise(self) -> Any:
        """
        Return a version of this object in a serialisable form.
        """
        raise NotImplementedError

    def encode_to_json(self) -> str:
        """
        Return a JSON string version of this object
        """
        return json.dumps(self.serialise())
